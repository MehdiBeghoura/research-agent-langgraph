from langgraph.types import Send
from typing import Literal
from src.llm import structured_model, client, verify_model, conflict_model, conflict_resolution_model, draft_model

MAX_ATTEMPTS = 3

def break_into_subtopics(state):
    topic = state["original_topic"]
    prompt = f"Break this research topic into exactly 3 distinct sub-angles to investigate separately: {topic}"
    result = structured_model.invoke(prompt)
    return {"subtopics": result.subtopics}


def fan_out_to_search(state):
    return [Send("search_one_subtopic", {"subtopic_text": s}) for s in state["subtopics"]]


def search_one_subtopic(state):
    query = state["subtopic_text"]
    for attempt in range(MAX_ATTEMPTS):
        response = client.search(query=query, search_depth="advanced")
        results = [r for r in response["results"] if r.get("content")]
        contents = [r["content"] for r in results]
        search_result = "\n\n".join(contents)
        sources = [{"title": r["title"], "url": r["url"]} for r in results]
        prompt = f"Subtopic: {query}\nSearch result: {search_result}\nDetermine whether the search result adequately answers the subtopic. Return true if it does, otherwise return false."
        try:
            verdict = verify_model.invoke(prompt)
            is_good = verdict.is_good_enough
        except Exception:
            is_good = False
        if is_good or attempt == MAX_ATTEMPTS - 1:
            return {"search_results": [search_result], "sources": sources}
        
        
def conflict_check_node(state):
    return {}


def conflict_check(state) -> Literal["resolve_conflict", "draft_response"]:
    combined = "\n\n".join(state["search_results"])
    verdict = conflict_model.invoke(f"Compare these sources and determine whether they contain any factual disagreements.\n\nSources:\n{combined}")
    if verdict.has_conflict:
        return "resolve_conflict"
    return "draft_response"


def resolve_conflict(state):
    combined = "\n\n".join(state["search_results"])
    verdict = conflict_resolution_model.invoke(f"Identify the conflicting claims, determine which claims are better supported, and explain how the disagreement should be handled.\n\nSources:\n{combined}")
    return {"results_conflicts": verdict.resolution}


def draft_response(state):
    combined = "\n\n".join(state["search_results"])
    conflict_note = state.get("results_conflicts")
    prompt = f"Topic: {state['original_topic']}\n\nSources:\n{combined}\n\n"
    if conflict_note:
        prompt += f"Note: {conflict_note}\n\n"
    prompt += "Write a concise, well-organized research brief answering the topic, citing key points from the sources. Do not include a references or citations section — sources will be listed separately by the application."
    response = draft_model.invoke(prompt)
    return {"draft_response": response.content}
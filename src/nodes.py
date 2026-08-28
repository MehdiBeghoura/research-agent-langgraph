from langgraph.types import Send
from typing import Literal
from langgraph.graph import END
from src.llm import structured_model




def break_into_subtopics(state):
    topic = state["original_topic"]
    prompt = f"Break this research topic into 3 distinct sub-angles to investigate separately: {topic}"
    result = structured_model.invoke(prompt)
    return {"subtopics": result.subtopics}



def fan_out_to_search(state):
    return [Send("search_one_subtopic", {"subtopic_text": s, "search_result":None, "attempts":0}) for s in state["subtopics"]]


def search_one_subtopic(state):
    
    search_result = f"Search result for {state['subtopic_text']}"
    return {"search_result": search_result, "search_results": [search_result], "attempts": state["attempts"]+1}

MAX_ATTEMPTS = 3

def verify_result(state) -> Literal["search_one_subtopic", "conflict_check_node"]:
    result = state["search_result"]
    attempts = state["attempts"]

    
    is_good_enough = result is not None and len(result) > 20

    if is_good_enough:
        return "conflict_check_node"
    elif attempts >= MAX_ATTEMPTS:
        
        return "conflict_check_node"
    else:
        return "search_one_subtopic"
    
def conflict_check_node(state):
    # exists only as a convergence point so LangGraph
    
    return {}

def conflict_check(state) -> Literal["resolve_conflict", "draft_response"]:
    results = state["search_results"]
    # Real version will compare actual content across sources for disagreement.
    has_conflict = len(results) < 3

    if has_conflict:
        return "resolve_conflict"
    else:
        return "draft_response"
    
    
    
def resolve_conflict(state):
    # Real version will compare actual claims across results and explain the discrepancy.
    conflict_note = "Sources appear to disagree on some details ,needs manual review."
    return {"results_conflicts": conflict_note}

def draft_response(state):
    # Real version will synthesize information from the search results into a coherent response.
    draft = "Draft response based on search results."
    return {"draft_response": draft}
    
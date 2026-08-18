from langgraph.types import Send
from typing import Literal
from langgraph.graph import END
def break_into_subtopics(state):
    # will call an LLM later.
    subtopics = [
      "cache invalidation approaches in backend systems",
      "write-through vs write-back caching strategies",
      "distributed cache consistency techniques",
    ]
    return {"subtopics": subtopics}



def fan_out_to_search(state):
    return [Send("search_one_subtopic", {"subtopic_text": s, "search_result":None, "attempts":0}) for s in state["subtopics"]]


def search_one_subtopic(state):
    
    search_result = f"Search result for {state['subtopic_text']}"
    return {"search_result": search_result, "search_results": [search_result], "attempts": state["attempts"]+1}

MAX_ATTEMPTS = 3

def verify_result(state) -> Literal["search_one_subtopic"]|  Literal[END]:
    result = state["search_result"]
    attempts = state["attempts"]

    
    is_good_enough = result is not None and len(result) > 20

    if is_good_enough:
        return END
    elif attempts >= MAX_ATTEMPTS:
        
        return END
    else:
        return "search_one_subtopic"
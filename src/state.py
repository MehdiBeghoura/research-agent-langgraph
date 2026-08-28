from typing import TypedDict, Annotated
import operator

class SubtopicState(TypedDict):
    subtopic_text: str
    
class ResearchState(TypedDict):
    original_topic: str
    subtopics: list[str]
    search_results: Annotated[list[str], operator.add]
    results_conflicts: str | None
    draft_response: str | None
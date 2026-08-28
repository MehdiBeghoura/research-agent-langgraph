from langgraph.graph import END, START, StateGraph
from src.nodes import break_into_subtopics, conflict_check, conflict_check_node, draft_response, fan_out_to_search, resolve_conflict, search_one_subtopic
from src.state import ResearchState

graph_builder = StateGraph(ResearchState)

graph_builder.add_node("break_into_subtopics", break_into_subtopics)

graph_builder.add_node("search_one_subtopic", search_one_subtopic)

graph_builder.add_node("conflict_check_node", conflict_check_node)

graph_builder.add_node("resolve_conflict", resolve_conflict)

graph_builder.add_node("draft_response", draft_response)

graph_builder.add_edge(START, "break_into_subtopics")

graph_builder.add_conditional_edges("break_into_subtopics", fan_out_to_search, ["search_one_subtopic"])

graph_builder.add_edge("search_one_subtopic", "conflict_check_node")

graph_builder.add_conditional_edges("conflict_check_node", conflict_check, ["resolve_conflict", "draft_response"])

graph_builder.add_edge("resolve_conflict", "draft_response")

graph_builder.add_edge("draft_response", END)

graph = graph_builder.compile()
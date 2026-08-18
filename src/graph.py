from langgraph.graph import StateGraph, START, END
from src.state import ResearchState
from src.nodes import break_into_subtopics, fan_out_to_search, search_one_subtopic, verify_result

graph_builder = StateGraph(ResearchState)
graph_builder.add_node("break_into_subtopics", break_into_subtopics)
graph_builder.add_node("search_one_subtopic", search_one_subtopic)
graph_builder.add_edge(START, "break_into_subtopics")

graph_builder.add_conditional_edges("break_into_subtopics", fan_out_to_search, ["search_one_subtopic"])
graph_builder.add_conditional_edges("search_one_subtopic", verify_result, ["search_one_subtopic", END])

graph = graph_builder.compile()
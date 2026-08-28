from src.graph import graph


if __name__ == "__main__":
    initial_state = {"original_topic": "Caching strategies in backend systems", "subtopics": [], "search_results": [], "results_conflicts": None, "draft_response": None}
    result = graph.invoke(initial_state)
    print(result)
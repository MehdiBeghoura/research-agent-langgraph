import streamlit as st
from src.graph import graph

st.set_page_config(page_title="Research Agent", page_icon="🔎")
st.title("🔎 Research Agent")
st.caption("Multi-source research with parallel search, retry, and conflict detection — built with LangGraph")

topic = st.text_input("Enter a research topic")

if st.button("Run Research", disabled=not topic):
    with st.spinner("Researching... this may take a minute"):
        initial_state = {
            "original_topic": topic,
            "subtopics": [],
            "search_results": [],
            "sources": [],
            "results_conflicts": None,
            "draft_response": None,
        }
        result = graph.invoke(initial_state)

    st.subheader("Subtopics Investigated")
    for s in result["subtopics"]:
        st.markdown(f"- {s}")

    if result.get("results_conflicts"):
        st.warning(f"**Conflict detected:** {result['results_conflicts']}")

    st.subheader("Research Brief")
    st.markdown(result["draft_response"])

    st.divider()
    st.subheader("Sources")
    seen = set()
    for src in result.get("sources", []):
        if src["url"] not in seen:
            seen.add(src["url"])
            st.markdown(f"- [{src['title']}]({src['url']})")
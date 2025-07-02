import os
import streamlit as st
from deepresearch.workflow import DeepResearch

st.title("DeepResearch Demo")
query = st.text_input("Enter your question")
depth = st.number_input("Depth", min_value=1, max_value=10, value=3, step=1)

if st.button("Run") and query:
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not openrouter_api_key or not tavily_api_key:
        st.error("Please set OPENROUTER_API_KEY and TAVILY_API_KEY environment variables.")
    else:
        dr = DeepResearch(openrouter_api_key, tavily_api_key)
        with st.spinner('Running research...'):
            report = dr.run(query, depth=int(depth))
        st.markdown(report)

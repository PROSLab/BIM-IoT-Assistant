from langchain_community.graphs import Neo4jGraph
import streamlit as st

# Neo4j configuration
neo4j_config = Neo4jGraph(
    url=st.secrets["NEO4J_URI"],
    username=st.secrets["NEO4J_USERNAME"],
    password=st.secrets["NEO4J_PASSWORD"],
)

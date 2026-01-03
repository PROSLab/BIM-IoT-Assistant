from rdflib_neo4j import Neo4jStoreConfig
from rdflib_neo4j import HANDLE_VOCAB_URI_STRATEGY

import streamlit as st

# Get your Aura Db free instance here: https://neo4j.com/cloud/aura-free/#test-drive-section
NEO4J_DB_URI="bolt://localhost:7687"
NEO4J_DB_USERNAME=st.secrets["NEO4J_USERNAME"]
NEO4J_DB_PWD=st.secrets["NEO4J_PASSWORD"]

auth_data = {'uri': NEO4J_DB_URI,
             'database': "neo4j",
             'user': NEO4J_DB_USERNAME,
             'pwd': NEO4J_DB_PWD}
from rdflib import Namespace

# Define your prefixes
prefixes = {
    'neo4ind': Namespace('http://neo4j.org/ind#'),
    'neo4voc': Namespace('http://neo4j.org/vocab/sw#'),
    'nsmntx': Namespace('http://neo4j.org/vocab/NSMNTX#'),
    'apoc': Namespace('http://neo4j.org/vocab/APOC#'),
    'graphql': Namespace('http://neo4j.org/vocab/GraphQL#')
}
# Define your custom mappings
config = Neo4jStoreConfig(auth_data=auth_data,
                          custom_prefixes=prefixes,
                          handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
                          batching=True)
from rdflib_neo4j import Neo4jStore
from rdflib import Graph
file_path = st.secrets["TTL_FILE_PATH"]

graph_store = Graph(store=Neo4jStore(config=config))
graph_store.parse(file_path,format="ttl")
graph_store.close(True)
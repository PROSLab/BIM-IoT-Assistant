from langchain.chains import OntotextGraphDBQAChain

from databases.graphdb_config import graphdb
from llm import anthropic_claude_model
from prompts.graphdb_building_prompt import SPARQL_BUILDING_PROMPT
from prompts.building_prompt import SPARQL_QA_BIM_PROMPT

building_assistant = OntotextGraphDBQAChain.from_llm(
    anthropic_claude_model,
    sparql_generation_prompt=SPARQL_BUILDING_PROMPT,
    qa_prompt=SPARQL_QA_BIM_PROMPT,
    graph=graphdb,
    verbose=True,
    allow_dangerous_requests=True
)

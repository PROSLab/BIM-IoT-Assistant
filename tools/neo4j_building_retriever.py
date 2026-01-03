from langchain.chains import GraphCypherQAChain

from databases.neo_graph import neo4j_config
from llm import anthropic_claude_model
from prompts.building_prompt import CYPHER_BUILDING_PROMPT, CYPHER_QA_BIM_PROMPT

cypher_qa = GraphCypherQAChain.from_llm(
    anthropic_claude_model,
    graph=neo4j_config,
    verbose=True,
    top_k=100,
    cypher_prompt=CYPHER_BUILDING_PROMPT,
    qa_prompt=CYPHER_QA_BIM_PROMPT,
    allow_dangerous_requests=True
)


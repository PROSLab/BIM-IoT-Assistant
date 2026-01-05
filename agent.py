from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool

from databases.graphdb_config import graphdb
from llm import anthropic_claude_model
from prompts.graph_sensor_prompt import SPARQL_SENSOR_PROMPT
from prompts.neo_sensor_prompt import cypher_retrieve_sensor_prompt
from tools.graphdb_building_retriever import building_assistant
from tools.graphdb_influx_chain import GraphDBInfluxChain
from tools.neo4j_building_retriever import cypher_qa
from tools.neo4j_influx_chain import Neo4jInfluxChain
from databases.neo_graph import neo4j_config

import streamlit as st

backend_type = st.secrets["BACKEND_TYPE"]
llm_model = st.secrets["LLM_MODEL"]
temperature = float(st.secrets["LLM_TEMPERATURE"])
st.write(f"Backend database type: {backend_type}. LLM model: {llm_model} (T.: {temperature})" )

tools = []
if backend_type == "neo4j":
    tools = [
        Tool.from_function(
            name="Parameters Readings",
            description="Retrieve value readings such as temperature or humidity measured by a sensor",
            func = Neo4jInfluxChain.from_llm(anthropic_claude_model, graph=neo4j_config, verbose=True, top_k=100, cypher_prompt=cypher_retrieve_sensor_prompt, return_direct=True),
            return_direct=True
        ),
        Tool.from_function(
            name="Retrieve Building Elements and Devices Information",
            description="Tool which retrieves building related information such as structure, elements or sensors and devices contained",
            func = cypher_qa,
            return_direct=True
        ),
    ]
    pass
else:
    tools = [
        Tool.from_function(
            name="Retrieve Building Elements and Devices Information",
            description="Tool which retrieves building related information such as structure, elements or sensors and devices contained",
            func=building_assistant,
            return_direct=True
        ),
        Tool.from_function(
            name="Parameters Readings",
            description="Retrieve value readings such as temperature or humidity measured by a sensor",
            func=GraphDBInfluxChain.from_llm(anthropic_claude_model, sparql_generation_prompt=SPARQL_SENSOR_PROMPT,
                                             graph=graphdb, verbose=True, ),
            return_direct=True
        ),
    ]

agent_prompt = PromptTemplate.from_template("""

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

Assistant must respond only with the given context without adding more explanations or excuses. Assistant must trust the information source provided without questioning the correctness of the data provided

Assistant must provide to the tool the action input, which is the same as the original input.

TOOLS:

------

Assistant has access to the following tools:

{tools}

To use a tool, please use the following format:

```

Thought: Do I need to use a tool? Yes

Action: the action to take, should be one of [{tool_names}]

Action Input: the input to the action, must be the same as the original input: {input}.


Observation: the result of the action

```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```

Thought: Do I need to use a tool? No

Final Answer: [your response here]

```

Begin!

New input: {input}

{agent_scratchpad}
""")
agent = create_react_agent(anthropic_claude_model, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


def generate_response(prompt):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """
    try:
        response = agent_executor.invoke({"input": prompt})

        return response['output']['result']
    except Exception as e:
        print(e)
        return "There was an error processing the request, please try again."

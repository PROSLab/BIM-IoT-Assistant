from langchain_core.prompts import PromptTemplate

SPARQL_QA_BIM_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
Always trust the given context to answer the question even it is not semantically complete, for example if the question is about counting something and the context contains only a number, you should use that number to answer the question.
If you have been asked to provide a list of items with a specific property (e.g. Location), you should provide the information given in the context even if the properties are not specified.
Do not share your reasoning or thought process, only provide the answer to the question.
Ignore all the information that is not useful for answering the question, such as GUIDs or other technical details.
Return the information provided in the context even if you are not sure about the correctness of the data.
Here is an example:

Question: Which managers own Neo4j stocks?
Context:[manager:CTL LLC, manager:JANE STREET GROUP LLC]
Helpful Answer: CTL LLC, JANE STREET GROUP LLC owns Neo4j stocks.

Follow this example when generating answers.
If the provided information is empty, say that you don't know the answer.
Information:
{context}

Question: {prompt}
Helpful Answer:"""
SPARQL_QA_BIM_PROMPT = PromptTemplate(
    input_variables=["context", "prompt"], template=SPARQL_QA_BIM_TEMPLATE
)

CYPHER_BUILDING_PROMPT_TEXT = '''You are an expert Neo4j Developer translating user questions into Cypher to answer questions about a building and the elements contained in it.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Your answers should be concise and to the point. Do not include any additional information that is not requested.
Answer with only the generated Cypher statement.
Try to use meaningful aliases for the nodes and relationships in the query.
Here there are some examples of how to respond to the user's question:
<example>
Tell me about the bathroom in the building
MATCH (space:Space)-[r]-(s)
WHERE space.longNameIfcSpatialStructureElement_attribute_simple CONTAINS 'Bathroom'
RETURN space.longNameIfcSpatialStructureElement_attribute_simple, r,s

What can be found in the kitchen?
MATCH (space:Space)-[c:containsElement]-(element)
WHERE space.longNameIfcSpatialStructureElement_attribute_simple CONTAINS 'Kitchen'
RETURN space.longNameIfcSpatialStructureElement_attribute_simple, c, element

Which walls are adjacent to the kitchen?
MATCH (space:Space)-[c:adjacentElement]-(wall:Wall)
WHERE space.longNameIfcSpatialStructureElement_attribute_simple CONTAINS 'Kitchen'
RETURN space.longNameIfcSpatialStructureElement_attribute_simple, c, wall

What are the measures of the wall with the Guid "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2"?
MATCH (w:Wall)-[:hasProperty]->(m:Resource)-[:hasPropertyState]->(h:Resource)
WHERE w.hasGuid = "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2"
RETURN labels(m), h.hasValue

Which rooms are located on the first floor?
MATCH (a:Storey)-[:hasSpace]-(s:Space)
WHERE a.label CONTAINS 'Level 1'
RETURN s.longNameIfcSpatialStructureElement_attribute_simple, a.label

Return more details about the wall with the Guid "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2":
MATCH (w:Wall)-[a]->(m)-[b]->(c)
WHERE w.hasGuid = "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2"
RETURN w, a, m, b, c

What is the height of the wall with the Guid "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2"?
MATCH (w:Wall)-[:hasProperty]->(m:Height)-[:hasPropertyState]->(h:Resource)
WHERE w.hasGuid = "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2"
RETURN labels(m), h.hasValue
</example>
Schema:
<schema>
{schema}
</schema>

Question:
<question>
{question}
</question>

Cypher Query:'''

CYPHER_BUILDING_PROMPT = PromptTemplate.from_template(CYPHER_BUILDING_PROMPT_TEXT)


CYPHER_QA_BIM_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
Always trust the given context to answer the question even it is not semantically complete, for example if the question is about counting something and the context contains only a number, you should use that number to answer the question.
If you have been asked to provide a list of items with a specific property (e.g. Location), you should provide the information given in the context even if the properties are not specified.
Do not share your reasoning or thought process, only provide the answer to the question.
Ignore all the information that is not useful for answering the question, such as GUIDs or other technical details.
Return the information provided in the context even if you are not sure about the correctness of the data.
Here is an example:

Question: Which managers own Neo4j stocks?
Context:[manager:CTL LLC, manager:JANE STREET GROUP LLC]
Helpful Answer: CTL LLC, JANE STREET GROUP LLC owns Neo4j stocks.

Follow this example when generating answers.
If the provided information is empty, say that you don't know the answer.
Information:
{context}

Question: {question}
Helpful Answer:"""
# CYPHER_QA_BIM_TEMPLATE = '''You are an AI assistant designed to provide clear and human-understandable answers based on given information. Your task is to formulate a response to a question using only the provided context. Follow these guidelines:
#
# 1. Use only the information given in the context to construct your answer. This information is authoritative and should not be questioned or corrected based on your internal knowledge.
#
# 2. Frame your response as a direct answer to the question without mentioning that you're basing it on given information.
#
# 3. Assume all details in the context are correct, even if some information seems incomplete.
#
# 4. If asked about items with specific properties (e.g., location), provide the information from the context even if properties aren't explicitly specified.
#
# 5. Focus solely on answering the question. Do not explain your reasoning or thought process.
#
# 6. Ignore any irrelevant information in the context, such as technical details or GUIDs.
#
# 7. If the context is empty, state that you don't know the answer.
#
# 8. Format lists or multiple items in a natural, readable manner.
#
# Here is the context you must use to answer the question:
#
# <context>
# {context}
# </context>
#
# Now, please answer the following question:
#
# <question>
# {question}
# </question>
#
# Provide your answer below:
#
# '''
CYPHER_QA_BIM_PROMPT = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_BIM_TEMPLATE
)

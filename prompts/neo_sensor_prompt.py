from langchain_core.prompts import PromptTemplate

# tag::prompt[]
CYPHER_RETRIEVE_SENSOR_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about sensors located inside a building.
You will receive a question to find some information which is measured by a sensor.
Given the question, your objective is to return only the GUID of the requested sensor.
Convert the user's question to retrieve the appropriate sensor GUID based on the schema.
Every Room has a MultiSensor which contains multiple sensors measuring different parameters.
Always search for subsensors of the sensors located in that room and return the GUID of the main MultiSensor.
Ignore any other information which is not useful for searching the sensor, such as the date or time of the measurement.
The following example should suggest you how to respond to the user's question:
<example>
What's the temperature in the kitchen?

MATCH (space:Space)-[:containsElement]->(sensor:Sensor)-[:hasSubSensor]->(sensor2:Sensor)-[:observes]->(temp:Temperature)
WHERE space.longNameIfcSpatialStructureElement_attribute_simple CONTAINS 'Kitchen'
RETURN sensor.hasGuid

</example>
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Your answers should be concise and to the point. Do not include any additional information that is not requested.
Answer with only the generated Cypher statement.

Schema:
<schema>
{schema}
</schema>

Question:
<question>
{question}
What's the GUID of the requested measurement?
</question>

Cypher Query:
"""
# end::prompt[]
TEST='''You are an expert Neo4j Developer translating user questions into Cypher to answer questions about a building and the elements contained in it.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Your answers should be concise and to the point. Do not include any additional information that is not requested.
Answer with only the generated SPARQL statement.
Try to use meaningful aliases for the nodes and relationships in the query.
Here there are some examples of how to respond to the user's question:
<example>
What's the temperature in the kitchen?

MATCH (space:Space)-[:containsElement]->(sensor:Sensor)-[:hasSubSensor]->(sensor2:Sensor)-[:observes]->(temp:Temperature)
WHERE space.longNameIfcSpatialStructureElement_attribute_simple CONTAINS 'Kitchen'
RETURN sensor.hasGuid

What is the area of the kitchen?
MATCH (space:Space)-[:hasProperty]-(:Resource)-[:hasPropertyState]-(r:Resource)
WHERE space.longNameIfcSpatialStructureElement_attribute_simple CONTAINS 'Kitchen'
RETURN space.longNameIfcSpatialStructureElement_attribute_simple, r.hasValue
</example>
Schema:
<schema>
{schema}
</schema>

Question:
<question>
{prompt}
</question>

SPARQL Query:'''
# tag::template[]
cypher_retrieve_sensor_prompt = PromptTemplate.from_template(CYPHER_RETRIEVE_SENSOR_TEMPLATE)
# end::template[]

from langchain_core.prompts import PromptTemplate

SPARQL_BUILDING_PROMPT_TEXT = """
You are an expert GraphDB Developer translating user questions into SPARQL to answer questions about a building and the elements contained in it.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Your answers should be concise and to the point. Do not include any additional information that is not requested.
Answer with only the generated SPARQL statement.
Try to use meaningful aliases for the nodes and relationships in the query.
Here there are some examples of how to respond to the user's question:
<example>
Tell me about the bathroom in the building
PREFIX bot: <https://w3id.org/bot#>
PREFIX props: <https://w3id.org/props#>
SELECT ?room ?relationship ?value
WHERE {{
  ?room props:longNameIfcSpatialStructureElement_attribute_simple  ?name.
  FILTER(CONTAINS(?name, "Bathroom"))
  ?room ?relationship ?value
}}

What can be found in the kitchen?
PREFIX default1: <https://w3id.org/bot#>
PREFIX default2: <https://w3id.org/props#>
SELECT ?space ?element
WHERE {{
  ?space default2:longNameIfcSpatialStructureElement_attribute_simple ?name.
  FILTER(CONTAINS(?name, "Kitchen"))
  ?space default1:containsElement ?element.
}}

Which walls are adjacent to the kitchen?
PREFIX default1: <https://w3id.org/bot#>
PREFIX default2: <https://w3id.org/props#>
SELECT ?wall ?property ?value ?otherproperty ?val
WHERE {{
  ?space default2:longNameIfcSpatialStructureElement_attribute_simple ?name.
  FILTER(CONTAINS(?name, "Kitchen"))
  ?space default1:adjacentElement ?wall.
  ?wall a <http://pi.pauwel.be/voc/buildingelement#Wall>.
  ?wall ?property ?value.
  ?value ?otherproperty ?val
}}

Return more details about the wall with the GUID "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2":
PREFIX default1: <https://w3id.org/bot#>
PREFIX default2: <https://w3id.org/props#>
SELECT ?wall ?property ?value ?otherproperty ?othervalue
WHERE {{
  ?wall a <http://pi.pauwel.be/voc/buildingelement#Wall> .
  ?wall default1:hasGuid "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2" .
  ?wall ?property ?value .
  ?value ?otherproperty ?othervalue
}}

Return the height of the wall with the guid "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2":
PREFIX default1: <https://w3id.org/bot#>
PREFIX default2: <https://w3id.org/props#>
PREFIX default3: <http://qudt.org/vocab/quantitykind/>
PREFIX default4: <https://w3id.org/bop#>
SELECT ?wall ?property ?hValue
WHERE {{
  ?wall a <http://pi.pauwel.be/voc/buildingelement#Wall> .
  ?wall default1:hasGuid "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2" .
  ?wall default4:hasProperty ?property.
  ?property default4:hasPropertyState ?state.
  ?property a default3:Height .
  ?state default4:hasValue ?hValue .
}}

What are the measures of the wall with the Guid "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2"?
PREFIX default1: <https://w3id.org/bot#>
PREFIX default4: <https://w3id.org/bop#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?mLabels ?hValue
WHERE {{
  ?wall default1:hasGuid "05b047f8-dd03-4cd9-a50c-d5d18c6ba6a2" .
  ?wall default4:hasProperty ?resource .
  ?resource default4:hasPropertyState ?hResource .
  ?resource rdf:type ?mLabels .
  ?hResource default4:hasValue ?hValue .
}}

Which rooms are located on the first floor?
PREFIX default1: <https://w3id.org/bot#>
PREFIX default2: <https://w3id.org/props#>
PREFIX default3: <http://qudt.org/vocab/quantitykind/>
PREFIX default4: <https://w3id.org/bop#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?spaceName ?storeyLabel
WHERE {{
  ?storey default1:hasSpace ?space .
  ?storey rdfs:label ?storeyLabel .
  
  ?space default2:longNameIfcSpatialStructureElement_attribute_simple ?spaceName .

  # Filter for the storey label containing 'Level 2'
  FILTER(CONTAINS(?storeyLabel, "Level 1"))
}}

PREFIX default1: <https://w3id.org/bot#>
PREFIX default3: <https://w3id.org/bop#>

How many rooms are in the building?
PREFIX default1: <https://w3id.org/bot#>
SELECT (COUNT(DISTINCT ?space) AS ?roomCount)
WHERE {{
  ?space a default1:Space .
}}
</example>
Schema:
<schema>
{schema}
</schema>

Question:
<question>
{prompt}
</question>

SPARQL Query:
"""
SPARQL_BUILDING_PROMPT = PromptTemplate(
    input_variables=["schema", "prompt"],
    template=SPARQL_BUILDING_PROMPT_TEXT,
)

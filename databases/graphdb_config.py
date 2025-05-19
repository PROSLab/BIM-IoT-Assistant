from langchain_community.graphs import OntotextGraphDBGraph

graphdb = OntotextGraphDBGraph(
    query_endpoint="http://localhost:7200/repositories/smartHomeDonkers",
    query_ontology = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
CONSTRUCT {
    ?class a rdfs:Class .
    ?class ?objectProperty ?relatedClass .
    ?class ?dataProperty "".
}
WHERE {
    {
        # Extract classes
        SELECT DISTINCT ?class
        WHERE {
            ?instance a ?class.
        }
    }
    {
        # Extract object properties for each class
        SELECT DISTINCT ?class ?objectProperty ?relatedClass
        WHERE {
            ?instance1 a ?class.
            ?instance2 a ?relatedClass.
            ?instance1 ?objectProperty ?instance2.
        }
    }
    {
        # Extract data properties for each class
        SELECT DISTINCT ?class ?dataProperty
        WHERE {
            ?instance a ?class.
            ?instance ?dataProperty ?dataValue.
            FILTER NOT EXISTS { ?dataValue a ?moreclass.}
        }
    }
}
"""
)
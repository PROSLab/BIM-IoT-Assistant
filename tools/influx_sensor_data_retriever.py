import streamlit as st
from influxdb_client import InfluxDBClient
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from llm import anthropic_claude_model


# Set up InfluxDB client
class InfluxDBQueryExecutor:
    def __init__(self, url, token, org):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.query_api = self.client.query_api()

    def execute_query(self, flux_query):
        """Executes a given Flux query on InfluxDB."""
        try:
            result = self.query_api.query(flux_query)
            return result
        except:
            return 'Error'


# Define the prompt template and LLM for generating a Flux query
def create_flux_query_generator(llm, sensor_id):
    """Create the LLMChain for generating Flux queries."""
    # Define the prompt template
    prompt_template = """
    You are an AI assistant tasked with generating Flux queries for an InfluxDB database containing smart home sensor data. Your goal is to create a query that accurately retrieves the requested information based on the given task. Follow these instructions carefully:

    1. You will be provided with a task description and a sensor identifier. The task description is enclosed in <task> tags, and the sensor identifier is a string value.
    
    <task>{Task}</task>
    
    2. The sensor identifier you must use in your query is:
    <sensor_id>""" + sensor_id + """</sensor_id>
    
    3. When generating the query, adhere to the following structure and requirements:
       - Use the "from(bucket: "OpenSmartHome")" as the starting point of your query.
       - Use the range() function to specify the time range.
       - Use filter() functions to select the correct measurement and sensor identifier.
       - Ignore any room names mentioned in the task and use the provided sensor identifier instead.
    
    4. Here are two examples of correctly formatted queries:
    
       Example 1:
       Question: Get the brightness readings of the given sensor identifier from the 15 March 2017
       
       from(bucket: "OpenSmartHome")
       |> range(start: 2017-03-15, stop: 2017-03-16)
       |> filter(fn: (r) => r._measurement == "Brightness")
       |> filter(fn: (r) => r.sensorId == " """ + sensor_id + """")
    
       Example 2:
       Question: Get the temperature readings of the given sensor identifier from the 15 March 2017 from 9 to 12
       
       from(bucket: "OpenSmartHome")
       |> range(start: 2017-03-15T09:00:00Z, stop: 2017-03-15T12:00:00Z)
       |> filter(fn: (r) => r._measurement == "Temperature")
       |> filter(fn: (r) => r.sensorId == " """ + sensor_id + """")
    
    5. For queries requesting data at a specific time:
       - Provide a time range from one minute before to 4 minutes after the requested time.
       - Example:
        Question: Get the temperature readings from 23 March 2017 at 18 from the bathroom
        
         from(bucket: "OpenSmartHome")
         |> range(start: 2017-03-23T17:59:00Z, stop: 2017-03-23T18:04:00Z)
         |> filter(fn: (r) => r._measurement == "Temperature")
         |> filter(fn: (r) => r.sensorId == " """ + sensor_id + """")
    
    6. Remember:
       - The bucket name is always "OpenSmartHome".
       - The first letter of parameter names should be uppercase (e.g., "Temperature", "Brightness").
    
    7. Generate the Flux query based on the task provided in the <task> tags. Return only the requested query without adding additional context, explanations, tags or other words and symbols which shouldn't be included in the query.
    
    [Your generated Flux query goes here]
    """

    # Create a PromptTemplate
    prompt = PromptTemplate(template=prompt_template, input_variables=["Task"])

    # Create and return the LLMChain with the prompt and the LLM
    return LLMChain(llm=llm, prompt=prompt)


# Define the tool to be executed by the agent
class InfluxDBTool:
    def __init__(self, sensor_id):
        # Initialize the query generator
        self.query_generator = create_flux_query_generator(anthropic_claude_model, sensor_id)

        # Initialize the InfluxDB query executor
        self.query_executor = InfluxDBQueryExecutor(
            url=st.secrets["INFLUXDB_URL"],
            token=st.secrets["INFLUXDB_TOKEN"],
            org=st.secrets["INFLUXDB_ORG"],
        )

    def run(self, task_description: str):
        """Generates and executes a Flux query for a given task description."""
        # Generate the Flux query
        generated_query = self.query_generator.invoke(task_description)['text']
        print("Generated Flux Query:", generated_query)

        # Execute the generated Flux query on InfluxDB
        execution_result = self.query_executor.execute_query(generated_query)
        return execution_result

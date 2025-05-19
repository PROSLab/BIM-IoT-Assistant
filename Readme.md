# BIM-IoT Assistant

## Description
BIM-IoT Assistant is a chatbot that integrates Building Information Modeling (BIM) data with Internet of Things (IoT) sensor data to provide intelligent responses to queries about buildings and their sensor readings. The system uses a knowledge graph (GraphDB) to store building information and time-series database (InfluxDB) to store sensor data.

### Directory Structure
- **competency-questions/**: Contains a PDF with questions the system should be able to answer
- **databases/**: Configuration files for GraphDB and InfluxDB connections
- **dataset/**: Contains the data files for the smart home example
- **prompts/**: Contains prompt templates for the LLM to generate SPARQL queries
- **tools/**: Contains tools for retrieving data from GraphDB and InfluxDB

## Requirements
- Python 3.8+
- GraphDB instance running locally or remotely
- InfluxDB instance running locally or remotely
- Anthropic API key for Claude LLM

## Installation and Setup
1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure the databases:
   - Set up GraphDB with the smart home dataset
   - Set up InfluxDB with the sensor data
   - Update the connection details in `databases/graphdb_config.py` and `databases/influx.py`
4. Configure the LLM:
   - Get an API key from Anthropic
   - Update the API key and model name in `llm.py`

## Usage
You can run the prototype by executing the following command in the terminal:
```
streamlit run bot.py
```

This will start a Streamlit web application where you can interact with the BIM-IoT Assistant. You can ask questions about the building structure, elements, sensors, and their readings.

Example queries:
- "List the rooms located on the first floor"
- "Information about a room"
- "Which is the lowest temperature registered in the kitchen?"

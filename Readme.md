# BIM-IoT Assistant

## Description
BIM-IoT Assistant is a chatbot that integrates Building Information Modeling (BIM) data with Internet of Things (IoT) sensor data to provide intelligent responses to queries about buildings and their sensor readings. The system uses a knowledge graph (GraphDB) to store building information and time-series database (InfluxDB) to store sensor data.

### Relevant Directories
- [**competency-questions/**](competency-questions): Contains a PDF with questions the system should be able to answer
- [**prompts/**](prompts): Contains prompt templates for the LLM to generate SPARQL queries
- [**dataset/**](dataset): Contains the data files for the smart home example

## Requirements
- Python 3.8+
- GraphDB instance
- InfluxDB instance
- Neo4J instance
- LLM API key
- Docker compose


## Installation and Setup
1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Database Setup

### Run instances with Docker Compose
You can run the databases using docker compose.
1. Copy the provided [`.env.example`](.env.example) in `.env` and edit the file based on your preferences.
2. Then start the docker compose with the command:
   ```
   docker compose up -d
   ```

3. You can check the logs with `docker compose logs -f`

Now you should be able to connect to the web interfaces od the databases:
   - InfluxDB (accessible at http://localhost:8086)
   - GraphDB (accessible at http://localhost:7200)
   - Neo4j (accessible at http://localhost:7474)

### Configure InfluxDB (optional if you do not use the Docker Compose):
   - Access the InfluxDB UI at http://localhost:8086
   - Create a new organization named "BIMIoT"
   - Create a new bucket named "OpenSmartHome"
   - Generate an API token and save it for later use

### Configure GraphDB
   - Access the GraphDB UI at http://localhost:7200
   - Create a new repository named "smartHome"

## Environment Setup

1. Copy the fine [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example) to `.streamlit/secrets.toml`).

2. Edit the variable choosing the LLM model and the database type (GraphDB or Neo4j). For Example:
```toml
# LLM API Ke
LLM_API_KEY = "your-anthropic-api-key"

# InfluxDB Configuration

# InfluxDB Configuration
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "your-influxdb-token"
INFLUXDB_ORG = "BIMIoT"
INFLUXDB_DATASET_SOURCE = "/dataset/OSH_Measurements"

GRAPHDB_URL = "http://localhost:7200/repositories/smartHome"

# Neo4j Database Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j user"
NEO4J_PASSWORD = "neo4j user's password"

TTL_FILE_PATH = "dataset/openSmartHome_Donkers.ttl"

# graphdb (default) or neo4j
BACKEND_TYPE = "graphdb"
```

## Data Import

### Importing Sensor Data to InfluxDB

1. If needed, update the path to your sensor data CSV files defined in `INFLUXDB_DATASET_SOURCE` (see [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example)) 

2. Run the import script:
   ```bash
   python import_sensor_data.py
   ```
   
3. Check the imported data (optional). 
From the query builder of InfluxDB you can use this query:
   ```
   from(bucket: "OpenSmartHome")
   |> range(start: 0) // Cerca dall'origine (Unix epoch) fino ad oggi
   |> first()         // Mostra solo il primo dato inserito in assoluto
   ```

### Importing Sensor Data to GraphDB
1. Import the TTL file containing the building graph data through the GraphDB workbench interface

### Importing Sensor Data to Neo4J
1. Update the path to the TTL file `TTL_FILE_PATH`.

2. Run the import script:
   ```bash
   python import_ttl_neo4j.py
   ```


## Usage
You can select the preferred backend by changing the value of `BACKEND_TYPE` ([`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example)).
The default is `graphdb` but you can change it in `neo4j`.

You can run the prototype by running the following command in the terminal:
```bash
streamlit run bot.py
```
This will start a Streamlit web application at the address http://localhost:8501/ 

You can now interact with the BIM-IoT Assistant. You can ask questions about the building structure, elements, sensors, and their readings.

Example queries:
- "List the rooms located on the first floor"
- "Information about a room"
- "Which is the lowest temperature registered in the kitchen?"

## Authors
- Daniele Parumboiu
- Massimo Callisto De Donato
- Emanuele Laurenzi

## Credits
- University of Camerino (UNICAM)
- University of Applied Sciences and Arts Northwestern Switzerland (FHNW)

## License
This project is licensed under the BSD-3-Clause License - see the LICENSE file for details.

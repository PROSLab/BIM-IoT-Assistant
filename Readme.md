# BIM-IoT Assistant

## Description
BIM-IoT Assistant is a chatbot that integrates Building Information Modeling (BIM) data with Internet of Things (IoT) sensor data to provide intelligent responses to queries about buildings and their sensor readings. The system uses a knowledge graph (GraphDB) to store building information and time-series database (InfluxDB) to store sensor data.

### Relevant Directories
- [**competency-questions/**](competency-questions): Contains a PDF with questions the system should be able to answer
- [**prompts/**](prompts): Contains prompt templates for the LLM to generate SPARQL queries
- [**dataset/**](dataset): Contains the data files for the smart home example

## Requirements
- Docker compose
- OpenRouter API key
- Python 3.8+
- GraphDB instance
- InfluxDB instance
- Neo4J instance

## Installation and Setup

This step is only required to import the initial dataset into the databases.

1. Clone this repository
2. Create and activate a virtual environment
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Database Setup

You can run the databases using docker compose.
1. Copy the provided [`.env.example`](.env.example) in `.env` and edit the file based on your preferences.
2. Start the docker compose with the command:
   ```
   docker compose up -d
   ```

3. You can check the logs with `docker compose logs -f`

Now, you should be able to connect at
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

### Application Environment Setup
To use the application, a proper dataset must be loaded in the databases. 
1. 
2. Copy the file [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example) to `.streamlit/secrets.toml`).

3. Edit the variable to choose the LLM model and the database type (GraphDB or Neo4j). For example:
```toml
# LLM API Key
LLM_API_KEY = "your-openrouter-api-key"

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

### Data Import

**IoT sensors dataset**

InfluxDB default dataset refers to the sensor data CSV files defined in `INFLUXDB_DATASET_SOURCE` (see [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example)).

To import the dataset, proceed as follows:

1. Run the import script:
   ```bash
   python import_sensor_data.py
   ```
   
2. Check the imported data (optional). 
From the query builder of InfluxDB you can use this query:
   ```
   from(bucket: "OpenSmartHome")
   |> range(start: 0) 
   |> first() 
   ```

**Importing RDF dataset to GraphDB**

The BIM dataset to load in GraphDB refers to the `TTL_FILE_PATH` file defined in `INFLUXDB_DATASET_SOURCE` (see [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example))
TTL file can be imported through the GraphDB workbench interface

**Importing LPG dataset to Neo4j**
1. Update the path to the TTL file `TTL_FILE_PATH` (see [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example)).

2. Run the import script:
   ```bash
   python import_ttl_neo4j.py
   ```

## Usage of the Virtual Assistant
You can select the preferred backend by changing the value of `BACKEND_TYPE` ([`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example)).
The default is `graphdb` but you can change it in `neo4j`.

You can restart the docker compose of the streamlit application:

```bash
docker compose stop streamlit
docker compose rm streamlit
docker compose up -d streamlit
```

You can also run the prototype by running the following command in the terminal:
```bash
streamlit run bot.py
```

To access the Streamlit web application, open the web browser at the address http://localhost:8501/ 

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

## References
This work is inspired by:

- Callisto De Donato, M., Laurenzi, E., & Porumboiu, D. (2025). _A hybrid artificial intelligence to support information retrieval in smart buildings_. 
Joint Proceedings of the BIR 2025 Workshops and Doctoral Consortium, 4034, 157–169. https://ceur-ws.org/Vol-4034/paper79.pdf

## License
This project is licensed under the BSD-3-Clause License - see the LICENSE file for details.


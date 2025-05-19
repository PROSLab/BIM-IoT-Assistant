from tools.influx_sensor_data_retriever import InfluxDBQueryExecutor

influx_config = InfluxDBQueryExecutor(url="INFLUXDB_URL", token="INFLUXDB_TOKEN",
                                                    org="INFLUXDB_ORG")
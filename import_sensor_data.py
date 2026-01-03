from collections import OrderedDict
from csv import DictReader
from pathlib import Path
import os
import reactivex as rx
from reactivex import operators as ops
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WriteOptions

import streamlit as st


def parse_row(row: OrderedDict, room: str, measurement: str):
    """Parse row of CSV file into Point
        ...

    :param row: the row of CSV file
    :return: Parsed csv row to [Point]
    """

    """
     For better performance is sometimes useful directly create a LineProtocol to avoid unnecessary escaping overhead:
     """
    sensorid = ""
    match room:
        case "Kitchen":
            sensorid = "b3ca6858-e675-4f4a-bca7-863846825601"
        case "Bathroom":
            sensorid = "b3ca6858-e675-4f4a-bca7-86384682547a"
        case "Dining":
            sensorid = "b3ca6858-e675-4f4a-bca7-86384683a0fc"
        case "Bedroom":
            sensorid = "b3ca6858-e675-4f4a-bca7-86384682559d"
        case "Living":
            sensorid = "b3ca6858-e675-4f4a-bca7-863846825941"
        case "Toilet":
            sensorid = "b3ca6858-e675-4f4a-bca7-8638468254e5"
        case "Outdoor":
            sensorid = "b3ca6858-e675-4f4a-bca7-863484682547"

    vl = float(row["value"])
    tm = int(row["time"])
    return (
        Point(measurement)
        .tag("sensorId", sensorid)
        .field("value", vl)
        .time(datetime.fromtimestamp(tm).isoformat())
    )


client = InfluxDBClient(
    url=st.secrets["INFLUXDB_URL"],
    token=st.secrets["INFLUXDB_TOKEN"],
    org=st.secrets["INFLUXDB_ORG"],
    debug=True,
)

"""
Create client that writes data in batches with 50_000 items.
"""
write_api = client.write_api(
    write_options=WriteOptions(batch_size=50_000, flush_interval=10_000)
)
print("Going to open folder: " + st.secrets["INFLUXDB_DATASET_SOURCE"])

paths = Path(st.secrets["INFLUXDB_DATASET_SOURCE"]).glob("**/*.csv")
for path in paths:
    # because path is object not string
    path_in_str = str(path)
    print(path_in_str)
    # Split the path and get the filename
    filename = os.path.basename(path_in_str)

    # Remove the file extension
    name_without_extension = os.path.splitext(filename)[0]

    # Split the remaining string and get the last two words
    words = name_without_extension.split("_")
    word1, word2 = words[-2], words[-1]

    """
    Converts into sequence of data point
    """
    data = rx.from_iterable(DictReader(open(path_in_str, "r"), delimiter="\t", fieldnames=['time','value'])).pipe(
        ops.map(lambda row: parse_row(row, word1, word2))
    )
    print("doing..")
    """
    Write data into InfluxDB
    """
    write_api.write(bucket="OpenSmartHome", record=data)

write_api.close()
"""
Close client
"""
client.close()

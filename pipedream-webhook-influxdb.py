from pipedream.script_helpers import (steps, export)
import os, time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
#from influxdb_client import InfluxDBClient, Point, client.write_api

token = "YOUR-TOKEN"
org = "YOUR-ORG-ID"
url = "YOUR-INFLUXDB-URL"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

datacakedata = steps["trigger"]["event"]["body"]
sensordata = steps["trigger"]["event"]["body"]["data"]
print(steps["trigger"]["event"]["body"]["data"])

write_api = client.write_api(write_options=SYNCHRONOUS)

database="YOUR-BUCKET"
measurement = sensordata['device_name']
print(measurement)


for item in sensordata['result']:
    field = item['field']
    value = item['value']
    print(f"Field: {field}, Value: {value}")
    point = (
        influxdb_client.Point(measurement).tag("serial",sensordata['device_serial']).field(field, value)
    )
    write_api.write(bucket=database, org=org, record=point)
    time.sleep(1)


print("Complete. Return to the InfluxDB UI.")

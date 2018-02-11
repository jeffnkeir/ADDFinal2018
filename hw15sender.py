import uuid
import datetime
import random
import json
from azure.servicebus import ServiceBusService

sbs = ServiceBusService(service_namespace='jnkhw15evthub01', shared_access_key_name='RootManageSharedAccessKey', shared_access_key_value='oZT//BAPYlfbxFkfhiKt3J11DRbHCReJA9V0DVh0tYQ=')
devices = []
for x in range(0, 10):
   devices.append(str(uuid.uuid4()))

for y in range(0,20):
   for dev in devices:
       reading = {'id': dev, 'timestamp': str(datetime.datetime.utcnow()), 'uv': random.random(), 'temperature': random.randint(70, 100), 'humidity': random.randint(70, 100)}
       s = json.dumps(reading)
       sbs.send_event('jnkhw15hub01', s)
   print(y)
   

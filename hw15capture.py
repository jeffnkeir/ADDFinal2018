
import os
import string
import json
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from azure.storage.blob import BlockBlobService

def processBlob(filename):
   reader = DataFileReader(open(filename, 'rb'), DatumReader())
   dict = {}
   for reading in reader:
       parsed_json = json.loads(reading["Body"])
       if not 'id' in parsed_json:
           return
       if not dict.has_key(parsed_json['id']):
           list = []
           dict[parsed_json['id']] = list
       else:
           list = dict[parsed_json['id']]
           list.append(parsed_json)
   reader.close()
   for device in dict.keys():
       deviceFile = open(device + '.csv', "a")
       for r in dict[device]:
           deviceFile.write(", ".join([str(r[x]) for x in r.keys()])+'\n')

def startProcessing(accountName, key, container):
   print('Processor started using path: ' + os.getcwd())
   block_blob_service = BlockBlobService(account_name=accountName, account_key=key)
   generator = block_blob_service.list_blobs(container)
   for blob in generator:
       if blob.properties.content_length > 508:
           print('Downloaded a non empty blob: ' + blob.name)
           cleanName = string.replace(blob.name, '/', '_')
           block_blob_service.get_blob_to_path(container, blob.name, cleanName)
           processBlob(cleanName)
           os.remove(cleanName)
       block_blob_service.delete_blob(container, blob.name)
startProcessing('jnkhw15stora01', 'J/7wuAfGJNxIv5IrtkJvDo2MyvNrMR/Bj3NQjTfrtgyLXQavGSQL31U94vaHaumtyIZEeLgFnjPoyp83n5mn5w==', 'jnkhw15test01')

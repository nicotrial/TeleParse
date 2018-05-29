from elasticsearch import Elasticsearch
from HackerPrint import hackerPrint, hackerPrintErr
import time
from datetime import datetime

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

import requests
res = requests.get('http://localhost:9200')
print(res.content)

settings1 = {
        "mappings": {
            "telegram": {
                "properties": {
                    "date": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                }
            },
        }
}
res1 = es.indices.create(index='testing', ignore=400, body=settings1)

print (datetime.now())
print (time.time())
print (time.localtime(time.time()))
hackerPrintErr("\n[!] Esto es una mierda y no funciona \n", "ERROR", True)



res1 = es.index(
    index="testing",
    doc_type="telegram",
    id=1,
    body={
        "msg.sender.id": "2",
        "msg.sender.first_name": "nombre",
        "date": 1514764800000
    }
)
print("done")

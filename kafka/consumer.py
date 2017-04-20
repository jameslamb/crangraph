#!/usr/bin/env python

from kafka import KafkaConsumer
import json
import pickle
import sys
consumer = KafkaConsumer('package_metadata',
                         bootstrap_servers='localhost:9092')

#for msg in consumer:
while True:
   msg = next(consumer)
   msg_dict = json.loads(msg.value)
   out_tuple = (msg_dict['package'], msg_dict['description'])
   print(type(out_tuple))
   print(out_tuple)

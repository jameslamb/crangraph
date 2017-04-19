#!/usr/bin/env python

from kafka import KafkaConsumer
import pickle
import sys

# Set up the consumer
consumer = KafkaConsumer('package_metadata', 
                         bootstrap_servers='localhost:9092',
                         value_deserializer=pickle.loads)

for msg in consumer:
   sys.stdout.write(str(msg.value))

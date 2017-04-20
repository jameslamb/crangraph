#from crangraph.storm.spouts import PackageMetadataSpout

from __future__ import absolute_import, print_function, unicode_literals

from kafka import KafkaConsumer
import pickle
from streamparse.spout import Spout

class PackageMetadataSpout(Spout):

    outputs = ['package', 'description']

    def initialize(self, stormconf, context):
            
        # Set up the consumer
        self.consumer = KafkaConsumer('package_metadata', 
                         bootstrap_servers='localhost:9092',
                         value_deserializer=pickle.loads)

    def next_tuple(self):
        self.emit(next(self.consumer))

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing
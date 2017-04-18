from kafka import KafkaConsumer
consumer = KafkaConsumer('crangraph_topic', bootstrap_servers='localhost:9092')

for msg in consumer:
    print (msg)

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(100):
    producer.send('crangraph_topic', b'James Jason Surya: ' + str(i))

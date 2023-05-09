import json
from kafka import KafkaConsumer

# create a Kafka consumer object with the specified bootstrap server(s) and topic name
consumer = KafkaConsumer('my-topic1', bootstrap_servers=['0.0.0.0:49153'], value_deserializer=lambda m: json.loads(m.decode('ascii')))

# continuously poll for new messages
for message in consumer:
    # print the received message and its partition and offset
    print('Received message: %s (partition=%d, offset=%d)' % (message.value, message.partition, message.offset))

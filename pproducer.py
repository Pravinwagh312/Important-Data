import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['10.52.0.245:49153'], value_serializer=lambda m: json.dumps(m).encode('ascii'))

# create a dictionary representing the message
message_dict = {'message': 'Hello, World!2024', 'count': 23}

# send the message to the 'newtopic' topic as a JSON string
future = producer.send('newtopic', value=message_dict)

try:
    record_metadata = future.get(timeout=10)
    print('Message sent to partition %s, offset %s' % (record_metadata.partition, record_metadata.offset))
except Exception as e:
    print('Failed to send message:', e)
finally:
    producer.close()

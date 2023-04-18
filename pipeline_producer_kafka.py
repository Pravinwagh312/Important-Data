import json
import requests
from kafka import KafkaProducer

# Fetch the data from a GitHub pipeline
response = requests.get('https://api.github.com/repos/Pravinwagh312/Git-Runner/commits')
data = response.json()

# Create a Kafka producer object
producer = KafkaProducer(
    bootstrap_servers=['0.0.0.0:49153'],
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

# Send each commit message to the 'newtopic' topic as a JSON string
for commit in data:
    message_dict = {'message': commit['commit']['message'], 'count': len(commit['commit']['message'])}
    future = producer.send('newtopic', value=message_dict)

    try:
        record_metadata = future.get(timeout=10)
        print('Message sent to partition %s, offset %s' % (record_metadata.partition, record_metadata.offset))
    except Exception as e:
        print('Failed to send message:', e)

# Close the Kafka producer object
producer.close()

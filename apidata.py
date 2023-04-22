import requests
from kafka import KafkaProducer
import json
from datetime import datetime, timedelta

# Set the authentication header with your GitHub personal access token
headers = {'Authorization': 'Bearer your_github_token'}

# Calculate the date range for the search query
from_date = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
to_date = datetime.now().isoformat() + 'Z'

# Construct the search query to search for completed workflow runs within the date range
query = f'is:completed updated:{from_date}..{to_date}'

# Make a GET request to the GitHub API's "Search for workflow runs" endpoint
response = requests.get('https://api.github.com/search/actions', headers=headers, params={'q': query, 'per_page': '100'})

# Extract the necessary KPI parameters from the API response
total_executed = response.json()['total_count']
successful_workflow = len([item for item in response.json()['items'] if item['conclusion'] == 'success'])
failed_workflow = len([item for item in response.json()['items'] if item['conclusion'] == 'failure'])
aborted_workflow = len([item for item in response.json()['items'] if item['conclusion'] == 'cancelled'])

# Print the KPI parameters
print(f'Total Workflow Executed: {total_executed}')
print(f'Successful Workflow in 7 days: {successful_workflow}')
print(f'Failure Workflow in 7 days: {failed_workflow}')
print(f'Aborted Workflow: {aborted_workflow}')

# Create a Kafka producer and send the KPI parameters to a Kafka topic
producer = KafkaProducer(bootstrap_servers=['your_kafka_broker'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))
producer.send('your_kafka_topic', {'total_executed': total_executed, 'successful_workflow': successful_workflow, 'failed_workflow': failed_workflow, 'aborted_workflow': aborted_workflow})
producer.flush()

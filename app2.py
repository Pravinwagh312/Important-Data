from flask import Flask, request, jsonify
from confluent_kafka import Producer
import psycopg2
import json

# Configure Kafka producer
kafka_conf = {
    'bootstrap.servers': 'my-kafka:9092',
}

# Create Kafka producer instance
producer = Producer(kafka_conf)

# Configure PostgreSQL connection
pg_conn = psycopg2.connect(
    host="my-postgres",
    port=5432,
    database="mydatabase",
    user="postgres",
    password="postgres"
)

app = Flask(__name__)

@app.route('/send_data', methods=['POST'])
def send_data():
    # Receive JSON data from client
    data = request.get_json()

    # Serialize data to JSON string
    data_str = json.dumps(data)

    # Send data to Kafka
    producer.produce('my_topic', key='key', value=data_str)

    # Commit messages to ensure delivery
    producer.flush()

    # Store data in PostgreSQL
    with pg_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO my_table (data) VALUES (%s)",
            (data_str,)
        )
        pg_conn.commit()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

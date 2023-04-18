import json
from kafka import KafkaConsumer
import psycopg2
from psycopg2 import OperationalError

# Set up a Postgres database connection
def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="myuser",
            password="mypassword"
        )
        print("Connection successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    return connection

# Create a table in the database
def create_table(connection):
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL,
            count INTEGER NOT NULL
        )
        """
    )
    print("Table created successfully")

# Create a Kafka consumer object
consumer = KafkaConsumer(
    'newtopic',
    bootstrap_servers=['0.0.0.0:49153'],
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)

# Create a database connection and table
conn = create_connection()
create_table(conn)

# Continuously poll for new messages and insert them into the database
for message in consumer:
    data = message.value

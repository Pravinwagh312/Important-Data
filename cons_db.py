from kafka import KafkaConsumer
import psycopg2

bootstrap_servers = '10.52.0.245:9092'
topic = 'my_topic1'

# PostgreSQL connection details
postgres_host = '172.20.0.2'
postgres_port = 5432  # default PostgreSQL port
postgres_db = 'mydatabase'
postgres_user = 'myuser'
postgres_password = 'mypassword'

# Create a Kafka consumer instance
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda x: x.decode('utf-8'),
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

# Connect to the PostgreSQL container
conn = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    dbname=postgres_db,
    user=postgres_user,
    password=postgres_password
)

# Create a cursor object
cur = conn.cursor()

# Replace this with your INSERT query to insert data into the appropriate table
insert_query = "INSERT INTO your_table (column1, column2, ...) VALUES (%s, %s, ...)"

# Iterate through the messages in the consumer and insert them into the PostgreSQL table
for message in consumer:
    print(f'Topic: {message.topic}, Partition: {message.partition}, Offset: {message.offset}, Key: {message.key}, Value: {message.value}')
    
    # Prepare the data to be inserted into the table
    # Modify this based on the structure of your table and the data in the message
    data = (message.value,)


    # Execute the insert query
    cur.execute(insert_query, data)

    # Commit the transaction
    conn.commit()

# Close the cursor and connection
cur.close()
conn.close()


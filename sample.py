version: '3'
services:
  zookeeper:
    image: wurstmeister/zookeeper
    container_name: zookeeper
    networks:
      kafka-net:
        ipv4_address: 172.20.0.2
  kafka:
    image: wurstmeister/kafka
    container_name: kafka
    environment:
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://172.20.0.3:9092"
      KAFKA_LISTENERS: "PLAINTEXT://0.0.0.0:9092"
      KAFKA_ZOOKEEPER_CONNECT: "172.20.0.2:2181"
    ports:
      - "9092:9092"
    networks:
      kafka-net:
        ipv4_address: 172.20.0.3
  producer:
    build: ./producer
    depends_on:
      - kafka
    networks:
      kafka-net:
  consumer:
    build: ./consumer
    depends_on:
      - kafka
    networks:
      kafka-net:
networks:
  kafka-net:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.20.0.0/16

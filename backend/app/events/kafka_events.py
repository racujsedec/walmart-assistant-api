"""Optional Kafka audit publisher. Never put raw prompts or PII into events."""
import json, os

def publish_audit(event: dict) -> None:
    brokers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    if not brokers:
        return  # local lab: no broker configured
    from confluent_kafka import Producer
    producer = Producer({"bootstrap.servers": brokers})
    producer.produce("assistant.audit.v1", value=json.dumps(event).encode())
    producer.flush(3)

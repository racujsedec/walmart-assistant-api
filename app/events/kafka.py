import os,json
async def publish_audit(event:dict):
 if not os.getenv('KAFKA_BOOTSTRAP_SERVERS'):return False
 from confluent_kafka import Producer
 p=Producer({'bootstrap.servers':os.environ['KAFKA_BOOTSTRAP_SERVERS']})
 p.produce('assistant-audit',json.dumps(event).encode());p.flush(5)
 return True
# Not wired to transactions. Production requires durable outbox and consumer idempotency.

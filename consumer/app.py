from kafka import KafkaConsumer
from mongo_manager import insert
import os

try:
	KAFKA_CLUSTER_URL = os.environ.get("KAFKA_CLUSTER_URL")
	print(KAFKA_CLUSTER_URL)
	TOPIC_ISTANBUL = os.environ.get("TOPIC_ISTANBUL")
	TOPIC_MOSCOW = os.environ.get("TOPIC_MOSCOW")
	TOPIC_BEIJING = os.environ.get("TOPIC_BEIJING")
	TOPIC_TOKYO = os.environ.get("TOPIC_TOKYO")
	TOPIC_LONDON = os.environ.get("TOPIC_LONDON")

	consumer = KafkaConsumer(	TOPIC_LONDON, 
								TOPIC_BEIJING, 
								TOPIC_MOSCOW,
								TOPIC_ISTANBUL,
								TOPIC_TOKYO, 
								bootstrap_servers=KAFKA_CLUSTER_URL)

	for msg in consumer:
		print(msg)
		insert(msg.value.decode('utf-8'))


except Exception as e:
	raise e
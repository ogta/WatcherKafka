import json
import time
from datetime import datetime
from kafka import SimpleClient
from kafka.common import OffsetRequestPayload
import os
from flask import Flask, Response, render_template

application = Flask(__name__)

TOPIC_ISTANBUL = os.environ.get("TOPIC_ISTANBUL")
TOPIC_MOSCOW = os.environ.get("TOPIC_MOSCOW")
TOPIC_BEIJING = os.environ.get("TOPIC_BEIJING")
TOPIC_TOKYO = os.environ.get("TOPIC_TOKYO")
TOPIC_LONDON = os.environ.get("TOPIC_LONDON")

@application.route('/')
def index():
    return render_template('index.html')

def find_offset(topic_name):
    brokers = os.environ.get("KAFKA_CLUSTER_IP")
    topic = topic_name
    client = SimpleClient(brokers)

    partitions = client.topic_partitions[topic]
    offset_requests = [OffsetRequestPayload(topic, p, -1, 1) for p in partitions.keys()]

    offsets_responses = client.send_offset_request(offset_requests)

    return offsets_responses[0].offsets[0]

@application.route('/monitoring')
def monitoring():

    def get_offset_count():
        while True:
            topic_istanbul = find_offset(TOPIC_ISTANBUL)
            topic_tokyo = find_offset(TOPIC_TOKYO)
            topic_moscow = find_offset(TOPIC_MOSCOW)
            topic_beijing = find_offset(TOPIC_BEIJING)
            topic_london = find_offset(TOPIC_LONDON)

            time_of_request = datetime.now().strftime('%H:%M:%S')
            json_data = json.dumps(
                {
                    'time_istanbul': time_of_request, 'value_istanbul': topic_istanbul,
                    'topic_tokyo': time_of_request, 'value_tokyo': topic_tokyo,
                    'topic_moscow': time_of_request, 'value_moscow': topic_moscow,
                    'topic_beijing': time_of_request, 'value_beijing': topic_beijing,
                    'topic_london': time_of_request, 'value_london': topic_london
                 })
            yield f"data:{json_data}\n\n"
            time.sleep(10)
    return Response(get_offset_count(), mimetype='text/event-stream')


if __name__ == '__main__':
    application.run(debug=True, threaded=True, host='0.0.0.0')

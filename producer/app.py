import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import sys
import os
from kafka import KafkaProducer
LOG_FILE_NAME = os.environ.get("LOG_FILE_NAME")

global counter
counter = 0

def send_message(log):
    print(log)
    ISTANBUL_LOG_SEPERATOR = "Istanbul"
    TOKYO_LOG_SEPERATOR = "Tokyo"
    MOSCOW_LOG_SEPERATOR = "Moskow"
    BEIJING_LOG_SEPERATOR = "Beijing"
    LONDON_LOG_SEPERATOR = "London"


    KAFKA_CLUSTER_URL = os.environ.get("KAFKA_CLUSTER_URL")
    TOPIC_ISTANBUL = os.environ.get("TOPIC_ISTANBUL")
    TOPIC_MOSCOW = os.environ.get("TOPIC_MOSCOW")
    TOPIC_BEIJING = os.environ.get("TOPIC_BEIJING")
    TOPIC_TOKYO = os.environ.get("TOPIC_TOKYO")
    TOPIC_LONDON = os.environ.get("TOPIC_LONDON")

    producer = KafkaProducer(bootstrap_servers=KAFKA_CLUSTER_URL)
    try:
        if ISTANBUL_LOG_SEPERATOR in log:
            producer.send(TOPIC_ISTANBUL, log.encode()).get()
        elif TOKYO_LOG_SEPERATOR in log:
            producer.send(TOPIC_TOKYO, log.encode()).get()
        elif MOSCOW_LOG_SEPERATOR in log:
            producer.send(TOPIC_MOSCOW, log.encode()).get()
        elif BEIJING_LOG_SEPERATOR in log:
            producer.send(TOPIC_BEIJING, log.encode()).get()
        elif LONDON_LOG_SEPERATOR in log:
            producer.send(TOPIC_LONDON, log.encode()).get()
    except Exception as e:
        raise e


def update_last_counter(counter_val):
    global counter
    counter = counter_val-1

def file_len():
    i = 0
    with open(LOG_FILE_NAME) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def find_changes_and_send_to_producer_factory(start):
    i = 0
    with open(LOG_FILE_NAME) as f:
        for i, l in enumerate(f):
            if i > start:
                send_message(l.strip())
    return i + 1



class FileChangesHandler(PatternMatchingEventHandler):
    patterns = ["*.txt", "*.lxml"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        last = file_len()
        if last > counter :
            update_last_counter(find_changes_and_send_to_producer_factory(counter))

        #print (event.src_path, event.event_type, last)  # for debug

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(FileChangesHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
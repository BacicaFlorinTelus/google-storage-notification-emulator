import tempfile
import time
import os

from google.cloud import pubsub_v1
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

topic_id = os.getenv("TOPIC_ID")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv("PUBSUB_PROJECT_ID"), topic_id)


class Watcher:
    DIRECTORY_TO_WATCH = "/var/watcher/files".format(tempfile.gettempdir())

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(2)
        except Exception as e:
            self.observer.stop()
            print("Error")
        self.observer.join()


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        print("Event type: {} \n Event path {}".format(event.event_type, event.src_path))
        if event.is_directory:
            return None
        elif event.event_type == "created":
            data_str = f"Empty payload"
            data = data_str.encode("utf-8")
            publisher.publish(
                topic_path, data, bucketId="", objectId=event.src_path
            )
            print("Event successfully sent to pubsub!")


if __name__ == '__main__':
    print("Watcher started!")
    w = Watcher()
    w.run()

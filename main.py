import tempfile
import time
import os

from google.cloud import pubsub_v1

topic_id = os.getenv("TOPIC_ID")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv("PUBSUB_PROJECT_ID"), topic_id)


class Watcher:
    DIRECTORY_TO_WATCH = "/var/watcher/files".format(tempfile.gettempdir())

    def run(self):
        event_handler = Handler(self.DIRECTORY_TO_WATCH)
        try:
            while True:
                time.sleep(0.5)
                event_handler.search_for_new_files()
        except Exception as e:
            print("Error")


class Handler:
    def __init__(self, directory):
        self.files = list()
        self.directory = directory

    def __get_files_from_directory(self):
        return os.listdir(self.directory)

    def search_for_new_files(self):
        new_files = self.__get_files_from_directory()
        for file in new_files:
            if file in self.files:
                print("New file created {}, an event will be send to pubsub!".format(file))
                object_id = self.directory + "/" + file
                data_str = f"Empty payload"
                data = data_str.encode("utf-8")
                publisher.publish(
                    topic_path, data, bucketId="", objectId=object_id
                )
                print("Event successfully sent to pubsub!\n")
        self.files = new_files


if __name__ == '__main__':
    print("Watcher started!")
    w = Watcher()
    w.run()

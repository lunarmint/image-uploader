import logging

from pymongo import MongoClient

from utils.config import config

log = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.username = config["database"]["username"]
        self.password = config["database"]["password"]
        self.hostname = config["database"]["hostname"]
        self.port = config["database"]["port"]
        self.database_name = "users"
        self.collection_name = config["database"]["collection_name"]

        if not all([self.hostname, self.port, self.username, self.password]):
            log.error("One or more database connection variables are missing.")
            raise SystemExit

        self.url = f"mongodb://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database_name}"

    def connect(self):
        return MongoClient(self.url)

    def get_users(self):
        client = self.connect()
        database = client[self.database_name]
        collection = database[self.collection_name]
        return collection

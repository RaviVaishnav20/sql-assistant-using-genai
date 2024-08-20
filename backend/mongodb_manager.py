from pymongo import MongoClient
import json

class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def connect_with_url(self, url, db_name):
        self.client = MongoClient(url)
        self.db = self.client[db_name]

    def upsert(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.replace_one(
            {"_id": document["_id"]},
            document,
            upsert=True
        )
        return result

    def delete(self, collection_name, _id):
        collection = self.db[collection_name]
        result = collection.delete_one({"_id": _id})
        return result

    def get(self, collection_name, _id):
        collection = self.db[collection_name]
        return collection.find_one({"_id": _id})

    def get_all(self, collection_name):
        collection = self.db[collection_name]
        return list(collection.find())

    def run_query(self, query, collection_name):
        try:
            collection = self.db[collection_name]
            result = collection.aggregate(pipeline=query)
            return json.dumps(list(result), default=str), "JSON"
        except Exception as e:
            return str(e), "TEXT"

    def get_collection_schemas(self, collection_name):
        sample_doc = self.db[collection_name].find_one()
        if sample_doc:
            return json.dumps(sample_doc, default=str, indent=2)
        return ""

    def get_collection_schemas_for_prompt(self, collection_name):
        schema = self.get_collection_schemas(collection_name)
        return f"Collection: {collection_name}\nSchema:\n{schema}\n"
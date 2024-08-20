#### mongodb_connection_test.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os


def test_mongodb_connection(mongo_url, db_name):
    try:
        # Attempt to establish a connection
        client = MongoClient(mongo_url)

        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')

        # If we reach this point, the connection is successful
        print("MongoDB connection successful!")

        # Get database
        db = client[db_name]

        # List all collections in the database
        collections = db.list_collection_names()
        print(f"Collections in {db_name}:")
        for collection in collections:
            print(f"- {collection}")

        # Get count of documents in each collection
        for collection in collections:
            count = db[collection].count_documents({})
            print(f"Collection '{collection}' has {count} documents")

        return True

    except ConnectionFailure:
        print("MongoDB connection failed!")
        return False
    finally:
        if 'client' in locals():
            client.close()


def insert_test_document(mongo_url, db_name, collection_name):
    try:
        client = MongoClient(mongo_url)
        db = client[db_name]
        collection = db[collection_name]

        # Insert a test document
        test_document = {"test_key": "test_value", "number": 42}
        result = collection.insert_one(test_document)

        print(f"Test document inserted with id: {result.inserted_id}")

        # Verify the document was inserted
        retrieved_doc = collection.find_one({"_id": result.inserted_id})
        print(f"Retrieved document: {retrieved_doc}")

        return True

    except Exception as e:
        print(f"Error inserting test document: {str(e)}")
        return False
    finally:
        if 'client' in locals():
            client.close()


def run_mongo_tests():
    # Get MongoDB connection details from environment variables
    mongo_url = "mongodb://localhost:27017" # os.environ.get("MONGO_URL")
    db_name = "test" #os.environ.get("MONGO_DB")

    if not mongo_url or not db_name:
        print("MongoDB connection details not found in environment variables.")
        return

    print("Testing MongoDB connection...")
    connection_successful = test_mongodb_connection(mongo_url, db_name)

    if connection_successful:
        print("\nTesting document insertion...")
        insert_test_document(mongo_url, db_name, "test_collection")


if __name__ == "__main__":
    run_mongo_tests()
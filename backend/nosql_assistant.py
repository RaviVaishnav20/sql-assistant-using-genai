# #### nosql_assistant.py
import os
from backend.mongodb_manager import MongoDBManager
from backend import llm
import backend.config as cfg
# MONGO_URL = os.environ.get("MONGO_URL")
# MONGO_DB = os.environ.get("MONGO_DB")
MONGO_URL = cfg.MONGO_URL
MONGO_DB = cfg.MONGO_DB
MONGODB_COLLECTION_SCHEMAS_CAP_REF = "COLLECTION_SCHEMAS"
RESPONSE_FORMAT_CAP_REF = "RESPONSE_FORMAT"
QUERY_DELIMITER = "---------"
example_query = [
    {"$match": {"field1": "value1"}},
    {"$group": {"_id": "$field2", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]
def nosql_assistant(message, collection_name):
    prompt = f"Fulfill this database query for MongoDB collection '{collection_name}': {message}."
    with MongoDBManager() as db:
        db.connect_with_url(MONGO_URL, MONGO_DB)

        collection_schemas = db.get_collection_schemas_for_prompt(collection_name)

        prompt = llm.add_cap_ref(
            prompt,
            f"Use these {MONGODB_COLLECTION_SCHEMAS_CAP_REF} to satisfy the database query. Use MongoDB query syntax. example query: {example_query}",
            MONGODB_COLLECTION_SCHEMAS_CAP_REF,
            collection_schemas,
        )

        prompt = llm.add_cap_ref(
            prompt,
            f"\n\nDo not give any opening remarks or comments and also do not give any concluding remarks or comments. I need to be able to easily parse the MongoDB query from your response. Give response in string",
            RESPONSE_FORMAT_CAP_REF,
            f"""<MongoDB query exclusively as raw text>""",
        )

        prompt_response = llm.prompt(
            f"Clean and format the following MongoDB query to ensure it is executable: {prompt} Ensure that the query adheres to MongoDB syntax standards, checks for potential issues, and confirms that the collection and field names are accurate. Do not include any code block markers in the response.")

        mongodb_query = prompt_response.strip()
        print("mongodb_query", mongodb_query)
        result = db.run_query(mongodb_query, collection_name)
        print("result", result)

        # Return only the result, no explanation or query
        return result[0], "TEXT", "", ""

#nosql_assistant(message, collection_name)
if __name__ == '__main__':
    message = f"Count the number of documents in the collection that have a 'food_type' field equal to 'ready-to-eat'"
    collection_name = "brooklyn.csv"
    for i in nosql_assistant(message, collection_name):
        print(i)
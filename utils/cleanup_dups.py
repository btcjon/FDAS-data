from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB URI and database name
mongodb_uri = os.getenv('MONGODB_URI')
db_name = os.getenv('DB_NAME')

# Create a MongoDB client
client = MongoClient(mongodb_uri)
db = client[db_name]
collection = db['positions']

# Get a cursor to all documents in the collection
cursor = collection.find()

# Create a set to hold the ids of documents to remove
ids_to_remove = set()

# Total duplicates counter
total_duplicates = 0

# Iterate over all documents in the collection
for doc in cursor:
    # Find duplicates of the current document
    duplicates = list(collection.find({'id': doc['id']}))

    # If there are duplicates
    if len(duplicates) > 1:
        num_duplicates = len(duplicates) - 1
        total_duplicates += num_duplicates

        # Skip the first document (it's the one we want to keep)
        duplicates.pop(0)

        # Add the ids of the remaining duplicates to the set of ids to remove
        for duplicate in duplicates:
            ids_to_remove.add(duplicate['_id'])

print(f"Total duplicates found: {total_duplicates}")

# Remove the duplicates
for id in ids_to_remove:
    collection.delete_one({'_id': id})
print(f"Total duplicates removed: {len(ids_to_remove)}")

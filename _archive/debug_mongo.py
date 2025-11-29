import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

# Load env vars
load_dotenv()

uri = os.environ.get('MONGO_URI')
print(f"MONGO_URI present: {bool(uri)}")

if not uri:
    print("Error: MONGO_URI is missing.")
    sys.exit(1)

print("Attempting to connect...")
try:
    client = MongoClient(
        uri, 
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    # Force a connection
    info = client.server_info()
    print("Connection SUCCESS!")
    print(f"Server version: {info.get('version')}")
    
    db = client.get_database()
    print(f"Database name: {db.name}")
    
    # Try a write
    print("Attempting write...")
    result = db.test_collection.insert_one({'test': 'data'})
    print(f"Write SUCCESS! ID: {result.inserted_id}")
    
    # Clean up
    db.test_collection.delete_one({'_id': result.inserted_id})
    print("Cleanup SUCCESS!")

except Exception as e:
    print(f"Connection FAILED: {e}")

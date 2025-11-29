import os
import pymongo
from pymongo import MongoClient
import certifi

# Global client to reuse connection
_client = None
_db = None

def get_db():
    global _client, _db
    if _db is not None:
        return _db
    
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        return None

    try:
        # ca=certifi.where() is often needed for SSL on some platforms
        # Add timeout to prevent hanging
        _client = MongoClient(
            mongo_uri, 
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000  # 5 second timeout
        )
        _db = _client.get_database() # Uses the db name from the URI
        # Test the connection
        _client.server_info()
        return _db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def mongo_get_all_books():
    db = get_db()
    if db is None:
        return []
    # Convert _id to string id for compatibility if id is missing
    books = list(db.books.find())
    for book in books:
        if 'id' not in book:
            book['id'] = str(book.get('_id'))
        
        if '_id' in book:
            del book['_id']
    return books

def mongo_get_book(book_id):
    db = get_db()
    if db is None:
        return None
    
    # Try finding by 'id' string field first (legacy compatibility)
    book = db.books.find_one({'id': book_id})
    
    if book:
        if 'id' not in book:
            book['id'] = str(book.get('_id'))
        
        if '_id' in book:
            del book['_id']
    return book

def mongo_save_book(book):
    db = get_db()
    if db is None:
        return False
    
    # Use 'id' as the unique identifier
    db.books.update_one(
        {'id': book['id']},
        {'$set': book},
        upsert=True
    )
    return True

def mongo_delete_book(book_id):
    db = get_db()
    if db is None:
        return False
    db.books.delete_one({'id': book_id})
    return True

def mongo_save_library(library_data):
    """
    Saves the entire library list. 
    For MongoDB, we iterate and save each book.
    """
    db = get_db()
    print(f"DEBUG: get_db() in mongo_save_library returned: {db}")
    if db is None:
        return False
    
    # This is a bit inefficient for bulk, but safe
    for book in library_data.get('books', []):
        mongo_save_book(book)
    return True

def mongo_save_feedback(feedback_data):
    """
    Saves a feedback/contact message to the 'feedback' collection.
    """
    db = get_db()
    if db is None:
        return False
    
    # Add a timestamp if not present (though app.py usually handles this, good to be safe)
    if 'timestamp' not in feedback_data:
        from datetime import datetime
        feedback_data['timestamp'] = datetime.now().isoformat()

    db.feedback.insert_one(feedback_data)
    return True

def mongo_get_all_feedback():
    """
    Retrieves all feedback messages, sorted by newest first.
    """
    db = get_db()
    if db is None:
        return []
    
    # Sort by _id descending (newest first) naturally, or use timestamp if available
    feedback_list = list(db.feedback.find().sort('_id', -1))
    
    # Clean up _id for frontend usage
    for item in feedback_list:
        if '_id' in item:
            item['_id'] = str(item['_id'])
            
    return feedback_list

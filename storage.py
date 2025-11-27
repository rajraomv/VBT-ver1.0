import os
import database

def load_library():
    """
    Loads the library from MongoDB.
    Returns an empty library structure if connection fails.
    """
    if os.environ.get('MONGO_URI'):
        try:
            books = database.mongo_get_all_books()
            return {'books': books}
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            return {'books': []}
    
    print("DEBUG: MONGO_URI not set. Returning empty library.")
    return {'books': []}

def save_library(data):
    """
    Saves the library to MongoDB.
    """
    if os.environ.get('MONGO_URI'):
        try:
            return database.mongo_save_library(data)
        except Exception as e:
            print(f"MongoDB save failed: {e}")
            return False
            
    print("DEBUG: MONGO_URI not set. Cannot save library.")
    return False

def get_book(book_id):
    """
    Retrieves a specific book from MongoDB.
    """
    if os.environ.get('MONGO_URI'):
        try:
            return database.mongo_get_book(book_id)
        except Exception as e:
            print(f"MongoDB get_book failed: {e}")
            return None

    print("DEBUG: MONGO_URI not set. Cannot get book.")
    return None

def delete_book(book_id):
    """
    Deletes a book from MongoDB.
    """
    if os.environ.get('MONGO_URI'):
        try:
            return database.mongo_delete_book(book_id)
        except Exception as e:
            print(f"MongoDB delete_book failed: {e}")
            return False

    print("DEBUG: MONGO_URI not set. Cannot delete book.")
    return False

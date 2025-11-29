import database

def load_library():
    """
    Loads the library from MongoDB.
    Returns an empty library structure if connection fails.
    """
    try:
        books = database.mongo_get_all_books()
        return {'books': books}
    except Exception as e:
        print(f"MongoDB load failed: {e}")
        return {'books': []}

def save_library(data):
    """
    Saves the library to MongoDB.
    """
    try:
        print("DEBUG: Calling database.mongo_save_library")
        result = database.mongo_save_library(data)
        print(f"DEBUG: database.mongo_save_library returned {result}")
        return result
    except Exception as e:
        print(f"MongoDB save failed: {e}")
        return False

def get_book(book_id):
    """
    Retrieves a specific book from MongoDB.
    """
    try:
        return database.mongo_get_book(book_id)
    except Exception as e:
        print(f"MongoDB get_book failed: {e}")
        return None

def delete_book(book_id):
    """
    Deletes a book from MongoDB.
    """
    try:
        return database.mongo_delete_book(book_id)
    except Exception as e:
        print(f"MongoDB delete_book failed: {e}")
        return False

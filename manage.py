import uuid
from storage import load_library, save_library, delete_book
from fetcher import fetch_playlist_info, fetch_video_description, parse_sections


def add_book_logic(url, title=None):
    """Fetch a YouTube playlist and add it as a book.
    Returns a dict with status and message.
    """
    print("Fetching playlist info... this may take a moment.")
    info = fetch_playlist_info(url)
    if not info:
        return {"status": "error", "message": "Failed to fetch playlist."}

    entries = info.get('entries') or []
    if not entries:
        return {"status": "error", "message": "Playlist contains no videos."}

    if not title:
        title = info.get('title', 'Untitled Playlist')

    library = load_library()
    # Check for duplicate playlist URL
    for book in library.get('books', []):
        if book.get('playlist_url') == url:
            return {"status": "error", "message": f"Book already exists: '{book['title']}'"}

    chapters = []
    total_videos = len(entries)
    print(f"Found {total_videos} videos. Fetching details and parsing sections...")
    for i, entry in enumerate(entries):
        if not entry:
            continue
        print(f"Processing {i+1}/{total_videos}: {entry.get('title')}")
        video_url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
        description = fetch_video_description(video_url)
        sections = parse_sections(description)
        chapters.append({
            'id': entry.get('id'),
            'title': entry.get('title'),
            'url': video_url,
            'duration': entry.get('duration'),
            'sections': sections
        })

    new_book = {
        'id': str(uuid.uuid4()),
        'title': title,
        'playlist_url': url,
        'chapters': chapters,
        'total_progress': 0
    }
    library.setdefault('books', []).append(new_book)
    save_library(library)
    return {"status": "success", "message": f"Book '{title}' added with {len(chapters)} chapters!"}


def add_book():
    url = input("Enter Playlist URL: ").strip()
    title = input("Enter Book Title: ").strip()
    result = add_book_logic(url, title)
    print(result['message'])


def refresh_book_logic(book_id):
    library = load_library()
    book = next((b for b in library.get('books', []) if b['id'] == book_id), None)
    if not book:
        return {"status": "error", "message": "Book not found"}
    print(f"Refreshing sections for '{book['title']}'...")
    for i, chapter in enumerate(book.get('chapters', [])):
        print(f"Processing {i+1}/{len(book['chapters'])}: {chapter['title']}")
        description = fetch_video_description(chapter['url'])
        chapter['sections'] = parse_sections(description)
    save_library(library)
    return {"status": "success", "message": "Sections updated successfully!"}


def refresh_sections():
    library = load_library()
    if not library.get('books'):
        print("No books in library.")
        return
    print("\nSelect a book to refresh sections:")
    for i, book in enumerate(library['books']):
        print(f"{i+1}. {book['title']}")
    try:
        choice = int(input("Choice: ")) - 1
        if 0 <= choice < len(library['books']):
            book = library['books'][choice]
            result = refresh_book_logic(book['id'])
            print(result['message'])
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


def delete_book_logic(book_id):
    success = delete_book(book_id)
    if success:
        return {"status": "success", "message": "Book deleted"}
    return {"status": "error", "message": "Book not found or failed to delete"}


def list_books():
    lib = load_library()
    for b in lib.get('books', []):
        print(f"- {b['title']} ({len(b.get('chapters', []))} chapters)")
        if b.get('chapters'):
            first_chap = b['chapters'][0]
            print(f"  Sample: Chapter 1 has {len(first_chap.get('sections', []))} sections")


def main():
    while True:
        print("\n--- Video Tracker Admin ---")
        print("1. Add Book")
        print("2. List Books")
        print("3. Remove Book (Not Implemented)")
        print("4. Refresh Sections")
        print("5. Exit")
        choice = input("Select option: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            list_books()
        elif choice == '3':
            print("Not implemented yet.")
        elif choice == '4':
            refresh_sections()
        elif choice == '5':
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()

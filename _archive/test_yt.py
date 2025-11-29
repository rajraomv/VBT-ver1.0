import yt_dlp
import json

def test_fetch():
    # A known public playlist (Python for Beginners)
    url = 'https://www.youtube.com/playlist?list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3'
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'ignoreerrors': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Fetching {url}...")
        info = ydl.extract_info(url, download=False)
        
        if 'entries' in info:
            print(f"Found {len(info['entries'])} entries.")
            for i, entry in enumerate(info['entries'][:3]):
                print(f"{i+1}: {entry.get('title')} (ID: {entry.get('id')})")
        else:
            print("No entries found.")

if __name__ == '__main__':
    test_fetch()

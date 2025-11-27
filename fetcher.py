import yt_dlp
import re

def fetch_playlist_info(url):
    """
    Fetches information about a playlist.
    Returns a dictionary with 'entries' containing video info.
    """
    ydl_opts = {
        'quiet': True,
        'ignoreerrors': True,
        'skip_download': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist', # Much faster, only gets metadata
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except Exception as e:
            print(f"Error fetching playlist: {e}")
            return None
def fetch_video_description(video_url):
    """
    Fetches the description of a single video.
    Returns an empty string if the video metadata cannot be retrieved.
    """
    ydl_opts = {
        'quiet': True,
        'ignoreerrors': True,
        'skip_download': True,  # we only want metadata
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            if info and isinstance(info, dict):
                return info.get('description', '')
            return ''
        except Exception as e:
            print(f"Error fetching video description for {video_url}: {e}")
            return ''

def parse_sections(description):
    """
    Parses timestamps and titles from a video description.
    Returns a list of dictionaries: {'start': 'MM:SS', 'title': '...', 'seconds': int}
    """
    sections = []
    if not description:
        return sections

    # Regex to find timestamps like 00:00, 1:23:45, etc.
    # It looks for a timestamp at the start of a line or after some text
    # We'll assume a common format: "00:00 Title" or "Title 00:00"
    
    # Pattern 1: Timestamp at start (e.g., "00:00 Intro")
    # Matches: start of line, optional whitespace, timestamp, separator (space, dash, etc.), title
    pattern1 = r'(?m)^\s*(\d{1,2}(?::\d{2})+)\s*[-–—:]?\s*(.+)$'
    
    matches = re.findall(pattern1, description)
    
    for timestamp, title in matches:
        seconds = timestamp_to_seconds(timestamp)
        sections.append({
            'start': timestamp,
            'title': title.strip(),
            'seconds': seconds
        })
        
    # If no matches found with pattern 1, we could try others, but let's stick to the most common for now.
    # Many descriptions use "Title 00:00", but "00:00 Title" is the standard for YouTube chapters.
    
    return sections

def timestamp_to_seconds(timestamp):
    """Converts a timestamp string (HH:MM:SS or MM:SS) to total seconds."""
    parts = list(map(int, timestamp.split(':')))
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    else:
        return 0

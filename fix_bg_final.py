# Script to fix background - use cover mode to fill screen
import os

files_to_update = [
    'templates/landing.html',
    'templates/library.html',
    'templates/book.html'
]

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change back to cover to fill the entire screen
    content = content.replace(
        "background: #f5e6d3 url('/static/images/background.jpg') no-repeat center center fixed;\n            background-size: contain;",
        "background: url('/static/images/background.jpg') no-repeat center center fixed;\n            background-size: cover;"
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

print("\nBackground will now fill the entire screen!")
print("Note: The decorative corners may be slightly cropped on smaller screens.")

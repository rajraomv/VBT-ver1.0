# Script to preserve border by using contain mode with matching background
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
    
    # Change to contain with a cream/beige background color to match the image
    content = content.replace(
        "background: url('/static/images/background.jpg') no-repeat center center fixed;\n            background-size: cover;",
        "background: #f5e6d3 url('/static/images/background.jpg') no-repeat center center fixed;\n            background-size: contain;"
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

print("\nBackground set to contain mode with matching background color!")
print("The decorative border will always be visible.")

# Script to change background to cover mode (fills entire page)
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
    
    # Change from contain to cover
    content = content.replace('background-size: contain;', 'background-size: cover;')
    
    # Also handle the case where it might be on same line
    content = content.replace(
        "background: url('/static/images/background.jpg') no-repeat center center fixed;\n            background-size: contain;\n            background-color: #0f172a;",
        "background: url('/static/images/background.jpg') no-repeat center center fixed;\n            background-size: cover;"
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

print("\nBackground set to cover mode (fills entire page)!")

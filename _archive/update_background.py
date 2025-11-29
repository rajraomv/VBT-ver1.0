# Script to update background image CSS for better display
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
    
    # Update background CSS to contain instead of cover for no distortion
    # and add positioning
    old_bg = "background: url('/static/images/background.jpg') no-repeat center center fixed;\n            background-size: cover;"
    new_bg = "background: url('/static/images/background.jpg') no-repeat center center fixed;\n            background-size: contain;\n            background-color: #0f172a;"
    
    if old_bg in content:
        content = content.replace(old_bg, new_bg)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Skipped {filepath} (pattern not found)")

print("\nBackground display updated!")

# Script to update colors from white to cream/beige
import os

files_to_update = [
    'templates/library.html',
    'templates/book.html',
    'templates/admin.html',
    'templates/login.html'
]

for filepath in files_to_update:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace white colors with cream/beige
    content = content.replace('--text-primary: #f8fafc;', '--text-primary: #f5e6d3;')
    content = content.replace('--text-secondary: #94a3b8;', '--text-secondary: #d4a574;')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filepath}")

print("\nAll files updated successfully!")

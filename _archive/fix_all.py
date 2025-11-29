# Comprehensive fix script
import os

print("=== Fixing all issues ===\n")

# 1. Fix book.html - restore clean version, add background, fix back link, update colors
with open('templates/book.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add background
content = content.replace(
    'background: var(--bg-color);',
    'background: url(\'/static/images/background.jpg\') no-repeat center center fixed;\n            background-size: cover;'
)

# Update colors
content = content.replace('--text-primary: #f8fafc;', '--text-primary: #f5e6d3;')
content = content.replace('--text-secondary: #94a3b8;', '--text-secondary: #d4a574;')

# Fix back link to go to /library instead of /
content = content.replace(
    '<a href="/" class="back-link">&larr; Back to Library</a>',
    '<a href="/library" class="back-link">&larr; Back to Library</a>'
)

with open('templates/book.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ Fixed book.html (background, colors, back link)")

# 2. Ensure library.html back link goes to home
with open('templates/library.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure library page links to home
if 'href="/library"' in content and 'Back to' not in content:
    content = content.replace('href="/library"', 'href="/"')
    
with open('templates/library.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ Verified library.html")

# 3. Ensure admin.html back link goes to library
with open('templates/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'href="/"',
    'href="/library"'
)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ Fixed admin.html back link")

print("\n=== All fixes applied! ===")
print("Restart your server to see changes.")

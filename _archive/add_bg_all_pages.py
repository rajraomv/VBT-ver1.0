# Script to add background image to admin and login pages
import os

files_to_update = {
    'templates/admin.html': 'background: var(--bg-color);',
    'templates/login.html': 'background: url(\'/static/images/background.jpg\') no-repeat center center fixed;'
}

# Admin page
with open('templates/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'background: var(--bg-color);',
    'background: url(\'/static/images/background.jpg\') no-repeat center center fixed;\n            background-size: cover;'
)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated admin.html")

# Login page already has background, just ensure it has cover
with open('templates/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'background-size: cover;' not in content:
    content = content.replace(
        'background: url(\'/static/images/background.jpg\') no-repeat center center fixed;',
        'background: url(\'/static/images/background.jpg\') no-repeat center center fixed;\n            background-size: cover;'
    )
    with open('templates/login.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated login.html")
else:
    print("login.html already has background")

print("\nAll pages now have the decorative background!")

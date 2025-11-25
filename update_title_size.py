# Script to reduce landing page title font size
with open('templates/landing.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Reduce h1 font size from 5em to 3.5em to fit in one line
content = content.replace('font-size: 5em;', 'font-size: 3.5em;')

with open('templates/landing.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated landing page title size!")

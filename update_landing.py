# Quick script to update landing.html
with open('templates/landing.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace background
content = content.replace(
    '            background: var(--bg-color);',
    '            background: url(\'/static/images/background.jpg\') no-repeat center center fixed;\n            background-size: cover;'
)

# Add greeting
content = content.replace(
    '    <div class="container">\n        <h1>Video Book Tracker</h1>',
    '    <div class="container">\n        <div style="font-family: cursive; color: orange; font-size: 1.5em; margin-bottom: -5px;">Namasthe! 🙏</div>\n        <h1>Video Book Tracker</h1>'
)

with open('templates/landing.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated landing.html successfully!")

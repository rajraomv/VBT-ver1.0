# Script to add padding to keep content within the border frame
import os

files_to_update = {
    'templates/landing.html': '.container {',
    'templates/library.html': '.container {',
}

for filepath, search_pattern in files_to_update.items():
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add padding to container to keep content within border
    # The border image has decorative corners, so we need significant padding
    old_container = """        .container {
            max-width: 1200px;
            margin: 0 auto;
        }"""
    
    new_container = """        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 80px;
            box-sizing: border-box;
        }"""
    
    if old_container in content:
        content = content.replace(old_container, new_container)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Skipped {filepath} (pattern not found)")

# For landing page, also update the container style
with open('templates/landing.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_landing_container = """        .container {
            text-align: center;
            max-width: 800px;
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
            z-index: 1;
        }"""

new_landing_container = """        .container {
            text-align: center;
            max-width: 800px;
            padding: 80px 100px;
            display: flex;
            flex-direction: column;
            align-items: center;
            z-index: 1;
        }"""

if old_landing_container in content:
    content = content.replace(old_landing_container, new_landing_container)
    with open('templates/landing.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated landing.html container padding")

print("\nContent will now stay within the decorative border!")

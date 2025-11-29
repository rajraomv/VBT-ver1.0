import os

content = "MONGO_URI=mongodb+srv://rajmongo:kandukur@vbtcluster.r9tisix.mongodb.net/vbt_library?appName=VBTcluster"
with open('.env', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Created .env file. Exists: {os.path.exists('.env')}")
with open('.env', 'r', encoding='utf-8') as f:
    print(f"Content: {f.read()}")

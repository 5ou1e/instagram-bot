import json

proxies = []
with open(r"C:\Python\Мои проекты\instagram-bot\_data\proxies.txt", "r") as file:
    lines = file.read().split('\n')

for line in lines:
    proxies.append(line)

print(json.dumps(proxies))

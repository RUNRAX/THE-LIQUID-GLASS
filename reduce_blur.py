import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Reduce CSS blur from 10px to 4px for higher clarity
html = re.sub(r'filter: blur\(\d+px\);', 'filter: blur(4px);', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Blur reduced, clarity increased.")

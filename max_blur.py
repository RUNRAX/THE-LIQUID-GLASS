import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Max out blur to 40px
html = re.sub(r'filter: blur\(\d+px\)', 'filter: blur(40px)', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Blur maxed out.")

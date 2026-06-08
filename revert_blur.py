import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Revert max blur back to 5px
html = html.replace('filter: blur(40px)', 'filter: blur(5px)')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Reverted to 5px blur.")

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I need to ensure .glass-3d-overlay has border: none;
html = html.replace('/* border removed */', 'border: none;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Border set to none.")

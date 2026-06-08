import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace scales
html = html.replace('scale="185"', 'scale="370"')
html = html.replace('scale="140"', 'scale="280"')
html = html.replace('scale="95"', 'scale="190"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success: Updated scales in index.html')

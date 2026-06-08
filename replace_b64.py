import re

with open('map_b64.txt', 'r', encoding='utf-8') as f:
    b64_str = f.read().strip()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the feImage href value
html = re.sub(r'<feImage href="data:image/png;base64,[a-zA-Z0-9+/=]+"', f'<feImage href="{b64_str}"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success: Replaced base64 string in index.html')

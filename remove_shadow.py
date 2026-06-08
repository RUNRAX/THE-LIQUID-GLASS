import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the entire box-shadow property
html = re.sub(r'box-shadow:\s*[^;]*;', '/* box-shadow removed */', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Box shadow removed.")

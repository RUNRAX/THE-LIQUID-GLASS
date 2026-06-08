import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Increase blur to 5px, and add contrast to increase clarity through the blur
html = re.sub(r'filter: blur\(\d+px\);', 'filter: blur(5px) contrast(1.2) saturate(1.1);', html)
# Just in case it already has contrast/saturate from a previous tweak
html = re.sub(r'filter: blur\(\d+px\) contrast\([^)]+\) saturate\([^)]+\);', 'filter: blur(5px) contrast(1.2) saturate(1.1);', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Blur increased, contrast added for clarity.")

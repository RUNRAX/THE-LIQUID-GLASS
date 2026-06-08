import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace any explicit width/height in feImage to match the container dimensions
html = re.sub(r'width="\d+" height="\d+" preserveAspectRatio="none" result="map"', 
              'width="480" height="320" preserveAspectRatio="none" result="map"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Dimensions updated")

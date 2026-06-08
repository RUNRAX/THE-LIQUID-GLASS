import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check if we already have an anti-alias blur
if '<feGaussianBlur stdDeviation="1.5" result="anti-alias"/>' not in html:
    html = html.replace('</feMerge>\n  </filter>', '</feMerge>\n    <!-- Anti-aliasing to smooth out 8-bit displacement banding -->\n    <feGaussianBlur stdDeviation="1.5" result="anti-alias"/>\n  </filter>')

# Let's also remove the map blur we added earlier, as it didn't help and just makes things slower
html = html.replace('result="raw-map"/>\n    <feGaussianBlur in="raw-map" stdDeviation="4" result="map"/>', 'result="map"/>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Anti-aliasing added.")

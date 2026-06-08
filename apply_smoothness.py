import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Lower the "frosted" blur to make the glass smooth
html = re.sub(r'<feGaussianBlur in="SourceGraphic" stdDeviation="\d+" result="frosted"/>',
              '<feGaussianBlur in="SourceGraphic" stdDeviation="2" result="frosted"/>', html)

# If we haven't already added smooth-map, add it after feImage
if 'result="smooth-map"' not in html:
    # Find the end of feImage
    # The feImage tag ends with />
    html = re.sub(r'(<feImage [^>]+ result="map"\s*/>)',
                  r'\1\n    <!-- Smooth the refraction map to remove 8-bit banding artifacts (High Smoothness) -->\n    <feGaussianBlur in="map" stdDeviation="6" result="smooth-map"/>',
                  html)
    
    # Update displacement maps to use smooth-map
    html = html.replace('in2="map"', 'in2="smooth-map"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied high smoothness to index.html")

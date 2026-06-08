with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add a blur to the displacement map to smooth out the 8-bit quantization steps
# This provides sub-pixel smoothness to the magnification
html = html.replace('result="map"/>', 'result="raw-map"/>\n    <feGaussianBlur in="raw-map" stdDeviation="4" result="map"/>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Map smoothed.")

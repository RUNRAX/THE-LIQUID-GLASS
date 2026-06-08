import re

with open('map_b64.txt', 'r', encoding='utf-8') as f:
    b64_str = f.read().strip()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Restore original base64 map
html = re.sub(r'<feImage href="data:image/bmp;base64,[a-zA-Z0-9+/=]+"', f'<feImage href="{b64_str}"', html)

# Remove the smooth-map blur
html = re.sub(r'\s*<!-- Smooth the refraction map.*?-->\s*<feGaussianBlur in="map" stdDeviation="6" result="smooth-map"/>', '', html, flags=re.DOTALL)

# Revert in2="smooth-map" to in2="map"
html = html.replace('in2="smooth-map"', 'in2="map"')

# Revert frosted stdDeviation back to 8
html = re.sub(r'<feGaussianBlur in="SourceGraphic" stdDeviation="\d+" result="frosted"/>', '<feGaussianBlur in="SourceGraphic" stdDeviation="8" result="frosted"/>', html)

# Revert scales back to 370, 280, 190
html = re.sub(r'scale="\d+" xChannelSelector="R" yChannelSelector="G" result="displaced-red"', 'scale="370" xChannelSelector="R" yChannelSelector="G" result="displaced-red"', html)
html = re.sub(r'scale="\d+" xChannelSelector="R" yChannelSelector="G" result="displaced-green"', 'scale="280" xChannelSelector="R" yChannelSelector="G" result="displaced-green"', html)
html = re.sub(r'scale="\d+" xChannelSelector="R" yChannelSelector="G" result="displaced-blue"', 'scale="190" xChannelSelector="R" yChannelSelector="G" result="displaced-blue"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Reverted successfully.')

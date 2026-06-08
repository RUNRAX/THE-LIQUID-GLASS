import base64
import struct
import math
import re

size = 320
pixel_data = bytearray()
center = size / 2.0
radius = size / 2.0
row_padding = (4 - ((size * 3) % 4)) % 4
scale = 100.0

for y in range(size - 1, -1, -1):
    for x in range(size):
        dx = (x - center) / radius
        dy = (y - center) / radius
        r = math.sqrt(dx*dx + dy*dy)
        
        disp_x = 0.0
        disp_y = 0.0
        
        if r <= 1.0:
            # Smooth sine wave: 0 at center, peaks at r=0.5, 0 at edge (r=1)
            # This ensures absolutely ZERO sharp cliffs at the edge, making the line invisible!
            distortion_magnitude = math.sin(r * math.pi) * 80.0
            disp_x = dx * distortion_magnitude
            disp_y = dy * distortion_magnitude
            
        val_r = 0.5 + (disp_x / scale)
        val_g = 0.5 + (disp_y / scale)
        
        val_r = max(0.0, min(1.0, val_r))
        val_g = max(0.0, min(1.0, val_g))
        val_b = 0.5
        
        c_r = int(val_r * 255)
        c_g = int(val_g * 255)
        c_b = int(val_b * 255)
        
        pixel_data.extend([c_b, c_g, c_r])
    pixel_data.extend([0] * row_padding)

file_size = 54 + len(pixel_data)
bmp_header = struct.pack('<ccIIIIiiHH', b'B', b'M', file_size, 0, 54, 40, size, size, 1, 24)
bmp_info = struct.pack('<IIIIII', 0, len(pixel_data), 0, 0, 0, 0)
bmp_data = bmp_header + bmp_info + pixel_data

b64_str = base64.b64encode(bmp_data).decode('utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS size and add blur to the sphere
html = re.sub(r'width:\s*200px;', 'width: 320px;', html)
html = re.sub(r'height:\s*200px;', 'height: 320px;', html)
html = re.sub(
    r'backdrop-filter:\s*url\(\#sphere-dispersion\);',
    'backdrop-filter: url(#sphere-dispersion) blur(6px);',
    html
)
html = re.sub(
    r'-webkit-backdrop-filter:\s*url\(\#sphere-dispersion\);',
    '-webkit-backdrop-filter: url(#sphere-dispersion) blur(6px);',
    html
)

# 2. Update SVG filter to new size and replace the base64 string
# We need to replace the feImage for the sphere specifically.
# Since there are two feImages, we'll use regex to target the one inside sphere-dispersion.
# Actually, the previous script injected the sphere SVG filter as a whole block at the end.
# We can just replace the whole sphere-dispersion block.
sphere_filter_pattern = r'<filter id="sphere-dispersion".*?</filter>'
new_svg_filter = f"""<filter id="sphere-dispersion" x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox" primitiveUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
    <feImage href="data:image/bmp;base64,{b64_str}" x="0" y="0" width="320" height="320" preserveAspectRatio="none" result="sphere-map"/>
    <feGaussianBlur in="sphere-map" stdDeviation="1" result="smooth-sphere-map"/>
    <feDisplacementMap in="SourceGraphic" in2="smooth-sphere-map" scale="100" xChannelSelector="R" yChannelSelector="G" result="sphere-dispersion"/>
  </filter>"""

html = re.sub(sphere_filter_pattern, new_svg_filter, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Sphere resized, lines smoothed out, blur added.")

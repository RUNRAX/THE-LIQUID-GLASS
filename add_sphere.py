import base64
import struct
import math
import re

size = 200
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
            # Marble effect: distort heavily near the surface/edges, smooth in the center
            distortion_magnitude = math.pow(r, 3) * 60.0
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

# 1. Add CSS
if '.sphere-lens' not in html:
    css = """
  .sphere-lens {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200px;
    height: 200px;
    border-radius: 50%;
    backdrop-filter: url(#sphere-dispersion);
    -webkit-backdrop-filter: url(#sphere-dispersion);
    pointer-events: none;
  }
</style>"""
    html = html.replace('</style>', css)

# 2. Add div
if '<div class="sphere-lens"></div>' not in html:
    html = html.replace('<div class="frost-layer" id="frost-layer"></div>', '<div class="frost-layer" id="frost-layer"></div>\n  <div class="sphere-lens"></div>')

# 3. Add SVG filter
if 'id="sphere-dispersion"' not in html:
    svg_filter = f"""
  <filter id="sphere-dispersion" x="-50%" y="-50%" width="200%" height="200%" filterUnits="objectBoundingBox" primitiveUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
    <feImage href="data:image/bmp;base64,{b64_str}" x="0" y="0" width="200" height="200" preserveAspectRatio="none" result="sphere-map"/>
    <feGaussianBlur in="sphere-map" stdDeviation="1" result="smooth-sphere-map"/>
    <feDisplacementMap in="SourceGraphic" in2="smooth-sphere-map" scale="100" xChannelSelector="R" yChannelSelector="G" result="sphere-dispersion"/>
  </filter>
</svg>"""
    html = html.replace('</svg>', svg_filter)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Spherical slab added.")

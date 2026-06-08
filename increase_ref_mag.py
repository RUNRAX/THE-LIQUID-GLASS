import base64
import struct
import math
import re

width = 480
height = 320
pixel_data = bytearray()
center_x = width / 2.0
center_y = height / 2.0

row_padding = (4 - ((width * 3) % 4)) % 4

# Moderate magnification (3x) to keep quality high with the frost blur
M = 3.0
K = (1.0 / M) - 1.0

# Increased scale for higher precision and stronger refraction
scale = 200.0

for y in range(height - 1, -1, -1):
    for x in range(width):
        disp_x = K * (x - center_x)
        disp_y = K * (y - center_y)
        
        # Add edge bevel distortion (increased from 20.0 to 40.0 for stronger refraction)
        dx = (x - center_x) / center_x
        dy = (y - center_y) / center_y
        
        edge_dist_x = math.pow(dx, 4) * dx * 40.0
        edge_dist_y = math.pow(dy, 4) * dy * 40.0
        
        disp_x += edge_dist_x
        disp_y += edge_dist_y
        
        val_r = 0.5 + (disp_x / scale)
        val_g = 0.5 + (disp_y / scale)
        
        # Clamp to prevent color wrapping artifacts
        val_r = max(0.0, min(1.0, val_r))
        val_g = max(0.0, min(1.0, val_g))
        val_b = 0.5
        
        r = int(val_r * 255)
        g = int(val_g * 255)
        b = int(val_b * 255)
        
        pixel_data.extend([b, g, r])
    pixel_data.extend([0] * row_padding)

file_size = 54 + len(pixel_data)
bmp_header = struct.pack('<ccIIIIiiHH', b'B', b'M', file_size, 0, 54, 40, width, height, 1, 24)
bmp_info = struct.pack('<IIIIII', 0, len(pixel_data), 0, 0, 0, 0)
bmp_data = bmp_header + bmp_info + pixel_data

b64_str = base64.b64encode(bmp_data).decode('utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the base64 image map
html = re.sub(r'data:image/bmp;base64,[a-zA-Z0-9+/=]+', f'data:image/bmp;base64,{b64_str}', html)

# Increase SVG scales to match python scale (200) and create strong chromatic aberration (200, 180, 160)
tags = re.findall(r'<feDisplacementMap[^>]+>', html)
if len(tags) >= 3:
    t0 = re.sub(r'scale="\d+"', 'scale="200"', tags[0])
    t1 = re.sub(r'scale="\d+"', 'scale="180"', tags[1])
    t2 = re.sub(r'scale="\d+"', 'scale="160"', tags[2])
    html = html.replace(tags[0], t0)
    html = html.replace(tags[1], t1)
    html = html.replace(tags[2], t2)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Magnification increased to 3x and refraction doubled.")

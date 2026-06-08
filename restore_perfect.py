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

# Pure edge bending lens (M = 1.0, meaning no center zoom)
M = 1.0
K = 0.0

scale = 100.0

for y in range(height - 1, -1, -1):
    for x in range(width):
        disp_x = K * (x - center_x)
        disp_y = K * (y - center_y)
        
        # Edge bevel distortion (power of 5 for sharp edge drop-off)
        dx = (x - center_x) / center_x
        dy = (y - center_y) / center_y
        
        edge_dist_x = math.pow(dx, 4) * dx * 20.0
        edge_dist_y = math.pow(dy, 4) * dy * 20.0
        
        disp_x += edge_dist_x
        disp_y += edge_dist_y
        
        val_r = 0.5 + (disp_x / scale)
        val_g = 0.5 + (disp_y / scale)
        
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

# Restore the SourceGraphic blur to 4 for the frosted look
if 'result="frosted"' not in html:
    # If the frost layer was removed or renamed
    html = html.replace('in="SourceGraphic"', 'in="SourceGraphic" stdDeviation="4" result="frosted"')
else:
    html = re.sub(r'<feGaussianBlur in="SourceGraphic" stdDeviation="[^"]*" result="frosted"\s*/>', '<feGaussianBlur in="SourceGraphic" stdDeviation="4" result="frosted"/>', html)
    # Just in case it was written without result="frosted" or something
    html = re.sub(r'<feGaussianBlur in="SourceGraphic" stdDeviation="[^"]*"/>\n', '<feGaussianBlur in="SourceGraphic" stdDeviation="4" result="frosted"/>\n', html)

# Set scales for chromatic aberration (100, 90, 80)
tags = re.findall(r'<feDisplacementMap[^>]+>', html)
if len(tags) >= 3:
    t0 = re.sub(r'scale="\d+"', 'scale="100"', tags[0])
    t1 = re.sub(r'scale="\d+"', 'scale="90"', tags[1])
    t2 = re.sub(r'scale="\d+"', 'scale="80"', tags[2])
    html = html.replace(tags[0], t0)
    html = html.replace(tags[1], t1)
    html = html.replace(tags[2], t2)

# Set final blur to a tiny anti-aliasing amount
html = re.sub(r'<feGaussianBlur in="final-dispersion" stdDeviation="[^"]+"/>', '<feGaussianBlur in="final-dispersion" stdDeviation="0.5"/>', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Restored to original elegant frosted glass state.")

import base64
import struct
import math
import re

size = 320
pixel_data = bytearray()
center = size / 2.0
radius = size / 2.0

for y in range(size - 1, -1, -1):
    for x in range(size):
        dx = (x - center) / radius
        dy = (y - center) / radius
        r = math.sqrt(dx*dx + dy*dy)
        
        if r > 1.0:
            factor = 0
        else:
            # Reverting back to the standard smooth spherical curve 
            # with a strong baseline magnification
            factor = 1.0 + r*r
            
        out_x = dx * factor
        out_y = dy * factor
        
        # Normalize by 2.0
        out_x_norm = out_x / 2.0
        out_y_norm = out_y / 2.0
        
        r_col = int(max(0, min(255, (out_x_norm + 1.0) * 127.5)))
        g_col = int(max(0, min(255, (out_y_norm + 1.0) * 127.5)))
        b_col = 127
        
        pixel_data.extend([b_col, g_col, r_col])

pixel_offset = 54
file_size = pixel_offset + len(pixel_data)
header = b'BM' + struct.pack('<I', file_size) + struct.pack('<H', 0) + struct.pack('<H', 0) + struct.pack('<I', pixel_offset)
dib_header = struct.pack('<I', 40) + struct.pack('<I', size) + struct.pack('<I', size) + struct.pack('<H', 1) + struct.pack('<H', 24) + struct.pack('<I', 0) + struct.pack('<I', len(pixel_data)) + struct.pack('<I', 2835) + struct.pack('<I', 2835) + struct.pack('<I', 0) + struct.pack('<I', 0)

bmp_data = header + dib_header + pixel_data
b64_str = 'data:image/bmp;base64,' + base64.b64encode(bmp_data).decode('ascii')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the base64 map
html = re.sub(r'<feImage href="data:image/bmp;base64,[a-zA-Z0-9+/=]+"', f'<feImage href="{b64_str}"', html)

# Revert scales from 925, 700, 475 back to 370, 280, 190
html = html.replace('scale="925"', 'scale="370"')
html = html.replace('scale="700"', 'scale="280"')
html = html.replace('scale="475"', 'scale="190"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success: Reverted to the smooth spherical refraction in index.html')

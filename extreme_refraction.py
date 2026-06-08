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
            # Extremely aggressive distortion curve
            # math.sqrt(r) shoots up very fast from 0, making the center distort heavily
            factor = 1.0 + 4.0 * math.sqrt(r)
            
        out_x = dx * factor
        out_y = dy * factor
        
        # Max factor is 5.0, so max out_x is 5.0. Normalize by 5.0
        out_x_norm = out_x / 5.0
        out_y_norm = out_y / 5.0
        
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

# Because we normalized by 5.0, we must scale the CSS displacement maps to compensate.
# Old normalization was 2.0 (scales 370, 280, 190).
# New normalization is 5.0, so we multiply the original base scales (185, 140, 95) by 5.0
# Base * 5: 185*5 = 925, 140*5 = 700, 95*5 = 475
html = html.replace('scale="370"', 'scale="925"')
html = html.replace('scale="280"', 'scale="700"')
html = html.replace('scale="190"', 'scale="475"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success: Replaced base64 string with extreme center refraction and updated scales in index.html')

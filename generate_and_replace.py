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
            # A real glass sphere has a strong baseline magnification (factor=1.0)
            # plus extra distortion at the edges.
            # Using factor = 1.0 + r*r gives strong refraction in the center
            # AND a nice fisheye curve at the edge!
            factor = 1.0 + r*r
            
        out_x = dx * factor
        out_y = dy * factor
        
        # Max out_x can be 1 * (1 + 1) = 2.0. So we need to normalize to avoid clipping.
        # But wait, if we divide by 2, we halve the overall scale. 
        # Let's normalize by dividing by 2.0 to keep it in [-1, 1].
        # out_x / 2.0 maps to [-1, 1]
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

html = re.sub(r'<feImage href="data:image/bmp;base64,[a-zA-Z0-9+/=]+"', f'<feImage href="{b64_str}"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success: Replaced base64 string with stronger center refraction in index.html')

import base64
import struct
import math
import re

width = 480
height = 320
pixel_data = bytearray()
center_x = width / 2.0
center_y = height / 2.0
radius_x = width / 2.0
radius_y = height / 2.0

# BMP rows are padded to a multiple of 4 bytes
row_padding = (4 - ((width * 3) % 4)) % 4

for y in range(height - 1, -1, -1):
    for x in range(width):
        dx = (x - center_x) / radius_x
        dy = (y - center_y) / radius_y
        
        # Soft lens bulge over the entire rectangle, no hard circle cutoff
        factor = 1.0 + math.pow(dx, 2) + math.pow(dy, 2)
        
        out_x = dx * factor
        out_y = dy * factor
        
        # Normalize
        out_x_norm = out_x / 2.0
        out_y_norm = out_y / 2.0
        
        r_col = int(max(0, min(255, (out_x_norm + 1.0) * 127.5)))
        g_col = int(max(0, min(255, (out_y_norm + 1.0) * 127.5)))
        b_col = 127
        
        pixel_data.extend([b_col, g_col, r_col])
    
    pixel_data.extend(b'\x00' * row_padding)

pixel_offset = 54
file_size = pixel_offset + len(pixel_data)
header = b'BM' + struct.pack('<I', file_size) + struct.pack('<H', 0) + struct.pack('<H', 0) + struct.pack('<I', pixel_offset)
dib_header = struct.pack('<I', 40) + struct.pack('<I', width) + struct.pack('<I', height) + struct.pack('<H', 1) + struct.pack('<H', 24) + struct.pack('<I', 0) + struct.pack('<I', len(pixel_data)) + struct.pack('<I', 2835) + struct.pack('<I', 2835) + struct.pack('<I', 0) + struct.pack('<I', 0)

bmp_data = header + dib_header + pixel_data
b64_str = 'data:image/bmp;base64,' + base64.b64encode(bmp_data).decode('ascii')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the base64 map
html = re.sub(r'<feImage href="data:image/bmp;base64,[a-zA-Z0-9+/=]+"', f'<feImage href="{b64_str}"', html)
# Update width and height
html = re.sub(r'width="\d+"\s+height="\d+"\s+preserveAspectRatio="none"', f'width="{width}" height="{height}" preserveAspectRatio="none"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success: Generated and applied cuboid refraction map')

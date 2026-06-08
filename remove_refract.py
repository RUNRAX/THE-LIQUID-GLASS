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

for y in range(height - 1, -1, -1):
    for x in range(width):
        # Zero refraction!
        disp_x = 0.0
        disp_y = 0.0
        
        val_r = 0.5
        val_g = 0.5
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

# Reduce CSS blur from 16px to 6px
html = re.sub(r'filter: blur\(\d+px\);', 'filter: blur(6px);', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Refraction removed, blur reduced.")

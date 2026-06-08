import base64
import struct
import math
import re

size = 640
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
            # High refraction with high quality curve
            factor = 1.0 + 3.0 * r*r
            
        out_x = dx * factor
        out_y = dy * factor
        
        # Max factor is 4.0, so max out_x is 4.0. Normalize by 4.0
        out_x_norm = out_x / 4.0
        out_y_norm = out_y / 4.0
        
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

# Increase blur to high blur
html = re.sub(r'<feGaussianBlur in="SourceGraphic" stdDeviation="\d+"', '<feGaussianBlur in="SourceGraphic" stdDeviation="24"', html)

# Because we normalized by 4.0, we must scale the CSS displacement maps.
# Original base scales (from generate_and_replace) were 185, 140, 95 (normalized by 2.0). 
# This means raw scale was ~92.5. Let's use roughly that raw scale * 4.0:
# 185/2 = 92.5. 92.5 * 4 = 370.
# So scales should be 370, 280, 190. (Which happen to be the current ones in index.html!)
# Let's make them even higher to ensure "high refraction": 
# e.g., 600, 450, 300
html = re.sub(r'scale="\d+" xChannelSelector="R" yChannelSelector="G" result="displaced-red"', 'scale="600" xChannelSelector="R" yChannelSelector="G" result="displaced-red"', html)
html = re.sub(r'scale="\d+" xChannelSelector="R" yChannelSelector="G" result="displaced-green"', 'scale="450" xChannelSelector="R" yChannelSelector="G" result="displaced-green"', html)
html = re.sub(r'scale="\d+" xChannelSelector="R" yChannelSelector="G" result="displaced-blue"', 'scale="300" xChannelSelector="R" yChannelSelector="G" result="displaced-blue"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success')

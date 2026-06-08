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

row_padding = (4 - ((width * 3) % 4)) % 4

for y in range(height - 1, -1, -1):
    for x in range(width):
        dx = (x - center_x) / radius_x
        dy = (y - center_y) / radius_y
        
        # Independent x and y factors create a purely rectangular/cuboidal lens
        # Using power of 4 or 6 gives a flat center and beveled edges
        factor_x = 1.0 + math.pow(dx, 6)
        factor_y = 1.0 + math.pow(dy, 6)
        
        out_x = dx * factor_x
        out_y = dy * factor_y
        
        # Max out_x when dx=1.0 is 1.0 * (1.0 + 1.0) = 2.0
        # Normalize by 2.0
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
html = re.sub(r'data:image/bmp;base64,[a-zA-Z0-9+/=]+', b64_str, html)

# Because we normalize by 2.0 instead of 3.0, we can restore the scale to a balanced value
# (Let's keep scale high but proportional, e.g., 370, 280, 190 was standard, we used 555 earlier)
# We'll use 450, 340, 230 to keep it strong but not overly distorted
html = re.sub(r'scale="\d+" xChannelSelector="R"', 'scale="450" xChannelSelector="R"', html)
html = re.sub(r'scale="\d+" xChannelSelector="G"', 'scale="340" xChannelSelector="G"', html)
html = re.sub(r'scale="\d+" xChannelSelector="B"', 'scale="230" xChannelSelector="B"', html)

# Add cache buster query parameter to ensure HTML is not fully cached if they load external assets,
# but we can't easily cache-bust the HTML file itself since it's the root. 
# The base64 replacement is inline so it will apply instantly on refresh!

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Generated decoupled rectangular lens map!')

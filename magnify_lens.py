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

# We want a magnification M
M = 5.0

# K is the displacement slope
# x_src = x + disp_x = x + K * (x - center_x) = center_x + (1+K)*(x - center_x)
# So 1 + K = 1 / M  => K = 1/M - 1
K = (1.0 / M) - 1.0

# We want disp_x = scale * (R - 0.5)
# Let's fix scale to 480.
scale = 480.0

# So disp_x = 480 * (R - 0.5)
# R = 0.5 + disp_x / 480 = 0.5 + K * (x - center_x) / 480

for y in range(height - 1, -1, -1):
    for x in range(width):
        # Base displacement for pure magnification
        disp_x = K * (x - center_x)
        disp_y = K * (y - center_y)
        
        # Let's add a bit of an edge bevel so it looks like glass
        # dx and dy in range [-1, 1]
        dx = (x - center_x) / center_x
        dy = (y - center_y) / center_y
        
        # Edge distortion increases at the edges (power 4)
        edge_dist_x = math.pow(dx, 4) * dx * 20.0
        edge_dist_y = math.pow(dy, 4) * dy * 20.0
        
        disp_x += edge_dist_x
        disp_y += edge_dist_y
        
        # Convert displacement to color values
        val_r = 0.5 + (disp_x / scale)
        val_g = 0.5 + (disp_y / scale)
        
        # Clamp to [0, 1]
        val_r = max(0.0, min(1.0, val_r))
        val_g = max(0.0, min(1.0, val_g))
        
        # B channel can be empty or 0.5
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

# Replace the base64 image
html = re.sub(r'data:image/bmp;base64,[a-zA-Z0-9+/=]+', f'data:image/bmp;base64,{b64_str}', html)

# Replace the scales to 480, 480, 480, but maybe slightly different for chromatic aberration
# M = 5 is when scale = 480.
# If scale is slightly larger, disp is larger.
# disp_x = scale * (R - 0.5). If scale > 480, disp is magnified more?
# Wait, R - 0.5 is negative for x < center. So larger scale means more negative disp, means more magnification!
html = re.sub(r'scale="\d+" xChannelSelector="R"', 'scale="500" xChannelSelector="R"', html, count=1) # Red
html = re.sub(r'scale="\d+" xChannelSelector="R"', 'scale="480" xChannelSelector="R"', html, count=1) # Green
html = re.sub(r'scale="\d+" xChannelSelector="R"', 'scale="460" xChannelSelector="R"', html, count=1) # Blue

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Lens regenerated with 5x magnification and chromatic aberration scales.")

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
scale = 200.0

# Define X and Y radii so the shape touches ALL 4 edges of the cuboid!
rx = width / 2.0   # 240
ry = height / 2.0  # 160

for y in range(height - 1, -1, -1):
    for x in range(width):
        # 1. Edge Refraction (from cuboid edges)
        dx_box = (x - center_x) / center_x
        dy_box = (y - center_y) / center_y
        
        edge_dist_x = -math.pow(dx_box, 12) * dx_box * 80.0
        edge_dist_y = -math.pow(dy_box, 12) * dy_box * 80.0
        
        # 2. Ellipse Refraction (fills the whole cuboid)
        dx_ell = (x - center_x) / rx
        dy_ell = (y - center_y) / ry
        r_ell = math.sqrt(dx_ell*dx_ell + dy_ell*dy_ell)
        
        ellipse_dist_x = 0.0
        ellipse_dist_y = 0.0
        
        if r_ell <= 1.0:
            # Smooth sine wave: 0 at center, peaks at 0.5, exactly 0 at edge
            mag = math.sin(r_ell * math.pi) * 120.0
            ellipse_dist_x = dx_ell * mag
            ellipse_dist_y = dy_ell * mag
            
        # Combine both refractions seamlessly
        disp_x = edge_dist_x + ellipse_dist_x
        disp_y = edge_dist_y + ellipse_dist_y
        
        val_r = 0.5 + (disp_x / scale)
        val_g = 0.5 + (disp_y / scale)
        
        val_r = max(0.0, min(1.0, val_r))
        val_g = max(0.0, min(1.0, val_g))
        val_b = 0.5
        
        # Proper rounding to prevent any sub-pixel neutral shifting
        c_r = int(round(val_r * 255))
        c_g = int(round(val_g * 255))
        c_b = int(round(val_b * 255))
        
        pixel_data.extend([c_b, c_g, c_r])
    pixel_data.extend([0] * row_padding)

file_size = 54 + len(pixel_data)
bmp_header = struct.pack('<ccIIIIiiHH', b'B', b'M', file_size, 0, 54, 40, width, height, 1, 24)
bmp_info = struct.pack('<IIIIII', 0, len(pixel_data), 0, 0, 0, 0)
bmp_data = bmp_header + bmp_info + pixel_data

b64_str = base64.b64encode(bmp_data).decode('utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the base64 map inside the MAIN glass-dispersion filter
html = re.sub(
    r'<feImage href="data:image/bmp;base64,[a-zA-Z0-9+/=]+" x="0" y="0" width="480" height="320" preserveAspectRatio="none" result="raw-map"/>',
    f'<feImage href="data:image/bmp;base64,{b64_str}" x="0" y="0" width="480" height="320" preserveAspectRatio="none" result="raw-map"/>',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Ellipse map applied successfully.")

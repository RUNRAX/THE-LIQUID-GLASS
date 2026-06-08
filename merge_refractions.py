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

# Radius of 160 makes it exactly 320px in diameter, touching the top and bottom of the 320px tall cuboid
sphere_radius = 160.0 

for y in range(height - 1, -1, -1):
    for x in range(width):
        # 1. Edge Refraction (from cuboid edges)
        dx_box = (x - center_x) / center_x
        dy_box = (y - center_y) / center_y
        
        edge_dist_x = -math.pow(dx_box, 12) * dx_box * 80.0
        edge_dist_y = -math.pow(dy_box, 12) * dy_box * 80.0
        
        # 2. Sphere Refraction (in the center)
        dx_sph = (x - center_x) / sphere_radius
        dy_sph = (y - center_y) / sphere_radius
        r_sph = math.sqrt(dx_sph*dx_sph + dy_sph*dy_sph)
        
        sphere_dist_x = 0.0
        sphere_dist_y = 0.0
        
        if r_sph <= 1.0:
            # Smooth sine wave: 0 at center, peaks at 0.5, exactly 0 at edge
            # This completely eliminates any sharp boundaries or visible lines.
            mag = math.sin(r_sph * math.pi) * 120.0
            sphere_dist_x = dx_sph * mag
            sphere_dist_y = dy_sph * mag
            
        # Combine both refractions seamlessly
        disp_x = edge_dist_x + sphere_dist_x
        disp_y = edge_dist_y + sphere_dist_y
        
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
# Since we might have multiple base64 strings if the old sphere one is still there,
# we need to be careful. The main map has width="480" height="320".
html = re.sub(
    r'<feImage href="data:image/bmp;base64,[a-zA-Z0-9+/=]+" x="0" y="0" width="480" height="320" preserveAspectRatio="none" result="raw-map"/>',
    f'<feImage href="data:image/bmp;base64,{b64_str}" x="0" y="0" width="480" height="320" preserveAspectRatio="none" result="raw-map"/>',
    html
)

# If the previous regex failed because the base64 was too long to match efficiently, let's do a split based replace:
if 'width="480" height="320" preserveAspectRatio="none" result="raw-map"' not in html:
    # Fallback brute force
    parts = html.split('result="raw-map"/>')
    for i in range(len(parts)-1):
        if 'width="480" height="320"' in parts[i]:
            start_idx = parts[i].rfind('href="data:image/bmp;base64,')
            if start_idx != -1:
                parts[i] = parts[i][:start_idx] + f'href="data:image/bmp;base64,{b64_str}" x="0" y="0" width="480" height="320" preserveAspectRatio="none" '
    html = 'result="raw-map"/>'.join(parts)


# Remove the temporary sphere-lens div, CSS, and SVG filter since it is now purely embedded in the main glass
html = re.sub(r'<div class="sphere-lens"></div>', '', html)
html = re.sub(r'\.sphere-lens\s*\{[^}]+\}', '', html)
html = re.sub(r'<filter id="sphere-dispersion".*?</filter>', '', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Unified map applied successfully.")

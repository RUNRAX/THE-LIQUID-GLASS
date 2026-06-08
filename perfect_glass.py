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

# NO magnification from the SVG filter itself! This guarantees zero pixel blocks.
M = 1.0
K = 0.0
scale = 200.0

for y in range(height - 1, -1, -1):
    for x in range(width):
        disp_x = K * (x - center_x)
        disp_y = K * (y - center_y)
        
        dx = (x - center_x) / center_x
        dy = (y - center_y) / center_y
        
        # Power of 12! This keeps the distortion ONLY at the absolute edge!
        edge_dist_x = -math.pow(dx, 12) * dx * 80.0
        edge_dist_y = -math.pow(dy, 12) * dy * 80.0
        
        disp_x += edge_dist_x
        disp_y += edge_dist_y
        
        val_r = 0.5 + (disp_x / scale)
        val_g = 0.5 + (disp_y / scale)
        
        val_r = max(0.0, min(1.0, val_r))
        val_g = max(0.0, min(1.0, val_g))
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

# Inject the flawless cloned background method for real, native magnification
if 'id="internal-bg"' not in html:
    bg_images = """
      <img src="Vibrant-Summer-Meadow-Watercolor.png" style="width: 100%; display: block;" alt="">
      <img src="bg1.png" style="width: 100%; display: block;" alt="">
      <img src="bg2.png" style="width: 100%; display: block;" alt="">
      <img src="bg3.png" style="width: 100%; display: block;" alt="">
"""
    new_internal = f"""
  <div style="position: absolute; inset: 0; border-radius: 2rem; overflow: hidden; pointer-events: none;">
    <div id="internal-bg" style="position: absolute; left: calc(-50vw + 240px); top: calc(-50vh + 160px); width: 100vw; transform: scale(3); will-change: transform, top; filter: blur(3px);">
{bg_images}
    </div>
  </div>
"""
    html = html.replace('<div class="frost-layer" id="frost-layer"></div>', new_internal + '\n  <div class="frost-layer" id="frost-layer"></div>')

    script = """
<script>
  function updateGlass() {
    const scrollY = window.scrollY;
    const bg = document.getElementById('internal-bg');
    if (bg) {
      bg.style.top = `calc(-50vh + 160px - ${scrollY}px)`;
      bg.style.transformOrigin = `50vw calc(50vh + ${scrollY}px)`;
    }
  }
  window.addEventListener('scroll', updateGlass);
  window.addEventListener('resize', updateGlass);
  updateGlass();
</script>
</body>
"""
    html = html.replace('</body>', script)

# The SVG filter no longer needs to blur the SourceGraphic heavily because we blur the internal CSS clone natively
html = re.sub(r'<feGaussianBlur in="SourceGraphic" stdDeviation="[^"]*" result="frosted"/>', '<feGaussianBlur in="SourceGraphic" stdDeviation="0" result="frosted"/>', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Perfect glass deployed.")

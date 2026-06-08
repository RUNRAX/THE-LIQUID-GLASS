with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bg_images = """
      <img src="Vibrant-Summer-Meadow-Watercolor.png" alt="">
      <img src="bg1.png" alt="">
      <img src="bg2.png" alt="">
      <img src="bg3.png" alt="">
"""

internal_bg = f"""
  <div style="position: absolute; inset: 0; border-radius: 2rem; overflow: hidden; pointer-events: none;">
    <div class="bg" style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%) scale(12); width: 100vw; height: 100vh;">
{bg_images}
    </div>
  </div>
"""

# Insert the internal background before the frost layer
html = html.replace('<div class="frost-layer" id="frost-layer"></div>', internal_bg + '\n  <div class="frost-layer" id="frost-layer"></div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Internal background injected.")

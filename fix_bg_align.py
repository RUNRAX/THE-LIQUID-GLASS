import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the previously injected internal background
html = re.sub(r'<div style="position: absolute; inset: 0; border-radius: 2rem; overflow: hidden; pointer-events: none;">\s*<div class="bg" .*?</div>\s*</div>', '', html, flags=re.DOTALL)

# Inject the new internal background with correct coordinates and ID
bg_images = """
      <img src="Vibrant-Summer-Meadow-Watercolor.png" style="width: 100%; display: block;" alt="">
      <img src="bg1.png" style="width: 100%; display: block;" alt="">
      <img src="bg2.png" style="width: 100%; display: block;" alt="">
      <img src="bg3.png" style="width: 100%; display: block;" alt="">
"""

new_internal = f"""
  <div style="position: absolute; inset: 0; border-radius: 2rem; overflow: hidden; pointer-events: none;">
    <div id="internal-bg" style="position: absolute; left: calc(-50vw + 240px); top: calc(-50vh + 160px); width: 100vw; transform: scale(12); will-change: transform, top;">
{bg_images}
    </div>
  </div>
"""

html = html.replace('<div class="frost-layer" id="frost-layer"></div>', new_internal + '\n  <div class="frost-layer" id="frost-layer"></div>')

# Add the script to sync the scroll position and transform origin
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
  updateGlass(); // init
</script>
</body>
"""

html = html.replace('</body>', script)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed internal background alignment and scrolling.")

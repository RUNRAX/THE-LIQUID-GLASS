import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Increase blur from 3px to 8px
html = html.replace('filter: blur(3px);', 'filter: blur(8px);')

# 2. Upgrade the javascript for buttery smooth scrolling
new_script = """
<script>
  const bg = document.getElementById('internal-bg');
  let lastScrollY = -1;
  
  function updateGlass() {
    const scrollY = window.scrollY;
    if (scrollY !== lastScrollY && bg) {
      bg.style.top = `calc(-50vh + 160px - ${scrollY}px)`;
      bg.style.transformOrigin = `50vw calc(50vh + ${scrollY}px)`;
      lastScrollY = scrollY;
    }
    requestAnimationFrame(updateGlass);
  }
  
  requestAnimationFrame(updateGlass);
</script>
</body>
"""

html = re.sub(r'<script>.*?</script>\n</body>', new_script, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Blur increased and scroll syncing smoothed.")

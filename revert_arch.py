import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the internal background div
html = re.sub(r'<div style="position: absolute; inset: 0; border-radius: 2rem; overflow: hidden; pointer-events: none;">\s*<div id="internal-bg".*?</div>\s*</div>', '', html, flags=re.DOTALL)

# Remove the script tag
html = re.sub(r'<script>.*?</script>', '', html, flags=re.DOTALL)

# Restore the final blur to 2.5
html = re.sub(r'<feGaussianBlur in="final-dispersion" stdDeviation="[^"]+"/>', '<feGaussianBlur in="final-dispersion" stdDeviation="2.5"/>', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Architectural changes reverted.")

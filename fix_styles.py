with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove border
html = html.replace('border: 1px solid rgba(255, 255, 255, 0.4);', '/* border removed */')

# 2. Remove white inset shadow
html = html.replace('inset 10px 10px 29px rgba(255, 255, 255, 0.8); /* Light 80% */', '')

# 3. Remove ::before
import re
html = re.sub(r'\.glass-3d-overlay::before\s*{[^}]*}', '/* removed ::before */', html)

# 4. Increase the final blur to 2.5 to hide 5x nearest-neighbor interpolation artifacts
html = html.replace('<feGaussianBlur in="final-dispersion" stdDeviation="1.5"/>', '<feGaussianBlur in="final-dispersion" stdDeviation="2.5"/>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Styles and anti-aliasing updated.")

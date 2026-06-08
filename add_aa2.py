with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the final output of the filter
if '<feGaussianBlur in="final-dispersion" stdDeviation="1.5"' not in html:
    html = html.replace('result="final-dispersion"/>', 'result="final-dispersion"/>\n    <feGaussianBlur in="final-dispersion" stdDeviation="1.5"/>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("AA added properly.")

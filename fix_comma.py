with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the trailing comma in box-shadow
html = html.replace('inset -10px -10px 29px rgba(0, 0, 0, 0.5), /* Depth 29 */', 'inset -10px -10px 29px rgba(0, 0, 0, 0.5) /* Depth 29 */')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Trailing comma fixed.")

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the specific scales. There are three feDisplacementMap tags.
# We will find them and replace their scales with 520, 480, 440 respectively.
def repl(m):
    return m.group(0).replace('scale="' + m.group(1) + '"', 'scale="{}"')

tags = re.findall(r'<feDisplacementMap[^>]+>', html)
if len(tags) >= 3:
    t0 = re.sub(r'scale="(\d+)"', 'scale="520"', tags[0])
    t1 = re.sub(r'scale="(\d+)"', 'scale="480"', tags[1])
    t2 = re.sub(r'scale="(\d+)"', 'scale="440"', tags[2])
    
    html = html.replace(tags[0], t0)
    html = html.replace(tags[1], t1)
    html = html.replace(tags[2], t2)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed scales.")

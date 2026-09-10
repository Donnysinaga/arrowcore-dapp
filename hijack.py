import os

# Read JS
with open('assets/index-vZxJGxcY.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace VeiledHood
js = js.replace('VeiledHood', 'HOODAI')
js = js.replace('veiledhood', 'hoodai')
js = js.replace('Veiledhood', 'Hoodai')

with open('assets/index-vZxJGxcY.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Read HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix asset links to point to absolute VeiledHood URLs except for the JS we downloaded
html = html.replace('href="/assets/index-sb9ALmBQ.css"', 'href="https://www.veiledhood.com/assets/index-sb9ALmBQ.css"')
html = html.replace('href="/favicon', 'href="https://www.veiledhood.com/favicon')
html = html.replace('<title>VeiledHood</title>', '<title>HOODAI</title>')

# Make sure it points to our modified local JS asset relative to repo root
html = html.replace('src="/assets/', 'src="./assets/')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Replacement successful")

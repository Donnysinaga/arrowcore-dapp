import os

# Files to process
html_files = ['index.html', 'app.html']
asset_files = [os.path.join('assets', f) for f in os.listdir('assets')]

# All text replacements
replacements = {
    'VeiledHood': 'Arrow Core',
    'veiledhood': 'arrowcore',
    'Veiledhood': 'Arrowcore',
    'HOODAI': 'Arrow Core',
    'hoodai': 'arrowcore',
    'https://x.com/arrowcore': 'https://x.com/Arrowcore_',
    'https://t.me/arrowcore': 'https://t.me/Arrowcore',
    # Just in case we encounter original links
    'https://twitter.com/veiledhood': 'https://x.com/Arrowcore_',
    'https://t.me/veiledhood_erc': 'https://t.me/Arrowcore'
}

def do_replace(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    # App.html routing fix: in index.html, change "/app" to "app.html"
    if file_path == 'assets\\index-vZxJGxcY.js' or file_path == 'assets/index-vZxJGxcY.js':
        content = content.replace('"/app"', '"app.html"')
        content = content.replace('href:"/app"', 'href:"app.html"')

    # Favicon replacements for HTML files
    if file_path.endswith('.html'):
        content = content.replace('href="/favicon.svg"', 'href="./logo.jpg"')
        content = content.replace('href="/favicon-32.png"', 'href="./logo.jpg"')
        # Make assets relative
        content = content.replace('src="/assets/', 'src="./assets/')
        content = content.replace('href="/assets/', 'href="./assets/')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for f in html_files + asset_files:
    try:
        do_replace(f)
        print(f"Processed {f}")
    except Exception as e:
        print(f"Failed {f}: {e}")

print("Replacement complete.")

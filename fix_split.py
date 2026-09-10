import os

# Files to process
files = [os.path.join('assets', f) for f in os.listdir('assets') if f.endswith('.js')]

for f_name in files:
    with open(f_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Target exact React structures safely
    content = content.replace('children:[`Veiled`,', 'children:[`Arrow `,\n')
    content = content.replace('className:`b`,children:`Hood`', 'className:`b`,children:`Core`')
    
    # Also fix title in index.html and app.html just in case
    
    with open(f_name, 'w', encoding='utf-8') as f:
        f.write(content)
        
html_files = ['index.html', 'app.html']
for h in html_files:
    with open(h, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('VeiledHood', 'Arrow Core')
    with open(h, 'w', encoding='utf-8') as f:
        f.write(c)

print("Split branding fixed")

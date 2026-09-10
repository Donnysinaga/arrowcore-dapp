import os
import re

files = [os.path.join('assets', f) for f in os.listdir('assets')]

for f_name in files:
    if not f_name.endswith('.js'): continue
    with open(f_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace any twitter/x link
    content = re.sub(r'https://(twitter|x)\.com/[a-zA-Z0-9_]+', 'https://x.com/Arrowcore_', content)
    # Replace any telegram link
    content = re.sub(r'https://t\.me/[a-zA-Z0-9_]+', 'https://t.me/Arrowcore', content)
    
    with open(f_name, 'w', encoding='utf-8') as f:
        f.write(content)
print("Social links updated")

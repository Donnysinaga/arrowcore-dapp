with open('assets/index-vZxJGxcY.js', 'r', encoding='utf-8') as f:
    data = f.read()

# Replace routing
data = data.replace('"/app"', '"app.html"')
data = data.replace('href:"/app"', 'href:"app.html"')

with open('assets/index-vZxJGxcY.js', 'w', encoding='utf-8') as f:
    f.write(data)
print("Routing fixed!")

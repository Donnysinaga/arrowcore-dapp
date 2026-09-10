import os
import re
import urllib.request

def download_file(url, dest):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(dest, 'wb') as f:
                f.write(response.read())
            print(f"Downloaded: {url} -> {dest}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

os.makedirs('assets', exist_ok=True)

# 1. LANDING PAGE
download_file("https://www.veiledhood.com/", "index.html")
with open("index.html", "r", encoding="utf-8") as f:
    landing_html = f.read()

landing_assets = re.findall(r'/(assets/[^"]+)', landing_html)
for asset in landing_assets:
    download_file(f"https://www.veiledhood.com/{asset}", asset)

# 2. APP DASHBOARD
download_file("https://app.veiledhood.com/", "app.html")
with open("app.html", "r", encoding="utf-8") as f:
    app_html = f.read()

app_assets = re.findall(r'/(assets/[^"]+)', app_html)
for asset in app_assets:
    download_file(f"https://app.veiledhood.com/{asset}", asset)

print("All assets downloaded successfully.")

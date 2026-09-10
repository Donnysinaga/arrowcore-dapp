import os

# 1. ADD TELEGRAM TO LANDING PAGE NAVBAR
js_file = 'assets/index-vZxJGxcY.js'
with open(js_file, 'r', encoding='utf-8') as f:
    js = f.read()

tw_str = r'`Twitter`,children:(0,m.jsx)(oe,{size:20})})'
tg_str = r'`Twitter`,children:(0,m.jsx)(oe,{size:20})}),(0,m.jsx)(`a`,{href:`https://t.me/Arrowcore`,target:`_blank`,rel:`noopener noreferrer`,style:{display:`flex`,alignItems:`center`,marginRight:`16px`,color:`inherit`,transition:`opacity 0.2s`,opacity:.8},onMouseEnter:e=>e.currentTarget.style.opacity=`1`,onMouseLeave:e=>e.currentTarget.style.opacity=`0.8`,"aria-label":`Telegram`,children:(0,m.jsx)(`svg`,{width:20,height:20,viewBox:`0 0 24 24`,fill:`currentColor`,children:(0,m.jsx)(`path`,{d:`M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.98 1.26-5.59 3.69-.53.36-1.01.53-1.44.52-.47-.01-1.38-.27-2.06-.49-.83-.27-1.49-.42-1.43-.88.03-.23.36-.48 1-.74 3.91-1.7 6.53-2.82 7.85-3.37 3.73-1.56 4.51-1.83 5.02-1.84.11 0 .36.03.49.13.11.08.15.19.16.3z`})})})'

js = js.replace(tw_str, tg_str)
with open(js_file, 'w', encoding='utf-8') as f:
    f.write(js)

# 2. INJECT LOGO CSS TO INDEX.HTML AND APP.HTML
css_inject = """
    <style>
      /* Hide original SVG logos */
      span[style*="color:var(--vio-lift)"] svg,
      span[style*="color: var(--vio-lift)"] svg,
      .lg > svg,
      .fl > svg,
      .fl > span:first-child > svg {
          display: none !important;
      }
      
      /* Inject custom logo image */
      span[style*="color:var(--vio-lift)"],
      span[style*="color: var(--vio-lift)"] {
          display: inline-flex !important;
          align-items: center;
          justify-content: center;
      }
      
      span[style*="color:var(--vio-lift)"]::before,
      span[style*="color: var(--vio-lift)"]::before {
          content: "";
          display: inline-block;
          width: 28px;
          height: 28px;
          background-image: url('./logo.jpg');
          background-size: cover;
          background-position: center;
          border-radius: 50%;
          margin-right: 6px;
      }
      
      .lg {
          display: flex !important;
          align-items: center !important;
      }
      .lg::before {
          content: "";
          display: inline-block;
          width: 28px;
          height: 28px;
          background-image: url('./logo.jpg');
          background-size: cover;
          background-position: center;
          border-radius: 50%;
          margin-right: 8px;
      }
    </style>
  </head>"""

for html_f in ['index.html', 'app.html']:
    with open(html_f, 'r', encoding='utf-8') as f:
        html = f.read()
    if '<style>' not in html:
        html = html.replace('</head>', css_inject)
        with open(html_f, 'w', encoding='utf-8') as f:
            f.write(html)

print("Logo and Telegram fixed!")

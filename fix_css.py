import re

css_inject = """<style>
      /* Hide original SVG logos */
      span[style*="color:var(--vio-lift)"] > svg,
      span[style*="color: var(--vio-lift)"] > svg,
      .lg > svg,
      .fl > svg {
          display: none !important;
      }
      
      /* Inject custom logo image ONLY on the span wrappers */
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
          vertical-align: middle;
      }
      
      /* If .lg directly has an SVG (no span), replace it */
      .lg > svg {
          display: none !important;
      }
      .lg:not(:has(span[style*="color"]))::before {
          content: "";
          display: inline-block;
          width: 28px;
          height: 28px;
          background-image: url('./logo.jpg');
          background-size: cover;
          background-position: center;
          border-radius: 50%;
          margin-right: 8px;
          vertical-align: middle;
      }

      /* Replace the massive right-side hero graphic (purple arches) with the logo */
      .art .arc, .art .core, .art .orb {
          display: none !important;
      }
      .art {
          background-image: url('./logo.jpg') !important;
          background-size: contain !important;
          background-position: center !important;
          background-repeat: no-repeat !important;
          border-radius: 50%;
          box-shadow: 0 0 100px rgba(0, 255, 100, 0.2);
          width: 400px;
          height: 400px;
          margin: 0 auto;
      }
      @media (max-width: 768px) {
          .art {
              width: 250px;
              height: 250px;
          }
      }
    </style>"""

for html_f in ['index.html', 'app.html']:
    with open(html_f, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace old style block with new one
    html = re.sub(r'<style>.*?</style>', css_inject, html, flags=re.DOTALL)
    
    with open(html_f, 'w', encoding='utf-8') as f:
        f.write(html)

print("CSS Fixed!")

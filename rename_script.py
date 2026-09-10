import re

# Process index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Replace Names
idx = re.sub(r'Arrow <span class="b">Core</span>', 'HOODAI', idx)
idx = idx.replace("Arrow Core", "HOODAI")
idx = idx.replace("arrowcore", "hoodai")
idx = idx.replace("Arrow", "HOODAI") # remaining standalone Arrows

# Add smooth scrolling
if 'scroll-behavior: smooth' not in idx:
    idx = idx.replace('</head>', '    <style>html { scroll-behavior: smooth; }</style>\n</head>')

# Add Roadmap section if it doesn't exist
roadmap_html = """
    <!-- Roadmap Section -->
    <section id="roadmap" class="sec">
        <div class="container">
            <div class="sec-h rv">
                <div class="sec-k">ROADMAP</div>
                <h2>The Path to Absolute Privacy</h2>
                <p class="sec-x">Our strategic milestones for the HOODAI ecosystem.</p>
            </div>
            <div class="roadmap-grid rv d1" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px; margin-top: 40px;">
                <div class="rm-card" style="background: var(--p2); border: 1px solid var(--vio); border-radius: 12px; padding: 24px;">
                    <div style="color: var(--vio-lift); font-weight: bold; margin-bottom: 8px;">Phase 1</div>
                    <h3 style="margin-bottom: 12px;">Protocol Launch</h3>
                    <ul style="color: var(--tx3); font-size: 14px; padding-left: 16px; line-height: 1.6;">
                        <li>Smart Contract Deployment</li>
                        <li>Web3 dApp Beta Release</li>
                        <li>Initial Security Audit</li>
                    </ul>
                </div>
                <div class="rm-card" style="background: var(--p2); border: 1px solid var(--line); border-radius: 12px; padding: 24px; opacity: 0.7;">
                    <div style="color: var(--tx4); font-weight: bold; margin-bottom: 8px;">Phase 2</div>
                    <h3 style="margin-bottom: 12px;">Ecosystem Expansion</h3>
                    <ul style="color: var(--tx3); font-size: 14px; padding-left: 16px; line-height: 1.6;">
                        <li>Cross-Chain Integration</li>
                        <li>HOODAI Token Generation Event</li>
                        <li>Decentralized Relayer Network</li>
                    </ul>
                </div>
                <div class="rm-card" style="background: var(--p2); border: 1px solid var(--line); border-radius: 12px; padding: 24px; opacity: 0.5;">
                    <div style="color: var(--tx4); font-weight: bold; margin-bottom: 8px;">Phase 3</div>
                    <h3 style="margin-bottom: 12px;">Global Adoption</h3>
                    <ul style="color: var(--tx3); font-size: 14px; padding-left: 16px; line-height: 1.6;">
                        <li>Mobile App Release</li>
                        <li>Institutional Privacy Pools</li>
                        <li>DAO Governance</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
"""

# Insert before FAQ section
if 'id="roadmap"' not in idx:
    idx = idx.replace('<!-- FAQ Section -->', roadmap_html + '\n    <!-- FAQ Section -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

# Process app.html
with open('app.html', 'r', encoding='utf-8') as f:
    app = f.read()

app = app.replace("Arrow Core", "HOODAI")
app = app.replace("arrowcore", "hoodai")
app = app.replace("Arrow", "HOODAI")

with open('app.html', 'w', encoding='utf-8') as f:
    f.write(app)

print("Renamed and Roadmap added!")

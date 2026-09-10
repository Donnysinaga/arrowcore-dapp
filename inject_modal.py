import re

with open('app.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject CSS
css = """
        /* WALLET MODAL */
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000; align-items: center; justify-content: center; backdrop-filter: blur(5px); }
        .modal-content { background: var(--ink); width: 340px; border-radius: 20px; border: 1px solid var(--line); padding: 24px; font-family: var(--mono); box-shadow: 0 10px 40px rgba(0,0,0,0.8); }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
        .modal-header h3 { margin: 0; font-size: 16px; color: var(--tx); font-weight: 700; }
        .modal-header button { background: var(--p3); border: none; color: var(--tx); width: 28px; height: 28px; border-radius: 50%; cursor: pointer; font-size: 12px; display:flex; align-items:center; justify-content:center; transition:0.2s; }
        .modal-header button:hover { background: var(--vio); color: white; }
        .wallet-option { display: flex; align-items: center; gap: 14px; width: 100%; background: var(--p1); border: 1px solid var(--line); padding: 14px 16px; border-radius: 14px; margin-bottom: 12px; color: var(--tx); font-family: var(--mono); cursor: pointer; transition: 0.2s; font-size: 15px; font-weight: 600; text-align:left; }
        .wallet-option:hover { background: var(--vio-dim); border-color: var(--vio); transform: translateY(-2px); }
    </style>"""
html = html.replace('</style>', css)

# 2. Inject HTML Modal
modal_html = """
    <!-- WALLET SELECTION MODAL -->
    <div id="walletModal" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Connect a Wallet</h3>
                <button onclick="closeWalletModal()">✖</button>
            </div>
            <div class="modal-options">
                <button class="wallet-option" onclick="selectWallet('metamask')">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg" width="28"/> MetaMask
                </button>
                <button class="wallet-option" onclick="selectWallet('trust')">
                    <img src="https://trustwallet.com/assets/images/media/assets/trust_logo.svg" width="28"/> Trust Wallet
                </button>
                <button class="wallet-option" onclick="selectWallet('okx')">
                    <img src="https://www.okx.com/cdn/assets/imgs/2211/D0E4AC0DA4CC3796.png" width="28"/> OKX Wallet
                </button>
                <button class="wallet-option" onclick="selectWallet('injected')">
                    <div style="width:28px; height:28px; background:var(--vio); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:16px;">🌐</div> Browser Wallet
                </button>
            </div>
        </div>
    </div>
    <script>"""
html = html.replace('<script>', modal_html, 1)

# 3. Replace JS logic
import re
new_js = """        function connectWallet() {
            if (signer != null) {
                if (confirm("Log out and disconnect wallet?")) {
                    signer = null;
                    userAddress = null;
                    document.getElementById('walletBtn').innerText = "Connect Wallet";
                    document.getElementById('networkBadge').innerHTML = "<i></i> Not Connected";
                    document.getElementById('balTransfer').innerText = "0.00";
                    document.getElementById('balSwap').innerText = "0.00";
                    document.getElementById('btnTransfer').innerText = "Please Connect Wallet";
                    document.getElementById('btnSwap').innerText = "Please Connect Wallet";
                }
                return;
            }
            document.getElementById('walletModal').style.display = 'flex';
        }

        function closeWalletModal() {
            document.getElementById('walletModal').style.display = 'none';
        }

        async function selectWallet(walletType) {
            closeWalletModal();
            let providerObj = null;

            if (walletType === 'metamask') {
                if (window.ethereum && window.ethereum.isMetaMask) providerObj = window.ethereum;
                else return alert("MetaMask is not installed in this browser.");
            } else if (walletType === 'trust') {
                if (window.trustwallet) providerObj = window.trustwallet;
                else if (window.ethereum && window.ethereum.isTrust) providerObj = window.ethereum;
                else return alert("Trust Wallet is not installed.");
            } else if (walletType === 'okx') {
                if (window.okxwallet) providerObj = window.okxwallet;
                else return alert("OKX Wallet is not installed.");
            } else {
                if (window.ethereum) providerObj = window.ethereum;
                else return alert("No Web3 wallet detected in this browser!");
            }

            const agree = confirm("Connect to Arrow Core Protocol?\\n\\nBy proceeding, you agree to our Terms of Service and acknowledge that this is a privacy-preserving network.");
            if (!agree) return;

            try {
                const provider = new ethers.BrowserProvider(providerObj);
                await provider.send("eth_requestAccounts", []);
                signer = await provider.getSigner();
                userAddress = await signer.getAddress();
                
                const balanceWei = await provider.getBalance(userAddress);
                const bal = parseFloat(ethers.formatEther(balanceWei)).toFixed(4);
                
                let icon = "";
                if(walletType==='metamask') icon = '<img src="https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg" width="14" style="vertical-align:middle; margin-right:6px;"/>';
                else if(walletType==='trust') icon = '<img src="https://trustwallet.com/assets/images/media/assets/trust_logo.svg" width="14" style="vertical-align:middle; margin-right:6px;"/>';
                else if(walletType==='okx') icon = '<img src="https://www.okx.com/cdn/assets/imgs/2211/D0E4AC0DA4CC3796.png" width="14" style="vertical-align:middle; margin-right:6px;"/>';
                else icon = '<span style="font-size:12px; margin-right:6px;">🌐</span>';

                document.getElementById('walletBtn').innerHTML = icon + userAddress.substring(0,6) + "..." + userAddress.substring(38) + ' <span style="opacity:0.6; margin-left:6px; font-size:10px;">✖</span>';
                document.getElementById('networkBadge').innerHTML = "<i></i> Connected";
                
                document.getElementById('balTransfer').innerText = bal;
                document.getElementById('balSwap').innerText = bal;

                document.getElementById('btnTransfer').innerText = "Execute Stealth Transfer";
                document.getElementById('btnSwap').innerText = "Execute Zero-Fee Swap";
            } catch (error) {
                console.error(error);
            }
        }
"""
html = re.sub(r'        async function connectWallet\(\) \{.*?(?=        function setStatus)', new_js, html, flags=re.DOTALL)

with open('app.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated successfully!")

from flask import Flask, render_template_string, request, send_file, jsonify
import requests
import io
import os

app = Flask(__name__)

API_KEY = os.environ.get('CLIPDROP_API_KEY')

# --- Premium HTML UI with Logo and Enhanced Categories ---
html_code = """
<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pothys Swarnamahal AI Designer</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

  :root {
    --gold:        #f1c40f;
    --gold-dim:    #af8b3b;
    --gold-glow:    rgba(241,196,15,0.18);
    --bg-deep:      #0a0a0a;
    --bg-card:      #111214;
    --bg-input:     #0f1012;
    --border:       #2a2a2d;
    --border-gold: rgba(241,196,15,0.25);
    --text-main:    #e4e4e4;
    --text-dim:     #666;
    --text-label:   #888;
  }

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    background: var(--bg-deep);
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 30px 18px;
  }

  .tablet {
    width: 1180px;
    max-width: 100%;
    background: #060607;
    border: 11px solid #2a2a2d;
    border-radius: 38px;
    padding: 32px 48px 36px;
    box-shadow: 0 0 80px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.04);
  }

  .header { text-align:center; margin-bottom:26px; }
  
  /* Logo Styling */
  .logo-container { margin-bottom: 15px; }
  .brand-logo { width: 160px; height: auto; filter: drop-shadow(0 0 5px rgba(241,196,15,0.3)); }

  .header h1 {
    font-family: 'Cinzel', serif;
    color: var(--gold);
    font-size: 22px;
    letter-spacing: 3.5px;
    font-weight: 600;
    text-transform: uppercase;
  }
  .header .sub {
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 2px;
    margin-top: 5px;
    text-transform: uppercase;
  }

  .main { display:flex; gap:36px; }
  .controls { flex:1; min-width:0; }
  .preview-col { flex:1.15; display:flex; flex-direction:column; }

  .fg { margin-bottom:18px; }
  .fg-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.6px;
    color: var(--text-label);
    margin-bottom: 7px;
  }

  .sel, .manual-inp {
    width: 100%;
    background: var(--bg-input);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px 14px;
    font-size: 13px;
    color: var(--gold);
    outline: none;
    cursor: pointer;
  }

  .manual-inp { display: none; margin-top: 8px; color: #fff; }
  .manual-inp.visible { display: block; }

  .gems-row { display:flex; gap:14px; flex-wrap:wrap; }
  .gem-opt { display: flex; align-items: center; gap: 7px; font-size: 12px; cursor: pointer; }
  
  .desc-ta {
    width: 100%; height: 80px;
    background: var(--bg-input);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: #fff; padding: 10px;
    resize: none; outline: none;
  }

  .preview-box {
    flex:1; min-height: 420px;
    background: var(--bg-input);
    border: 1.5px solid var(--border-gold);
    border-radius: 18px;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden; margin-bottom: 18px;
  }
  .preview-box img { max-width: 100%; max-height: 100%; object-fit: contain; }
  .preview-box img:fullscreen { object-fit: contain; background: black; }

  .loader {
    width: 40px; height: 40px;
    border: 3px solid #333; border-top-color: var(--gold);
    border-radius: 50%; animation: spin 1s linear infinite;
  }
  @keyframes spin { to { transform:rotate(360deg); } }

  .gen-btn {
    width: 100%; padding: 16px;
    background: linear-gradient(135deg, #f3d078 0%, #c9973d 50%, #af8b3b 100%);
    color: #000; font-weight: bold; border: none; border-radius: 10px; cursor: pointer;
  }
  .gen-btn:disabled { opacity: 0.5; }

  .sec-row { display:flex; gap:10px; }
  .sec-btn {
    flex:1; padding: 12px; background: #1a1a1c; color: #fff;
    border: 1px solid var(--border); border-radius: 10px; cursor: pointer;
    font-size: 12px; display: flex; align-items: center; justify-content: center; gap: 5px;
  }

  .status-bar { margin-top:10px; font-size:11px; text-align:center; height:16px; color: var(--text-dim); }
</style>
</head>
<body>

<div class="tablet">
  <div class="header">
    <div class="logo-container">
      <img src="/static/logo.png" alt="Pothys Logo" class="brand-logo" onerror="this.style.display='none'">
    </div>
    <h1>✦ Pothys Swarnamahal AI Jewel Designer ✦</h1>
    <div class="sub">Powered By Pothys</div>
  </div>

  <div class="main">
    <div class="controls">
      <div class="fg">
        <div class="fg-label">Metal & Style</div>
        <select class="sel" id="metalSelect">
          <option value="916 KDM Gold">✦ 916 KDM Gold</option>
          <option value="Antique Gold">✦ Antique Gold</option>
          <option value="Pure Silver">✦ Pure Silver</option>
          <option value="Platinum">✦ Platinum</option>
          <option value="Rose Gold">✦ Rose Gold</option>
          <option value="White Gold">✦ White Gold</option>
        </select>
      </div>

      <div class="fg">
        <div class="fg-label">Design Motif</div>
        <select class="sel" id="motifSelect" onchange="checkManual()">
          <option value="Peacock">🦚 Peacock (Mayil)</option>
          <option value="Goddess Lakshmi">🪷 Goddess Lakshmi</option>
          <option value="Temple Architecture">🏛️ Temple Traditional</option>
          <option value="Mango (Manga Malai)">🥭 Mango Motif</option>
          <option value="Lotus">🌸 Lotus Flower</option>
          <option value="Elephant">🐘 Elephant (Gaja)</option>
          <option value="Floral Pattern">💐 Modern Floral</option>
          <option value="Manual">⌨️ Manual Type</option>
        </select>
        <input type="text" class="manual-inp" id="manualMotif" placeholder="Type custom motif...">
      </div>

      <div class="fg">
        <div class="fg-label">Jewelry Category</div>
        <select class="sel" id="categorySelect">
          <option value="NECKLACE">Necklace</option>
          <option value="HARAM">Long Haram</option>
          <option value="JHUMKA">Jhumka / Earring</option>
          <option value="OTTIYANAM">Ottiyanam (Waist Belt)</option>
          <option value="BRACELET">Bracelet</option>
          <option value="BANGLE">Bangle</option>
          <option value="PENDANT">Pendant</option>
          <option value="RING">Finger Ring</option>
          <option value="MANGALSUTRA">Mangalsutra (Thali)</option>
        </select>
      </div>

      <div class="fg">
        <div class="fg-label">Add Gemstones</div>
        <div class="gems-row" id="gemsGroup">
          <label class="gem-opt"><input type="checkbox" value="Diamond"> 💎 Diamond</label>
          <label class="gem-opt"><input type="checkbox" value="Ruby"> 🔴 Ruby</label>
          <label class="gem-opt"><input type="checkbox" value="Emerald"> 💚 Emerald</label>
          <label class="gem-opt"><input type="checkbox" value="Pearls"> 🐚 Pearls</label>
        </div>
      </div>

      <div class="fg">
        <div class="fg-label">Description (Thanglish OK)</div>
        <textarea class="desc-ta" id="descInput" placeholder="Ex: Heavy bridal ottiyanam with ruby stones..."></textarea>
      </div>
    </div>

    <div class="preview-col">
      <div class="preview-box" id="previewBox">
        <span id="placeholderText">வடிவம் இங்கே தோன்றும்</span>
      </div>

      <button class="gen-btn" id="generateBtn">✨ புதிய வடிவம் உருவாக்கு</button>

      <div class="sec-row">
        <button class="sec-btn" id="downloadBtn" disabled>⬇️ Download</button>
        <button class="sec-btn" id="fullScreenBtn" disabled>🖥️ Full Screen</button>
      </div>
      <div class="status-bar" id="statusBar">&nbsp;</div>
    </div>
  </div>
</div>

<script>
  let currentUrl = null;

  function checkManual() {
    const v = document.getElementById("motifSelect").value;
    document.getElementById("manualMotif").classList.toggle("visible", v === "Manual");
  }

  document.getElementById("generateBtn").onclick = async () => {
    const box = document.getElementById("previewBox");
    const btn = document.getElementById("generateBtn");
    const status = document.getElementById("statusBar");
    const gems = [...document.querySelectorAll("#gemsGroup input:checked")].map(i => i.value);

    btn.disabled = true;
    box.innerHTML = '<div class="loader"></div>';
    status.innerText = "Designing in progress...";

    const data = {
      metal: document.getElementById("metalSelect").value,
      category: document.getElementById("categorySelect").value,
      motif: document.getElementById("motifSelect").value === "Manual" ? document.getElementById("manualMotif").value : document.getElementById("motifSelect").value,
      gems: gems,
      desc: document.getElementById("descInput").value
    };

    try {
      const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      if (!res.ok) throw new Error("Server Error");

      const blob = await res.blob();
      currentUrl = URL.createObjectURL(blob);
      box.innerHTML = `<img src="${currentUrl}" id="outputImg">`;
      
      document.getElementById("downloadBtn").disabled = false;
      document.getElementById("fullScreenBtn").disabled = false;
      status.innerText = "✓ Design Generated";
    } catch (e) {
      box.innerHTML = "Error!";
      status.innerText = "Failed to connect.";
    } finally {
      btn.disabled = false;
    }
  };

  document.getElementById("downloadBtn").onclick = () => {
    const a = document.createElement("a");
    a.href = currentUrl;
    a.download = "Pothys_Design.png";
    a.click();
  };

  document.getElementById("fullScreenBtn").onclick = () => {
    const img = document.getElementById("outputImg");
    if (img.requestFullscreen) img.requestFullscreen();
    else if (img.webkitRequestFullscreen) img.webkitRequestFullscreen();
  };
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_code)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    metal = data.get('metal')
    category = data.get('category')
    motif = data.get('motif')
    gems = ", ".join(data.get('gems', []))
    desc = data.get('desc', '')

    prompt = f"Luxury {metal} {category}, {motif} design, {gems} gemstones, {desc}, realistic, highly detailed, professional jewelry photography, cinematic lighting, 8k resolution."

    try:
        if not API_KEY:
            return jsonify({"error": "Missing CLIPDROP_API_KEY"}), 500
        response = requests.post(
            'https://clipdrop-api.co/text-to-image/v1',
            files={'prompt': (None, prompt, 'text/plain')},
            headers={'x-api-key': API_KEY}
        )
        if response.ok:
            return send_file(io.BytesIO(response.content), mimetype='image/png')
        else:
            return jsonify({"error": "API Error"}), 400
    except Exception as e:
        return str(e), 500

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

#!/usr/bin/env python3
"""
gen_apresentacao.py — Company Connection · Análise Geográfica de Participantes
Grupo 5 · IBMEC RJ · Análise de Dados (IBM3297) · 2026.1
Complete rebuild — navy/amber palette, Playfair Display + Inter
"""
import base64, os

def load_b64(path):
    try:
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

images = {
    'cidades':         '/tmp/graficos/grafico_028_0.png',
    'bairros':         '/tmp/graficos/grafico_030_1.png',
    'temporal':        '/tmp/graficos/grafico_032_2.png',
    'pizza':           '/tmp/graficos/grafico_034_3.png',
    'histograma':      '/tmp/graficos/grafico_036_4.png',
    'cep3':            '/tmp/graficos/grafico_039_5.png',
    'heatmap_bairros': '/tmp/graficos/grafico_041_6.png',
    'heatmap_cep3':    '/tmp/graficos/grafico_043_7.png',
    'cotovelo':        '/tmp/graficos/grafico_050_8.png',
    'scatter1':        '/tmp/graficos/grafico_058_9.png',
    'scatter2':        '/tmp/graficos/grafico_059_10.png',
    'arvore':          '/tmp/graficos/grafico_071_11.png',
    'importancia':     '/tmp/graficos/grafico_073_12.png',
}

b64 = {k: load_b64(v) for k, v in images.items()}

# ─── helpers ──────────────────────────────────────────────────────────────────

def img(key, style=""):
    return f'<img src="data:image/png;base64,{b64[key]}" style="max-width:100%;display:block;{style}" alt="{key}">'

def section_label(text):
    return f'<div class="section-label"><span class="dot"></span>{text}</div>'

def concept(text, title=None):
    t = f'<div class="concept-title">{title}</div>' if title else ''
    return f'<div class="concept-box">{t}<p>{text}</p></div>'

def insight(text):
    return f'<div class="insight-box"><span class="insight-icon">💡</span><div><strong>O que isso significa:</strong><p>{text}</p></div></div>'

def code_cell(code, cell_num=1, loader_msg="Executando...", loader_sub=""):
    return f'''<div class="code-cell">
  <div class="cell-header">
    <span class="cell-in">In [{cell_num}]:</span>
    <button class="run-btn" data-msg="{loader_msg}" data-sub="{loader_sub}">&#9654; RUN</button>
  </div>
  <pre><code class="language-python">{code}</code></pre>
</div>'''

def step(n, content):
    return f'<div class="step-content" data-step="{n}">{content}</div>'

# ─── CSS ──────────────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --navy:        #1a2744;
  --navy-mid:    #243560;
  --amber:       #e8a020;
  --amber-light: #f5b942;
  --bg:          #f4f6f9;
  --bg-white:    #ffffff;
  --bg-card:     #eef1f7;
  --border:      #d1d9e6;
  --text:        #1a2744;
  --text-mid:    #3d4f6e;
  --text-light:  #6b7c99;
  --green:       #2d8a4e;
  --red:         #c0392b;
  --blue-soft:   #3b6cb7;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  width: 100%; height: 100%;
  overflow: hidden;
  background: var(--bg);
  font-family: 'Inter', sans-serif;
  color: var(--text);
  -webkit-font-smoothing: antialiased;
}

/* ── PROGRESS BAR ── */
#progress-bar {
  position: fixed; top: 0; left: 0; height: 3px;
  background: var(--navy); z-index: 1000;
  transition: width 0.3s ease;
}

/* ── SLIDE COUNTER ── */
#slide-counter {
  position: fixed; bottom: 18px; left: 24px; z-index: 1000;
  font-size: 12px; color: var(--text-light); font-weight: 500;
  letter-spacing: 0.05em;
}

/* ── NAV ARROWS ── */
#nav-prev, #nav-next {
  position: fixed; bottom: 14px; z-index: 1000;
  background: var(--navy); color: white; border: none;
  width: 38px; height: 38px; border-radius: 50%;
  font-size: 16px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.2s, transform 0.15s;
}
#nav-prev { right: 72px; }
#nav-next { right: 24px; }
#nav-prev:hover, #nav-next:hover { background: var(--amber); transform: scale(1.1); }

/* ── SLIDES CONTAINER ── */
#deck {
  width: 100vw; height: 100vh;
  position: relative; overflow: hidden;
}

.slide {
  position: absolute; inset: 0;
  display: none; flex-direction: column;
  background: var(--bg);
  padding: 48px 64px 72px;
  overflow-y: auto;
  animation: fadeIn 0.35s ease;
}
.slide.active { display: flex; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }

/* ── SECTION LABEL ── */
.section-label {
  display: flex; align-items: center; gap: 8px;
  font-size: 11px; font-weight: 600; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--amber);
  margin-bottom: 10px;
}
.section-label .dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--amber); flex-shrink: 0;
}

/* ── SLIDE TITLE ── */
.slide-title {
  font-family: 'Playfair Display', serif;
  font-size: 38px; font-weight: 700;
  color: var(--navy); line-height: 1.15;
  margin-bottom: 6px;
}
.slide-subtitle {
  font-size: 14px; color: var(--text-light);
  font-style: italic; margin-bottom: 20px;
}

/* ── CONCEPT BOX ── */
.concept-box {
  border-left: 4px solid var(--amber);
  background: var(--bg-white);
  padding: 14px 18px;
  border-radius: 0 6px 6px 0;
  margin-bottom: 18px;
  font-size: 13.5px; line-height: 1.65;
  color: var(--text-mid);
}
.concept-title {
  font-weight: 700; color: var(--navy);
  font-size: 11px; letter-spacing: 0.12em;
  text-transform: uppercase; margin-bottom: 6px; color: var(--amber);
}

/* ── INSIGHT BOX ── */
.insight-box {
  display: flex; gap: 12px; align-items: flex-start;
  background: var(--navy); color: white;
  border-radius: 8px; padding: 14px 18px;
  margin-top: 14px; font-size: 13px; line-height: 1.6;
}
.insight-box .insight-icon { font-size: 20px; flex-shrink: 0; margin-top: 1px; }
.insight-box strong { display: block; font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--amber); margin-bottom: 4px; }
.insight-box p { color: rgba(255,255,255,0.85); }

/* ── CODE CELL ── */
.code-cell {
  border-radius: 8px; overflow: hidden;
  border: 1px solid var(--border);
  margin-bottom: 14px;
}
.cell-header {
  display: flex; align-items: center; justify-content: space-between;
  background: var(--navy); padding: 8px 14px;
}
.cell-in { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--amber); }
.run-btn {
  background: var(--amber); color: var(--navy);
  border: none; border-radius: 4px; padding: 4px 12px;
  font-size: 12px; font-weight: 700; cursor: pointer;
  transition: background 0.2s;
}
.run-btn:hover { background: var(--amber-light); }
.code-cell pre { margin: 0; }
.code-cell pre code { font-family: 'JetBrains Mono', monospace !important; font-size: 12.5px !important; padding: 14px !important; }

/* ── STEP CONTENT ── */
.step-content {
  opacity: 0; max-height: 0; overflow: hidden;
  transition: opacity 0.4s ease, max-height 0.4s ease;
  pointer-events: none;
}
.step-content.revealed {
  opacity: 1; max-height: 2000px;
  pointer-events: all;
}

/* ── TERMINAL OUTPUT ── */
.terminal-box {
  background: #0d1117; border-radius: 6px;
  padding: 16px 18px; font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: #c9d1d9; line-height: 1.8;
  margin-bottom: 14px;
}
.terminal-box .t-key { color: var(--amber); }
.terminal-box .t-bar { color: #3b6cb7; }

/* ── STAT CARDS ── */
.stat-row { display: flex; gap: 14px; margin-bottom: 16px; flex-wrap: wrap; }
.stat-card {
  flex: 1; min-width: 140px;
  border-radius: 10px; padding: 18px 16px;
  display: flex; flex-direction: column; gap: 4px;
}
.stat-card.navy { background: var(--navy); color: white; }
.stat-card.amber { background: var(--amber); color: var(--navy); }
.stat-card.green { background: #e8f5ee; border-left: 4px solid var(--green); }
.stat-card.red   { background: #fdecea; border-left: 4px solid var(--red); }
.stat-card .stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 32px; font-weight: 700; line-height: 1;
}
.stat-card.navy .stat-num { color: var(--amber); }
.stat-card.amber .stat-num { color: var(--navy); }
.stat-card .stat-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.75; }
.stat-card .stat-desc { font-size: 12px; line-height: 1.45; opacity: 0.8; margin-top: 4px; }

/* ── TWO COLUMNS ── */
.two-col { display: flex; gap: 20px; flex: 1; }
.col-35 { flex: 0 0 35%; }
.col-40 { flex: 0 0 40%; }
.col-60 { flex: 0 0 60%; }
.col-65 { flex: 0 0 65%; }
.col-50 { flex: 1; }

/* ── GENERIC CARD ── */
.card {
  background: var(--bg-white);
  border-radius: 10px; padding: 18px;
  border: 1px solid var(--border);
}
.card.navy { background: var(--navy); color: white; border-color: transparent; }
.card.amber-top { border-top: 4px solid var(--amber); }
.card-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--amber); margin-bottom: 6px;
}
.card-num {
  font-family: 'Playfair Display', serif;
  font-size: 48px; font-weight: 700; line-height: 1;
  margin-bottom: 6px;
}
.card-title { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
.card-body { font-size: 13px; line-height: 1.6; color: var(--text-mid); }
.card.navy .card-body { color: rgba(255,255,255,0.8); }
.card.navy .card-title { color: white; }

/* ── BADGE ── */
.badge {
  display: inline-block;
  background: var(--amber); color: var(--navy);
  font-size: 10px; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; padding: 4px 10px; border-radius: 12px;
  margin-bottom: 14px;
}
.badge.navy { background: var(--navy); color: var(--amber); }
.badge.green { background: var(--green); color: white; }
.badge.red { background: var(--red); color: white; }
.badge.blue { background: var(--blue-soft); color: white; }

/* ── TABLE ── */
.styled-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.styled-table th {
  background: var(--navy); color: white;
  padding: 10px 12px; text-align: left;
  font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;
}
.styled-table td { padding: 10px 12px; border-bottom: 1px solid var(--border); }
.styled-table tr:nth-child(even) td { background: var(--bg-card); }
.styled-table .td-num { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: var(--amber); }
.styled-table .row-amber td { background: #fff8e6; }
.styled-table .row-green td { background: #e8f5ee; }
.styled-table .row-red   td { background: #fdecea; }

/* ── PIPELINE ── */
.pipeline { display: flex; align-items: center; gap: 0; margin: 18px 0; flex-wrap: wrap; }
.pipe-card {
  background: var(--navy); color: white;
  border-radius: 8px; padding: 14px 16px;
  flex: 1; min-width: 100px; text-align: center;
}
.pipe-num { font-family: 'Playfair Display', serif; font-size: 24px; color: var(--amber); font-weight: 700; }
.pipe-icon { font-size: 20px; margin: 4px 0; }
.pipe-title { font-size: 13px; font-weight: 700; }
.pipe-sub { font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 3px; }
.pipe-arrow { color: var(--amber); font-size: 20px; padding: 0 4px; flex-shrink: 0; }

/* ── LIST ── */
.check-list { list-style: none; padding: 0; }
.check-list li { padding: 5px 0; font-size: 13px; line-height: 1.5; display: flex; gap: 8px; align-items: flex-start; }
.check-list li::before { content: '•'; color: var(--amber); font-weight: 700; flex-shrink: 0; }

/* ── LOADER OVERLAY ── */
#loader-overlay {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(26, 39, 68, 0.95);
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none;
  transition: opacity 0.3s;
}
#loader-overlay.visible { opacity: 1; pointer-events: all; }
.loader-inner { text-align: center; }
.loader-ring {
  width: 56px; height: 56px; border-radius: 50%;
  border: 4px solid rgba(232, 160, 32, 0.3);
  border-top-color: #e8a020;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 20px;
}
@keyframes spin { to { transform: rotate(360deg); } }
#loader-msg { color: white; font-size: 20px; font-weight: 600; }
#loader-sub { color: rgba(255,255,255,0.6); font-size: 13px; margin-top: 8px; }
.loader-track { width: 280px; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin: 24px auto 0; }
#loader-bar { height: 100%; background: #e8a020; border-radius: 2px; transition: width 0.4s ease; width: 0; }

/* ── CAPA ── */
#slide-1 {
  background: var(--navy) !important;
  padding: 0 !important;
  flex-direction: row;
  overflow: hidden;
}
.capa-bar {
  width: 6px; background: var(--amber);
  flex-shrink: 0; align-self: stretch;
}
.capa-content {
  padding: 52px 64px 52px 56px;
  display: flex; flex-direction: column;
  justify-content: center; flex: 1;
}
.capa-eyebrow {
  font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--amber); font-weight: 600; margin-bottom: 32px;
}
.capa-title {
  font-family: 'Playfair Display', serif;
  font-size: 68px; font-weight: 900; color: white;
  line-height: 1.05; margin-bottom: 16px;
}
.capa-subtitle {
  font-size: 16px; color: rgba(255,255,255,0.65);
  font-style: italic; margin-bottom: 28px;
}
.capa-line { width: 300px; height: 3px; background: var(--amber); margin-bottom: 24px; }
.capa-group { color: var(--amber); font-size: 12px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 8px; }
.capa-names { color: rgba(255,255,255,0.85); font-size: 13.5px; line-height: 1.9; }
.capa-footer {
  margin-top: auto; padding-top: 32px;
  font-size: 12px; color: rgba(255,255,255,0.4); letter-spacing: 0.05em;
}

/* ── AGENDA ── */
.agenda-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px; flex: 1;
}
.agenda-item {
  background: var(--bg-white); border-radius: 10px;
  padding: 20px 22px; border: 1px solid var(--border);
  display: flex; gap: 16px; align-items: flex-start;
}
.agenda-num {
  font-family: 'Playfair Display', serif;
  font-size: 42px; font-weight: 700; color: var(--amber);
  line-height: 1; flex-shrink: 0;
}
.agenda-item-title { font-size: 15px; font-weight: 700; color: var(--navy); margin-bottom: 4px; }
.agenda-item-sub { font-size: 12px; color: var(--text-light); line-height: 1.45; }

/* ── AMBER UNDERLINE ── */
.amber-underline {
  width: 60px; height: 4px; background: var(--amber); border-radius: 2px; margin-bottom: 24px;
}

/* ── DARK COMPANY CARD ── */
.company-left {
  background: var(--navy); color: white;
  border-radius: 10px; padding: 24px;
  display: flex; flex-direction: column; gap: 12px;
  justify-content: center;
}
.company-left .co-icon { font-size: 36px; }
.company-left .co-bold { color: var(--amber); font-weight: 700; font-size: 15px; }
.company-left .co-line { color: rgba(255,255,255,0.75); font-size: 13.5px; }

/* ── RIGHT SECTIONS ── */
.right-sections { display: flex; flex-direction: column; gap: 16px; }
.right-section-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--amber); margin-bottom: 4px;
}
.right-section-text { font-size: 13px; line-height: 1.65; color: var(--text-mid); }

/* ── PAIN CARDS (slide 4) ── */
.pain-cards { display: flex; gap: 16px; flex: 1; margin-top: 10px; }
.pain-card {
  flex: 1; border-radius: 10px; padding: 22px;
  background: var(--bg-white); border: 1px solid var(--border);
  display: flex; flex-direction: column;
}
.pain-card.highlight { background: var(--navy); color: white; border-top: 4px solid var(--amber); }
.pain-card .pain-num {
  font-family: 'Playfair Display', serif;
  font-size: 48px; font-weight: 700; line-height: 1;
  margin-bottom: 8px;
}
.pain-card .pain-num.navy-num { color: var(--navy); }
.pain-card .pain-num.amber-num { color: var(--amber); }
.pain-card .pain-title { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.pain-card.highlight .pain-title { color: white; }
.pain-card .pain-body { font-size: 12.5px; line-height: 1.6; color: var(--text-mid); flex: 1; }
.pain-card.highlight .pain-body { color: rgba(255,255,255,0.8); }
.focus-badge { display: inline-block; background: var(--amber); color: var(--navy); font-size: 9px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 3px 8px; border-radius: 10px; margin-top: 10px; }

/* ── HAS/HAS NOT PANELS ── */
.has-panels { display: flex; gap: 16px; margin-bottom: 16px; }
.has-panel {
  flex: 1; background: var(--bg-white); border-radius: 8px; padding: 16px;
  border: 1px solid var(--border);
}
.has-panel.has-yes { border-left: 4px solid var(--green); }
.has-panel.has-no  { border-left: 4px solid var(--red); }
.has-panel-title { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 10px; }
.has-panel.has-yes .has-panel-title { color: var(--green); }
.has-panel.has-no  .has-panel-title { color: var(--red); }
.has-panel ul { list-style: none; padding: 0; }
.has-panel ul li { font-size: 13px; padding: 3px 0; color: var(--text-mid); }

/* ── COMPARISON LAYOUT (slide 7) ── */
.compare-layout { display: flex; gap: 16px; align-items: stretch; flex: 1; }
.compare-card {
  flex: 1; border-radius: 10px; padding: 22px;
  background: var(--bg-white); border: 1px solid var(--border);
}
.compare-card.navy { background: var(--navy); border-color: transparent; }
.compare-card-title { font-size: 13px; font-weight: 700; margin-bottom: 4px; }
.compare-card.navy .compare-card-title { color: white; }
.compare-card-sub { font-size: 11px; color: var(--amber); margin-bottom: 14px; font-style: italic; }
.compare-arrow { display: flex; align-items: center; justify-content: center; font-size: 32px; color: var(--navy); flex-shrink: 0; padding: 0 4px; }
.compare-list { list-style: none; padding: 0; }
.compare-list li { font-size: 13px; padding: 5px 0; border-bottom: 1px solid rgba(0,0,0,0.06); color: var(--text-mid); }
.compare-card.navy .compare-list li { color: rgba(255,255,255,0.8); border-bottom-color: rgba(255,255,255,0.08); }
.strike { text-decoration: line-through; opacity: 0.5; }

/* ── MODEL CARDS (slide 9) ── */
.model-cards { display: flex; gap: 20px; flex: 1; }
.model-card {
  flex: 1; background: var(--navy); color: white;
  border-radius: 12px; padding: 26px;
}
.model-section { margin-bottom: 14px; }
.model-section-title { font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--amber); margin-bottom: 4px; }
.model-section-body { font-size: 13px; color: rgba(255,255,255,0.82); line-height: 1.6; }
.model-icon { font-size: 28px; margin-bottom: 6px; }
.model-name { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: white; margin-bottom: 4px; }
.model-tagline { font-size: 13px; color: rgba(255,255,255,0.6); font-style: italic; margin-bottom: 16px; }

/* ── CLUSTER TABLE (slide 20) ── */
.cluster-row-0 td { background: #fff8e6; }
.cluster-row-1 td { background: #e8f5ee; }
.cluster-row-2 td { background: var(--bg-white); }
.cluster-row-3 td { background: #fdecea; }

/* ── RECOMMENDATION COLUMNS (slide 24) ── */
.rec-cols { display: flex; gap: 16px; flex: 1; }
.rec-col { flex: 1; border-radius: 10px; overflow: hidden; border: 1px solid var(--border); display: flex; flex-direction: column; }
.rec-col-header { padding: 14px 18px; font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }
.rec-col-header.green { background: var(--green); color: white; }
.rec-col-header.red   { background: var(--red);   color: white; }
.rec-col-header.blue  { background: var(--blue-soft); color: white; }
.rec-col-body { padding: 16px; flex: 1; background: var(--bg-white); display: flex; flex-direction: column; gap: 10px; }
.rec-col-num { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 700; }
.rec-col-num.green { color: var(--green); }
.rec-col-num.red   { color: var(--red); }
.rec-col-num.blue  { color: var(--blue-soft); }
.rec-col-body p { font-size: 12px; color: var(--text-mid); line-height: 1.5; }
.rec-col-body ul { list-style: none; padding: 0; }
.rec-col-body ul li { font-size: 12px; color: var(--text); padding: 2px 0; }
.rec-col-body ul li::before { content: '›  '; color: var(--amber); font-weight: 700; }
.action-chip { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 4px 10px; border-radius: 12px; margin-top: 6px; }
.action-chip.green { background: #e8f5ee; color: var(--green); }
.action-chip.red   { background: #fdecea; color: var(--red); }
.action-chip.blue  { background: #e8eef8; color: var(--blue-soft); }

/* ── BUDGET DONUT (slide 26) ── */
.budget-layout { display: flex; gap: 32px; align-items: center; flex: 1; }
.donut-wrap { flex-shrink: 0; }
.donut-svg { width: 220px; height: 220px; }
.budget-rows { flex: 1; display: flex; flex-direction: column; gap: 18px; }
.budget-row { display: flex; gap: 14px; align-items: flex-start; }
.budget-pct { font-family: 'Playfair Display', serif; font-size: 42px; font-weight: 700; line-height: 1; flex-shrink: 0; width: 80px; }
.budget-pct.red   { color: var(--red); }
.budget-pct.green { color: var(--green); }
.budget-pct.blue  { color: var(--blue-soft); }
.budget-row-title { font-size: 15px; font-weight: 700; color: var(--navy); }
.budget-row-desc  { font-size: 12.5px; color: var(--text-mid); line-height: 1.5; margin-top: 2px; }

/* ── STEP CARDS (slide 27) ── */
.step-cards { display: flex; gap: 14px; margin: 18px 0; }
.step-card {
  flex: 1; background: var(--bg-white); border-radius: 8px;
  padding: 16px; border: 1px solid var(--border); text-align: center;
}
.step-card .step-icon { font-size: 24px; margin-bottom: 8px; }
.step-card .step-title { font-size: 13px; font-weight: 700; color: var(--navy); margin-bottom: 4px; }
.step-card .step-desc { font-size: 11.5px; color: var(--text-light); line-height: 1.45; }

/* ── VALUE CARDS (slide 28) ── */
.value-cards { display: flex; gap: 16px; flex: 1; }
.value-card {
  flex: 1; background: var(--navy); color: white;
  border-radius: 12px; padding: 26px;
}
.value-icon-circle {
  width: 48px; height: 48px; border-radius: 50%;
  background: var(--amber); display: flex; align-items: center; justify-content: center;
  font-size: 22px; margin-bottom: 14px;
}
.value-title { font-size: 16px; font-weight: 700; color: white; margin-bottom: 8px; }
.value-body { font-size: 13px; color: rgba(255,255,255,0.8); line-height: 1.6; }

/* ── CLOSING SLIDE ── */
#slide-30 {
  background: var(--navy) !important;
  align-items: center; justify-content: center;
  text-align: center;
}
.closing-icon {
  width: 90px; height: 90px; border-radius: 50%;
  background: rgba(232,160,32,0.15); border: 2px solid var(--amber);
  display: flex; align-items: center; justify-content: center;
  font-size: 40px; margin: 0 auto 24px;
}
.closing-title {
  font-family: 'Playfair Display', serif;
  font-size: 80px; font-weight: 700; color: white; line-height: 1;
  margin-bottom: 8px;
}
.closing-underline { width: 80px; height: 4px; background: var(--amber); border-radius: 2px; margin: 0 auto 16px; }
.closing-sub { font-size: 16px; color: rgba(255,255,255,0.6); font-style: italic; margin-bottom: 40px; }
.closing-footer { font-size: 12px; color: rgba(255,255,255,0.35); letter-spacing: 0.1em; }

/* ── HIGHLIGHT BOX ── */
.highlight-box {
  background: var(--navy); color: white;
  border-radius: 10px; padding: 22px 26px;
  display: flex; gap: 16px; align-items: center;
  margin-bottom: 18px;
}
.highlight-box-icon { font-size: 32px; flex-shrink: 0; }
.highlight-box-text { flex: 1; }
.highlight-box-text strong { font-size: 17px; color: white; display: block; margin-bottom: 4px; }
.highlight-box-text em { font-size: 13px; color: rgba(255,255,255,0.65); }

/* ── PSEUDO CODE ── */
.pseudo-code {
  background: #0d1117; border-radius: 6px;
  padding: 16px 18px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: #c9d1d9; line-height: 1.9;
}
.pseudo-code .pc-comment { color: #6b7c99; }
.pseudo-code .pc-keyword { color: var(--amber); }

/* ── EDUCATIONAL CONCEPTS (slide 10, 18, 21) ── */
.edu-cards { display: flex; flex-direction: column; gap: 14px; flex: 1; }
.edu-card {
  background: var(--bg-white); border-left: 4px solid var(--amber);
  border-radius: 0 8px 8px 0; padding: 14px 18px;
  border: 1px solid var(--border); border-left: 4px solid var(--amber);
}
.edu-card-title { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--amber); margin-bottom: 6px; }
.edu-card-body { font-size: 13px; line-height: 1.65; color: var(--text-mid); }

/* ── CHIPS ── */
.chip-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px; }
.chip {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 20px; padding: 5px 14px;
  font-size: 12px; font-weight: 500; color: var(--text);
}
.chip.amber { background: #fff3d4; border-color: var(--amber); color: var(--navy); }

/* ── IMPORTANCE CHIPS ── */
.importance-chips { display: flex; gap: 12px; margin-top: 12px; flex-wrap: wrap; }
.imp-chip {
  border-radius: 8px; padding: 10px 16px;
  font-size: 13px; font-weight: 600;
}
.imp-chip.amber { background: #fff3d4; border: 2px solid var(--amber); color: var(--navy); font-size: 15px; }
.imp-chip.navy  { background: var(--navy); color: white; }
.imp-chip.muted { background: var(--bg-card); color: var(--text-light); font-size: 12px; }

/* ── SCROLL WITHIN SLIDE ── */
.slide { scrollbar-width: thin; scrollbar-color: var(--border) transparent; }
"""

# ─── SLIDES ───────────────────────────────────────────────────────────────────

def slide(n, content, extra_class=""):
    return f'<div class="slide {extra_class}" id="slide-{n}" data-slide="{n}">{content}</div>\n'

def slide_header(section, title, subtitle=None):
    s = section_label(section)
    t = f'<h1 class="slide-title">{title}</h1>'
    sub = f'<p class="slide-subtitle">{subtitle}</p>' if subtitle else ''
    return s + t + sub

# SLIDE 1: CAPA
S1 = slide(1, '''
<div class="capa-bar"></div>
<div class="capa-content">
  <div class="capa-eyebrow">PROJETO APLICADO · 2026.1</div>
  <h1 class="capa-title">Análise Geográfica de<br>Participantes</h1>
  <p class="capa-subtitle">Inteligência de marketing aplicada à Company Connection</p>
  <div class="capa-line"></div>
  <div class="capa-group">GRUPO 5</div>
  <div class="capa-names">
    Gabriel Maino Chamas<br>
    Gabriela Borsoi Cohen<br>
    Hyan Lucas Alves Fernandes<br>
    Isabelle de Brito Cavalcante<br>
    João Gabriel Stor Bittencourt<br>
    Malena Catallini
  </div>
  <div class="capa-footer">IBMEC RJ &nbsp;·&nbsp; Análise de Dados (IBM3297) &nbsp;·&nbsp; Prof. Paulo Josef Hirsch</div>
</div>
''')

# SLIDE 2: AGENDA
S2 = slide(2, '''
<h1 class="slide-title" style="font-family:'Playfair Display',serif;font-size:44px;color:var(--navy);margin-bottom:6px;">Agenda</h1>
<div class="amber-underline"></div>
<div class="agenda-grid">
  <div class="agenda-item">
    <div class="agenda-num">01</div>
    <div><div class="agenda-item-title">Introdução ao Problema</div>
    <div class="agenda-item-sub">Quem é a Company Connection, o contexto e o desafio</div></div>
  </div>
  <div class="agenda-item">
    <div class="agenda-num">02</div>
    <div><div class="agenda-item-title">Metodologia</div>
    <div class="agenda-item-sub">Como abordamos os dados e os modelos escolhidos</div></div>
  </div>
  <div class="agenda-item">
    <div class="agenda-num">03</div>
    <div><div class="agenda-item-title">Resultados Obtidos</div>
    <div class="agenda-item-sub">O que descobrimos — com demonstração ao vivo</div></div>
  </div>
  <div class="agenda-item">
    <div class="agenda-num">04</div>
    <div><div class="agenda-item-title">Recomendações</div>
    <div class="agenda-item-sub">Plano de ação concreto para o marketing</div></div>
  </div>
  <div class="agenda-item">
    <div class="agenda-num">05</div>
    <div><div class="agenda-item-title">Conclusão</div>
    <div class="agenda-item-sub">O valor entregue e a reusabilidade da solução</div></div>
  </div>
  <div class="agenda-item">
    <div class="agenda-num">06</div>
    <div><div class="agenda-item-title">Perguntas e Respostas</div>
    <div class="agenda-item-sub">Discussão aberta</div></div>
  </div>
</div>
''')

# SLIDE 3: A COMPANY CONNECTION
S3 = slide(3, f'''
{slide_header("01 · INTRODUÇÃO AO PROBLEMA", "A Company Connection")}
<div class="two-col" style="flex:1;">
  <div class="col-35">
    <div class="company-left" style="height:100%;">
      <div class="co-icon">🏢</div>
      <div class="co-bold">Empresa de 2024</div>
      <div class="co-line">Operação nacional</div>
      <div class="co-line">~40–50 colaboradores</div>
    </div>
  </div>
  <div class="col-65">
    <div class="right-sections">
      <div>
        <div class="right-section-label">O QUE FAZEM</div>
        <div class="right-section-text">Operam sorteios totalmente legalizados para influenciadores digitais e marcas, usando títulos de capitalização e bilhetes lotéricos. O participante compra um bilhete e concorre a prêmios em sorteios regulamentados.</div>
      </div>
      <div>
        <div class="right-section-label">POR QUE EXISTEM</div>
        <div class="right-section-text">Cobrem uma lacuna jurídica do mercado: a maioria dos influenciadores conduzia sorteios de forma irregular, sujeitos a multas e investigações. A Company Connection oferece a estrutura legal para operar com segurança.</div>
      </div>
      <div>
        <div class="right-section-label">PRINCIPAIS CLIENTES</div>
        <div class="right-section-text">Influenciadores de grande expressão como Wesley Alemão e Razuki, além de marcas que utilizam sorteios em campanhas promocionais.</div>
      </div>
    </div>
  </div>
</div>
''')

# SLIDE 4: TRÊS DORES
S4 = slide(4, f'''
{slide_header("01 · INTRODUÇÃO AO PROBLEMA", "As três dores do negócio")}
<div class="pain-cards">
  <div class="pain-card">
    <div class="pain-num navy-num">01</div>
    <div class="pain-title">Concorrência informal</div>
    <div class="pain-body">Operadores irregulares oferecem prêmios maiores pelo mesmo preço, pois não recolhem impostos (~30–40% de carga tributária). Competição desleal estrutural.</div>
  </div>
  <div class="pain-card highlight">
    <div class="pain-num amber-num">02</div>
    <div class="pain-title">Decisões no feeling</div>
    <div class="pain-body">O time de marketing decide campanhas observando outros influenciadores, sem olhar o perfil real do próprio público.</div>
    <div><span class="focus-badge">FOCO DO NOSSO PROJETO</span></div>
  </div>
  <div class="pain-card">
    <div class="pain-num navy-num">03</div>
    <div class="pain-title">Dependência técnica</div>
    <div class="pain-body">Análises simples (segmentação por região, reativação) exigem profissional com Excel/SQL, criando gargalo operacional.</div>
  </div>
</div>
<p style="font-style:italic;color:var(--navy);font-size:14px;margin-top:14px;text-align:center;font-weight:500;">"É aqui que dados podem fazer diferença concreta."</p>
''')

# SLIDE 5: PROBLEMA ESCOLHIDO
S5 = slide(5, f'''
{slide_header("01 · INTRODUÇÃO AO PROBLEMA", "O problema escolhido")}
<div class="highlight-box">
  <div class="highlight-box-icon">🗄️</div>
  <div class="highlight-box-text">
    <strong>100 mil registros de uma base esquecida — sem virar inteligência.</strong>
    <em>Base do produto Cap Mania, sorteio semanal operado entre 2022 e 2024 e posteriormente descontinuado.</em>
  </div>
</div>
<div class="right-section-label" style="margin-bottom:12px;">POR QUE ISSO IMPORTA</div>
<div style="display:flex;gap:14px;flex:1;">
  <div class="edu-card" style="flex:1;">
    <div class="edu-card-title">Dinheiro mal direcionado</div>
    <div class="edu-card-body">Mídia paga sem dados do próprio público gera CAC mais alto. Investimento sem direcionamento é desperdício mensurável.</div>
  </div>
  <div class="edu-card" style="flex:1;">
    <div class="edu-card-title">Oportunidades perdidas</div>
    <div class="edu-card-body">Milhares de clientes dormentes esperando uma campanha de reativação. Cada dia sem ação é receita deixada na mesa.</div>
  </div>
  <div class="edu-card" style="flex:1;">
    <div class="edu-card-title">Falta de escalabilidade</div>
    <div class="edu-card-body">Cada nova decisão depende de profissional técnico — não escala. O script que entregaremos resolve isso.</div>
  </div>
</div>
''')

# SLIDE 6: A BASE
S6 = slide(6, f'''
{slide_header("02 · METODOLOGIA", "A base que recebemos")}
<div class="stat-row" style="margin-bottom:18px;">
  <div class="stat-card navy"><div class="stat-num">100.365</div><div class="stat-label">registros no total</div></div>
  <div class="stat-card navy"><div class="stat-num">5</div><div class="stat-label">colunas disponíveis</div></div>
  <div class="stat-card navy"><div class="stat-num">2022–25</div><div class="stat-label">período coberto</div></div>
  <div class="stat-card amber"><div class="stat-num">99,7%</div><div class="stat-label">estão no Rio de Janeiro</div></div>
</div>
<div class="has-panels">
  <div class="has-panel has-yes">
    <div class="has-panel-title">✓ O QUE TEMOS</div>
    <ul>
      <li>bairro</li><li>cidade</li><li>UF (estado)</li>
      <li>CEP</li><li>data da última compra</li>
    </ul>
  </div>
  <div class="has-panel has-no">
    <div class="has-panel-title">✗ O QUE NÃO TEMOS</div>
    <ul>
      <li>Idade / faixa etária</li><li>Gênero</li><li>Telefone / DDD</li>
      <li>E-mail / contato</li><li>Nome / CPF (dados pessoais)</li>
    </ul>
  </div>
</div>
<div class="concept-box" style="margin-bottom:0;">
  <div class="concept-title">NOTA EDUCACIONAL</div>
  <p>A ausência de dados demográficos não é um problema — é uma oportunidade de mostrar o que se faz com apenas 5 colunas. Toda a análise é construída sobre localização e data.</p>
</div>
''')

# SLIDE 7: REVISÃO DE METODOLOGIA
S7 = slide(7, f'''
{slide_header("02 · METODOLOGIA", "A revisão de metodologia", "Inspecionar a base antes de modelar é parte do método. Foi exatamente isso que nos guiou:")}
<div class="compare-layout">
  <div class="compare-card">
    <div class="compare-card-title">PROPOSTA INICIAL</div>
    <div class="compare-card-sub">Antes</div>
    <ul class="compare-list">
      <li class="strike">Análise de escopo nacional</li>
      <li class="strike">Variáveis demográficas (idade, telefone, e-mail)</li>
      <li class="strike">Segmentação individual por cliente</li>
      <li class="strike">Mapa de calor como "modelo"</li>
    </ul>
  </div>
  <div class="compare-arrow">→</div>
  <div class="compare-card navy">
    <div class="compare-card-title">METODOLOGIA REVISADA</div>
    <div class="compare-card-sub">Depois</div>
    <ul class="compare-list">
      <li>Foco regional: Rio de Janeiro</li>
      <li>Apenas variáveis efetivamente disponíveis</li>
      <li>Segmentação por bairro (não por pessoa)</li>
      <li>Dois modelos da matéria: K-Means + Árvore</li>
    </ul>
  </div>
</div>
<p style="font-style:italic;font-weight:700;color:var(--navy);font-size:14px;margin-top:14px;text-align:center;">"Análise mais profunda, mais acionável, mais honesta com os dados."</p>
''')

# SLIDE 8: PIPELINE
S8 = slide(8, f'''
{slide_header("02 · METODOLOGIA", "Pipeline analítico", "Seis etapas executadas em sequência, do Google Colab à recomendação final.")}
<div class="pipeline">
  <div class="pipe-card"><div class="pipe-num">1</div><div class="pipe-icon">🗄️</div><div class="pipe-title">Coleta</div><div class="pipe-sub">Carregamento do CSV</div></div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-card"><div class="pipe-num">2</div><div class="pipe-icon">⚙️</div><div class="pipe-title">Limpeza</div><div class="pipe-sub">Padronização, acentos, UF</div></div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-card"><div class="pipe-num">3</div><div class="pipe-icon">📊</div><div class="pipe-title">Variáveis</div><div class="pipe-sub">Recência, status, CEP-3</div></div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-card"><div class="pipe-num">4</div><div class="pipe-icon">🔍</div><div class="pipe-title">Exploração</div><div class="pipe-sub">Estatísticas e gráficos</div></div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-card"><div class="pipe-num">5</div><div class="pipe-icon">🧠</div><div class="pipe-title">Modelagem</div><div class="pipe-sub">K-Means + Árvore</div></div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-card"><div class="pipe-num">6</div><div class="pipe-icon">🎯</div><div class="pipe-title">Recomendações</div><div class="pipe-sub">Plano de ação</div></div>
</div>
<div class="concept-box" style="background:var(--navy);border-color:var(--amber);">
  <div class="concept-title" style="color:var(--amber);">💡 DEMONSTRAÇÃO AO VIVO</div>
  <p style="color:rgba(255,255,255,0.85);">Durante a apresentação, mostraremos cada uma dessas etapas executando ao vivo. O código foi desenhado para ser reutilizável em qualquer base com a mesma estrutura de 5 colunas.</p>
</div>
''')

# SLIDE 9: OS DOIS MODELOS
S9 = slide(9, f'''
{slide_header("02 · METODOLOGIA", "Os dois modelos escolhidos", "Cobrimos as duas grandes famílias da matéria — não supervisionado e supervisionado.")}
<div class="model-cards">
  <div class="model-card">
    <div class="card-label">MODELO 1 · NÃO SUPERVISIONADO</div>
    <div class="model-icon">👥</div>
    <div class="model-name">K-Means</div>
    <div class="model-tagline">Agrupa bairros em tiers de oportunidade</div>
    <div class="model-section"><div class="model-section-title">RESPONDE</div><div class="model-section-body">Que tipos de bairro existem na nossa base?</div></div>
    <div class="model-section"><div class="model-section-title">ENTREGA</div><div class="model-section-body">4 perfis nomeados de bairros, com características distintas de volume, recência e engajamento.</div></div>
    <div class="model-section"><div class="model-section-title">POR QUE NÃO SUPERVISIONADO?</div><div class="model-section-body">Não precisamos de "respostas certas" — deixamos o algoritmo descobrir os agrupamentos naturais. Ideal quando queremos explorar padrões desconhecidos.</div></div>
  </div>
  <div class="model-card">
    <div class="card-label">MODELO 2 · SUPERVISIONADO</div>
    <div class="model-icon">🌳</div>
    <div class="model-name">Árvore de Decisão</div>
    <div class="model-tagline">Identifica padrões geográficos do comportamento</div>
    <div class="model-section"><div class="model-section-title">RESPONDE</div><div class="model-section-body">Qual variável geográfica mais influencia a compra recente?</div></div>
    <div class="model-section"><div class="model-section-title">ENTREGA</div><div class="model-section-body">Importância relativa de cada variável geográfica e regras visuais interpretáveis pelo marketing.</div></div>
    <div class="model-section"><div class="model-section-title">POR QUE SUPERVISIONADO?</div><div class="model-section-body">Aqui temos uma variável-alvo conhecida (RECENTE ou ANTIGO). O modelo aprende com esses rótulos para descobrir padrões geográficos.</div></div>
  </div>
</div>
<p style="font-size:12px;color:var(--text-light);font-style:italic;text-align:center;margin-top:10px;">"Mapa de calor é visualização, não modelo — figura no Bloco 5 do notebook como apoio exploratório."</p>
''')

# SLIDE 10: CONCEITO LIMPEZA (educational)
S10 = slide(10, f'''
{slide_header("03 · RESULTADOS", "Por que limpeza de dados importa")}
<div class="edu-cards">
  <div class="edu-card">
    <div class="edu-card-title">O problema dos dados reais</div>
    <div class="edu-card-body">Dados do mundo real chegam sujos. A mesma cidade pode aparecer como "Rio de Janeiro", "RIO DE JANEIRO", "rio de janeiro" e "Rio de Janeiro " (com espaço). Para um modelo de machine learning, essas são QUATRO cidades diferentes — o que distorce qualquer análise.</div>
  </div>
  <div class="edu-card">
    <div class="edu-card-title">As três técnicas que usamos</div>
    <div class="edu-card-body">1. <strong>Padronização:</strong> tudo em caixa alta + remoção de espaços.&nbsp;&nbsp; 2. <strong>Remoção de acentos</strong> via normalização Unicode (NITERÓI → NITEROI).&nbsp;&nbsp; 3. <strong>Invalidação de UFs</strong> fora dos 27 estados brasileiros.</div>
  </div>
  <div class="edu-card">
    <div class="edu-card-title">Engenharia de variáveis</div>
    <div class="edu-card-body">Criar informação nova a partir do que já existe. Da coluna <code style="background:var(--bg-card);padding:2px 5px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:12px;">ultima_compra</code> (uma data), derivamos: recência em dias, status RECENTE/ANTIGO, e CEP-3 (sub-região postal para campanhas geolocalizadas).</div>
  </div>
</div>
''')

# SLIDE 11: BLOCO 2 — LIMPEZA [code + result]
CODE_B2 = """# Padronização: tudo em caixa alta + sem espaços extras
df['cidade'] = df['cidade'].str.upper().str.strip()
df['bairro'] = df['bairro'].str.upper().str.strip()
df['uf']     = df['uf'].str.upper().str.strip()

# Remove acentos (NITERÓI → NITEROI)
# Decompõe caracteres → converte para ASCII → descarta o que não é ASCII
for col in ['cidade', 'bairro']:
    df[col] = df[col].str.normalize('NFKD')\\
                     .str.encode('ascii', errors='ignore')\\
                     .str.decode('utf-8')

# UFs inválidas → None (mais honesto do que inventar um estado)
ufs_validas = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA',
               'MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN',
               'RS','RO','RR','SC','SP','SE','TO']
df.loc[~df['uf'].isin(ufs_validas), 'uf'] = None

# Converte data de texto para datetime (necessário para calcular recência)
df['ultima_compra'] = pd.to_datetime(df['ultima_compra'])"""

_s11_step1 = step(1, (
    '<div class="terminal-box">'
    '<div><span class="t-key">UFs encontradas após a limpeza:</span></div>'
    '<div>RJ &nbsp;&nbsp; 82.875 &nbsp; <span class="t-bar">██████████████████████████</span> 99,7%</div>'
    '<div>SP &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 47 &nbsp; <span class="t-bar">▏</span></div>'
    '<div>MG &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 16 &nbsp; <span class="t-bar">▏</span></div>'
    '<div>DF &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 15 &nbsp; <span class="t-bar">▏</span></div>'
    '<div>...outros &nbsp; 12</div>'
    '<div>&nbsp;</div>'
    '<div>Data mais antiga: &nbsp; <span class="t-key">2022-12-03</span></div>'
    '<div>Data mais recente: &nbsp;<span class="t-key">2025-07-06</span></div>'
    '<div>Período coberto: &nbsp;&nbsp; <span class="t-key">946 dias</span></div>'
    '</div>'
    + insight("A limpeza confirma o que veremos na EDA: 99,7% dos registros são do RJ. Isso não é problema — é uma descoberta que orienta toda a análise subsequente. A decisão de focar no RJ é baseada em evidência, não em suposição.")
))

S11 = slide(11, (
    slide_header("03 · RESULTADOS", "Bloco 2 — Limpeza e Padronização")
    + concept("A base tem inconsistências de formatação, acentuação variável e UFs inválidas. Antes de qualquer análise, precisamos garantir que 'NITERÓI' e 'NITEROI' sejam tratados como a mesma cidade. Usamos normalização Unicode (NFKD) — uma técnica de 1 linha que cobre todos os acentos de uma vez.")
    + code_cell(CODE_B2, 2, "Executando Bloco 2...", "Limpeza · padronização · normalização de acentos")
    + _s11_step1
))

# SLIDE 12: BLOCO 3 — ENGENHARIA [code + result]
CODE_B3 = """# Recência: dias desde a última compra até a data mais recente da base
data_corte = df['ultima_compra'].max()  # 2025-07-06
df['recencia_dias'] = (data_corte - df['ultima_compra']).dt.days

# Status: RECENTE (comprou nos últimos 365 dias) ou ANTIGO
df['status_recente'] = 'ANTIGO'
df.loc[df['recencia_dias'] <= DIAS_RECENTE, 'status_recente'] = 'RECENTE'

# CEP-3: sub-região postal (primeiros 3 dígitos do CEP)
# Ex: 22230-060 → '222' (Zona Sul do RJ)
df['cep3'] = df['cep'].astype(str).str[:3]"""

_s12_step1 = step(1, (
    '<div class="stat-row">'
    '<div class="stat-card navy"><div class="stat-num">479 dias</div><div class="stat-label">Recência média</div><div class="stat-desc">Mediana: 470 dias. A base está dormindo há mais de 1 ano em média.</div></div>'
    '<div class="stat-card red"><div class="stat-num">64.355</div><div class="stat-label">Clientes ANTIGOS</div><div class="stat-desc">77,7% da base — produto descontinuado em 2024.</div></div>'
    '<div class="stat-card green"><div class="stat-num">18.520</div><div class="stat-label">Clientes RECENTES</div><div class="stat-desc">22,3% — ainda engajados apesar da descontinuação.</div></div>'
    '</div>'
    + insight("A maioria esmagadora está dormindo. Mas isso é oportunidade: 64 mil pessoas que já compraram uma vez e podem ser reativadas. O status_recente que criamos aqui será a variável-alvo da Árvore de Decisão — o modelo aprenderá a identificar o perfil geográfico dos recentes.")
))

S12 = slide(12, (
    slide_header("03 · RESULTADOS", "Bloco 3 — Engenharia de Variáveis")
    + concept("Com apenas uma coluna de data, criamos três variáveis novas. Recência: quantos dias se passaram desde a última compra — transforma uma data em número comparável. Status: classifica cada cliente como RECENTE (≤365 dias) ou ANTIGO — cria a variável-alvo da Árvore de Decisão. CEP-3: os três primeiros dígitos do CEP identificam sub-regiões postais dos Correios — granularidade ideal para campanhas de Meta Ads e Google Ads.")
    + code_cell(CODE_B3, 3, "Executando Bloco 3...", "Calculando recência · classificando status · extraindo CEP-3")
    + _s12_step1
))

# SLIDE 13: O QUE A EDA REVELOU
S13 = slide(13, f'''
{slide_header("03 · RESULTADOS", "O que a análise exploratória revelou")}
<div class="badge">DEMONSTRAÇÃO · BLOCOS 4–5</div>
<div class="stat-row" style="flex:1;align-items:stretch;">
  <div class="stat-card navy" style="flex:1;justify-content:center;">
    <div class="stat-num">78%</div>
    <div class="stat-label">dos clientes são ANTIGOS</div>
    <div class="stat-desc">O produto descontinuado em 2024 deixou a maior parte da base inativa — daí o foco em reativação.</div>
  </div>
  <div class="stat-card navy" style="flex:1;justify-content:center;">
    <div class="stat-num">75</div>
    <div class="stat-label">sub-regiões postais únicas</div>
    <div class="stat-desc">Granularidade ideal para campanhas de mídia paga geo-segmentada (Meta Ads, Google Ads).</div>
  </div>
  <div class="stat-card navy" style="flex:1;justify-content:center;">
    <div class="stat-num">323</div>
    <div class="stat-label">bairros com massa crítica</div>
    <div class="stat-desc">Bairros com 50+ participantes — base estatística sólida para a clusterização K-Means.</div>
  </div>
</div>
<div class="concept-box" style="background:var(--navy);border-color:var(--amber);">
  <div class="concept-title" style="color:var(--amber);">AO VIVO</div>
  <p style="color:rgba(255,255,255,0.85);">Top 15 cidades · Top 20 bairros · Evolução temporal das compras · Heatmap bairro × status</p>
</div>
''')

# SLIDE 14: EDA — ONDE ESTÃO [2 steps]
_s14_step1 = step(1,
    '<div style="text-align:center;margin-bottom:12px;">' + img("cidades","max-height:42vh;margin:0 auto;") + '</div>'
    + insight("Campo Grande, Guaratiba, Bangu. A Zona Oeste domina — não a Zona Sul como a intuição de muitos suporia. Isso tem implicações diretas para onde concentrar campanhas de mídia paga.")
)
_s14_step2 = step(2,
    '<div style="text-align:center;margin-bottom:12px;">' + img("bairros","max-height:38vh;margin:0 auto;") + '</div>'
    + insight("No nível bairro, a concentração é ainda mais nítida. Os 20 maiores bairros concentram uma fração desproporcional da base — exatamente onde o K-Means encontrará o cluster Núcleo Estratégico.")
)
S14 = slide(14, (
    slide_header("03 · RESULTADOS", "Onde estão os participantes?")
    + concept("O primeiro passo da análise exploratória é sempre perguntar: onde estão os dados? Para uma empresa de marketing, isso significa: em quais cidades e bairros está concentrado o público? A resposta surpreende.")
    + _s14_step1 + _s14_step2
), "data-steps='2'")

# SLIDE 15: EDA — TEMPORAL [1 step]
_s15_step1 = step(1,
    '<div style="text-align:center;margin-bottom:12px;">' + img("temporal","max-height:52vh;margin:0 auto;") + '</div>'
    + insight("O gráfico mostra claramente o auge em meados de 2024 e a queda abrupta após a descontinuação. Isso explica os 77% de clientes antigos: não é abandono voluntário — é consequência da pausa no produto. A base existe e pode ser reativada quando um novo produto for lançado.")
)
S15 = slide(15, (
    slide_header("03 · RESULTADOS", "A linha do tempo do produto")
    + concept("A análise temporal responde: quando o produto teve seu auge? A curva de compras conta a história completa do Cap Mania — lançamento, crescimento, pico e descontinuação. Entender isso é fundamental para interpretar o alto volume de clientes antigos.")
    + _s15_step1
), "data-steps='1'")

# SLIDE 16: EDA — DORMÊNCIA [2 steps]
_s16_step1 = step(1,
    '<div style="display:flex;gap:16px;margin-bottom:12px;">'
    + '<div style="flex:1;text-align:center;">' + img("pizza","max-height:40vh;margin:0 auto;") + '</div>'
    + '<div style="flex:1;text-align:center;">' + img("histograma","max-height:40vh;margin:0 auto;") + '</div>'
    + '</div>'
    + insight("A linha vermelha no histograma é nosso corte. A maioria dos clientes está muito além dela — candidatos à reativação. O gráfico de pizza dá a proporção: 3 em cada 4 clientes não compram há mais de um ano.")
)
_s16_step2 = step(2, (
    '<div class="insight-box">'
    '<span class="insight-icon">📌</span>'
    '<div><strong>CONEXÃO COM O PRÓXIMO MODELO</strong>'
    '<p>A Árvore de Decisão será treinada para prever exatamente essa variável — RECENTE ou ANTIGO. O modelo aprenderá a associar padrões geográficos a esses dois perfis.</p>'
    '</div></div>'
))
S16 = slide(16, (
    slide_header("03 · RESULTADOS", "77% dormentes — e o que isso significa")
    + concept("Definimos como recente qualquer compra nos últimos 365 dias. Essa escolha de parâmetro está no Bloco 0 e pode ser ajustada. O histograma de recência mostra a distribuição completa: onde está a maioria dos clientes no eixo do tempo, e como o nosso corte de 365 dias separa as duas populações.")
    + _s16_step1 + _s16_step2
), "data-steps='2'")

# SLIDE 17: HEATMAPS [2 steps]
_s17_step1 = step(1,
    '<div style="text-align:center;margin-bottom:12px;">' + img("heatmap_bairros","max-height:46vh;margin:0 auto;") + '</div>'
    + insight("Os bairros mais escuros na coluna ANTIGO são exatamente os que aparecerão no Top 10 em Risco — alto volume de clientes que pararam de comprar.")
)
_s17_step2 = step(2,
    '<div style="text-align:center;margin-bottom:12px;">' + img("heatmap_cep3","max-height:46vh;margin:0 auto;") + '</div>'
    + insight("O CEP-3 agrega por sub-regiões postais — uma visão menos granular que o bairro, mas útil para campanhas de raio no Google Ads ou Meta Ads.")
)
S17 = slide(17, (
    slide_header("03 · RESULTADOS", "Mapa de calor: bairro por bairro")
    + concept("O heatmap cruza duas variáveis categóricas — bairro e status do cliente. Cada célula representa a contagem de clientes naquela combinação. A intensidade da cor indica concentração. Para o marketing: bairros com calor em ANTIGO são alvos de reativação; bairros com calor em RECENTE merecem manutenção. Lembre: heatmap é VISUALIZAÇÃO — não é modelo.")
    + _s17_step1 + _s17_step2
), "data-steps='2'")

# SLIDE 18: CONCEITO K-MEANS
S18 = slide(18, f'''
{slide_header("03 · RESULTADOS", "O que é o K-Means?")}
<div class="badge">MODELO 1 · NÃO SUPERVISIONADO</div>
<div class="two-col" style="flex:1;gap:24px;">
  <div class="col-60">
    <div class="edu-cards">
      <div class="edu-card">
        <div class="edu-card-title">O algoritmo em palavras simples</div>
        <div class="edu-card-body">K-Means é um algoritmo de agrupamento. Você define K (quantos grupos quer), e ele distribui os dados nesses grupos de forma que elementos dentro do mesmo grupo sejam parecidos entre si e diferentes dos outros grupos. Ele não precisa de "respostas certas" — descobre os padrões sozinho.</div>
      </div>
      <div class="edu-card">
        <div class="edu-card-title">Por que usamos no nível BAIRRO, não cliente?</div>
        <div class="edu-card-body">O produto foi descontinuado em 2024. Individualmente, quase todo cliente está "antigo" — há pouca variabilidade para o modelo trabalhar. Mas alguns BAIRROS INTEIROS se mantiveram mais ativos que outros. Essa diferença regional é o que o K-Means consegue enxergar.</div>
      </div>
      <div class="edu-card">
        <div class="edu-card-title">As 3 dimensões do agrupamento</div>
        <div class="edu-card-body">
          <div class="chip-row">
            <span class="chip amber">📊 Volume — total de participantes no bairro</span>
            <span class="chip amber">📅 Recência mediana — tempo médio sem comprar</span>
            <span class="chip amber">✅ % Recentes — proporção de clientes ativos</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="col-40">
    <div class="edu-card" style="margin-bottom:14px;">
      <div class="edu-card-title">Pseudocódigo do K-Means</div>
      <div class="pseudo-code">
        <span class="pc-comment">1. Sorteia K centros aleatórios</span><br>
        <span class="pc-comment">2. Atribui cada ponto ao</span><br>
        &nbsp;&nbsp;&nbsp;<span class="pc-comment">centro mais próximo</span><br>
        <span class="pc-comment">3. Recalcula cada centro como</span><br>
        &nbsp;&nbsp;&nbsp;<span class="pc-comment">a média dos seus pontos</span><br>
        <span class="pc-comment">4. Repete até os centros</span><br>
        &nbsp;&nbsp;&nbsp;<span class="pc-comment">não se moverem mais</span>
      </div>
    </div>
    <div class="edu-card">
      <div class="edu-card-title">Por que padronizar as variáveis?</div>
      <div class="edu-card-body">K-Means usa DISTÂNCIA entre pontos. Volume pode chegar a 2.000, enquanto % recentes vai de 0 a 100. Sem padronizar, volume dominaria o cálculo. StandardScaler coloca tudo na mesma escala (média 0, desvio 1).</div>
    </div>
  </div>
</div>
''')

# SLIDE 19: COTOVELO [1 step]
_s19_step1 = step(1,
    '<div style="text-align:center;margin-bottom:12px;">' + img("cotovelo","max-height:50vh;margin:0 auto;") + '</div>'
    + insight("A inertia cai rapidamente de K=2 a K=4. A partir de K=4, a melhora é marginal — o joelho está em K=4. Escolhemos esse valor. Além da estatística, 4 grupos é prático para o marketing: não é pouco (3 seria insuficiente para nuances), não é demais (5+ fica confuso para acionar).")
)
S19 = slide(19, (
    slide_header("03 · RESULTADOS", "Quantos grupos? O método do cotovelo")
    + concept("Diferente de outros algoritmos, o K-Means exige que você escolha K antes de rodar. Para não escolher arbitrariamente, usamos o método do cotovelo: rodamos o K-Means com K de 2 a 10 e medimos a inertia (soma das distâncias de cada ponto ao centro do seu grupo). Quanto menor a inertia, mais compactos os grupos — mas um K muito alto fragmenta demais. O cotovelo da curva indica o ponto ideal.")
    + _s19_step1
), "data-steps='1'")

# SLIDE 20: K-MEANS TIERS [2 steps]
_s20_table = (
    '<div class="badge">DEMONSTRAÇÃO COLAB · BLOCO 6</div>'
    '<div style="margin-bottom:16px;overflow-x:auto;">'
    '<table class="styled-table"><thead>'
    '<tr><th>Cluster</th><th>Nome</th><th>Bairros</th><th>Volume médio</th><th>% Recentes</th><th>Característica</th></tr>'
    '</thead><tbody>'
    '<tr class="cluster-row-0"><td>&#x1F3C6;</td><td><strong>Núcleo Estratégico</strong></td><td>6</td><td>1.642</td><td>26,1%</td><td>Megabairros — poucos, mas volume gigante</td></tr>'
    '<tr class="cluster-row-1"><td>&#x1F49A;</td><td><strong>Engajado</strong></td><td>69</td><td>98</td><td>29,4%</td><td>Maior proporção de recentes — melhor engajamento</td></tr>'
    '<tr class="cluster-row-2"><td>&#x1F4CA;</td><td><strong>Massa Padrão</strong></td><td>162</td><td>181</td><td>25,8%</td><td>Perfil médio, sem destaque para mais ou menos</td></tr>'
    '<tr class="cluster-row-3"><td>&#x1F4C9;</td><td><strong>Em Declínio</strong></td><td>86</td><td>102</td><td>19,6%</td><td>Pior recência — candidatos a reativação</td></tr>'
    '</tbody></table></div>'
)
_s20_step1 = step(1, '<div style="text-align:center;margin-bottom:10px;">' + img("scatter1","max-height:36vh;margin:0 auto;") + '</div>')
_s20_step2 = step(2,
    '<div style="display:flex;gap:16px;margin-bottom:10px;">'
    + '<div style="flex:1;text-align:center;">' + img("scatter1","max-height:32vh;margin:0 auto;") + '</div>'
    + '<div style="flex:1;text-align:center;">' + img("scatter2","max-height:32vh;margin:0 auto;") + '</div>'
    + '</div>'
    + insight("Os pontos no canto superior direito são o Núcleo Estratégico — alto volume, boa recência. Os pontos no canto inferior esquerdo são o Em Declínio. O K-Means encontrou estruturas naturais que fazem sentido de negócio.")
)
S20 = slide(20, (
    slide_header("03 · RESULTADOS", "K-Means: 4 tiers de bairros descobertos")
    + _s20_table + _s20_step1 + _s20_step2
), "data-steps='2'")

# SLIDE 21: CONCEITO ÁRVORE
S21 = slide(21, f'''
{slide_header("03 · RESULTADOS", "O que é a Árvore de Decisão?")}
<div class="badge">MODELO 2 · SUPERVISIONADO</div>
<div class="two-col" style="flex:1;gap:24px;">
  <div class="col-60">
    <div class="edu-cards">
      <div class="edu-card">
        <div class="edu-card-title">O algoritmo em palavras simples</div>
        <div class="edu-card-body">A árvore de decisão é um modelo supervisionado — aprende com exemplos rotulados. Ela cria uma sequência de perguntas binárias que, seguidas em ordem, levam a uma conclusão: RECENTE ou ANTIGO. Cada pergunta é escolhida pelo algoritmo para separar melhor as duas classes.</div>
      </div>
      <div class="edu-card">
        <div class="edu-card-title">Por que só variáveis geográficas?</div>
        <div class="edu-card-body">Se incluíssemos a recência como preditora, seria trapaça — recência define RECENTE/ANTIGO. Ao usar APENAS cidade, bairro e CEP, forçamos o modelo a descobrir padrões geográficos puros.</div>
      </div>
      <div class="edu-card">
        <div class="edu-card-title">Por que class_weight='balanced'?</div>
        <div class="edu-card-body">Base desbalanceada: 75% ANTIGO vs 25% RECENTE. Sem ajuste, a árvore aprende o atalho preguiçoso: sempre prever ANTIGO. Isso dá 75% de acurácia mas identifica zero recentes — inútil. O balanceamento força o modelo a aprender a distinguir de verdade.</div>
      </div>
    </div>
  </div>
  <div class="col-40">
    <div class="edu-cards">
      <div class="edu-card">
        <div class="edu-card-title">max_depth=5: por quê?</div>
        <div class="edu-card-body">Sem limite de profundidade, a árvore cresce indefinidamente e "decora" os dados de treino (overfitting). Com 5 níveis, ela generaliza e ainda é possível visualizar e explicar. Essa limitação é uma decisão metodológica consciente.</div>
      </div>
      <div class="edu-card">
        <div class="edu-card-title">Treino e teste (70/30)</div>
        <div class="edu-card-body">Separamos 70% dos dados para treinar e 30% para testar. O modelo "faz prova" com dados que nunca viu. Se vai bem no treino mas mal no teste, decorou — isso é overfitting. <code style="background:var(--bg-card);padding:2px 5px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:11px;">stratify=y</code> garante que a proporção RECENTE/ANTIGO seja igual nos dois conjuntos.</div>
      </div>
    </div>
  </div>
</div>
''')

# SLIDE 22: ÁRVORE — VISUALIZAÇÃO [1 step]
_s22_step1 = step(1,
    '<div style="text-align:center;margin-bottom:12px;">' + img("arvore","max-height:55vh;margin:0 auto;") + '</div>'
    + insight("Raiz (topo) = primeira pergunta. Galho esquerdo = resposta verdadeira, galho direito = falsa. Azul = maioria ANTIGO, laranja = maioria RECENTE. As folhas mais laranja indicam onde o modelo identifica concentração de clientes recentes.")
)
S22 = slide(22, (
    slide_header("03 · RESULTADOS", "A estrutura da árvore")
    + concept("Cada nó da árvore é uma pergunta: bairro_cod <= X?. Cada galho é uma resposta (sim ou não). Cada folha é uma conclusão (RECENTE ou ANTIGO). A cor indica a classe majoritária; a impureza de Gini mede o quão misturadas estão as classes naquele nó. O algoritmo escolheu automaticamente as perguntas que melhor separam as classes com apenas 5 níveis de profundidade.")
    + _s22_step1
), "data-steps='1'")

# SLIDE 23: ÁRVORE — O ACHADO [1 step]
_s23_step1 = step(1,
    '<div style="text-align:center;margin-bottom:12px;">' + img("importancia","max-height:38vh;margin:0 auto;") + '</div>'
    + '<div class="importance-chips">'
    + '<div class="imp-chip amber">&#x1F3D8; <strong>Bairro</strong> — variável mais preditiva — campanhas no nível bairro</div>'
    + '<div class="imp-chip navy">&#x1F4EE; <strong>CEP-3</strong> — segundo lugar — útil para raio em Meta Ads</div>'
    + '<div class="imp-chip muted">&#x1F3D9; <strong>Cidade</strong> — menor contribuição — granularidade insuficiente</div>'
    + '</div>'
    + insight("A análise confirma: segmentar por cidade é genérico demais; segmentar por CEP completo é específico demais (31 mil CEPs únicos no RJ). O bairro é a granularidade ideal — e a árvore chegou a essa conclusão sozinha.")
    + '<div class="concept-box" style="margin-top:12px;">'
    + '<div class="concept-title">ANÁLISE CRÍTICA</div>'
    + '<p>A acurácia geral do modelo (49%) não é o foco aqui. Prever cliente a cliente é estruturalmente difícil — produto descontinuado, sinal preditivo fraco. O valor da árvore é INTERPRETATIVO: confirmar qual variável geográfica explica o comportamento da base.</p>'
    + '</div>'
)
S23 = slide(23, (
    slide_header("03 · RESULTADOS", "Bairro é a variável mais importante")
    + concept("A árvore calcula automaticamente o quanto cada variável contribuiu para as separações — chamamos de importância. Uma variável com importância 0.65 significa que 65% do poder preditivo do modelo veio dela. Essa métrica responde diretamente à pergunta de negócio: em qual nível geográfico o marketing deve segmentar?")
    + _s23_step1
), "data-steps='1'")

# SLIDE 24: TRÊS LISTAS
S24 = slide(24, f'''
{slide_header("03 · RESULTADOS", "Três listas priorizadas de bairros")}
<div class="badge">DEMONSTRAÇÃO COLAB · BLOCO 8</div>
<div class="rec-cols">
  <div class="rec-col">
    <div class="rec-col-header green">TOP 10 ESTRELA · MANTER</div>
    <div class="rec-col-body">
      <div><div class="rec-col-num green">2.808</div><p>clientes recentes</p></div>
      <p style="font-style:italic;font-size:12px;">Alto volume + alta % de recentes</p>
      <p>Manter investimento em mídia paga geo-segmentada</p>
      <ul>
        <li>Campo Grande</li><li>Santa Cruz</li><li>Bangu</li>
        <li>Realengo</li><li>Paciência</li>
      </ul>
      <div><span class="action-chip green">Google Ads + Instagram</span></div>
    </div>
  </div>
  <div class="rec-col">
    <div class="rec-col-header red">TOP 10 EM RISCO · REATIVAR</div>
    <div class="rec-col-body">
      <div><div class="rec-col-num red">5.435</div><p>clientes dormentes</p></div>
      <p style="font-style:italic;font-size:12px;">Alto volume + baixa % de recentes</p>
      <p>Campanha de reativação urgente — maior potencial de retorno</p>
      <ul>
        <li>Centro</li><li>Guaratiba</li><li>Taquara</li>
        <li>Inhoaíba</li><li>Ramos</li>
      </ul>
      <div><span class="action-chip red">Meta Ads geo + WhatsApp</span></div>
    </div>
  </div>
  <div class="rec-col">
    <div class="rec-col-header blue">TOP 10 EMERGENTES · EXPANDIR</div>
    <div class="rec-col-body">
      <div><div class="rec-col-num blue">682</div><p>participantes</p></div>
      <p style="font-style:italic;font-size:12px;">Baixo volume + alta % de recentes</p>
      <p>Testes A/B com investimento pequeno para validar expansão</p>
      <ul>
        <li>Encantado (40,3%)</li><li>Jd. José Bonifácio (39,1%)</li>
        <li>Quitandinha (38%)</li><li>Aracatiba (37,2%)</li><li>Vila Itamarati (36,6%)</li>
      </ul>
      <div><span class="action-chip blue">Meta Ads A/B</span></div>
    </div>
  </div>
</div>
<p style="font-size:12px;color:var(--text-light);font-style:italic;margin-top:10px;text-align:center;">AO VIVO NO COLAB: tabelas detalhadas com cada um dos 30 bairros priorizados</p>
''')

# SLIDE 25: PLANO TOP 5
S25 = slide(25, f'''
{slide_header("04 · RECOMENDAÇÕES", "Plano de ação: Top 5 prioridades", "Os 5 bairros com maior potencial imediato de retorno — todos categoria REATIVAÇÃO.")}
<table class="styled-table" style="margin-bottom:18px;">
  <thead>
    <tr>
      <th>#</th><th>BAIRRO</th><th>VOLUME</th><th>% RECENTES</th><th>POTENCIAL</th><th>CANAL</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong style="color:var(--amber);font-family:'Playfair Display',serif;font-size:20px;">1</strong></td><td><strong>CENTRO</strong></td><td>2.009</td><td>24,9%</td><td>1.509 clientes</td><td>Meta Ads + WhatsApp</td></tr>
    <tr><td><strong style="color:var(--amber);font-family:'Playfair Display',serif;font-size:20px;">2</strong></td><td><strong>GUARATIBA</strong></td><td>1.028</td><td>23,9%</td><td>782 clientes</td><td>Meta Ads + WhatsApp</td></tr>
    <tr><td><strong style="color:var(--amber);font-family:'Playfair Display',serif;font-size:20px;">3</strong></td><td><strong>TAQUARA</strong></td><td>712</td><td>23,0%</td><td>548 clientes</td><td>Meta Ads + WhatsApp</td></tr>
    <tr><td><strong style="color:var(--amber);font-family:'Playfair Display',serif;font-size:20px;">4</strong></td><td><strong>INHOAÍBA</strong></td><td>621</td><td>24,0%</td><td>472 clientes</td><td>Meta Ads + WhatsApp</td></tr>
    <tr><td><strong style="color:var(--amber);font-family:'Playfair Display',serif;font-size:20px;">5</strong></td><td><strong>RAMOS</strong></td><td>619</td><td>24,7%</td><td>466 clientes</td><td>Meta Ads + WhatsApp</td></tr>
  </tbody>
</table>
<div class="concept-box" style="background:var(--navy);border-color:var(--amber);">
  <div class="concept-title" style="color:var(--amber);">💡</div>
  <p style="color:rgba(255,255,255,0.85);font-style:italic;">Total de 3.777 clientes dormentes nos 5 primeiros bairros — base concreta para definir o orçamento de reativação. KPI sugerido: 5% de taxa de reativação em 90 dias = 189 clientes recuperados.</p>
</div>
''')

# SLIDE 26: ORÇAMENTO
DONUT_SVG = '''<svg class="donut-svg" viewBox="0 0 220 220">
  <circle cx="110" cy="110" r="80" fill="none" stroke="#eef1f7" stroke-width="36"/>
  <circle cx="110" cy="110" r="80" fill="none" stroke="#c0392b" stroke-width="36"
    stroke-dasharray="251.3 502.65" stroke-dashoffset="0" transform="rotate(-90 110 110)"/>
  <circle cx="110" cy="110" r="80" fill="none" stroke="#2d8a4e" stroke-width="36"
    stroke-dasharray="175.9 502.65" stroke-dashoffset="-251.3" transform="rotate(-90 110 110)"/>
  <circle cx="110" cy="110" r="80" fill="none" stroke="#3b6cb7" stroke-width="36"
    stroke-dasharray="75.4 502.65" stroke-dashoffset="-427.2" transform="rotate(-90 110 110)"/>
  <text x="110" y="105" text-anchor="middle" font-family="Playfair Display,serif" font-size="22" font-weight="700" fill="#1a2744">100%</text>
  <text x="110" y="128" text-anchor="middle" font-family="Inter,sans-serif" font-size="10" fill="#6b7c99">distribuído</text>
</svg>'''

S26 = slide(26, f'''
{slide_header("04 · RECOMENDAÇÕES", "Alocação sugerida de orçamento", "Distribuição inicial baseada no potencial dimensionado de cada categoria.")}
<div class="budget-layout">
  <div class="donut-wrap">{DONUT_SVG}</div>
  <div class="budget-rows">
    <div class="budget-row">
      <div class="budget-pct red">50%</div>
      <div>
        <div class="budget-row-title">REATIVAÇÃO</div>
        <div class="budget-row-desc">Maior potencial imediato: 5.435 clientes dormentes em 10 bairros</div>
      </div>
    </div>
    <div class="budget-row">
      <div class="budget-pct green">35%</div>
      <div>
        <div class="budget-row-title">MANUTENÇÃO</div>
        <div class="budget-row-desc">Preservação da base ativa: 2.808 clientes recentes a serem retidos</div>
      </div>
    </div>
    <div class="budget-row">
      <div class="budget-pct blue">15%</div>
      <div>
        <div class="budget-row-title">EXPANSÃO</div>
        <div class="budget-row-desc">Teste e aprendizado: 682 participantes em mercados pouco explorados</div>
      </div>
    </div>
  </div>
</div>
<p style="font-size:13px;color:var(--text-light);font-style:italic;text-align:center;margin-top:14px;">Total dimensionado: 8.925 clientes acionáveis através do plano de ação.</p>
''')

# SLIDE 27: ATIVO PERMANENTE
S27 = slide(27, f'''
{slide_header("05 · CONCLUSÃO", "Não é uma análise pontual — é um ativo permanente")}
<div class="highlight-box">
  <div class="highlight-box-icon">🔄</div>
  <div class="highlight-box-text">
    <strong>O script funciona em qualquer base com as mesmas 5 colunas.</strong>
    <em>Quando a Company Connection lançar um novo produto, basta trocar o arquivo CSV e rodar o notebook — em minutos, novas listas priorizadas estão prontas para o marketing.</em>
  </div>
</div>
<div class="right-section-label" style="margin-bottom:14px;">COMO REUTILIZAR EM UMA BASE NOVA</div>
<div class="step-cards">
  <div class="step-card">
    <div class="step-icon">1️⃣</div>
    <div class="step-title">Trocar o CSV</div>
    <div class="step-desc">Substituir o arquivo de entrada com a base nova</div>
  </div>
  <div class="step-card">
    <div class="step-icon">2️⃣</div>
    <div class="step-title">Ajustar parâmetros</div>
    <div class="step-desc">Bloco 0: caminho, UF de foco, dias para "recente"</div>
  </div>
  <div class="step-card">
    <div class="step-icon">3️⃣</div>
    <div class="step-title">Executar tudo</div>
    <div class="step-desc">Run All no Colab — pipeline completo roda em minutos</div>
  </div>
  <div class="step-card">
    <div class="step-icon">4️⃣</div>
    <div class="step-title">Coletar saídas</div>
    <div class="step-desc">5 arquivos CSV prontos para o time de marketing</div>
  </div>
</div>
''')

# SLIDE 28: VALOR ENTREGUE
S28 = slide(28, f'''
{slide_header("05 · CONCLUSÃO", "O valor entregue à Company Connection")}
<div class="value-cards">
  <div class="value-card">
    <div class="value-icon-circle">🧠</div>
    <div class="value-title">De "feeling" para dados</div>
    <div class="value-body">O marketing passa a decidir com base no perfil real da própria base de participantes — não mais copiando o que outros influenciadores fazem.</div>
  </div>
  <div class="value-card">
    <div class="value-icon-circle">💰</div>
    <div class="value-title">Plano dimensionado</div>
    <div class="value-body">Cada recomendação vem com número absoluto de clientes em potencial — orienta orçamento sem ambiguidade.</div>
  </div>
  <div class="value-card">
    <div class="value-icon-circle">🔄</div>
    <div class="value-title">Ativo permanente</div>
    <div class="value-body">Não é entregável único: o script é reutilizável a cada novo produto, sem necessidade de novo desenvolvimento.</div>
  </div>
</div>
<div class="insight-box" style="margin-top:18px;justify-content:center;text-align:center;">
  <div style="font-size:15px;font-weight:600;font-style:italic;color:white;">
    "De 100.365 linhas paradas para 3 listas priorizadas — esse é o valor da análise de dados."
  </div>
</div>
''')

# SLIDE 29: AGENDA REVISITADA
def _agenda_item_recap(n, t, s):
    return (
        '<div style="display:flex;gap:16px;align-items:center;background:var(--bg-white);border-radius:8px;padding:14px 18px;border:1px solid var(--border);">'
        + '<span style="font-family:Playfair Display,serif;font-size:28px;font-weight:700;color:var(--amber);width:40px;">' + n + '</span>'
        + '<span style="font-size:16px;">&#x2705;</span>'
        + '<div><div style="font-size:14px;font-weight:700;color:var(--navy);">' + t + '</div>'
        + '<div style="font-size:12px;color:var(--text-light);">' + s + '</div></div></div>'
    )

_s29_items = ''.join([
    _agenda_item_recap(n, t, s)
    for n, t, s in [
        ("01","Introdução ao Problema","Empresa, contexto, dores e base de dados"),
        ("02","Metodologia","Pipeline analítico e os dois modelos escolhidos"),
        ("03","Resultados","EDA + K-Means (4 tiers) + Árvore (importância de bairro)"),
        ("04","Recomendações","3 listas de 10 bairros + plano de ação com KPIs"),
        ("05","Conclusão","Valor entregue + ativo permanente reutilizável"),
    ]
])

S29 = slide(29, (
    slide_header("06 · PERGUNTAS E RESPOSTAS", "O que cobrimos hoje")
    + '<div style="display:flex;flex-direction:column;gap:10px;flex:1;justify-content:center;">'
    + _s29_items
    + '</div>'
))

# SLIDE 30: CLOSING
S30 = slide(30, '''
<div class="closing-icon">❓</div>
<h1 class="closing-title">Perguntas?</h1>
<div class="closing-underline"></div>
<p class="closing-sub">Obrigado pela atenção.</p>
<p class="closing-footer">Grupo 5 &nbsp;·&nbsp; IBMEC RJ &nbsp;·&nbsp; Análise de Dados &nbsp;·&nbsp; 2026.1</p>
''')

ALL_SLIDES = [S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,
              S11,S12,S13,S14,S15,S16,S17,S18,S19,S20,
              S21,S22,S23,S24,S25,S26,S27,S28,S29,S30]

TOTAL = len(ALL_SLIDES)

# ─── STEP MESSAGES ────────────────────────────────────────────────────────────

STEP_MESSAGES = {
    11: {1: ("Executando Bloco 2...", "Limpeza · padronização · normalização de acentos"),
         2: ("Processando output...", "Calculando distribuição por UF e validando datas")},
    12: {1: ("Executando Bloco 3...", "Calculando recência · classificando status · extraindo CEP-3"),
         2: ("Processando estatísticas...", "Agregando por status_recente")},
    14: {1: ("Renderizando...", "Top 15 cidades por volume de participantes"),
         2: ("Renderizando...", "Top 20 bairros por volume de participantes")},
    15: {1: ("Renderizando...", "Evolução temporal das últimas compras por mês")},
    16: {1: ("Renderizando...", "Distribuição de status RECENTE vs ANTIGO"),
         2: ("Calculando...", "Histograma da recência com corte de 365 dias")},
    17: {1: ("Renderizando...", "Heatmap top 20 bairros × status do cliente"),
         2: ("Renderizando...", "Heatmap top 20 sub-regiões postais × status")},
    19: {1: ("Calculando inertia...", "K-Means rodando para K=2, 3, 4, ..., 10")},
    20: {1: ("Renderizando...", "Dispersão Volume × % Recentes colorido por cluster"),
         2: ("Renderizando...", "Dispersão Recência × % Recentes colorido por cluster")},
    22: {1: ("Treinando e renderizando...", "DecisionTreeClassifier · max_depth=5 · class_weight=balanced")},
    23: {1: ("Calculando...", "feature_importances_ · cidade · bairro · cep3")},
}

# build JS map
step_js_lines = []
for sn, steps in STEP_MESSAGES.items():
    for st, (msg, sub) in steps.items():
        step_js_lines.append(f'  [{sn},{st}]: ["{msg}", "{sub}"]')
STEP_JS_MAP = "{\n" + ",\n".join(step_js_lines) + "\n}"

# ─── JAVASCRIPT ───────────────────────────────────────────────────────────────

JS = f"""
const TOTAL = {TOTAL};
let current = 1;

const stepMessages = {STEP_JS_MAP};

function getSlideSteps(n) {{
  const el = document.getElementById('slide-' + n);
  return el ? parseInt(el.getAttribute('data-steps') || '0') : 0;
}}

function getCurrentStep(n) {{
  const el = document.getElementById('slide-' + n);
  return el ? parseInt(el.getAttribute('data-current-step') || '0') : 0;
}}

function setCurrentStep(n, s) {{
  const el = document.getElementById('slide-' + n);
  if (el) el.setAttribute('data-current-step', s);
}}

function showSlide(n) {{
  document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
  const el = document.getElementById('slide-' + n);
  if (el) el.classList.add('active');
  document.getElementById('slide-counter').textContent = n + ' / ' + TOTAL;
  const pct = (n / TOTAL) * 100;
  document.getElementById('progress-bar').style.width = pct + '%';
  current = n;
}}

function revealStep(slideNum, stepNum) {{
  const el = document.querySelector('#slide-' + slideNum + ' [data-step="' + stepNum + '"]');
  if (el) el.classList.add('revealed');
  setCurrentStep(slideNum, stepNum);
}}

function showLoader(msg, sub, callback) {{
  const overlay = document.getElementById('loader-overlay');
  document.getElementById('loader-msg').textContent = msg;
  document.getElementById('loader-sub').textContent = sub;
  const bar = document.getElementById('loader-bar');
  bar.style.width = '0%';
  overlay.classList.add('visible');
  setTimeout(() => bar.style.width = '30%', 100);
  setTimeout(() => bar.style.width = '65%', 500);
  setTimeout(() => bar.style.width = '90%', 1000);
  setTimeout(() => bar.style.width = '100%', 1500);
  setTimeout(() => {{
    overlay.classList.remove('visible');
    setTimeout(callback, 300);
  }}, 1800);
}}

function advance() {{
  const steps = getSlideSteps(current);
  const done  = getCurrentStep(current);
  if (done < steps) {{
    const next = done + 1;
    const key  = current + ',' + next;
    const msgs = stepMessages[key] || ['Processando...', ''];
    showLoader(msgs[0], msgs[1], () => revealStep(current, next));
  }} else if (current < TOTAL) {{
    showSlide(current + 1);
  }}
}}

function retreat() {{
  if (current > 1) showSlide(current - 1);
}}

document.addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight' || e.key === ' ') {{ e.preventDefault(); advance(); }}
  if (e.key === 'ArrowLeft')                   {{ e.preventDefault(); retreat(); }}
}});

document.getElementById('nav-next').addEventListener('click', advance);
document.getElementById('nav-prev').addEventListener('click', retreat);

// RUN buttons
document.addEventListener('click', e => {{
  const btn = e.target.closest('.run-btn');
  if (!btn) return;
  const msg = btn.getAttribute('data-msg') || 'Executando...';
  const sub = btn.getAttribute('data-sub') || '';
  const slideEl = btn.closest('.slide');
  if (!slideEl) return;
  const sn = parseInt(slideEl.getAttribute('data-slide'));
  const done = getCurrentStep(sn);
  const steps = getSlideSteps(sn);
  if (done < steps) {{
    showLoader(msg, sub, () => revealStep(sn, done + 1));
  }}
}});

document.addEventListener('DOMContentLoaded', () => {{
  showSlide(1);
  document.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el));
}});
"""

# ─── ASSEMBLE HTML ────────────────────────────────────────────────────────────

html_output = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Company Connection — Análise Geográfica · Grupo 5 · IBMEC 2026.1</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
<style>
{CSS}
</style>
</head>
<body>

<div id="progress-bar"></div>
<span id="slide-counter">1 / {TOTAL}</span>
<button id="nav-prev" title="Anterior">&#8592;</button>
<button id="nav-next" title="Próximo">&#8594;</button>

<!-- LOADER OVERLAY -->
<div id="loader-overlay">
  <div class="loader-inner">
    <div class="loader-ring"></div>
    <div id="loader-msg">Executando...</div>
    <div id="loader-sub"></div>
    <div class="loader-track"><div id="loader-bar"></div></div>
  </div>
</div>

<!-- SLIDES -->
<div id="deck">
{"".join(ALL_SLIDES)}
</div>

<script>
{JS}
</script>
</body>
</html>"""

out_path = '/home/user/PAD/apresentacao.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_output)

size_kb = os.path.getsize(out_path) / 1024
print(f"Generated: {out_path}")
print(f"Size: {size_kb:.1f} KB")
print(f"Slides: {TOTAL}")

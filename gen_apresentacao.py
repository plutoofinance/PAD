#!/usr/bin/env python3
import base64, os

def load_b64(path):
    try:
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        # Return a 1x1 transparent PNG as fallback
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

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Company Connection — Análise de Dados | IBMEC 2026.1</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
<style>
:root {{
  --bg: #f4f5f6;
  --bg-secondary: #e8eaed;
  --bg-card: #ffffff;
  --bg-card-hover: #f8f9fa;
  --border: rgba(52,63,77,0.1);
  --border-bright: rgba(52,63,77,0.2);
  --text-primary: #343f4d;
  --text-secondary: #5a6a7a;
  --text-muted: #8a9aaa;
  --accent-blue: #6aadb8;
  --accent-cyan: #4d9aa8;
  --accent-amber: #ff4b28;
  --accent-green: #2aa87a;
  --accent-red: #ff4b28;
  --accent-purple: #6aadb8;
  --gradient-blue: linear-gradient(135deg, #6aadb8, #4d9aa8);
  --code-bg: #f0f2f4;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body {{
  width: 100%; height: 100%;
  overflow: hidden;
  background: var(--bg);
  color: var(--text-primary);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
}}

body {{
  background-image:
    linear-gradient(rgba(52,63,77,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(52,63,77,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}}

/* ============ FIXED UI ============ */
#top-progress {{
  position: fixed; top: 0; left: 0; right: 0; height: 3px;
  background: rgba(52,63,77,0.05);
  z-index: 1000;
}}
#top-progress-fill {{
  height: 100%;
  background: linear-gradient(90deg, #6aadb8, #ff4b28);
  transition: width 0.5s cubic-bezier(.4,0,.2,1);
  box-shadow: 0 0 12px rgba(106,173,184,0.5);
}}

#chapter-indicator {{
  position: fixed; top: 20px; left: 28px;
  font-size: 10px; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--text-muted);
  z-index: 999; display: flex; align-items: center; gap: 8px;
  transition: opacity 0.3s;
}}
#chapter-indicator .dot {{
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent-blue);
  box-shadow: 0 0 8px var(--accent-blue);
}}
#chapter-indicator .chapter-text {{ color: var(--accent-blue); }}

#slide-counter {{
  position: fixed; bottom: 28px; left: 28px;
  font-size: 11px; font-weight: 500; letter-spacing: 0.08em;
  color: var(--text-muted); z-index: 999;
  font-feature-settings: "tnum";
}}

#nav-arrows {{
  position: fixed; bottom: 20px; right: 28px;
  display: flex; gap: 10px; z-index: 999;
}}
.nav-btn {{
  width: 42px; height: 42px; border-radius: 50%;
  border: 1px solid var(--border-bright);
  background: rgba(52,63,77,0.05);
  backdrop-filter: blur(12px);
  color: var(--text-secondary);
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  font-size: 16px; transition: all 0.2s ease;
  user-select: none;
}}
.nav-btn:hover {{
  background: rgba(106,173,184,0.15);
  border-color: var(--accent-blue);
  color: var(--accent-blue);
  box-shadow: 0 0 20px rgba(106,173,184,0.3);
}}
.nav-btn:active {{ transform: scale(0.92); }}

/* ============ PRESENTATION CONTAINER ============ */
#presentation {{
  width: 100vw; height: 100vh;
  position: relative; overflow: hidden;
}}

.slide {{
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  padding: 64px 72px 72px;
  opacity: 0;
  transform: translateX(100%);
  transition: transform 0.5s cubic-bezier(.4,0,.2,1), opacity 0.5s ease;
  pointer-events: none;
  overflow: hidden;
}}
.slide.active {{
  opacity: 1; transform: translateX(0); pointer-events: all;
}}
.slide.exit-left {{
  opacity: 0; transform: translateX(-100%);
}}

/* ============ TYPOGRAPHY ============ */
.slide-title {{
  font-size: 38px; font-weight: 800;
  background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.15; margin-bottom: 6px;
}}
.slide-subtitle {{
  font-size: 16px; font-weight: 500; color: var(--text-secondary);
  margin-bottom: 28px; letter-spacing: 0.02em;
}}
.slide-subtitle.amber {{ color: var(--accent-amber); }}
.slide-subtitle.blue {{ color: var(--accent-blue); }}
.slide-subtitle.purple {{ color: var(--accent-purple); }}
.context-text {{
  font-size: 14px; color: var(--text-secondary); line-height: 1.7;
  font-style: italic; margin-bottom: 22px;
  padding: 14px 18px; background: var(--bg-card);
  border-left: 3px solid var(--accent-blue);
  border-radius: 0 8px 8px 0;
}}

/* ============ CARDS ============ */
.glass-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
  transition: border-color 0.2s, background 0.2s;
}}
.glass-card:hover {{
  border-color: var(--border-bright);
  background: var(--bg-card-hover);
}}
.card-icon {{ font-size: 28px; margin-bottom: 12px; }}
.card-title {{ font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; letter-spacing: 0.03em; }}
.card-body {{ font-size: 13px; color: var(--text-secondary); line-height: 1.65; }}

/* ============ GRIDS ============ */
.grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }}
.grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 22px; }}
.col-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; align-items: start; }}

/* ============ STEPS ============ */
.step {{
  opacity: 0;
  transform: translateY(22px);
  transition: opacity 0.45s ease, transform 0.45s ease;
}}
.step.revealed {{
  opacity: 1; transform: translateY(0);
}}

/* ============ LOADER ============ */
#exec-loader {{
  position: fixed;
  bottom: 0; left: 0; right: 0;
  height: 0; /* toggled via .visible */
  background: linear-gradient(to top, rgba(8,12,24,0.98) 60%, transparent 100%);
  display: flex; align-items: flex-end; justify-content: center;
  padding-bottom: 90px;
  z-index: 500;
  opacity: 0; pointer-events: none;
  transition: opacity 0.2s ease;
}}
#exec-loader.visible {{
  opacity: 1; pointer-events: all;
  height: 100vh;
}}
.exec-loader-inner {{
  display: flex; flex-direction: column; align-items: center; gap: 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-bright);
  border-radius: 14px;
  padding: 22px 40px;
  min-width: 320px;
  box-shadow: 0 4px 24px rgba(52,63,77,0.12), 0 1px 4px rgba(52,63,77,0.08);
}}
.jupyter-cell-indicator {{
  display: flex; align-items: center; gap: 3px;
  font-family: 'JetBrains Mono', monospace; font-size: 15px;
}}
.cell-bracket {{ color: var(--text-muted); }}
.cell-star {{
  color: var(--accent-blue);
  animation: pulse-star 0.8s ease-in-out infinite alternate;
}}
@keyframes pulse-star {{
  from {{ opacity: 0.4; }}
  to {{ opacity: 1; text-shadow: 0 0 12px var(--accent-blue); }}
}}
.exec-status {{
  font-size: 12px; color: var(--text-secondary);
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.04em;
}}
.exec-progress-track {{
  width: 260px; height: 3px;
  background: rgba(52,63,77,0.08);
  border-radius: 2px; overflow: hidden;
}}
.exec-progress-fill {{
  height: 100%; width: 0%;
  background: linear-gradient(90deg, #6aadb8, #ff4b28);
  border-radius: 2px;
  box-shadow: 0 0 8px rgba(106,173,184,0.4);
}}
.exec-progress-fill.animating {{
  transition: width 1.2s ease-in-out;
}}

/* ============ CODE BLOCKS ============ */
.jupyter-cell {{
  border-radius: 12px; overflow: hidden;
  border: 1px solid var(--border);
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 14px;
}}
.jupyter-cell-header {{
  display: flex; align-items: center; gap: 10px;
  padding: 8px 16px;
  background: rgba(52,63,77,0.03);
  border-bottom: 1px solid var(--border);
}}
.jupyter-in-label {{
  font-size: 11px; color: var(--accent-blue);
  font-family: 'JetBrains Mono', monospace; letter-spacing: 0.05em;
}}
.jupyter-cell pre {{
  margin: 0 !important; border-radius: 0 !important;
  background: var(--code-bg) !important;
  font-size: 12.5px !important; line-height: 1.65 !important;
  padding: 16px 18px !important;
  overflow-x: auto;
}}
.jupyter-cell pre code {{ font-size: 12.5px !important; }}

.terminal-output {{
  background: #f0f2f4;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: #343f4d;
  line-height: 1.7;
  overflow-x: auto;
  margin-bottom: 14px;
}}
.terminal-output .out-label {{
  font-size: 10px; color: var(--text-muted);
  margin-bottom: 6px; letter-spacing: 0.08em;
}}

/* ============ DATA TABLE ============ */
.data-table {{
  width: 100%; border-collapse: collapse;
  font-size: 12.5px; border-radius: 10px; overflow: hidden;
  border: 1px solid var(--border);
}}
.data-table th {{
  background: rgba(52,63,77,0.05);
  padding: 10px 14px; text-align: left;
  font-size: 10px; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--text-secondary);
  border-bottom: 1px solid var(--border);
}}
.data-table td {{
  padding: 9px 14px; border-bottom: 1px solid rgba(52,63,77,0.04);
  color: var(--text-primary); vertical-align: middle;
}}
.data-table tr:last-child td {{ border-bottom: none; }}
.data-table tr.row-amber td {{ background: rgba(255,75,40,0.06); }}
.data-table tr.row-green td {{ background: rgba(16,185,129,0.06); }}
.data-table tr.row-blue td {{ background: rgba(106,173,184,0.08); }}
.data-table tr.row-red td {{ background: rgba(255,75,40,0.06); }}

/* ============ STAT CARDS ============ */
.stat-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 22px;
  text-align: center;
}}
.stat-label {{ font-size: 11px; color: var(--text-muted); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; }}
.stat-value {{ font-size: 28px; font-weight: 800; line-height: 1.1; margin-bottom: 4px; }}
.stat-sub {{ font-size: 11px; color: var(--text-secondary); }}
.stat-card.blue .stat-value {{ color: var(--accent-blue); }}
.stat-card.green .stat-value {{ color: var(--accent-green); }}
.stat-card.red .stat-value {{ color: var(--accent-red); }}
.stat-card.amber .stat-value {{ color: var(--accent-amber); }}

/* ============ CALLOUT / INSIGHT ============ */
.callout {{
  background: rgba(255,75,40,0.08);
  border: 1px solid rgba(255,75,40,0.25);
  border-left: 4px solid var(--accent-amber);
  border-radius: 0 10px 10px 0;
  padding: 14px 18px;
  font-size: 13.5px; color: var(--text-primary);
  line-height: 1.65; font-style: italic;
  margin-top: 14px;
}}
.callout.blue {{
  background: rgba(106,173,184,0.08);
  border-color: rgba(106,173,184,0.3);
  border-left-color: var(--accent-blue);
}}
.callout.green {{
  background: rgba(16,185,129,0.06);
  border-color: rgba(16,185,129,0.2);
  border-left-color: var(--accent-green);
}}

/* ============ CHIPS ============ */
.chip {{
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 12px; border-radius: 20px;
  font-size: 12px; font-weight: 600; letter-spacing: 0.03em;
}}
.chip.blue {{ background: rgba(106,173,184,0.12); color: var(--accent-blue); border: 1px solid rgba(106,173,184,0.2); }}
.chip.amber {{ background: rgba(255,75,40,0.12); color: var(--accent-amber); border: 1px solid rgba(255,75,40,0.2); }}
.chip.green {{ background: rgba(16,185,129,0.12); color: var(--accent-green); border: 1px solid rgba(16,185,129,0.2); }}
.chip.red {{ background: rgba(255,75,40,0.12); color: var(--accent-red); border: 1px solid rgba(255,75,40,0.2); }}
.chip.purple {{ background: rgba(106,173,184,0.12); color: var(--accent-purple); border: 1px solid rgba(106,173,184,0.2); }}
.chip.muted {{ background: rgba(52,63,77,0.05); color: var(--text-secondary); border: 1px solid var(--border); }}

/* ============ IMAGE CONTAINERS ============ */
.chart-img {{
  width: 100%; height: auto; max-height: 50vh;
  object-fit: contain; border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  display: block;
}}
.chart-img.tall {{ max-height: 55vh; }}
.chart-img.full {{ max-height: 60vh; }}

/* ============ SLIDE-SPECIFIC STYLES ============ */

/* Slide 1 — Hook */
.slide-hook {{
  display: flex !important; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center;
  background: radial-gradient(ellipse 80% 60% at 50% 50%, rgba(106,173,184,0.1) 0%, transparent 70%);
  padding: 40px !important;
}}
.hook-num {{
  font-size: clamp(80px, 12vw, 130px); font-weight: 900;
  line-height: 1; letter-spacing: -0.04em;
  color: var(--text-primary);
  animation: fadeInUp 0.7s ease 0.1s both;
}}
.hook-line-2 {{
  font-size: clamp(36px, 5vw, 62px); font-weight: 300;
  color: var(--text-secondary); letter-spacing: -0.02em;
  animation: fadeInUp 0.7s ease 0.4s both;
}}
.hook-line-3 {{
  font-size: clamp(22px, 3vw, 42px); font-weight: 600;
  color: var(--accent-amber);
  animation: fadeInUp 0.7s ease 0.7s both;
  margin-top: 12px;
}}
.hook-line-4 {{
  font-size: clamp(14px, 1.8vw, 22px); color: var(--text-muted);
  font-weight: 400; max-width: 600px;
  animation: fadeInUp 0.7s ease 1.0s both;
  margin-top: 10px;
}}
.hook-line-5 {{
  font-size: clamp(18px, 2.2vw, 30px); color: var(--accent-blue);
  font-style: italic; font-weight: 600;
  animation: fadeInUp 0.7s ease 1.3s both;
  margin-top: 14px;
}}
.hook-hint {{
  margin-top: 40px;
  font-size: 12px; color: var(--text-muted);
  letter-spacing: 0.1em; text-transform: uppercase;
  animation: blink 2s ease-in-out 2s infinite;
}}
@keyframes blink {{
  0%, 100% {{ opacity: 0.3; }}
  50% {{ opacity: 1; }}
}}
@keyframes fadeInUp {{
  from {{ opacity: 0; transform: translateY(30px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

/* Slide 5 — Big number */
.big-pct {{
  font-size: clamp(80px, 14vw, 140px); font-weight: 900;
  letter-spacing: -0.04em; line-height: 1;
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 40px rgba(106,173,184,0.25));
  text-align: center;
}}

/* Pipeline nodes */
.pipeline-wrap {{
  display: flex; flex-direction: column; gap: 16px;
  margin-top: 10px;
}}
.pipeline-row {{
  display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
}}
.pipeline-node {{
  display: flex; flex-direction: column; align-items: center;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 16px;
  min-width: 80px; text-align: center;
  font-size: 11px;
}}
.pipeline-node .node-num {{
  font-size: 10px; font-weight: 600; letter-spacing: 0.08em;
  margin-bottom: 4px;
}}
.pipeline-node .node-label {{
  font-size: 11px; font-weight: 500; color: var(--text-primary);
}}
.pipeline-node.blue {{ border-color: rgba(106,173,184,0.25); }}
.pipeline-node.blue .node-num {{ color: var(--accent-blue); }}
.pipeline-node.purple {{ border-color: rgba(106,173,184,0.25); }}
.pipeline-node.purple .node-num {{ color: var(--accent-purple); }}
.pipeline-node.teal {{ border-color: rgba(6,182,212,0.3); }}
.pipeline-node.teal .node-num {{ color: var(--accent-cyan); }}
.pipeline-node.amber {{ border-color: rgba(255,75,40,0.25); }}
.pipeline-node.amber .node-num {{ color: var(--accent-amber); }}
.pipeline-node.green {{ border-color: rgba(16,185,129,0.3); }}
.pipeline-node.green .node-num {{ color: var(--accent-green); }}
.pipeline-arrow {{ color: var(--text-muted); font-size: 16px; flex-shrink: 0; }}
.pipeline-group-label {{
  font-size: 9px; font-weight: 700; letter-spacing: 0.15em;
  text-transform: uppercase; margin-bottom: 6px;
}}

/* Contrast boxes slide 3 */
.contrast-box {{
  border-radius: 12px; padding: 20px 24px;
}}
.contrast-box.red-tint {{
  background: rgba(255,75,40,0.07);
  border: 1px solid rgba(255,75,40,0.2);
}}
.contrast-box.green-tint {{
  background: rgba(16,185,129,0.07);
  border: 1px solid rgba(16,185,129,0.2);
}}
.contrast-box-title {{
  font-size: 13px; font-weight: 700; margin-bottom: 10px;
  letter-spacing: 0.05em;
}}
.contrast-box.red-tint .contrast-box-title {{ color: var(--accent-red); }}
.contrast-box.green-tint .contrast-box-title {{ color: var(--accent-green); }}
.contrast-box ul {{
  list-style: none; padding: 0;
}}
.contrast-box ul li {{
  font-size: 12.5px; color: var(--text-secondary);
  padding: 4px 0; border-bottom: 1px solid rgba(52,63,77,0.04);
  line-height: 1.5;
}}
.contrast-box ul li:last-child {{ border-bottom: none; }}

/* Strikethrough list */
.strike-list {{ list-style: none; padding: 0; }}
.strike-list li {{
  font-size: 12.5px; padding: 5px 0;
  color: var(--text-muted);
  text-decoration: line-through;
  border-bottom: 1px solid rgba(52,63,77,0.03);
}}
.clean-list {{ list-style: none; padding: 0; }}
.clean-list li {{
  font-size: 12.5px; padding: 5px 0;
  color: var(--text-primary);
  border-bottom: 1px solid rgba(52,63,77,0.04);
  display: flex; align-items: center; gap: 8px;
}}
.clean-list li::before {{
  content: '▸'; color: var(--accent-cyan); font-size: 10px;
}}

/* Col header */
.col-header {{
  font-size: 12px; font-weight: 700; letter-spacing: 0.06em;
  padding: 8px 14px; border-radius: 8px; margin-bottom: 14px;
  display: inline-block;
}}
.col-header.red {{ background: rgba(255,75,40,0.1); color: var(--accent-red); }}
.col-header.green {{ background: rgba(16,185,129,0.1); color: var(--accent-green); }}

/* Pull quote */
.pull-quote {{
  font-size: clamp(16px, 2.5vw, 24px); font-weight: 500;
  color: var(--accent-amber);
  text-align: center;
  line-height: 1.55;
  border-top: 1px solid rgba(255,75,40,0.2);
  border-bottom: 1px solid rgba(255,75,40,0.2);
  padding: 24px 40px; margin: 20px 0;
  background: rgba(255,75,40,0.04);
  border-radius: 0;
}}
.pull-quote::before {{ content: '\\201C'; font-size: 1.4em; opacity: 0.5; margin-right: 4px; }}
.pull-quote::after {{ content: '\\201D'; font-size: 1.4em; opacity: 0.5; margin-left: 4px; }}

/* Stat row */
.stat-row {{
  display: flex; align-items: center; gap: 8px;
  justify-content: center; flex-wrap: wrap;
  margin-top: 16px;
}}
.stat-row-item {{
  font-size: 12px; color: var(--text-muted); padding: 5px 12px;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 20px;
}}
.stat-row-item strong {{ color: var(--text-secondary); font-weight: 600; }}
.stat-row-sep {{ color: var(--text-muted); opacity: 0.4; }}

/* Recommendation lists */
.rec-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden; display: flex; flex-direction: column;
}}
.rec-card-header {{
  padding: 14px 18px;
  font-size: 13px; font-weight: 700;
  letter-spacing: 0.03em;
}}
.rec-card-header.green {{ background: rgba(16,185,129,0.12); color: var(--accent-green); }}
.rec-card-header.red {{ background: rgba(255,75,40,0.12); color: var(--accent-red); }}
.rec-card-header.blue {{ background: rgba(106,173,184,0.12); color: var(--accent-blue); }}
.rec-badge {{
  display: inline-block; padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 600; margin-bottom: 6px;
}}
.rec-badge.green {{ background: rgba(16,185,129,0.15); color: var(--accent-green); }}
.rec-badge.red {{ background: rgba(255,75,40,0.15); color: var(--accent-red); }}
.rec-badge.blue {{ background: rgba(106,173,184,0.15); color: var(--accent-blue); }}
.rec-desc {{ font-size: 11px; color: var(--text-muted); margin-bottom: 10px; }}
.rec-card-body {{ padding: 14px 18px; flex: 1; }}
.rec-list {{ list-style: none; padding: 0; }}
.rec-list li {{
  font-size: 11.5px; padding: 5px 0;
  color: var(--text-secondary);
  border-bottom: 1px solid rgba(52,63,77,0.04);
  display: flex; justify-content: space-between; align-items: center;
}}
.rec-list li:last-child {{ border-bottom: none; }}
.rec-list li .name {{ font-weight: 600; color: var(--text-primary); }}
.rec-list li .stats {{ font-size: 10.5px; color: var(--text-muted); }}
.rec-card-footer {{ padding: 12px 18px; border-top: 1px solid var(--border); }}

/* Action plan */
.priority-badge {{
  display: inline-flex; align-items: center; justify-content: center;
  width: 24px; height: 24px; border-radius: 50%;
  font-size: 11px; font-weight: 700;
  background: rgba(106,173,184,0.15);
  color: var(--accent-blue); flex-shrink: 0;
}}
.action-row {{
  display: grid;
  grid-template-columns: 30px 1fr 100px 80px 1fr 130px;
  gap: 10px; align-items: center;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 12px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  margin-bottom: 6px;
}}
.action-row .bairro-name {{ font-weight: 700; color: var(--text-primary); font-size: 12.5px; }}
.action-row .cat-tag {{
  font-size: 10px; font-weight: 600; letter-spacing: 0.06em;
  padding: 2px 8px; border-radius: 4px;
  text-align: center;
}}
.cat-tag.reativacao {{ background: rgba(255,75,40,0.12); color: var(--accent-red); }}
.cat-tag.manutencao {{ background: rgba(16,185,129,0.12); color: var(--accent-green); }}
.action-row .potencial {{ font-size: 11px; color: var(--text-secondary); }}
.action-row .acao {{ font-size: 11.5px; color: var(--text-primary); }}
.action-row .canal {{ font-size: 10.5px; color: var(--accent-blue); }}
.action-header {{
  display: grid;
  grid-template-columns: 30px 1fr 100px 80px 1fr 130px;
  gap: 10px;
  padding: 6px 14px;
  font-size: 9px; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 4px;
}}

/* Budget bars */
.budget-bar-wrap {{
  display: flex; align-items: stretch;
  border-radius: 10px; overflow: hidden;
  height: 36px; margin-bottom: 22px;
  border: 1px solid var(--border);
}}
.budget-segment {{
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; letter-spacing: 0.04em;
  transition: flex 0.3s;
}}
.budget-segment.amber {{ background: rgba(255,75,40,0.2); color: var(--accent-amber); flex: 50; }}
.budget-segment.green {{ background: rgba(16,185,129,0.15); color: var(--accent-green); flex: 35; border-left: 1px solid var(--border); border-right: 1px solid var(--border); }}
.budget-segment.blue {{ background: rgba(106,173,184,0.12); color: var(--accent-blue); flex: 15; }}

/* Closing */
.slide-closing {{
  display: flex !important; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center;
  background: radial-gradient(ellipse 70% 50% at 50% 50%, rgba(106,173,184,0.08) 0%, transparent 70%);
}}
.closing-title {{
  font-size: clamp(24px, 4vw, 44px); font-weight: 800;
  color: var(--text-primary); margin-bottom: 8px;
  line-height: 1.2;
}}
.closing-subtitle {{
  font-size: clamp(20px, 3vw, 36px); font-weight: 700;
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 36px;
}}
.feature-cards {{ display: flex; gap: 16px; margin-bottom: 32px; justify-content: center; }}
.feature-card {{
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 14px; padding: 22px 20px; max-width: 230px;
  text-align: left;
}}
.feature-card .icon {{ font-size: 26px; margin-bottom: 10px; }}
.feature-card .title {{ font-size: 13px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; }}
.feature-card .desc {{ font-size: 12px; color: var(--text-secondary); line-height: 1.6; }}
.group-info {{ font-size: 11px; color: var(--text-muted); line-height: 1.8; }}
.group-info .course {{ font-size: 10px; color: var(--text-muted); opacity: 0.6; }}

/* Dimensions chips */
.dim-chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}

/* Section header */
.section-head {{
  font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 12px; margin-top: 6px;
}}

/* Scrollable area for charts */
.chart-scroll {{
  flex: 1; overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(52,63,77,0.1) transparent;
}}

/* Two-decision cards */
.decision-card {{
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 18px; margin-bottom: 10px;
}}
.decision-card .dc-title {{
  font-size: 12px; font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 6px;
}}
.decision-card.amber .dc-title {{ color: var(--accent-amber); }}
.decision-card.blue .dc-title {{ color: var(--accent-blue); }}
.decision-card .dc-body {{ font-size: 12px; color: var(--text-secondary); line-height: 1.6; }}

</style>
</head>
<body>

<!-- FIXED UI -->
<div id="top-progress"><div id="top-progress-fill" style="width:4.5%"></div></div>

<div id="chapter-indicator">
  <div class="dot"></div>
  <span class="chapter-text" id="chapter-text"></span>
</div>

<div id="slide-counter">01 / 22</div>

<div id="nav-arrows">
  <button class="nav-btn" id="btn-prev" title="Slide anterior" onclick="retreat()">&#8592;</button>
  <button class="nav-btn" id="btn-next" title="Próximo" onclick="advance()">&#8594;</button>
</div>

<!-- LOADER -->
<div id="exec-loader">
  <div class="exec-loader-inner">
    <div class="jupyter-cell-indicator">
      <span class="cell-bracket">In [</span>
      <span class="cell-star">*</span>
      <span class="cell-bracket">]:</span>
    </div>
    <div class="exec-status" id="loader-status">Executando célula Python...</div>
    <div class="exec-progress-track">
      <div class="exec-progress-fill" id="loader-progress"></div>
    </div>
  </div>
</div>

<!-- PRESENTATION -->
<div id="presentation">

<!-- ========== SLIDE 1: HOOK ========== -->
<div class="slide slide-hook active" data-slide="1" data-steps="0" data-chapter="">
  <div class="hook-num">100.365</div>
  <div class="hook-line-2">registros.</div>
  <div class="hook-line-3">Nenhuma análise.</div>
  <div class="hook-line-4">Nenhuma decisão de marketing baseada em dados.</div>
  <div class="hook-line-5">Até agora.</div>
  <div class="hook-hint">Pressione → para começar</div>
</div>

<!-- ========== SLIDE 2: O CLIENTE ========== -->
<div class="slide" data-slide="2" data-steps="0" data-chapter="01 — O Cliente">
  <div class="slide-title">Company Connection</div>
  <div class="slide-subtitle amber">Sorteios legalizados para influenciadores digitais</div>
  <div class="grid-3" style="flex:1;align-items:start;margin-top:12px;">
    <div class="glass-card">
      <div class="card-icon">🎯</div>
      <div class="card-title">O Produto</div>
      <div class="card-body">Participantes compram títulos de capitalização ou bilhetes lotéricos e concorrem a prêmios. Modelo escalável, digital, focado em influência.</div>
    </div>
    <div class="glass-card">
      <div class="card-icon">📱</div>
      <div class="card-title">O Mercado</div>
      <div class="card-body">Influenciadores digitais como canal de venda. Base de participantes construída via redes sociais e marketing de influência.</div>
    </div>
    <div class="glass-card">
      <div class="card-icon">📊</div>
      <div class="card-title">O Desafio</div>
      <div class="card-body">Empresa fundada em 2024. Crescimento rápido, mas sem inteligência de dados. Decisões tomadas no feeling.</div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 3: O PROBLEMA ========== -->
<div class="slide" data-slide="3" data-steps="0" data-chapter="01 — O Cliente">
  <div class="slide-title">Decisão no Feeling</div>
  <div class="pull-quote">Eles copiavam o que outros influenciadores faziam — sem olhar o próprio público.</div>
  <div class="col-2" style="margin-top:10px;">
    <div class="contrast-box red-tint">
      <div class="contrast-box-title">Antes</div>
      <ul><li>Orçamento de mídia distribuído igualmente</li><li>Sem saber onde os clientes estão</li><li>Sem saber quem ainda compra</li></ul>
    </div>
    <div class="contrast-box green-tint">
      <div class="contrast-box-title">O que análise de dados muda</div>
      <ul><li>Direcionar orçamento por bairro</li><li>Identificar onde reativar</li><li>Identificar onde expandir</li></ul>
    </div>
  </div>
  <div class="stat-row" style="margin-top:20px;">
    <div class="stat-row-item"><strong>100.365 registros</strong></div>
    <span class="stat-row-sep">·</span>
    <div class="stat-row-item">nunca analisados</div>
    <span class="stat-row-sep">·</span>
    <div class="stat-row-item">disponíveis desde 2024</div>
  </div>
</div>

<!-- ========== SLIDE 4: A BASE DE DADOS ========== -->
<div class="slide" data-slide="4" data-steps="1" data-chapter="02 — Os Dados">
  <div class="slide-title">O Que Esperávamos vs. O Que Encontramos</div>
  <div class="col-2" style="margin-top:16px;">
    <div>
      <div class="col-header red">❌ O que a proposta assumia</div>
      <ul class="strike-list">
        <li>Faixa etária</li><li>Número de telefone</li><li>CPF</li><li>E-mail</li>
        <li>Histórico completo de compras</li><li>Distribuição nacional</li>
      </ul>
    </div>
    <div>
      <div class="col-header green">✅ O que realmente tínhamos</div>
      <ul class="clean-list">
        <li><code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent-cyan);">bairro</code></li>
        <li><code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent-cyan);">cidade</code></li>
        <li><code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent-cyan);">uf</code></li>
        <li><code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent-cyan);">cep</code></li>
        <li><code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent-cyan);">ultima_compra</code></li>
      </ul>
    </div>
  </div>
  <div class="step step-1" style="margin-top:22px;">
    <div class="callout">"Com apenas 5 colunas — todas geográficas ou temporais — construímos uma análise completa de segmentação. Limitação virou foco."</div>
  </div>
</div>

<!-- ========== SLIDE 5: O ACHADO ========== -->
<div class="slide" data-slide="5" data-steps="1" data-chapter="02 — Os Dados">
  <div class="slide-title">99,7% dos Participantes</div>
  <div class="slide-subtitle blue">estão no Rio de Janeiro</div>
  <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;">
    <div class="big-pct">99.7%</div>
    <div class="stat-row">
      <div class="stat-row-item"><strong>82.875 registros</strong></div>
      <span class="stat-row-sep">·</span>
      <div class="stat-row-item">no RJ</div>
      <span class="stat-row-sep">·</span>
      <div class="stat-row-item">contra apenas ~200 no resto do Brasil</div>
    </div>
    <div class="step step-1" style="width:100%;max-width:680px;">
      <div class="callout">"Essa descoberta mudou tudo. Em vez de uma análise nacional rasa, fizemos uma análise profunda do mercado fluminense — bairro por bairro."</div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 6: O PIPELINE ========== -->
<div class="slide" data-slide="6" data-steps="0" data-chapter="03 — A Solução">
  <div class="slide-title">O Pipeline de Análise</div>
  <div class="slide-subtitle">10 blocos, do dado bruto à decisão</div>
  <div class="pipeline-wrap" style="flex:1;justify-content:center;">
    <div>
      <div class="pipeline-group-label" style="color:var(--accent-blue);">Fundação</div>
      <div class="pipeline-row">
        <div class="pipeline-node blue"><span class="node-num">0</span><span class="node-label">Parâmetros</span></div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node blue"><span class="node-num">1</span><span class="node-label">Carga</span></div>
        <div class="pipeline-arrow" style="margin-left:12px;color:var(--accent-purple);">⟹</div>
      </div>
    </div>
    <div>
      <div class="pipeline-group-label" style="color:var(--accent-purple);">Preparação</div>
      <div class="pipeline-row">
        <div class="pipeline-node purple"><span class="node-num">2</span><span class="node-label">Limpeza</span></div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node purple"><span class="node-num">3</span><span class="node-label">Engenharia</span></div>
        <div class="pipeline-arrow" style="margin-left:12px;color:var(--accent-cyan);">⟹</div>
      </div>
    </div>
    <div>
      <div class="pipeline-group-label" style="color:var(--accent-cyan);">Exploração</div>
      <div class="pipeline-row">
        <div class="pipeline-node teal"><span class="node-num">4</span><span class="node-label">EDA</span></div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node teal"><span class="node-num">5</span><span class="node-label">Heatmaps</span></div>
        <div class="pipeline-arrow" style="margin-left:12px;color:var(--accent-amber);">⟹</div>
      </div>
    </div>
    <div>
      <div class="pipeline-group-label" style="color:var(--accent-amber);">Modelos</div>
      <div class="pipeline-row">
        <div class="pipeline-node amber"><span class="node-num">6</span><span class="node-label">K-Means</span></div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node amber"><span class="node-num">7</span><span class="node-label">Árvore</span></div>
        <div class="pipeline-arrow" style="margin-left:12px;color:var(--accent-green);">⟹</div>
      </div>
    </div>
    <div>
      <div class="pipeline-group-label" style="color:var(--accent-green);">Entrega</div>
      <div class="pipeline-row">
        <div class="pipeline-node green"><span class="node-num">8</span><span class="node-label">Recomendações</span></div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node green"><span class="node-num">9</span><span class="node-label">Plano</span></div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node green"><span class="node-num">10</span><span class="node-label">Export</span></div>
      </div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 7: BLOCO 1 CARREGAMENTO ========== -->
<div class="slide" data-slide="7" data-steps="2" data-chapter="03 — A Solução" data-step-types="code,output">
  <div class="slide-title">Bloco 1 — Carregamento dos Dados</div>
  <div class="context-text">"Lemos o CSV e fazemos a primeira inspeção. O objetivo é entender a escala e o estado bruto da base antes de qualquer transformação."</div>
  <div class="chart-scroll">
    <div class="step step-1">
      <div class="jupyter-cell">
        <div class="jupyter-cell-header">
          <span class="jupyter-in-label">In [1]:</span>
          <span style="font-size:10px;color:var(--text-muted);margin-left:auto;">bloco_01_carga.py</span>
        </div>
        <pre><code class="language-python">df = pd.read_csv(CAMINHO_CSV)

print('Total de linhas:', len(df))
print('Total de colunas:', df.shape[1])
print('Colunas:', list(df.columns))</code></pre>
      </div>
    </div>
    <div class="step step-2">
      <div class="terminal-output">
        <div class="out-label">Out [1]:</div>
Total de linhas: 100365
Total de colunas: 5
Colunas: ['bairro', 'cidade', 'uf', 'cep', 'ultima_compra']
      </div>
      <table class="data-table" style="margin-top:8px;">
        <thead><tr><th>bairro</th><th>cidade</th><th>uf</th><th>cep</th><th>ultima_compra</th></tr></thead>
        <tbody>
          <tr><td>Largo da Batalha</td><td>Niterói</td><td>RJ</td><td>24310460</td><td>2024-08-24</td></tr>
          <tr><td>Mutondo</td><td><em style="color:var(--text-muted)">NaN</em></td><td><em style="color:var(--text-muted)">NaN</em></td><td>24450660</td><td>2024-08-31</td></tr>
          <tr><td>Fonseca</td><td>Niterói</td><td>RJ</td><td>24130390</td><td>2022-12-03</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<!-- ========== SLIDE 8: BLOCO 2 LIMPEZA ========== -->
<div class="slide" data-slide="8" data-steps="2" data-chapter="03 — A Solução" data-step-types="code,output">
  <div class="slide-title">Bloco 2 — Limpeza e Padronização</div>
  <div class="context-text">"Dados reais vêm sujos. 'Rio de Janeiro' e 'RIO DE JANEIRO' são a mesma cidade — mas para um modelo são duas. Precisamos corrigir isso antes de qualquer análise."</div>
  <div class="chart-scroll">
    <div class="step step-1">
      <div class="jupyter-cell">
        <div class="jupyter-cell-header">
          <span class="jupyter-in-label">In [2]:</span>
          <span style="font-size:10px;color:var(--text-muted);margin-left:auto;">bloco_02_limpeza.py</span>
        </div>
        <pre><code class="language-python"># Padronização: caixa alta + sem espaços extras
df['cidade'] = df['cidade'].str.upper().str.strip()
df['bairro'] = df['bairro'].str.upper().str.strip()

# Remove acentos (NITERÓI → NITEROI)
df['cidade'] = df['cidade'].str.normalize('NFKD') \\
    .str.encode('ascii', errors='ignore').str.decode('utf-8')

# Marca UFs inválidas como nulo
ufs_validas = ['AC','AL','AP','AM','BA','CE','DF','ES','GO',
               'MA','MT','MS','MG','PA','PB','PR','PE','PI',
               'RJ','RN','RS','RO','RR','SC','SP','SE','TO']
df.loc[~df['uf'].isin(ufs_validas), 'uf'] = None

# Converte data de texto para datetime
df['ultima_compra'] = pd.to_datetime(df['ultima_compra'])</code></pre>
      </div>
    </div>
    <div class="step step-2">
      <div class="terminal-output">
        <div class="out-label">Out [2]:</div>
UFs encontradas após a limpeza:
RJ    82875
SP       47
MG       16
DF       15
...

Data mais antiga:  2022-12-03
Data mais recente: 2025-07-06
      </div>
      <div class="callout" style="margin-top:10px;">"Após limpeza: 99,7% dos registros válidos pertencem ao RJ."</div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 9: BLOCO 3 ENGENHARIA ========== -->
<div class="slide" data-slide="9" data-steps="2" data-chapter="03 — A Solução" data-step-types="code,output">
  <div class="slide-title">Bloco 3 — Engenharia de Variáveis</div>
  <div class="context-text">"A base original não tem 'comportamento' — só datas. Transformamos datas em inteligência: criamos recência, status e CEP-3."</div>
  <div class="chart-scroll">
    <div class="step step-1">
      <div class="jupyter-cell">
        <div class="jupyter-cell-header">
          <span class="jupyter-in-label">In [3]:</span>
          <span style="font-size:10px;color:var(--text-muted);margin-left:auto;">bloco_03_engenharia.py</span>
        </div>
        <pre><code class="language-python"># Recência: dias desde a última compra
data_corte = df['ultima_compra'].max()
df['recencia_dias'] = (data_corte - df['ultima_compra']).dt.days

# Status: RECENTE (≤ 365 dias) ou ANTIGO
df['status_recente'] = 'ANTIGO'
df.loc[df['recencia_dias'] &lt;= 365, 'status_recente'] = 'RECENTE'

# CEP-3: sub-região postal (primeiros 3 dígitos)
df['cep3'] = df['cep'].astype(str).str[:3]</code></pre>
      </div>
    </div>
    <div class="step step-2">
      <div class="grid-3" style="margin-top:8px;">
        <div class="stat-card blue">
          <div class="stat-label">Recência média</div>
          <div class="stat-value">479 dias</div>
          <div class="stat-sub">Mediana: 470 dias</div>
        </div>
        <div class="stat-card red">
          <div class="stat-label">Clientes ANTIGOS</div>
          <div class="stat-value">64.355</div>
          <div class="stat-sub">77,7% da base</div>
        </div>
        <div class="stat-card green">
          <div class="stat-label">Clientes RECENTES</div>
          <div class="stat-value">18.520</div>
          <div class="stat-sub">22,3% da base</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 10: EDA ONDE ESTÃO ========== -->
<div class="slide" data-slide="10" data-steps="2" data-chapter="04 — O Que Descobrimos" data-step-types="chart,chart">
  <div class="slide-title" style="font-size:30px;">A Zona Oeste Domina</div>
  <div class="context-text">"Campo Grande, Santa Cruz, Bangu. Os 'grandes celeiros' da Company Connection estão na Zona Oeste do Rio — não na Zona Sul como muitos imaginariam."</div>
  <div class="chart-scroll" style="flex:1;">
    <div class="step step-1">
      <img class="chart-img" src="data:image/png;base64,{b64['cidades']}" alt="Top 15 cidades">
    </div>
    <div class="step step-2" style="margin-top:14px;">
      <img class="chart-img" src="data:image/png;base64,{b64['bairros']}" alt="Top 20 bairros">
    </div>
  </div>
</div>

<!-- ========== SLIDE 11: EDA QUANDO COMPRARAM ========== -->
<div class="slide" data-slide="11" data-steps="1" data-chapter="04 — O Que Descobrimos" data-step-types="chart">
  <div class="slide-title" style="font-size:30px;">O Produto Cresceu em 2024 — e Parou</div>
  <div class="context-text">"O Cap Mania teve seu auge em meados de 2024 e foi descontinuado. O gráfico conta a história: crescimento, pico, e depois silêncio. Isso explica por que 77% da base está 'dormente'."</div>
  <div class="chart-scroll" style="flex:1;">
    <div class="step step-1">
      <img class="chart-img full" src="data:image/png;base64,{b64['temporal']}" alt="Evolução temporal">
      <div class="callout" style="margin-top:12px;">"O pico de atividade coincide com lançamentos de sorteios em 2024. A base existe — só precisa ser reativada."</div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 12: EDA QUEM AINDA COMPRA ========== -->
<div class="slide" data-slide="12" data-steps="2" data-chapter="04 — O Que Descobrimos" data-step-types="chart,output">
  <div class="slide-title" style="font-size:30px;">77% Dormentes. 23% Ativos.</div>
  <div class="context-text">"Definimos como 'recente' qualquer compra nos últimos 365 dias. A distribuição é clara: a maioria da base não compra há mais de um ano — mas ainda existe e pode ser reativada."</div>
  <div class="chart-scroll" style="flex:1;">
    <div class="step step-1">
      <div class="grid-2">
        <img class="chart-img" src="data:image/png;base64,{b64['pizza']}" alt="Distribuição RECENTE vs ANTIGO">
        <img class="chart-img" src="data:image/png;base64,{b64['histograma']}" alt="Histograma de recência">
      </div>
    </div>
    <div class="step step-2">
      <div class="callout" style="margin-top:14px;">"A linha vermelha no histograma marca o corte de 365 dias. A maioria está muito além dela — candidatos à reativação."</div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 13: HEATMAPS ========== -->
<div class="slide" data-slide="13" data-steps="3" data-chapter="04 — O Que Descobrimos" data-step-types="chart,chart,chart">
  <div class="slide-title" style="font-size:30px;">Onde Estão os Ativos — Bairro por Bairro</div>
  <div class="context-text">"O heatmap cruza bairro com status. Calor intenso = muitos clientes naquela combinação. Bairros com calor em ANTIGO são candidatos à reativação."</div>
  <div class="chart-scroll" style="flex:1;">
    <div class="step step-1" style="margin-bottom:14px;">
      <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:6px;">5.1 — Top regiões postais (CEP-3)</div>
      <img class="chart-img" src="data:image/png;base64,{b64['cep3']}" alt="Top CEP-3">
    </div>
    <div class="grid-2">
      <div class="step step-2">
        <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:6px;">5.2 — Heatmap bairros × status</div>
        <img class="chart-img" src="data:image/png;base64,{b64['heatmap_bairros']}" alt="Heatmap bairros × status">
      </div>
      <div class="step step-3">
        <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:6px;">5.3 — Heatmap CEP-3 × status</div>
        <img class="chart-img" src="data:image/png;base64,{b64['heatmap_cep3']}" alt="Heatmap CEP-3 × status">
      </div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 14: K-MEANS A PERGUNTA ========== -->
<div class="slide" data-slide="14" data-steps="0" data-chapter="05 — Os Modelos">
  <div class="slide-title">Modelo 1: K-Means</div>
  <div class="slide-subtitle blue">"Que tipos de bairros existem nesta base?"</div>
  <div class="col-2" style="flex:1;align-items:start;margin-top:10px;">
    <div class="glass-card">
      <div class="card-title" style="margin-bottom:12px;">O Algoritmo</div>
      <div class="card-body">"K-Means é um algoritmo não supervisionado. Ele não precisa de 'respostas certas' — descobre padrões sozinho. Pedimos para ele agrupar os 323 bairros do RJ em grupos similares, com base em três dimensões:"</div>
      <div class="dim-chips" style="margin-top:14px;">
        <span class="chip blue">📊 Volume <small style="margin-left:4px;opacity:.7;">total de participantes</small></span>
        <span class="chip amber">📅 Recência mediana <small style="margin-left:4px;opacity:.7;">tempo médio sem comprar</small></span>
        <span class="chip green">✅ % Recentes <small style="margin-left:4px;opacity:.7;">proporção de clientes ativos</small></span>
      </div>
    </div>
    <div class="glass-card">
      <div class="card-title" style="margin-bottom:12px;">Por que no nível bairro?</div>
      <div class="card-body" style="margin-bottom:14px;">"Individualmente, quase todo cliente está 'antigo' — o produto foi descontinuado. Mas alguns bairros se mantiveram mais ativos que outros. Marketing toma decisões geográficas, não pessoa por pessoa."</div>
      <div class="callout blue" style="margin-top:0;font-style:normal;font-size:12px;">Nível de análise: <strong style="color:var(--accent-blue)">bairro</strong> (não pessoa), com métricas agregadas por bairro como features para o modelo.</div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 15: K-MEANS COTOVELO ========== -->
<div class="slide" data-slide="15" data-steps="1" data-chapter="05 — Os Modelos" data-step-types="chart">
  <div class="slide-title">O Método do Cotovelo</div>
  <div class="context-text">"Testamos K de 2 a 10. Plotamos a inertia — quanto menor, mais compactos os grupos. O 'cotovelo' da curva indica onde adicionar mais grupos para de melhorar: K = 4."</div>
  <div class="chart-scroll" style="flex:1;">
    <div class="step step-1">
      <img class="chart-img full" src="data:image/png;base64,{b64['cotovelo']}" alt="Método do cotovelo K-Means">
      <div class="callout" style="margin-top:12px;">"K = 4 é o ponto onde a curva 'vira'. Além disso, 4 grupos é um número prático para o marketing acionar — não é pouco, não é demais."</div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 16: K-MEANS 4 TIERS ========== -->
<div class="slide" data-slide="16" data-steps="2" data-chapter="05 — Os Modelos" data-step-types="chart,chart">
  <div class="slide-title">Quatro Perfis de Bairro</div>
  <table class="data-table" style="margin-bottom:14px;">
    <thead><tr><th>Cluster</th><th>Nome</th><th>Bairros</th><th>Volume médio</th><th>% Recentes</th></tr></thead>
    <tbody>
      <tr class="row-amber"><td><strong>3</strong></td><td>🏆 Núcleo Estratégico</td><td>6</td><td>1.641</td><td>26,1%</td></tr>
      <tr class="row-green"><td><strong>2</strong></td><td>💚 Engajado</td><td>69</td><td>98</td><td>29,4%</td></tr>
      <tr class="row-blue"><td><strong>0</strong></td><td>📊 Massa Padrão</td><td>162</td><td>181</td><td>25,8%</td></tr>
      <tr class="row-red"><td><strong>1</strong></td><td>📉 Em Declínio</td><td>86</td><td>102</td><td>19,6%</td></tr>
    </tbody>
  </table>
  <div class="chart-scroll" style="flex:1;">
    <div class="grid-2">
      <div class="step step-1">
        <img class="chart-img" src="data:image/png;base64,{b64['scatter1']}" alt="Volume × % Recentes">
      </div>
      <div class="step step-2">
        <img class="chart-img" src="data:image/png;base64,{b64['scatter2']}" alt="Recência × % Recentes">
      </div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 17: ÁRVORE A PERGUNTA ========== -->
<div class="slide" data-slide="17" data-steps="0" data-chapter="05 — Os Modelos">
  <div class="slide-title">Modelo 2: Árvore de Decisão</div>
  <div class="slide-subtitle purple">"O que a localização revela sobre o comportamento de compra?"</div>
  <div class="col-2" style="flex:1;align-items:start;margin-top:10px;">
    <div class="glass-card">
      <div class="card-title" style="margin-bottom:12px;">O Algoritmo</div>
      <div class="card-body" style="margin-bottom:14px;">"A árvore de decisão é supervisionada — aprende com exemplos rotulados (RECENTE ou ANTIGO) e descobre as regras que melhor separam as duas classes, usando apenas variáveis geográficas."</div>
      <div class="section-head">Features utilizadas</div>
      <div class="dim-chips">
        <span class="chip muted">🏘️ Bairro</span>
        <span class="chip muted">🏙️ Cidade</span>
        <span class="chip muted">📮 CEP-3</span>
      </div>
      <div class="section-head" style="margin-top:14px;">Target</div>
      <span class="chip purple">🎯 RECENTE ou ANTIGO</span>
    </div>
    <div>
      <div class="decision-card amber">
        <div class="dc-title">class_weight='balanced'</div>
        <div class="dc-body">"Base: 75% ANTIGO / 25% RECENTE. Sem ajuste, a árvore aprenderia a sempre prever ANTIGO e ficaria 'certa' 75% do tempo — mas inútil. O balanceamento força o modelo a aprender a distinguir de verdade."</div>
      </div>
      <div class="decision-card blue">
        <div class="dc-title">max_depth=5</div>
        <div class="dc-body">"Uma árvore sem limite decora os dados (overfitting). Com profundidade 5, ela generaliza — e ainda é possível visualizar e explicar ao marketing."</div>
      </div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 18: ÁRVORE VISUALIZAÇÃO ========== -->
<div class="slide" data-slide="18" data-steps="1" data-chapter="05 — Os Modelos" data-step-types="chart">
  <div class="slide-title">A Estrutura da Árvore</div>
  <div class="context-text">"Cada nó é uma pergunta. Cada folha é uma conclusão: RECENTE ou ANTIGO. O algoritmo escolheu essas perguntas automaticamente — as que melhor separam as classes."</div>
  <div class="chart-scroll" style="flex:1;">
    <div class="step step-1">
      <img class="chart-img tall" src="data:image/png;base64,{b64['arvore']}" alt="Árvore de Decisão" style="max-height:58vh;">
    </div>
  </div>
</div>

<!-- ========== SLIDE 19: ÁRVORE O ACHADO ========== -->
<div class="slide" data-slide="19" data-steps="1" data-chapter="05 — Os Modelos" data-step-types="chart">
  <div class="slide-title">O Bairro é o Que Mais Importa</div>
  <div class="context-text">"A árvore calcula automaticamente quanto cada variável contribuiu para as separações. O resultado confirma a intuição do projeto: bairro contém mais informação preditiva do que cidade ou CEP."</div>
  <div class="chart-scroll" style="flex:1;">
    <div class="step step-1">
      <img class="chart-img" src="data:image/png;base64,{b64['importancia']}" alt="Importância das variáveis">
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px;align-items:center;">
        <span class="chip amber" style="font-size:13px;padding:7px 16px;">Bairro → variável mais preditiva</span>
        <span class="chip muted">CEP-3 → segundo lugar</span>
        <span class="chip muted">Cidade → menor contribuição</span>
      </div>
      <div class="callout blue" style="margin-top:14px;">"Conclusão de negócio: campanhas devem ser segmentadas no nível bairro — nem cidade (genérico demais), nem rua (específico demais)."</div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 20: AS TRÊS LISTAS ========== -->
<div class="slide" data-slide="20" data-steps="0" data-chapter="06 — As Recomendações">
  <div class="slide-title">Bairros Priorizados</div>
  <div class="slide-subtitle">Três perfis, três estratégias</div>
  <div class="grid-3" style="flex:1;align-items:start;overflow-y:auto;">
    <div class="rec-card">
      <div class="rec-card-header green">⭐ Estrela — Manter</div>
      <div class="rec-card-body">
        <div class="rec-badge green">2.808 clientes ativos</div>
        <div class="rec-desc">Alto volume + alto % recentes</div>
        <ul class="rec-list">
          <li><span class="name">Campo Grande</span><span class="stats">2.274 part. / 26,1% rec.</span></li>
          <li><span class="name">Santa Cruz</span><span class="stats">1.785 / 26,9%</span></li>
          <li><span class="name">Bangu</span><span class="stats">1.584 / 26,8%</span></li>
          <li><span class="name">Realengo</span><span class="stats">1.171 / 27,7%</span></li>
          <li><span class="name">Paciência</span><span class="stats">796 / 29,4%</span></li>
        </ul>
      </div>
      <div class="rec-card-footer"><span class="chip green" style="font-size:11px;">Google Ads + Instagram</span></div>
    </div>
    <div class="rec-card">
      <div class="rec-card-header red">🔴 Em Risco — Reativar</div>
      <div class="rec-card-body">
        <div class="rec-badge red">5.435 dormentes</div>
        <div class="rec-desc">Alto volume + baixo % recentes</div>
        <ul class="rec-list">
          <li><span class="name">Centro</span><span class="stats">2.009 part. / 24,9% rec.</span></li>
          <li><span class="name">Guaratiba</span><span class="stats">1.028 / 23,9%</span></li>
          <li><span class="name">Taquara</span><span class="stats">712 / 23,0%</span></li>
          <li><span class="name">Inhoaíba</span><span class="stats">621 / 24,0%</span></li>
          <li><span class="name">Ramos</span><span class="stats">619 / 24,7%</span></li>
        </ul>
      </div>
      <div class="rec-card-footer"><span class="chip red" style="font-size:11px;">Meta Ads geo + WhatsApp</span></div>
    </div>
    <div class="rec-card">
      <div class="rec-card-header blue">🚀 Emergente — Expandir</div>
      <div class="rec-card-body">
        <div class="rec-badge blue">682 participantes</div>
        <div class="rec-desc">Baixo volume + alto % recentes</div>
        <ul class="rec-list">
          <li><span class="name">Encantado</span><span class="stats">62 part. / 40,3% rec.</span></li>
          <li><span class="name">Jd. José Bonifácio</span><span class="stats">64 / 39,1%</span></li>
          <li><span class="name">Quitandinha</span><span class="stats">50 / 38,0%</span></li>
          <li><span class="name">Aracatiba</span><span class="stats">86 / 37,2%</span></li>
          <li><span class="name">Vila Itamarati</span><span class="stats">82 / 36,6%</span></li>
        </ul>
      </div>
      <div class="rec-card-footer"><span class="chip blue" style="font-size:11px;">Meta Ads teste A/B</span></div>
    </div>
  </div>
</div>

<!-- ========== SLIDE 21: PLANO DE AÇÃO ========== -->
<div class="slide" data-slide="21" data-steps="0" data-chapter="06 — As Recomendações">
  <div class="slide-title">Plano de Ação</div>
  <div class="slide-subtitle">Executável na segunda-feira de manhã</div>
  <div class="budget-bar-wrap">
    <div class="budget-segment amber">50% Reativação</div>
    <div class="budget-segment green">35% Manutenção</div>
    <div class="budget-segment blue">15% Expansão</div>
  </div>
  <div class="action-header">
    <div>#</div><div>Bairro</div><div>Categoria</div><div>Potencial</div><div>Ação</div><div>Canal</div>
  </div>
  <div class="action-row">
    <div class="priority-badge">1</div>
    <div class="bairro-name">CENTRO</div>
    <div><span class="cat-tag reativacao">REATIVAÇÃO</span></div>
    <div class="potencial">1.509 clientes</div>
    <div class="acao">Oferta especial</div>
    <div class="canal">Meta Ads geo + WhatsApp</div>
  </div>
  <div class="action-row">
    <div class="priority-badge">2</div>
    <div class="bairro-name">GUARATIBA</div>
    <div><span class="cat-tag reativacao">REATIVAÇÃO</span></div>
    <div class="potencial">782 clientes</div>
    <div class="acao">Oferta especial</div>
    <div class="canal">Meta Ads geo + WhatsApp</div>
  </div>
  <div class="action-row">
    <div class="priority-badge">3</div>
    <div class="bairro-name">CAMPO GRANDE</div>
    <div><span class="cat-tag manutencao">MANUTENÇÃO</span></div>
    <div class="potencial">594 clientes</div>
    <div class="acao">Novos sorteios</div>
    <div class="canal">Google Ads + Instagram</div>
  </div>
  <div class="action-row">
    <div class="priority-badge">4</div>
    <div class="bairro-name">TAQUARA</div>
    <div><span class="cat-tag reativacao">REATIVAÇÃO</span></div>
    <div class="potencial">548 clientes</div>
    <div class="acao">Oferta especial</div>
    <div class="canal">Meta Ads geo + WhatsApp</div>
  </div>
  <div class="action-row">
    <div class="priority-badge">5</div>
    <div class="bairro-name">SANTA CRUZ</div>
    <div><span class="cat-tag manutencao">MANUTENÇÃO</span></div>
    <div class="potencial">480 clientes</div>
    <div class="acao">Novos sorteios</div>
    <div class="canal">Google Ads + Instagram</div>
  </div>
  <div class="callout" style="margin-top:14px;font-size:12px;">"KPI principal: 5% de taxa de reativação em 90 dias = ~272 clientes recuperados nos 10 bairros em risco"</div>
</div>

<!-- ========== SLIDE 22: ENCERRAMENTO ========== -->
<div class="slide slide-closing" data-slide="22" data-steps="0" data-chapter="">
  <div class="closing-title">Não entregamos uma análise.</div>
  <div class="closing-subtitle">Entregamos uma ferramenta.</div>
  <div class="feature-cards">
    <div class="feature-card">
      <div class="icon">🔄</div>
      <div class="title">Reutilizável</div>
      <div class="desc">Troque o CSV. Ajuste o Bloco 0. Rode. Em 5 minutos, novas listas priorizadas para qualquer produto futuro.</div>
    </div>
    <div class="feature-card">
      <div class="icon">📁</div>
      <div class="title">5 arquivos CSV</div>
      <div class="desc">tiers_por_bairro.csv · bairros_estrela.csv · bairros_risco.csv · bairros_emergentes.csv · plano_de_acao.csv</div>
    </div>
    <div class="feature-card">
      <div class="icon">🎯</div>
      <div class="title">Zero fricção</div>
      <div class="desc">O time de marketing usa o plano_de_acao.csv sem abrir o Python. Decisão baseada em dados, sem precisar de analista.</div>
    </div>
  </div>
  <div class="group-info">
    <div>Grupo 5 — Gabriel Maino · Gabriela Cohen · Hyan Lucas · Isabelle Cavalcante · João Bittencourt · Malena Catallini</div>
    <div class="course">Projeto Aplicado — IBM3297 — IBMEC RJ — 2026.1</div>
  </div>
</div>

</div><!-- /presentation -->

<script>
(function() {{
  'use strict';

  const TOTAL_SLIDES = 22;
  let currentSlide = 1;
  let currentStep = 0;
  let isAnimating = false;

  // Step type → loader status message
  const STATUS_MESSAGES = {{
    'code':   'Executando célula Python...',
    'output': 'Processando output...',
    'chart':  'Renderizando visualização...',
  }};

  function getSlideEl(n) {{
    return document.querySelector(`.slide[data-slide="${{n}}"]`);
  }}

  function getMaxSteps(n) {{
    const el = getSlideEl(n);
    return el ? parseInt(el.dataset.steps || '0') : 0;
  }}

  function getStepType(slideN, stepN) {{
    const el = getSlideEl(slideN);
    if (!el) return 'output';
    const types = (el.dataset.stepTypes || '').split(',');
    return types[stepN - 1] || 'output';
  }}

  function updateUI() {{
    // Progress bar
    const pct = (currentSlide / TOTAL_SLIDES) * 100;
    document.getElementById('top-progress-fill').style.width = pct + '%';

    // Slide counter
    const sc = document.getElementById('slide-counter');
    const pad = n => String(n).padStart(2, '0');
    sc.textContent = pad(currentSlide) + ' / ' + pad(TOTAL_SLIDES);

    // Chapter
    const el = getSlideEl(currentSlide);
    const chap = el ? (el.dataset.chapter || '') : '';
    const ct = document.getElementById('chapter-text');
    const ci = document.getElementById('chapter-indicator');
    if (chap) {{
      ct.textContent = chap;
      ci.style.opacity = '1';
    }} else {{
      ci.style.opacity = '0';
    }}
  }}

  function revealStep(stepN) {{
    const el = getSlideEl(currentSlide);
    if (!el) return;
    const stepEl = el.querySelector(`.step-${{stepN}}`);
    if (stepEl) {{
      stepEl.classList.add('revealed');
    }}
  }}

  function showLoader(stepType, callback) {{
    const loader = document.getElementById('exec-loader');
    const statusEl = document.getElementById('loader-status');
    const progressEl = document.getElementById('loader-progress');

    statusEl.textContent = STATUS_MESSAGES[stepType] || STATUS_MESSAGES['output'];
    progressEl.style.transition = 'none';
    progressEl.style.width = '0%';

    loader.classList.add('visible');

    // Trigger reflow then animate
    requestAnimationFrame(() => {{
      requestAnimationFrame(() => {{
        progressEl.classList.add('animating');
        progressEl.style.width = '100%';
      }});
    }});

    setTimeout(() => {{
      loader.classList.remove('visible');
      progressEl.classList.remove('animating');
      progressEl.style.transition = 'none';
      progressEl.style.width = '0%';
      callback();
    }}, 1400);
  }}

  function goToSlide(n) {{
    if (n < 1 || n > TOTAL_SLIDES || isAnimating) return;
    isAnimating = true;

    const fromEl = getSlideEl(currentSlide);
    const toEl = getSlideEl(n);
    if (!toEl) {{ isAnimating = false; return; }}

    const direction = n > currentSlide ? 1 : -1;

    // Set initial position for incoming slide
    toEl.style.transition = 'none';
    toEl.style.transform = direction > 0 ? 'translateX(100%)' : 'translateX(-100%)';
    toEl.style.opacity = '0';
    toEl.style.pointerEvents = 'none';

    // Make incoming slide visible but positioned off-screen
    requestAnimationFrame(() => {{
      requestAnimationFrame(() => {{
        if (fromEl) {{
          fromEl.style.transition = 'transform 0.5s cubic-bezier(.4,0,.2,1), opacity 0.5s ease';
          fromEl.style.transform = direction > 0 ? 'translateX(-100%)' : 'translateX(100%)';
          fromEl.style.opacity = '0';
          fromEl.classList.remove('active');
        }}

        toEl.style.transition = 'transform 0.5s cubic-bezier(.4,0,.2,1), opacity 0.5s ease';
        toEl.style.transform = 'translateX(0)';
        toEl.style.opacity = '1';
        toEl.style.pointerEvents = 'all';
        toEl.classList.add('active');

        setTimeout(() => {{
          if (fromEl) {{
            fromEl.style.transition = '';
            fromEl.style.transform = '';
            fromEl.style.opacity = '';
            fromEl.style.pointerEvents = '';
          }}
          currentSlide = n;
          currentStep = 0;
          isAnimating = false;
          updateUI();
        }}, 520);
      }});
    }});
  }}

  function advance() {{
    if (isAnimating) return;
    const maxSteps = getMaxSteps(currentSlide);

    if (currentStep < maxSteps) {{
      const nextStep = currentStep + 1;
      const stepType = getStepType(currentSlide, nextStep);
      isAnimating = true;
      showLoader(stepType, () => {{
        currentStep = nextStep;
        revealStep(currentStep);
        isAnimating = false;
      }});
    }} else {{
      if (currentSlide < TOTAL_SLIDES) {{
        goToSlide(currentSlide + 1);
      }}
    }}
  }}

  function retreat() {{
    if (isAnimating) return;
    if (currentSlide > 1) {{
      goToSlide(currentSlide - 1);
    }}
  }}

  // Keyboard
  document.addEventListener('keydown', (e) => {{
    if (e.key === 'ArrowRight' || e.key === ' ') {{
      e.preventDefault();
      advance();
    }} else if (e.key === 'ArrowLeft') {{
      e.preventDefault();
      retreat();
    }}
  }});

  // Expose to onclick handlers
  window.advance = advance;
  window.retreat = retreat;

  // Init
  updateUI();

  // Syntax highlighting
  document.addEventListener('DOMContentLoaded', () => {{
    if (window.hljs) hljs.highlightAll();
  }});
  if (document.readyState !== 'loading') {{
    if (window.hljs) hljs.highlightAll();
  }}
}})();
</script>
</body>
</html>"""

out_path = '/home/user/PAD/apresentacao.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(out_path) // 1024
print(f"Done. File: {out_path}")
print(f"Size: {size_kb} KB ({size_kb/1024:.1f} MB)")

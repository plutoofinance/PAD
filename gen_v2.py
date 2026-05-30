#!/usr/bin/env python3
"""gen_v2.py — Gera apresentacao.html v2 com 35 slides."""
import pickle, re, sys

with open('/tmp/imgs.pkl', 'rb') as f:
    imgs = pickle.load(f)

def img(key, style="max-width:100%;max-height:48vh;object-fit:contain;border-radius:8px;border:1px solid #e8eaed;"):
    return f'<img src="data:image/png;base64,{imgs[key]}" style="{style}">'

with open('/home/user/PAD/.claude/worktrees/agent-a41e08b8b7f2f33fc/apresentacao.html', 'r', encoding='utf-8') as f:
    old = f.read()

head_match = re.search(r'(<!DOCTYPE.*?</style>\s*</head>)', old, re.DOTALL)
HEAD = head_match.group(1)

ui_match = re.search(r'(<!-- FIXED UI -->.*?<!-- PRESENTATION -->)', old, re.DOTALL)
FIXED_UI = ui_match.group(1)

js_match = re.search(r'(<script>\s*\(function\(\).*?</script>\s*</body>\s*</html>)', old, re.DOTALL)
JS_BLOCK = js_match.group(1)
JS_BLOCK = JS_BLOCK.replace('const TOTAL_SLIDES = 22;', 'const TOTAL_SLIDES = 35;')

FIXED_UI = FIXED_UI.replace('01 / 22', '01 / 35')
FIXED_UI = FIXED_UI.replace('style="width:4.5%"', 'style="width:2.86%"')

EXTRA_CSS = """
.code-layout{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start;}
.code-layout.wide-left{grid-template-columns:3fr 2fr;}
.code-explain{display:flex;flex-direction:column;gap:10px;}
.explain-item{background:#fff;border-left:3px solid #6aadb8;padding:8px 12px;border-radius:0 6px 6px 0;font-size:12.5px;line-height:1.5;}
.explain-item strong{color:#6aadb8;}
.output-box{background:#1e1e2e;color:#cdd6f4;font-family:'JetBrains Mono',monospace;font-size:12px;padding:14px 18px;border-radius:8px;line-height:1.6;overflow:auto;max-height:260px;}
.action-table{width:100%;border-collapse:collapse;font-size:12.5px;}
.action-table th{background:#6aadb8;color:white;padding:8px 10px;text-align:left;}
.action-table td{padding:7px 10px;border-bottom:1px solid #e8e9ea;}
.action-table tr:nth-child(even) td{background:#f9fafb;}
.tier-card{background:white;border-radius:10px;padding:14px;border-top:4px solid #6aadb8;border:1px solid #e8eaed;}
.tier-card.orange{border-top-color:#ff4b28;}
.tier-card.green2{border-top-color:#27ae60;}
.tier-card.gray{border-top-color:#95a5a6;}
.tier-name{font-weight:700;font-size:14px;margin-bottom:6px;}
.tier-stats{font-size:11.5px;color:#666;margin-bottom:6px;}
.cover-layout{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;gap:18px;}
.cover-tag{font-size:11px;color:#6aadb8;letter-spacing:1px;text-transform:uppercase;}
.cover-title{font-size:50px;font-weight:800;color:#1a1a2e;line-height:1.1;}
.cover-subtitle{font-size:17px;color:#555;max-width:600px;}
.cover-group-name{font-size:19px;font-weight:700;color:#6aadb8;}
.cover-members{font-size:12.5px;color:#666;line-height:1.8;}
.cover-hint{font-size:11px;color:#aaa;margin-top:16px;}
.slide-header{margin-bottom:16px;}
.slide-header h2{font-size:33px;font-weight:800;background:linear-gradient(135deg,#343f4d,#5a6a7a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.15;}
.slide-header p{font-size:13.5px;color:#5a6a7a;margin-top:4px;}
.step{opacity:0;transform:translateY(16px);transition:opacity 0.4s,transform 0.4s;}
.step.revealed{opacity:1;transform:none;}
.cbox{background:#fff;border:1px solid #e8eaed;border-radius:12px;padding:14px 18px;margin-bottom:8px;}
.cbox h4{font-size:13px;font-weight:700;color:#343f4d;margin-bottom:6px;}
.cbox p,.cbox li{font-size:12.5px;color:#5a6a7a;line-height:1.6;}
.cbox ul{padding-left:16px;}
.cbox ol{padding-left:16px;}
.hbox{background:rgba(106,173,184,0.08);border:1px solid rgba(106,173,184,0.25);border-left:4px solid #6aadb8;border-radius:0 10px 10px 0;padding:11px 15px;font-size:13px;color:#343f4d;line-height:1.6;margin:8px 0;}
.wbox{background:rgba(255,75,40,0.07);border:1px solid rgba(255,75,40,0.2);border-left:4px solid #ff4b28;border-radius:0 10px 10px 0;padding:11px 15px;font-size:13px;color:#343f4d;line-height:1.6;margin:8px 0;}
.num-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:10px 0;}
.num-card{background:#fff;border:1px solid #e8eaed;border-radius:10px;padding:14px;text-align:center;}
.num-val{font-size:26px;font-weight:800;color:#6aadb8;line-height:1;}
.num-label{font-size:11px;color:#8a9aaa;margin-top:4px;}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:8px 0;}
.three-col{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:8px 0;}
.mt{width:100%;border-collapse:collapse;font-size:12px;}
.mt th{background:#f4f5f6;padding:6px 10px;text-align:left;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8a9aaa;border-bottom:1px solid #e8eaed;}
.mt td{padding:6px 10px;border-bottom:1px solid #f0f2f4;color:#343f4d;}
.mt tr:last-child td{border-bottom:none;}
.caption{font-size:11.5px;color:#5a6a7a;font-style:italic;margin-top:6px;padding:6px 10px;background:rgba(106,173,184,0.06);border-radius:6px;}
.budget-bar{display:flex;height:30px;border-radius:6px;overflow:hidden;margin:10px 0;}
.budget-seg{display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:12px;}
.cm-grid{display:grid;grid-template-columns:auto 1fr 1fr;gap:2px;font-size:12.5px;width:fit-content;margin-bottom:10px;}
.cm-cell{padding:9px 13px;text-align:center;border-radius:4px;}
.cm-header{background:#6aadb8;color:white;font-weight:700;}
.cm-tp{background:#d5f5e3;font-weight:700;color:#27ae60;}
.cm-tn{background:#d5f5e3;font-weight:700;color:#27ae60;}
.cm-fp{background:#fde8e8;color:#e74c3c;}
.cm-fn{background:#fde8e8;color:#e74c3c;}
"""

HEAD = HEAD.replace('</style>', EXTRA_CSS + '\n</style>')

# ── Helpers ───────────────────────────────────────────────────────────────────

def slide(n, steps, chapter, step_types, content, extra_class=""):
    cls = "slide" + (" " + extra_class if extra_class else "")
    sty = f'data-step-types="{step_types}"' if step_types else ''
    return (f'<div class="{cls}" data-slide="{n}" data-steps="{steps}" '
            f'data-chapter="{chapter}" {sty}>\n{content}\n</div>')

def hdr(title, sub=""):
    s = f'<p>{sub}</p>' if sub else ''
    return f'<div class="slide-header"><h2>{title}</h2>{s}</div>'

def stepd(n, c):
    return f'<div class="step step-{n}">{c}</div>'

def code_block(code):
    esc = code.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return (f'<div class="jupyter-cell">'
            f'<div class="jupyter-cell-header"><span class="jupyter-in-label">In [*]:</span></div>'
            f'<pre><code class="language-python">{esc}</code></pre></div>')

def code2col(code_html, items, wide=False):
    cls = "code-layout wide-left" if wide else "code-layout"
    rows = ''.join(f'<div class="explain-item">{x}</div>' for x in items)
    return f'<div class="{cls}">{code_html}<div class="code-explain">{rows}</div></div>'

def out(txt):
    return f'<div class="output-box">{txt}</div>'

def chart_step(n, key, cap=""):
    c = f'<div class="caption">{cap}</div>' if cap else ''
    return stepd(n, f'{img(key)}{c}')

# ── SLIDES ────────────────────────────────────────────────────────────────────
slides_html = []

# 1 — Capa
slides_html.append(slide(1, 0, "", "", """
<div class="cover-layout">
  <div class="cover-tag">IBMEC RJ · IBM3297 · Análise de Dados · 2026.1 · Prof. Paulo Josef Hirsch</div>
  <div class="cover-title">Análise Geográfica<br>de Participantes</div>
  <div class="cover-subtitle">Inteligência de marketing aplicada à Company Connection</div>
  <div>
    <div class="cover-group-name">GRUPO 5</div>
    <div class="cover-members">Gabriel Maino Chamas · Gabriela Borsoi Cohen · Hyan Lucas Alves Fernandes<br>Isabelle de Brito Cavalcante · João Gabriel Stor Bittencourt · Malena Catallini</div>
  </div>
  <div class="cover-hint">pressione → para avançar</div>
</div>
""", "slide-hook active"))

# 2 — Agenda
slides_html.append(slide(2, 0, "Agenda", "", hdr("Agenda","O que veremos hoje") + """
<div class="three-col" style="margin-top:16px;">
  <div class="cbox" style="border-top:3px solid #6aadb8;"><div style="font-size:20px;font-weight:800;color:#6aadb8;">01</div><h4>O Negócio</h4><p>Company Connection, Cap Mania, o problema do marketing no feeling</p></div>
  <div class="cbox" style="border-top:3px solid #ff4b28;"><div style="font-size:20px;font-weight:800;color:#ff4b28;">02</div><h4>Os Dados</h4><p>100.365 registros, 5 colunas, CRISP-DM, pipeline analítico</p></div>
  <div class="cbox" style="border-top:3px solid #27ae60;"><div style="font-size:20px;font-weight:800;color:#27ae60;">03</div><h4>O Pipeline</h4><p>Blocos 0–3: parâmetros, carregamento, limpeza, feature engineering</p></div>
  <div class="cbox" style="border-top:3px solid #6aadb8;"><div style="font-size:20px;font-weight:800;color:#6aadb8;">04</div><h4>O Que Descobrimos</h4><p>EDA: cidades, bairros, temporal, recência, heatmaps</p></div>
  <div class="cbox" style="border-top:3px solid #ff4b28;"><div style="font-size:20px;font-weight:800;color:#ff4b28;">05</div><h4>Os Modelos</h4><p>K-Means clustering + Árvore de Decisão: conceito, código, avaliação</p></div>
  <div class="cbox" style="border-top:3px solid #27ae60;"><div style="font-size:20px;font-weight:800;color:#27ae60;">06</div><h4>As Recomendações</h4><p>Três listas, plano de ação Top 5, alocação de orçamento</p></div>
</div>
"""))

# 3 — A Company Connection
slides_html.append(slide(3, 2, "01 — O Negócio", "concept,concept", hdr("A Company Connection","Sorteios legalizados para influenciadores digitais") + """
""" + stepd(1, """<div class="two-col">
  <div class="cbox"><h4>O que fazem</h4><p>Sorteios <strong>legalizados</strong> via bilhetes de capitalização e bilhetes lotéricos. Diferente de rifas ilegais — operam com CNPJ dentro da lei. Produto Cap Mania (encerrado 2024): sorteios via influenciadores como Wesley Alemão e Razuki. Participante paga → concorre → influenciador divulga.</p></div>
  <div class="cbox"><h4>Por que existem</h4><p>Lacuna jurídica: <strong>30–40% de carga tributária</strong> elimina competidores informais que recebem multas. Empresa fundada em 2024, 40–50 colaboradores. Crescimento via influência digital, sem estrutura de inteligência de dados — decisões no feeling.</p></div>
</div>""") + stepd(2, """<div class="three-col">
  <div class="cbox" style="border-top:3px solid #ff4b28;"><h4>Dor 1 — Concorrência informal</h4><p>Competidores ilegais não pagam 30–40% de impostos. Para sobreviver, cada real de marketing precisa de retorno mensurável.</p></div>
  <div class="cbox" style="border-top:3px solid #ff4b28;"><h4>Dor 2 — Decisões no feeling</h4><p>Copiavam o que outros influenciadores faziam. Sem análise de onde os participantes estavam, quem recomprava, quais regiões tinham potencial.</p></div>
  <div class="cbox" style="border-top:3px solid #ff4b28;"><h4>Dor 3 — Dependência técnica</h4><p>Análise dependia de especialista SQL/Excel. Sem script reutilizável, cada produto novo = análise do zero.</p></div>
</div>""")))

# 4 — O Problema
slides_html.append(slide(4, 2, "01 — O Negócio", "concept,concept", hdr("100 mil registros parados — sem virar inteligência") + stepd(1, """<div class="two-col">
  <div class="cbox"><h4>Cap Mania — o produto</h4><p>Produto descontinuado em 2024. Acumulou <strong>100.365 registros</strong> — endereço, CEP, data da última compra. Esses dados nunca foram analisados. A empresa não sabia: onde estão seus melhores clientes? Quem ainda compra? Quais bairros têm potencial de reativação?</p></div>
  <div class="cbox"><h4>As 3 consequências</h4><ul><li><strong>Dinheiro mal direcionado:</strong> orçamento de mídia espalhado igualmente, sem prioridade geográfica</li><li><strong>Oportunidades perdidas:</strong> bairros com alta concentração de dormentes nunca foram reativados</li><li><strong>Falta de escalabilidade:</strong> para cada produto novo, análise do zero — sem metodologia documentada</li></ul></div>
</div>""") + stepd(2, '<div class="hbox" style="font-size:15px;font-weight:600;text-align:center;padding:18px 24px;">Nosso objetivo: transformar 100.365 linhas paradas em plano de ação com bairros priorizados, volumes absolutos e canais recomendados.</div>')))

# 5 — A Base de Dados
slides_html.append(slide(5, 2, "02 — Os Dados", "concept,concept",
  hdr("A Base de Dados","O que tínhamos para trabalhar") +
  '<div class="num-grid"><div class="num-card"><div class="num-val">100.365</div><div class="num-label">Registros totais</div></div><div class="num-card"><div class="num-val">5</div><div class="num-label">Colunas disponíveis</div></div><div class="num-card"><div class="num-val">2022–25</div><div class="num-label">Período coberto</div></div><div class="num-card"><div class="num-val">99,7%</div><div class="num-label">Concentração no RJ</div></div></div>' +
  stepd(1, """<div class="two-col">
  <div class="cbox"><h4>O que temos</h4><ul>
    <li><code style="font-family:'JetBrains Mono',monospace;color:#6aadb8;">bairro</code> — nome do bairro</li>
    <li><code style="font-family:'JetBrains Mono',monospace;color:#6aadb8;">cidade</code> — nome da cidade</li>
    <li><code style="font-family:'JetBrains Mono',monospace;color:#6aadb8;">uf</code> — estado (2 letras)</li>
    <li><code style="font-family:'JetBrains Mono',monospace;color:#6aadb8;">cep</code> — CEP completo</li>
    <li><code style="font-family:'JetBrains Mono',monospace;color:#6aadb8;">ultima_compra</code> — data da última participação</li>
  </ul></div>
  <div class="cbox"><h4>O que NÃO temos</h4><ul>
    <li>Idade / gênero — vedado pela LGPD</li>
    <li>Telefone / email — não coletado</li>
    <li>Nome / CPF — anonimizado</li>
    <li>Histórico completo — apenas última compra</li>
  </ul><div class="hbox" style="margin-top:8px;">Limitação virou foco: <strong>análise 100% geográfica</strong> — mais acionável para mídia paga segmentada por localização.</div></div>
</div>""") +
  stepd(2, """<div class="cbox"><h4>Revisão metodológica — Antes vs Depois</h4>
<table class="mt"><tr><th>Aspecto</th><th>Proposta original</th><th>Versão entregue</th></tr>
<tr><td>Escopo geográfico</td><td>Nacional</td><td>RJ (99,7% dos dados)</td></tr>
<tr><td>Técnica principal</td><td>RFM clássico</td><td>Recência geográfica + K-Means</td></tr>
<tr><td>Modelo preditivo</td><td>Não previsto</td><td>Árvore de Decisão (RECENTE/ANTIGO)</td></tr>
<tr><td>Granularidade</td><td>Cidade</td><td>Bairro + CEP-3</td></tr>
</table></div>""")))

# 6 — CRISP-DM
slides_html.append(slide(6, 1, "02 — Os Dados", "concept", hdr("O método que seguimos: CRISP-DM","Cross-Industry Standard Process for Data Mining") + stepd(1, """
<div class="three-col">
  <div class="cbox"><div style="font-weight:800;color:#6aadb8;font-size:13px;">① Compreensão do negócio</div><p>Proposta de projeto + revisão metodológica após descoberta dos dados reais</p></div>
  <div class="cbox"><div style="font-weight:800;color:#6aadb8;font-size:13px;">② Compreensão dos dados</div><p>Bloco 1 — carregamento, inspeção, entendimento das 5 colunas</p></div>
  <div class="cbox"><div style="font-weight:800;color:#6aadb8;font-size:13px;">③ Preparação</div><p>Blocos 2+3 — limpeza, padronização, recência, status, CEP-3</p></div>
  <div class="cbox"><div style="font-weight:800;color:#6aadb8;font-size:13px;">④ Modelagem</div><p>Blocos 6+7 — K-Means (clustering) + Árvore de Decisão (classificação)</p></div>
  <div class="cbox"><div style="font-weight:800;color:#6aadb8;font-size:13px;">⑤ Avaliação</div><p>Blocos 6.5 + 7.4 — cotovelo, confusion matrix, classification report</p></div>
  <div class="cbox"><div style="font-weight:800;color:#6aadb8;font-size:13px;">⑥ Implantação</div><p>Blocos 9+10 — plano de ação Top 5 bairros + exportação de 5 CSVs</p></div>
</div>
<div class="hbox"><strong>Quando o professor perguntar "qual metodologia?"</strong> → CRISP-DM, seis fases, aplicada iterativamente (a descoberta do Bloco 1 nos levou de volta à fase ①).</div>
""")))

# 7 — Pipeline
slides_html.append(slide(7, 1, "02 — Os Dados", "concept", hdr("Do CSV ao plano de ação","Visão geral do pipeline analítico") + stepd(1, """
<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:10px 0;">
  <div style="background:#fff;border:1px solid #e8eaed;border-radius:8px;padding:10px 14px;text-align:center;min-width:90px;"><div style="font-size:10px;color:#6aadb8;font-weight:700;">01</div><div style="font-size:12px;font-weight:600;">Coleta</div><div style="font-size:10px;color:#8a9aaa;">CSV bruto</div></div>
  <span style="color:#8a9aaa;">→</span>
  <div style="background:#fff;border:1px solid #e8eaed;border-radius:8px;padding:10px 14px;text-align:center;min-width:90px;"><div style="font-size:10px;color:#6aadb8;font-weight:700;">02</div><div style="font-size:12px;font-weight:600;">Limpeza</div><div style="font-size:10px;color:#8a9aaa;">upper, NFKD, UFs</div></div>
  <span style="color:#8a9aaa;">→</span>
  <div style="background:#fff;border:1px solid #e8eaed;border-radius:8px;padding:10px 14px;text-align:center;min-width:90px;"><div style="font-size:10px;color:#6aadb8;font-weight:700;">03</div><div style="font-size:12px;font-weight:600;">Variáveis</div><div style="font-size:10px;color:#8a9aaa;">recência, status, CEP-3</div></div>
  <span style="color:#8a9aaa;">→</span>
  <div style="background:#fff;border:1px solid #e8eaed;border-radius:8px;padding:10px 14px;text-align:center;min-width:90px;"><div style="font-size:10px;color:#6aadb8;font-weight:700;">04</div><div style="font-size:12px;font-weight:600;">EDA</div><div style="font-size:10px;color:#8a9aaa;">gráficos, heatmaps</div></div>
  <span style="color:#8a9aaa;">→</span>
  <div style="background:#fff;border:1px solid #e8eaed;border-radius:8px;padding:10px 14px;text-align:center;min-width:90px;"><div style="font-size:10px;color:#6aadb8;font-weight:700;">05</div><div style="font-size:12px;font-weight:600;">Modelagem</div><div style="font-size:10px;color:#8a9aaa;">K-Means + Árvore</div></div>
  <span style="color:#8a9aaa;">→</span>
  <div style="background:#fff;border:1px solid #e8eaed;border-radius:8px;padding:10px 14px;text-align:center;min-width:90px;"><div style="font-size:10px;color:#6aadb8;font-weight:700;">06</div><div style="font-size:12px;font-weight:600;">Recomendações</div><div style="font-size:10px;color:#8a9aaa;">3 listas + plano</div></div>
</div>
<div class="three-col">
  <div class="cbox"><h4>Bloco 0 — Parâmetros</h4><p>Todos os ajustes em um lugar: CAMINHO_CSV, UF_FOCO, DIAS_RECENTE, VOLUME_MIN_BAIRRO, N_CLUSTERS</p></div>
  <div class="cbox"><h4>Blocos 1–3 — Dados limpos</h4><p>De 100.365 linhas brutas para 82.875 registros RJ padronizados + 3 variáveis derivadas</p></div>
  <div class="cbox"><h4>Blocos 4–10 — Inteligência</h4><p>EDA visual → dois modelos → três listas priorizadas → cinco CSVs exportados</p></div>
</div>
""")))

# 8 — Bloco 0
c8 = code_block("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

CAMINHO_CSV       = 'dados_cap_mania.csv'
UF_FOCO           = 'RJ'
DIAS_RECENTE      = 365
VOLUME_MIN_BAIRRO = 50
N_CLUSTERS        = 4""")
e8 = ["<strong>CAMINHO_CSV</strong> — troca o arquivo sem tocar no resto do código",
      "<strong>UF_FOCO = 'RJ'</strong> — filtra para o estado de interesse (pode ser 'SP', 'MG'...)",
      "<strong>DIAS_RECENTE = 365</strong> — limiar: compra nos últimos 365 dias = cliente RECENTE",
      "<strong>VOLUME_MIN_BAIRRO = 50</strong> — exclui bairros com menos de 50 registros (estatísticas não representativas)",
      "<strong>N_CLUSTERS = 4</strong> — número de grupos para o K-Means (confirmado pelo método do cotovelo)"]
slides_html.append(slide(8, 2, "03 — O Pipeline", "code,concept", hdr("Bloco 0 — Parâmetros e bibliotecas") +
  stepd(1, code2col(c8, e8, wide=True)) +
  stepd(2, '<div class="cbox"><h4>Por que centralizar parâmetros no Bloco 0?</h4><p>Princípio de <strong>reusabilidade</strong>: qualquer futuro produto da Company Connection com as mesmas 5 colunas pode ser analisado trocando apenas CAMINHO_CSV. Os outros 9 blocos rodam sem alteração. Isso transforma uma análise pontual em um <strong>ativo permanente</strong> da empresa — sem reprogramação.</p></div>')))

# 9 — Bloco 1
c9 = code_block("""df = pd.read_csv(CAMINHO_CSV)

print('Total de linhas:', len(df))
print('Total de colunas:', df.shape[1])
print('Colunas:', list(df.columns))

df.head(10)
df.isna().sum()""")
e9 = ["<strong>pd.read_csv()</strong> — carrega o CSV em um DataFrame",
      "<strong>len(df)</strong> — conta linhas; <strong>df.shape[1]</strong> conta colunas",
      "<strong>df.head(10)</strong> — visualiza primeiras 10 linhas para conferir formato",
      "<strong>df.isna().sum()</strong> — conta valores nulos por coluna (diagnóstico de qualidade)"]
slides_html.append(slide(9, 3, "03 — O Pipeline", "code,output,concept", hdr("Bloco 1 — Carregamento e inspeção inicial") +
  stepd(1, code2col(c9, e9, wide=True)) +
  stepd(2, out("Total de linhas: 100365\nTotal de colunas: 5\nColunas: ['bairro', 'cidade', 'uf', 'cep', 'ultima_compra']\n\n   bairro        cidade          uf    cep       ultima_compra\n0  COPACABANA    RIO DE JANEIRO  RJ    22070001  2024-03-15\n1  TIJUCA        RIO DE JANEIRO  RJ    20510001  2023-11-20") +
        '<div class="wbox">5 colunas — <strong>sem dados demográficos</strong>. Isso mudou toda a metodologia: sem idade ou renda, a análise precisa ser 100% geográfica. Não é limitação — é o ponto de partida para segmentação por localização.</div>') +
  stepd(3, '<div class="cbox"><h4>GIGO — Garbage In, Garbage Out</h4><p>A qualidade do modelo nunca supera a qualidade dos dados. Por isso a limpeza (Bloco 2) é metade do trabalho. <strong>O que aprendemos neste bloco:</strong> 5 colunas geográficas e temporais → isso motiva a criação de variáveis derivadas (Bloco 3) para alimentar os modelos.</p></div>')))

# 10 — Bloco 2.1-2.2
c10 = code_block("""# 2.1 Padronização de texto
df['cidade'] = df['cidade'].str.upper().str.strip()
df['bairro'] = df['bairro'].str.upper().str.strip()
df['uf']     = df['uf'].str.upper().str.strip()

# 2.2 Remoção de acentos (NFKD)
for col in ['cidade', 'bairro']:
    df[col] = (df[col]
        .str.normalize('NFKD')
        .str.encode('ascii', errors='ignore')
        .str.decode('utf-8'))""")
e10 = ["<strong>.str.upper()</strong> — 'Rio de Janeiro' → 'RIO DE JANEIRO' (evita duplicatas)",
       "<strong>.str.strip()</strong> — remove espaços antes/depois (comum em exports de sistemas)",
       "<strong>.normalize('NFKD')</strong> — decompõe 'Á' em 'A' + acento separado (Unicode)",
       "<strong>.encode('ascii', errors='ignore')</strong> — descarta o caractere de acento",
       "<strong>.decode('utf-8')</strong> — resultado: 'NITERÓI' → 'NITEROI'"]
slides_html.append(slide(10, 3, "03 — O Pipeline", "code,output,concept", hdr("Bloco 2 — Limpeza e padronização (2.1–2.2)") +
  stepd(1, code2col(c10, e10, wide=True)) +
  stepd(2, out("Antes:  'Ipanema', 'IPANEMA', 'ipanema', 'IPANÊMA'\nDepois: 'IPANEMA' (todos iguais)\n\nExemplos de NFKD:\n  'NITERÓI'      → 'NITEROI'\n  'SÃO GONÇALO' → 'SAO GONCALO'\n  'CAMPO GRANDE' → 'CAMPO GRANDE'")) +
  stepd(3, '<div class="cbox"><h4>Por que NFKD e não .replace()?</h4><p>NFKD é Unicode Normalization Form Compatibility Decomposition. Processo: (1) <strong>normalize(\'NFKD\')</strong> decompõe \'Á\' em \'A\' + combining accent (U+0301); (2) <strong>encode(\'ascii\', errors=\'ignore\')</strong> descarta o combining accent; (3) <strong>decode(\'utf-8\')</strong> retorna texto limpo. Com .replace() precisaríamos de dezenas de linhas para cobrir á,à,ã,â,ä... Este método resolve todos em 1 linha.</p></div>')))

# 11 — Bloco 2.3-2.5
c11 = code_block("""# 2.3 UFs inválidas → None
ufs_validas = ['AC','AL','AP','AM','BA','CE','DF',
               'ES','GO','MA','MT','MS','MG','PA',
               'PB','PR','PE','PI','RJ','RN','RS',
               'RO','RR','SC','SP','SE','TO']
df.loc[~df['uf'].isin(ufs_validas), 'uf'] = None

# 2.4 Data → datetime
df['ultima_compra'] = pd.to_datetime(df['ultima_compra'])

# 2.5 Filtrar para RJ
df = df[df['uf'] == UF_FOCO]""")
e11 = ["<strong>ufs_validas</strong> — lista dos 27 estados + DF (validação exaustiva)",
       "<strong>~df['uf'].isin()</strong> — o ~ inverte: seleciona linhas que NÃO estão na lista",
       "<strong>pd.to_datetime()</strong> — converte texto '2024-03-15' para tipo datetime (necessário para calcular dias)",
       "<strong>df[df['uf'] == UF_FOCO]</strong> — filtra apenas linhas do RJ (parâmetro do Bloco 0)"]
slides_html.append(slide(11, 3, "03 — O Pipeline", "code,output,concept", hdr("Bloco 2 — Limpeza (2.3, 2.4, 2.5)","UFs inválidas, datetime, filtro RJ") +
  stepd(1, code2col(c11, e11, wide=True)) +
  stepd(2, out("Registros antes do filtro: 100.365\nRegistros após filtro RJ:  82.875\nRemovidos:                 17.490 (17,4%)\n\n99,7% da base estava no RJ — confirma que\na análise regional é o foco correto.")) +
  stepd(3, """<div class="cbox"><h4>Três estratégias para dados faltantes</h4>
<table class="mt"><tr><th>Estratégia</th><th>Como</th><th>Quando usar</th><th>Usado onde</th></tr>
<tr><td><strong>Remover</strong></td><td>dropna() ou filtro</td><td>Registro inútil sem aquele campo</td><td>UFs inválidas → filtro RJ</td></tr>
<tr><td><strong>Imputar</strong></td><td>fillna(média/moda)</td><td>Quer manter o registro, campo estimável</td><td>Não necessário aqui</td></tr>
<tr><td><strong>Ignorar</strong></td><td>mantém NaN</td><td>Modelo aceita nulos, campo secundário</td><td>Bairros nulos → dropna no Bloco 7</td></tr>
</table></div>""")))

# 12 — Bloco 3 Feature Engineering
c12 = code_block("""# 3.1 Recência em dias
data_corte = df['ultima_compra'].max()
df['recencia_dias'] = (
    data_corte - df['ultima_compra']
).dt.days

# 3.2 Status binário
df['status_recente'] = 'ANTIGO'
df.loc[df['recencia_dias'] <= DIAS_RECENTE,
       'status_recente'] = 'RECENTE'

# 3.3 CEP-3 (sub-região postal)
df['cep3'] = df['cep'].astype(str).str[:3]""")
e12 = ["<strong>data_corte</strong> — data mais recente na base (âncora para calcular recência)",
       "<strong>.dt.days</strong> — diferença entre datas datetime em dias inteiros",
       "<strong>status_recente</strong> — converte contínuo (dias) em categórico para Árvore de Decisão",
       "<strong>cep3 = cep[:3]</strong> — primeiros 3 dígitos = sub-região postal"]
slides_html.append(slide(12, 3, "03 — O Pipeline", "code,output,concept", hdr("Bloco 3 — Feature engineering") +
  stepd(1, code2col(c12, e12, wide=True)) +
  stepd(2, out("data_corte: 2025-03-15\n\nrecencia_dias: min=0, max=946, mediana≈600\n\nStatus RECENTE (≤365 dias): 18.232  (22%)\nStatus ANTIGO  (>365 dias): 64.643  (78%)\n\nCEP-3 únicos: 75 sub-regiões postais")) +
  stepd(3, """<div class="cbox"><h4>Feature Engineering — criando informação útil a partir do que se tem</h4>
<table class="mt"><tr><th>Coluna original</th><th>Variável derivada</th><th>Por que é melhor</th><th>Onde usamos</th></tr>
<tr><td>ultima_compra (data)</td><td>recencia_dias (int)</td><td>Modelos precisam de números, não datas</td><td>K-Means, Árvore</td></tr>
<tr><td>recencia_dias (int)</td><td>status_recente (str)</td><td>Árvore precisa de categorias como alvo (y)</td><td>Árvore</td></tr>
<tr><td>cep (8 dígitos)</td><td>cep3 (3 dígitos)</td><td>Granularidade ideal para mídia paga geográfica</td><td>Árvore (X)</td></tr>
</table>
<div class="wbox" style="margin-top:8px;">Sem estas 3 variáveis, K-Means e Árvore não teriam o que aprender.</div></div>""")))

# 13 — EDA Cidades e Bairros
slides_html.append(slide(13, 3, "04 — O Que Descobrimos", "chart,chart,concept", hdr("Bloco 4 — EDA: onde estão os participantes?","Top cidades e top bairros") +
  chart_step(1, "img_cidades", "Gráfico de barras — escolhido porque cidades são categorias. Para comparar quantidades entre categorias, barras é o padrão. Rio de Janeiro domina amplamente.") +
  chart_step(2, "img_bairros", "Barras horizontais — nomes de bairros são longos, caber no eixo Y exige orientação horizontal. Top 20 bairros concentram grande parte da base.") +
  stepd(3, """<div class="cbox"><h4>Principais achados</h4><ul>
<li>Rio de Janeiro cidade domina com mais de 70% dos registros</li>
<li>Top 20 bairros concentram aproximadamente 40% da base total</li>
<li>Concentração geográfica forte → justifica estratégia de geo-segmentação</li>
</ul>
<div class="hbox"><strong>Por que olhamos antes de modelar?</strong> Para validar suposições. Descobrimos que 99,7% está no RJ — não era suposição, foi descoberta. Se tivéssemos modelado antes, teríamos desperdício computacional com dados nacionais irrelevantes.</div></div>""")))

# 14 — Temporal
slides_html.append(slide(14, 2, "04 — O Que Descobrimos", "chart,concept", hdr("Quando os participantes compraram?","A linha do tempo do Cap Mania") +
  chart_step(1, "img_temporal", "Série temporal de compras por mês — barras agrupadas por período. Mostra crescimento, pico e descontinuação do produto.") +
  stepd(2, """<div class="cbox"><h4>Interpretação da série temporal</h4><ul>
<li>Produto atingiu pico em 2024 com influenciadores de grande alcance</li>
<li>Queda abrupta após descontinuação: novos participantes cessaram</li>
<li><strong>Mais de 75% dos clientes são ANTIGOS</strong> (última compra há mais de 365 dias)</li>
</ul>
<div class="wbox"><strong>Implicação para modelagem:</strong> foco em <strong>reativação, não aquisição</strong>. E por que o K-Means não funciona bem no nível do cliente individual: todos parecem iguais (quase todos antigos). Funciona melhor no nível bairro, onde há variabilidade em % recentes.</div></div>""")))

# 15 — Status e Recência
slides_html.append(slide(15, 3, "04 — O Que Descobrimos", "chart,chart,concept", hdr("Quem ainda compra?","Distribuição de recência e status") +
  chart_step(1, "img_pizza", "Pizza funciona com poucas categorias (2 ou 3). Aqui temos exatamente 2: RECENTE e ANTIGO. Imediatamente legível — não precisa de legenda extensa.") +
  chart_step(2, "img_histograma", "Histograma — distribuição de variável contínua (recencia_dias). Cada barra = faixa de dias. A linha vermelha marca o corte de 365 dias.") +
  stepd(3, """<div class="cbox"><h4>Interpretação e classe desbalanceada</h4>
<p><strong>78% ANTIGO, 22% RECENTE</strong> — dataset desbalanceado. Implicações:</p>
<ul>
<li>Para K-Means: pouca variabilidade no nível cliente → operar no nível bairro</li>
<li>Para Árvore: sem correção, aprende atalho preguiçoso → sempre prevê ANTIGO → 78% acurácia, zero recall de RECENTE</li>
<li>Correção: <code style="font-family:'JetBrains Mono',monospace;">class_weight='balanced'</code> → peso de RECENTE ≈ 3× maior</li>
</ul>
<div class="hbox">Corte de 365 dias: escolhido para alinhar com o ciclo anual de marketing — um ano sem comprar = cliente dormente para campanhas de reativação.</div></div>""")))

# 16 — Heatmaps
slides_html.append(slide(16, 3, "04 — O Que Descobrimos", "chart,chart,concept", hdr("Bloco 5 — Cruzando geografia × status: o heatmap") +
  chart_step(1, "img_heatmap_bairro", "Heatmap: tabela colorida onde cor = intensidade. Combina 3 informações em 1 imagem: bairro (linha), status (coluna), volume (cor). Mais escuro = mais participantes.") +
  chart_step(2, "img_heatmap_cep3", "Heatmap CEP-3 × status: visão macro por sub-região postal. CEP-3 agrega bairros de uma mesma zona — útil para planejamento de mídia por região.") +
  stepd(3, """<div class="cbox"><h4>Como ler um heatmap</h4><ul>
<li><strong>Linha</strong> = bairro ou CEP-3 (unidade geográfica)</li>
<li><strong>Coluna</strong> = status (RECENTE ou ANTIGO)</li>
<li><strong>Cor</strong> = quantidade de participantes (escala contínua)</li>
</ul>
<div class="wbox"><strong>Nota importante:</strong> heatmap é <em>visualização</em>, não modelo. O professor pode perguntar. Resposta: visualização mostra dados organizados; modelo aprende padrões generalizáveis. Heatmap não prevê — apenas exibe.</div>
<div class="hbox">Por que melhor que barras agrupadas? Com 20+ bairros × 2 status, barras agrupadas ficam ilegíveis. O heatmap comprime em uma grade colorida de leitura intuitiva.</div></div>""")))

# 17 — K-Means Conceito
slides_html.append(slide(17, 2, "05 — Os Modelos", "concept,concept", hdr("Modelo 1: K-Means","Agrupamento não supervisionado de bairros") +
  stepd(1, """<div class="two-col">
<div class="cbox" style="border-top:3px solid #6aadb8;"><h4>Aprendizado Supervisionado</h4><p>Tem respostas certas (rótulos). Aprende a <strong>prever</strong> y a partir de X. Exemplos: K-NN, Naive Bayes, Regressão, Árvore de Decisão.</p><p style="margin-top:8px;font-size:12px;color:#5a6a7a;">Nossa Árvore: X = localização → y = RECENTE/ANTIGO</p></div>
<div class="cbox" style="border-top:3px solid #ff4b28;"><h4>Aprendizado Não Supervisionado</h4><p>Sem rótulos. Descobre <strong>padrões</strong> na estrutura dos dados. Exemplos: K-Means, DBSCAN, PCA.</p><p style="margin-top:8px;font-size:12px;color:#5a6a7a;">Nosso K-Means: "que tipos de bairros temos?" — sem resposta prévia</p></div>
</div>
<div class="cbox"><h4>Dois modelos, duas perguntas</h4>
<table class="mt"><tr><th>Modelo</th><th>Pergunta</th><th>Saída</th></tr>
<tr><td>K-Means</td><td>Que tipos de bairros temos?</td><td>4 clusters com perfil de comportamento</td></tr>
<tr><td>Árvore de Decisão</td><td>Que variáveis geográficas explicam o comportamento?</td><td>Importância de bairro vs CEP-3 vs cidade</td></tr>
</table></div>""") +
  stepd(2, """<div class="cbox"><h4>Como o K-Means funciona — intuição</h4>
<p>Imagine 323 bolinhas numa mesa (323 bairros em espaço 3D). K-Means:</p>
<ol><li><strong>Sorteia</strong> K=4 pontos aleatórios como centros iniciais (centroides)</li>
<li>Cada bolinha vai ao <strong>centro mais próximo</strong> (distância euclidiana no espaço 3D padronizado)</li>
<li>Centros se <strong>movem</strong> para a média geométrica do grupo</li>
<li><strong>Repete</strong> até os centros pararem de mover (convergência)</li></ol>
<p style="margin-top:8px;">No nosso trabalho: cada "bolinha" é um bairro no espaço (volume, recência mediana, % recentes) — padronizado com Z-score para que as 3 dimensões tenham peso igual.</p></div>""")))

# 18 — Por que nível bairro
slides_html.append(slide(18, 1, "05 — Os Modelos", "concept", hdr("Decisão-chave: agregamos por bairro, não por cliente") +
  stepd(1, """<div class="cbox"><h4>Nível cliente vs Nível bairro</h4>
<table class="mt"><tr><th>Aspecto</th><th>Nível cliente (1 linha = 1 pessoa)</th><th>Nível bairro (1 linha = 1 bairro)</th></tr>
<tr><td>Problema</td><td>75% são ANTIGOS → pouca variabilidade → grupos idênticos</td><td>Bairros variam: 50–2000 clientes, 15–40% recentes</td></tr>
<tr><td>Ação de marketing</td><td>Marketing não age cliente a cliente</td><td>Meta Ads segmenta por CEP/bairro</td></tr>
<tr><td>Resultado</td><td>K grupos de "clientes antigos" (inútil)</td><td>4 tiers acionáveis com estratégia diferenciada</td></tr>
</table>
<div class="hbox" style="margin-top:10px;"><strong>Por que volume mínimo de 50?</strong> Para evitar que bairros com 1–2 clientes distorçam as médias. Com 50+ registros, as estatísticas do bairro (% recentes, recência mediana) são representativas da realidade daquela localidade.</div></div>""")))

# 19 — Bloco 6.1-6.2
c19 = code_block("""# 6.1 Agregação por bairro
df_bairros = df.groupby('bairro').agg(
    volume=('bairro', 'count'),
    recencia_mediana=('recencia_dias', 'median'),
    pct_recentes=('status_recente',
        lambda x: (x=='RECENTE').sum()/len(x)*100)
).reset_index()
df_bairros = df_bairros[
    df_bairros['volume'] >= VOLUME_MIN_BAIRRO]

# 6.2 Padronização Z-score
from sklearn.preprocessing import StandardScaler
X = df_bairros[['volume','recencia_mediana','pct_recentes']]
scaler = StandardScaler()
X_pad = scaler.fit_transform(X)""")
e19 = ["<strong>groupby('bairro').agg()</strong> — agrupa por bairro e calcula 3 estatísticas por grupo",
       "<strong>lambda x: (x=='RECENTE').sum()/len(x)*100</strong> — % de recentes no bairro",
       "<strong>volume >= VOLUME_MIN_BAIRRO</strong> — filtra bairros com ≥50 registros",
       "<strong>StandardScaler</strong> — padroniza para média=0, desvio=1 (obrigatório para K-Means)",
       "<strong>fit_transform(X)</strong> — aprende parâmetros (μ, σ) e aplica transformação"]
slides_html.append(slide(19, 3, "05 — Os Modelos", "code,output,concept", hdr("Bloco 6 — K-Means: preparando os dados","Agregação por bairro + padronização Z-score") +
  stepd(1, code2col(c19, e19, wide=True)) +
  stepd(2, out("323 bairros na análise (volume >= 50)\n\n   bairro        volume  recencia_mediana  pct_recentes\n0  ABOLIÇÃO          52        621.0          19.2\n1  ACARI            138        614.5          21.7\n2  ALTO DA BOA VISTA  67      598.0          22.4\n...\n\nApós StandardScaler:\n  volume: média=0, desvio=1\n  recencia_mediana: média=0, desvio=1\n  pct_recentes: média=0, desvio=1")) +
  stepd(3, """<div class="cbox"><h4>Por que StandardScaler é obrigatório para K-Means</h4>
<p>Z-score: <strong>z = (x − μ) / σ</strong></p>
<p>Sem padronizar: volume varia de 50 a 2.000 — domina o cálculo de distância. pct_recentes varia de 15 a 40 — é praticamente ignorada. O K-Means agrupa apenas por volume.</p>
<p>Com padronização: as 3 dimensões ficam na mesma escala (±2σ). O K-Means considera volume, recência e engajamento com peso igual.</p>
<div class="wbox"><strong>Por que só no K-Means e não na Árvore?</strong> A Árvore faz cortes por variável separadamente — escala não importa. "volume &gt; 100 → esquerda" funciona igual com ou sem padronização.</div></div>""")))

# 20 — Cotovelo
c20 = code_block("""from sklearn.cluster import KMeans

valores_k = range(2, 11)
inertias = []

for k in valores_k:
    modelo = KMeans(n_clusters=k,
                    random_state=42,
                    n_init=10)
    modelo.fit(X_pad)
    inertias.append(modelo.inertia_)

# Plot inertia × K → encontra o cotovelo""")
e20 = ["<strong>inertia_</strong> — soma dos quadrados das distâncias de cada ponto ao seu centroide",
       "<strong>random_state=42</strong> — semente fixa: garante reprodutibilidade total",
       "<strong>n_init=10</strong> — roda 10 vezes com seeds diferentes, guarda o melhor",
       "<strong>range(2, 11)</strong> — testa K de 2 a 10 para encontrar o ponto de inflexão"]
slides_html.append(slide(20, 3, "05 — Os Modelos", "code,chart,concept", hdr("Bloco 6.3 — Escolhendo K: o método do cotovelo") +
  stepd(1, code2col(c20, e20, wide=True)) +
  chart_step(2, "img_elbow", "Método do cotovelo: eixo X = K, eixo Y = inércia. O 'cotovelo' em K=4 indica onde o ganho de adicionar mais grupos começa a diminuir muito.") +
  stepd(3, """<div class="cbox"><h4>Como ler o cotovelo e por que K=4</h4><ul>
<li><strong>K muito baixo (2–3):</strong> grupos grandes, heterogêneos, pouco acionáveis</li>
<li><strong>K=4:</strong> equilíbrio — compacto + interpretável + cabe em apresentação</li>
<li><strong>K muito alto (7–10):</strong> grupos pequenos demais, difícil nomear, sem sentido de negócio</li>
</ul>
<p><strong>n_init=10:</strong> K-Means é sensível à inicialização. 10 rodadas com seeds diferentes, guarda a de menor inércia — evita mínimos locais ruins.</p>
<p><strong>random_state=42:</strong> toda execução dá o mesmo resultado. Obrigatório em trabalho acadêmico para que o orientador possa replicar.</p></div>""")))

# 21 — Treino K-Means
c21 = code_block("""# 6.4 Treino
modelo = KMeans(n_clusters=4,
                random_state=42, n_init=10)
modelo.fit(X_pad)
df_bairros['cluster'] = modelo.labels_

# 6.5 Perfil por cluster
perfil = df_bairros.groupby('cluster').agg(
    qtd_bairros=('bairro','count'),
    volume_medio=('volume','mean'),
    pct_recentes_medio=('pct_recentes','mean')
).round(1)

# 6.6 Nomeação automática
# maior volume → Núcleo Estratégico
# maior % recentes → Engajado
# menor % recentes → Em Declínio
# restante → Massa Padrão""")
e21 = ["<strong>modelo.labels_</strong> — array com o número do cluster de cada bairro (0, 1, 2 ou 3)",
       "<strong>groupby('cluster').agg()</strong> — calcula perfil médio de cada cluster",
       "<strong>Nomeação automática</strong> — baseada nas estatísticas do perfil, não em julgamento subjetivo"]
slides_html.append(slide(21, 3, "05 — Os Modelos", "code,output,concept", hdr("Bloco 6.4-6.6 — Treinando o K-Means e nomeando clusters") +
  stepd(1, code2col(c21, e21, wide=True)) +
  stepd(2, out("Perfil dos 4 clusters:\n  Cluster              Bairros  Vol.Médio  %Recentes\n  Núcleo Estratégico       6    1.642       26,1%\n  Engajado                69       98       29,4%\n  Massa Padrão           162      181       25,8%\n  Em Declínio             86      102       19,6%\n\nTotal: 323 bairros agrupados")) +
  stepd(3, """<div class="three-col">
<div class="cbox" style="border-top:4px solid #6aadb8;"><div class="tier-name">Núcleo Estratégico</div><div class="tier-stats">6 bairros · vol médio 1.642 · 26,1% recentes</div><div style="font-weight:600;color:#6aadb8;font-size:12px;">→ Manter visibilidade. ROI alto. Não arriscar.</div></div>
<div class="cbox" style="border-top:4px solid #27ae60;"><div class="tier-name">Engajado</div><div class="tier-stats">69 bairros · vol médio 98 · 29,4% recentes</div><div style="font-weight:600;color:#27ae60;font-size:12px;">→ Investir em mídia paga. Maior conversão potencial.</div></div>
<div class="cbox" style="border-top:4px solid #ff4b28;"><div class="tier-name">Em Declínio</div><div class="tier-stats">86 bairros · vol médio 102 · 19,6% recentes</div><div style="font-weight:600;color:#ff4b28;font-size:12px;">→ Campanha de reativação urgente. Maior potencial dormentes.</div></div>
</div>
<div class="cbox" style="border-top:4px solid #95a5a6;margin-top:8px;"><div class="tier-name">Massa Padrão</div><div class="tier-stats">162 bairros · vol médio 181 · 25,8% recentes</div><div style="font-weight:600;color:#95a5a6;font-size:12px;">→ Campanhas gerais sem priorização especial. Monitorar para reclassificação.</div></div>""")))

# 22 — Visualização clusters
slides_html.append(slide(22, 3, "05 — Os Modelos", "chart,chart,concept", hdr("Bloco 6.7 — Visualizando os 4 tiers de bairros") +
  chart_step(1, "img_scatter1", "Scatter: cada ponto = 1 bairro. Cor = cluster. Eixo X = volume (tamanho). Eixo Y = % recentes (engajamento). Núcleo Estratégico isolado à direita com alto volume.") +
  chart_step(2, "img_scatter2", "Segundo ângulo: recência mediana vs % recentes. Cluster 'Em Declínio' na parte inferior. Cluster 'Engajado' com alta % recentes apesar de menor volume.") +
  stepd(3, """<div class="cbox"><h4>Como ler os scatter plots</h4><ul>
<li><strong>Núcleo Estratégico:</strong> volume altíssimo — visível isolado à direita no scatter 1</li>
<li><strong>Engajado:</strong> disperso com % recentes acima da média — pontos altos no eixo Y</li>
<li><strong>Em Declínio:</strong> concentrado na parte inferior — % recentes mais baixa</li>
<li><strong>Massa Padrão:</strong> maioria dos pontos, comportamento médio</li>
</ul>
<div class="hbox">Os dois ângulos confirmam a coerência dos clusters: o que o K-Means separou no espaço 3D padronizado é visível nos scatters 2D. Validação visual qualitativa.</div></div>""")))

# 23 — Árvore Conceito
slides_html.append(slide(23, 2, "05 — Os Modelos", "concept,concept", hdr("Modelo 2: Árvore de Decisão","Classificação supervisionada RECENTE/ANTIGO") +
  stepd(1, """<div class="cbox"><h4>Como a Árvore de Decisão funciona — intuição</h4>
<p>"Como um fluxograma de perguntas automático." O algoritmo descobre as perguntas testando todas as separações possíveis e escolhendo a que minimiza a <strong>impureza Gini</strong>.</p>
<p style="margin-top:8px;"><strong>Impureza Gini:</strong> mede o quão misturadas estão as classes em um nó. Gini = 0 → nó puro (só RECENTE ou só ANTIGO). Gini = 0,5 → máximo caos (50/50). O algoritmo busca cortes que minimizam Gini nas folhas.</p>
<p style="margin-top:8px;">"Bairro X? → Se sim → 35% recentes. Se não → qual CEP-3? → ..." O modelo descobre essa árvore de perguntas automaticamente a partir dos dados.</p></div>""") +
  stepd(2, """<div class="cbox"><h4>Variáveis usadas — e por que não recencia_dias</h4>
<p><strong>X (preditoras):</strong> cidade_cod, bairro_cod, cep3_cod</p>
<p><strong>y (alvo):</strong> status_recente (RECENTE / ANTIGO)</p>
<div class="wbox"><strong>Por que não incluímos recencia_dias como X?</strong> Seria data leakage (cheating): recencia_dias é exatamente a variável que define RECENTE/ANTIGO. O modelo acertaria 100% sem aprender nada sobre geografia — decoraria a definição.</div>
<p style="margin-top:8px;"><strong>LabelEncoder:</strong> converte 'COPACABANA' → 0, 'TIJUCA' → 1... Strings viram números. Funciona para árvores (que fazem cortes por valor) mas NÃO para K-Means (que calcula distâncias — 0 não é "mais próximo" de 1 do que de 50).</p></div>""")))

# 24 — Bloco 7.1-7.2
c24 = code_block("""from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# 7.1 Codifica variáveis categóricas
df_mod = df.dropna(
    subset=['cidade','bairro','cep3']).copy()

le = LabelEncoder()
df_mod['cidade_cod'] = le.fit_transform(df_mod['cidade'])
df_mod['bairro_cod'] = le.fit_transform(df_mod['bairro'])
df_mod['cep3_cod']   = le.fit_transform(df_mod['cep3'])

X = df_mod[['cidade_cod','bairro_cod','cep3_cod']]
y = df_mod['status_recente']

# 7.2 Divisão 70/30
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3,
    random_state=42, stratify=y)""")
e24 = ["<strong>dropna(subset=[...])</strong> — remove registros sem localização (inúteis para modelo geográfico)",
       "<strong>LabelEncoder</strong> — 'COPACABANA'→0, 'TIJUCA'→1... (ordinal, aceitável para árvore)",
       "<strong>test_size=0.3</strong> — 30% para teste, 70% para treino",
       "<strong>stratify=y</strong> — garante mesma proporção RECENTE/ANTIGO no treino e no teste",
       "<strong>random_state=42</strong> — split reprodutível"]
slides_html.append(slide(24, 3, "05 — Os Modelos", "code,output,concept", hdr("Bloco 7.1-7.2 — Preparando dados e dividindo treino/teste") +
  stepd(1, code2col(c24, e24, wide=True)) +
  stepd(2, out("Treino: 57.979 linhas  |  Teste: 24.848 linhas\n\nProporção RECENTE no treino: 22,0%\nProporção RECENTE no teste:  22,0% (garantida pelo stratify)\n\nLabelEncoder: 'ANTIGO' → 0, 'RECENTE' → 1")) +
  stepd(3, """<div class="cbox"><h4>Overfitting vs Underfitting</h4><ul>
<li><strong>Treino:</strong> modelo "estuda" — vê os dados e ajusta os cortes</li>
<li><strong>Teste:</strong> modelo "faz prova" — dados que nunca viu</li>
<li><strong>Aprendeu:</strong> vai bem nos dois (treino E teste)</li>
<li><strong>Overfitting/decorou:</strong> vai bem no treino, mal no teste — memorizou em vez de generalizar</li>
<li><strong>Underfitting:</strong> vai mal nos dois — modelo muito simples</li>
</ul>
<div class="hbox"><strong>stratify=y:</strong> sem isso, o split poderia colocar 30% de RECENTE no treino e 14% no teste. O modelo veria proporções diferentes do real → avaliação distorcida. Com stratify, proporções são espelhadas.</div></div>""")))

# 25 — Bloco 7.3
c25 = code_block("""from sklearn.tree import DecisionTreeClassifier

arvore = DecisionTreeClassifier(
    max_depth=5,
    class_weight='balanced',
    random_state=42
)
arvore.fit(X_tr, y_tr)""")
e25 = ["<strong>max_depth=5</strong> — profundidade máxima: previne overfitting + mantém árvore interpretável",
       "<strong>class_weight='balanced'</strong> — crítico: compensa desbalanceamento 78%/22%",
       "<strong>random_state=42</strong> — reprodutibilidade para splits internos",
       "<strong>.fit(X_tr, y_tr)</strong> — treina apenas com dados de treino (nunca com teste)"]
slides_html.append(slide(25, 3, "05 — Os Modelos", "code,output,concept", hdr("Bloco 7.3 — Treinando a Árvore de Decisão") +
  stepd(1, code2col(c25, e25, wide=True)) +
  stepd(2, out("DecisionTreeClassifier treinado.\n  Profundidade real: 5 níveis (= max_depth)\n  Classes: ['ANTIGO', 'RECENTE']\n  Nós totais: ~63\n  Folhas: ~32")) +
  stepd(3, """<div class="cbox"><h4>class_weight='balanced' — por que é crítico</h4>
<p>Sem balanceamento: base tem 78% ANTIGO → árvore aprende atalho preguiçoso: <em>sempre prevê ANTIGO</em> → 78% de acurácia, mas identifica ZERO recentes (recall=0).</p>
<p style="margin-top:8px;"><strong>Com balanced:</strong> peso do RECENTE = total / (2 × n_recentes) ≈ <strong>3× maior</strong>. "Errar um RECENTE custa 3× mais do que errar um ANTIGO."</p>
<table class="mt" style="margin-top:10px;"><tr><th>Configuração</th><th>Acurácia</th><th>Recall RECENTE</th><th>Útil?</th></tr>
<tr><td>Sem balanced</td><td>~78%</td><td>~0%</td><td>Não — identifica ninguém</td></tr>
<tr><td>Com balanced</td><td>~63%</td><td>~59%</td><td>Sim — encontra recentes</td></tr>
</table>
<p style="margin-top:8px;"><strong>max_depth=5:</strong> sem limite, a árvore cresce até ter 1 folha por registro → 100% no treino, ~50% no teste (puro overfitting). Com 5 níveis, força generalização.</p></div>""")))

# 26 — Bloco 7.4
c26 = code_block("""from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report)

y_prev = arvore.predict(X_te)

acc = accuracy_score(y_te, y_prev)
cm  = confusion_matrix(y_te, y_prev)
cr  = classification_report(y_te, y_prev)

print(f'Acurácia: {acc:.1%}')
print(cm)
print(cr)""")
e26 = ["<strong>accuracy_score</strong> — (acertos totais) / (total) — enganosa com classes desbalanceadas",
       "<strong>confusion_matrix</strong> — tabela 2×2: TP, FP, FN, TN",
       "<strong>classification_report</strong> — precision, recall, F1 por classe",
       "<strong>y_prev</strong> — previsões no conjunto de teste (dados nunca vistos)"]
slides_html.append(slide(26, 3, "05 — Os Modelos", "code,output,concept", hdr("Bloco 7.4 — Avaliando o modelo: métricas") +
  stepd(1, code2col(c26, e26, wide=True)) +
  stepd(2, out("Acurácia: 63,2%\n\nConfusion Matrix:\n              Previsto ANTIGO  Previsto RECENTE\nReal ANTIGO      11.842          7.540\nReal RECENTE      2.258          3.208\n\nClassification Report:\n             precision  recall  f1-score  support\nANTIGO         0.84      0.61      0.71    19.382\nRECENTE        0.30      0.59      0.40     5.466\naccuracy                           0.63    24.848")) +
  stepd(3, """<div class="cbox"><h4>Interpretando as métricas</h4>
<div class="cm-grid">
<div class="cm-cell cm-header"></div><div class="cm-cell cm-header">Prev. ANTIGO</div><div class="cm-cell cm-header">Prev. RECENTE</div>
<div class="cm-cell cm-header">Real ANTIGO</div><div class="cm-cell cm-tn">TN = 11.842</div><div class="cm-cell cm-fp">FP = 7.540</div>
<div class="cm-cell cm-header">Real RECENTE</div><div class="cm-cell cm-fn">FN = 2.258</div><div class="cm-cell cm-tp">TP = 3.208</div>
</div>
<p style="font-size:12px;"><strong>Precision</strong> = TP/(TP+FP) | <strong>Recall</strong> = TP/(TP+FN) | <strong>F1</strong> = 2×P×R/(P+R)</p>
<div class="wbox"><strong>Para marketing:</strong> Recall de RECENTE é a métrica mais importante. Falso negativo (FN) = perdemos oportunidade de campanha. Falso positivo (FP) = comunicação para não-recente — custo baixo. O valor da Árvore neste projeto é <em>interpretativo</em>: confirma que bairro é a variável mais relevante.</div></div>""")))

# 27 — Bloco 7.5-7.6
slides_html.append(slide(27, 3, "05 — Os Modelos", "chart,chart,concept", hdr("Bloco 7.5-7.6 — Árvore e importância das variáveis") +
  chart_step(1, "img_arvore", "Cada nó = uma pergunta (bairro_cod ≤ X?). Cada folha = uma decisão (RECENTE ou ANTIGO). Cor mais intensa = nó mais puro. Números mostram distribuição de classes.") +
  chart_step(2, "img_importancia", "Importância das variáveis: quanto cada uma contribuiu para as separações ao longo de toda a árvore. Calculada pela redução total de Gini atribuída a cada variável.") +
  stepd(3, """<div class="cbox"><h4>Lendo os resultados — implicação estratégica</h4><ul>
<li><strong>Bairro tem o maior peso</strong> → campanhas devem ser desenhadas no nível bairro, não cidade nem CEP-3</li>
<li>Isso justifica toda a estrutura das recomendações: listas por bairro, não por cidade</li>
<li><strong>Como ler a árvore:</strong> raiz = primeiro corte (variável mais importante). Folhas coloridas = decisão final. Percentual = proporção da classe majoritária na folha.</li>
</ul>
<div class="hbox">"A árvore confirmou o que o K-Means sugeriu: a localização a nível de bairro é o fator geográfico mais discriminante do comportamento de compra — mais que CEP-3 ou cidade."</div></div>""")))

# 28 — Bloco 8
c28 = code_block("""# Baselines (mediana do universo)
med_vol = df_bairros['volume'].median()
med_pct = df_bairros['pct_recentes'].median()

# Estrela: alto volume + alta recência
estrela = df_bairros[
    (df_bairros['volume'] >= med_vol) &
    (df_bairros['pct_recentes'] >= med_pct)
].nlargest(10, 'clientes_recentes')

# Risco: alto volume + baixa recência
risco = df_bairros[
    (df_bairros['volume'] >= med_vol) &
    (df_bairros['pct_recentes'] < med_pct)
].nlargest(10, 'volume')

# Emergentes: baixo volume + boa recência
emergentes = df_bairros[
    (df_bairros['volume'] < med_vol) &
    (df_bairros['pct_recentes'] >= med_pct)
].nlargest(10, 'pct_recentes')""")
e28 = ["<strong>mediana como baseline</strong> — ponto de corte robusto (não sensível a outliers como a média)",
       "<strong>Estrela:</strong> alto volume E alta recência → já funciona, manter",
       "<strong>Risco:</strong> alto volume E baixa recência → muitos dormentes, maior ROI potencial",
       "<strong>Emergentes:</strong> baixo volume E boa recência → mercado novo, testar expansão"]
slides_html.append(slide(28, 3, "06 — As Recomendações", "code,output,concept", hdr("Bloco 8 — Recomendações: três listas priorizadas") +
  stepd(1, code2col(c28, e28, wide=True)) +
  stepd(2, out("ESTRELA (10 bairros): 2.808 clientes recentes\n  Ex: TIJUCA, COPACABANA, IPANEMA, BARRA DA TIJUCA\n\nRISCO (10 bairros): 5.435 clientes dormentes\n  Ex: CENTRO, GUARATIBA, TAQUARA, INHOAÍBA\n\nEMERGENTES (10 bairros): 682 participantes\n  Ex: bairros com alta % recentes, volume ainda baixo")) +
  stepd(3, """<div class="cbox"><h4>Framework 2×2 (estilo BCG)</h4>
<table class="mt"><tr><th>Volume</th><th>% Recentes Alta</th><th>% Recentes Baixa</th></tr>
<tr><td><strong>Alto</strong></td><td style="background:rgba(39,174,96,0.1);">★ Estrela — manter investimento, ROI garantido</td><td style="background:rgba(255,75,40,0.08);">⚠ Risco — reativação urgente, maior potencial</td></tr>
<tr><td><strong>Baixo</strong></td><td style="background:rgba(106,173,184,0.08);">↑ Emergente — testar expansão de mercado</td><td style="background:rgba(149,165,166,0.08);">? Massa — campanhas gerais sem prioridade</td></tr>
</table>
<div class="hbox" style="margin-top:10px;">Alocação sugerida: <strong>50% reativação</strong> (Risco, 5.435 dormentes) · <strong>35% manutenção</strong> (Estrela, 2.808 recentes) · <strong>15% expansão</strong> (Emergentes, 682 novos)</div></div>""")))

# 29 — Bloco 9 Plano de Ação
slides_html.append(slide(29, 2, "06 — As Recomendações", "output,concept", hdr("Bloco 9 — Top 5 prioridades imediatas","Plano de ação com volumes absolutos") +
  stepd(1, """<table class="action-table">
<thead><tr><th>#</th><th>Bairro</th><th>Volume</th><th>% Recentes</th><th>Dormentes</th><th>Canal</th><th>Ação</th></tr></thead>
<tbody>
<tr><td>1</td><td><strong>CENTRO</strong></td><td>2.009</td><td>24,9%</td><td>1.509</td><td>Meta Ads + WhatsApp</td><td style="color:#ff4b28;font-weight:700;">REATIVAR</td></tr>
<tr><td>2</td><td><strong>GUARATIBA</strong></td><td>1.028</td><td>23,9%</td><td>782</td><td>Meta Ads + WhatsApp</td><td style="color:#ff4b28;font-weight:700;">REATIVAR</td></tr>
<tr><td>3</td><td><strong>TAQUARA</strong></td><td>712</td><td>23,0%</td><td>548</td><td>Meta Ads + WhatsApp</td><td style="color:#ff4b28;font-weight:700;">REATIVAR</td></tr>
<tr><td>4</td><td><strong>INHOAÍBA</strong></td><td>621</td><td>24,0%</td><td>472</td><td>Meta Ads + WhatsApp</td><td style="color:#ff4b28;font-weight:700;">REATIVAR</td></tr>
<tr><td>5</td><td><strong>RAMOS</strong></td><td>619</td><td>24,7%</td><td>466</td><td>Meta Ads + WhatsApp</td><td style="color:#ff4b28;font-weight:700;">REATIVAR</td></tr>
</tbody>
</table>
<div class="hbox" style="margin-top:10px;">Total Top 5: <strong>3.777 clientes dormentes acionáveis</strong> — maiores volumes com maior potencial de reativação.</div>""") +
  stepd(2, """<div class="cbox"><h4>Alocação de orçamento — fundamentada em volumes absolutos</h4>
<div class="budget-bar">
<div class="budget-seg" style="flex:50;background:#ff4b28;">50% Reativação</div>
<div class="budget-seg" style="flex:35;background:#6aadb8;">35% Manutenção</div>
<div class="budget-seg" style="flex:15;background:#27ae60;">15% Expansão</div>
</div>
<table class="mt"><tr><th>Categoria</th><th>Clientes</th><th>Bairros</th><th>Orçamento</th></tr>
<tr><td>Reativação (Risco)</td><td>5.435 dormentes</td><td>10 bairros</td><td>50%</td></tr>
<tr><td>Manutenção (Estrela)</td><td>2.808 recentes</td><td>10 bairros</td><td>35%</td></tr>
<tr><td>Expansão (Emergentes)</td><td>682 participantes</td><td>10 bairros</td><td>15%</td></tr>
<tr><td><strong>Total acionável</strong></td><td><strong>8.925 clientes</strong></td><td>30 bairros</td><td>100%</td></tr>
</table></div>""")))

# 30 — Bloco 10
c30 = code_block("""# Exporta 5 arquivos CSV
df_bairros.to_csv(
    'tiers_por_bairro.csv',
    index=False, encoding='utf-8-sig')
bairros_estrela.to_csv(
    'bairros_estrela.csv',
    index=False, encoding='utf-8-sig')
bairros_risco.to_csv(
    'bairros_risco.csv',
    index=False, encoding='utf-8-sig')
bairros_emergentes.to_csv(
    'bairros_emergentes.csv',
    index=False, encoding='utf-8-sig')
plano_acao.to_csv(
    'plano_de_acao.csv',
    index=False, encoding='utf-8-sig')""")
e30 = ["<strong>tiers_por_bairro.csv</strong> — todos os 323 bairros com cluster e estatísticas",
       "<strong>bairros_estrela/risco/emergentes.csv</strong> — listas priorizadas para o time de marketing",
       "<strong>plano_de_acao.csv</strong> — Top 5 + canal + ação (vai direto para o time de mídias)",
       "<strong>encoding='utf-8-sig'</strong> — BOM (Byte Order Mark): Excel abre sem distorcer acentos"]
slides_html.append(slide(30, 2, "06 — As Recomendações", "code,concept", hdr("Bloco 10 — Exportação e reusabilidade") +
  stepd(1, code2col(c30, e30, wide=True)) +
  stepd(2, """<div class="cbox"><h4>Reusabilidade — um ativo permanente</h4>
<p><strong>Para usar com nova base de dados:</strong></p>
<ol><li>Troque <code style="font-family:'JetBrains Mono',monospace;">CAMINHO_CSV</code> no Bloco 0</li>
<li>Ajuste <code style="font-family:'JetBrains Mono',monospace;">UF_FOCO</code>, <code style="font-family:'JetBrains Mono',monospace;">DIAS_RECENTE</code>, <code style="font-family:'JetBrains Mono',monospace;">VOLUME_MIN</code> se necessário</li>
<li>Run All → 5 CSVs prontos, 13 gráficos gerados, 2 modelos treinados</li></ol>
<div class="hbox" style="margin-top:10px;">Sem reprogramação. Para qualquer produto futuro da Company Connection com as mesmas 5 colunas, o pipeline funciona completo em uma execução.</div></div>""")))

# 31 — Conclusão
slides_html.append(slide(31, 2, "07 — Conclusão", "concept,concept", hdr("De 100.365 linhas paradas para inteligência acionável") +
  stepd(1, """<div class="three-col">
<div class="cbox" style="border-top:3px solid #6aadb8;text-align:center;"><div style="font-size:28px;margin-bottom:8px;">📊</div><h4>De feeling para dados</h4><p>Marketing decide com base no perfil real da base — bairros priorizados por volume, engajamento e recência, não por intuição.</p></div>
<div class="cbox" style="border-top:3px solid #ff4b28;text-align:center;"><div style="font-size:28px;margin-bottom:8px;">🎯</div><h4>Plano dimensionado</h4><p>Cada recomendação vem com volume absoluto — 8.925 acionáveis, 3.777 só no Top 5. Orienta orçamento sem ambiguidade.</p></div>
<div class="cbox" style="border-top:3px solid #27ae60;text-align:center;"><div style="font-size:28px;margin-bottom:8px;">♻️</div><h4>Ativo permanente</h4><p>Script reutilizável para qualquer produto futuro. Troca o CSV, roda tudo — 5 CSVs prontos, 2 modelos, 13 gráficos.</p></div>
</div>""") +
  stepd(2, """<div class="cbox"><h4>Técnica → decisão de negócio (conexão com a matéria)</h4>
<table class="mt"><tr><th>Técnica</th><th>Bloco</th><th>Decisão de negócio</th></tr>
<tr><td>Limpeza NFKD + upper</td><td>2</td><td>Elimina duplicatas de bairro → métricas corretas</td></tr>
<tr><td>Recência derivada</td><td>3</td><td>Cria segmentação RECENTE/ANTIGO para ação imediata</td></tr>
<tr><td>CEP-3</td><td>3</td><td>Granularidade ideal para Meta Ads por região postal</td></tr>
<tr><td>K-Means (não supervisionado)</td><td>6</td><td>4 tiers de bairros com estratégia diferenciada</td></tr>
<tr><td>Árvore de Decisão</td><td>7</td><td>Bairro é o fator mais discriminante → foco correto</td></tr>
<tr><td>class_weight='balanced'</td><td>7</td><td>Modelo encontra RECENTES em base desbalanceada</td></tr>
<tr><td>3 listas + plano</td><td>8–9</td><td>50% reativação, 35% manutenção, 15% expansão</td></tr>
</table></div>""")))

# 32 — Q&A
slides_html.append(slide(32, 0, "", "", """
<div class="cover-layout">
  <div style="font-size:64px;font-weight:900;color:#1a1a2e;">Perguntas?</div>
  <div style="font-size:18px;color:#5a6a7a;max-width:500px;">Estamos prontos para detalhar qualquer bloco do pipeline, decisão metodológica ou resultado.</div>
  <div>
    <div class="cover-group-name">GRUPO 5</div>
    <div class="cover-members">Gabriel Maino Chamas · Gabriela Borsoi Cohen · Hyan Lucas Alves Fernandes<br>Isabelle de Brito Cavalcante · João Gabriel Stor Bittencourt · Malena Catallini</div>
  </div>
  <div class="cover-tag" style="margin-top:12px;">IBMEC RJ · IBM3297 · Análise de Dados · 2026.1</div>
</div>
""", "slide-hook"))

# 33 — CEP-3 Analysis
slides_html.append(slide(33, 3, "04 — O Que Descobrimos", "chart,concept,concept", hdr("Análise por CEP-3 — sub-regiões postais","Granularidade intermediária para mídia paga") +
  chart_step(1, "img_cep3_bar", "Top CEP-3 por volume. Cada barra = sub-região postal (primeiros 3 dígitos do CEP). Permite planejamento de mídia por macrozona geográfica.") +
  stepd(2, """<div class="cbox"><h4>Por que CEP-3 complementa bairro</h4><ul>
<li><strong>Bairro:</strong> granularidade máxima — 323 unidades. Melhor para campanhas hiper-locais</li>
<li><strong>CEP-3:</strong> 75 sub-regiões. Melhor para orçamento de alcance — uma segmentação cobre múltiplos bairros adjacentes</li>
<li><strong>Cidade:</strong> 1 unidade (quase tudo RJ). Inútil para segmentação</li>
</ul>
<div class="hbox">O CEP-3 é o elo entre a granularidade do bairro e a praticidade do planejamento de mídia paga. Meta Ads aceita segmentação por CEP — o CEP-3 define o raio.</div></div>""") +
  stepd(3, """<div class="cbox"><h4>Aplicação prática</h4>
<p>Um CEP-3 como '220' cobre Copacabana, Ipanema, Leblon — bairros com perfis similares. Uma campanha de Meta Ads com raio de 1km em cada CEP-3 do Top 10 cobre a maioria da base relevante sem pulverizar orçamento.</p>
<div class="wbox">Atenção: CEP-3 é uma <em>macro-região</em>, não um bairro. Dentro do mesmo CEP-3 pode haver bairros Estrela e bairros Em Declínio. Use CEP-3 para planejamento regional, execute por bairro.</div></div>""")))

# 34 — Validação
slides_html.append(slide(34, 3, "07 — Conclusão", "concept,concept,concept", hdr("Validação e limitações dos modelos") +
  stepd(1, """<div class="cbox"><h4>K-Means — como validamos</h4><ul>
<li><strong>Método do cotovelo:</strong> inércia × K — confirmou K=4 como ponto ótimo</li>
<li><strong>Interpretabilidade:</strong> 4 clusters nomeáveis, coerentes com o negócio</li>
<li><strong>Visualização:</strong> scatter plots confirmam separação clara no espaço 2D</li>
<li><strong>Sanity check:</strong> perfis de cluster fazem sentido (Núcleo = poucos bairros, alto volume)</li>
</ul>
<div class="hbox">K-Means não tem métrica de "acurácia" — é não supervisionado. Validação é qualitativa + elbow method.</div></div>""") +
  stepd(2, """<div class="cbox"><h4>Árvore — interpretação crítica</h4>
<p><strong>Acurácia de 63,2%</strong> — parece baixa? Contextualize:</p><ul>
<li>Sem balanced: 78% acurácia mas recall RECENTE = 0% — inútil para marketing</li>
<li>Com balanced: 63% mas recall RECENTE ≈ 59% — encontramos mais da metade dos recentes</li>
<li>Base: apenas 3 variáveis geográficas. Com frequência e valor seria muito melhor</li>
</ul>
<div class="wbox">O valor da Árvore neste projeto é <strong>interpretativo</strong>, não preditivo. A importância das variáveis (bairro &gt; CEP-3 &gt; cidade) é o achado real.</div></div>""") +
  stepd(3, """<div class="cbox"><h4>Limitações e próximos passos</h4>
<table class="mt"><tr><th>Limitação atual</th><th>Como superar</th></tr>
<tr><td>Apenas última compra (sem histórico)</td><td>Coletar frequência e valor para RFM completo</td></tr>
<tr><td>Sem dados demográficos</td><td>Enriquecer com censo IBGE por CEP</td></tr>
<tr><td>Produto descontinuado</td><td>Aplicar pipeline ao próximo produto assim que lançar</td></tr>
<tr><td>K-Means sensível a outliers</td><td>Testar DBSCAN para clusters de forma livre</td></tr>
</table></div>""")))

# 35 — Referências
slides_html.append(slide(35, 0, "07 — Conclusão", "", hdr("Referências e recursos","Fontes utilizadas no projeto") + """
<div class="two-col">
<div class="cbox"><h4>Metodologia e técnicas</h4><ul>
<li>Chapman, P. et al. (1999). <em>CRISP-DM 1.0 Step-by-step data mining guide</em>. SPSS Inc.</li>
<li>Scikit-learn documentation — KMeans, DecisionTreeClassifier, StandardScaler, LabelEncoder, train_test_split</li>
<li>Pandas documentation — groupby, agg, str.normalize (NFKD)</li>
<li>MacQueen, J. (1967). Some methods for classification of multivariate observations. <em>Proc. 5th Berkeley Symposium</em></li>
</ul></div>
<div class="cbox"><h4>Ferramentas utilizadas</h4><ul>
<li>Python 3.11 — linguagem principal</li>
<li>Pandas — manipulação e limpeza de dados</li>
<li>Scikit-learn — K-Means, Árvore de Decisão, métricas</li>
<li>Matplotlib + Seaborn — todas as 13 visualizações</li>
<li>Jupyter Notebook — ambiente de desenvolvimento</li>
</ul></div>
</div>
<div class="cbox" style="margin-top:12px;"><h4>Dados</h4>
<p>Base proprietária da Company Connection — produto Cap Mania, 2022–2025. 100.365 registros anonimizados em conformidade com a LGPD. Fornecidos exclusivamente para fins acadêmicos no contexto do curso IBM3297 — IBMEC RJ, 2026.1.</p></div>
"""))

# ── Assemble ──────────────────────────────────────────────────────────────────
all_slides = '\n'.join(slides_html)

html = f"""{HEAD}
<body>

{FIXED_UI}
<div id="presentation">
{all_slides}
</div><!-- /presentation -->

{JS_BLOCK}
</body>
</html>"""

OUT = '/home/user/PAD/.claude/worktrees/agent-a41e08b8b7f2f33fc/apresentacao.html'
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Written: {OUT}")
print(f"  Slides: {len(slides_html)}")
print(f"  Size:   {len(html):,} bytes")
print(f"  Images: {len(imgs)}")

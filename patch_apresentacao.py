#!/usr/bin/env python3
"""
Patch apresentacao.html:
1. Loader → fullscreen centered with spinner ring
2. Educational "concept" steps skip loader (instant reveal)
3. Richer educational content added to every slide
4. More descriptive loader status messages
"""

import re

with open('/home/user/PAD/apresentacao.html', encoding='utf-8') as f:
    html = f.read()

# ──────────────────────────────────────────────────────────
# 1. LOADER CSS: fullscreen centered + spinner
# ──────────────────────────────────────────────────────────
OLD_LOADER_CSS = """/* ============ LOADER ============ */
#exec-loader {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  height: 0; /* toggled via .visible */
  background: linear-gradient(to top, rgba(8,12,24,0.98) 60%, transparent 100%);
  display: flex; align-items: flex-end; justify-content: center;
  padding-bottom: 90px;
  z-index: 500;
  opacity: 0; pointer-events: none;
  transition: opacity 0.2s ease;
}
#exec-loader.visible {
  opacity: 1; pointer-events: all;
  height: 100vh;
}
.exec-loader-inner {
  display: flex; flex-direction: column; align-items: center; gap: 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-bright);
  border-radius: 14px;
  padding: 22px 40px;
  min-width: 320px;
  box-shadow: 0 4px 24px rgba(52,63,77,0.12), 0 1px 4px rgba(52,63,77,0.08);
}"""

NEW_LOADER_CSS = """/* ============ LOADER — fullscreen centered ============ */
#exec-loader {
  position: fixed; inset: 0;
  background: rgba(8,12,24,0.93);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999;
  opacity: 0; pointer-events: none;
  transition: opacity 0.28s ease;
}
#exec-loader.visible {
  opacity: 1; pointer-events: all;
}
/* Spinner ring */
.ldr-ring {
  width: 60px; height: 60px; border-radius: 50%;
  border: 5px solid rgba(106,173,184,0.18);
  border-top-color: #6aadb8;
  animation: spin-ldr 0.9s linear infinite;
}
@keyframes spin-ldr { to { transform: rotate(360deg); } }
.exec-loader-inner {
  display: flex; flex-direction: column; align-items: center; gap: 22px;
  background: rgba(20,30,48,0.98);
  border: 1px solid rgba(106,173,184,0.22);
  border-radius: 18px;
  padding: 48px 72px;
  min-width: 400px;
  box-shadow: 0 28px 72px rgba(0,0,0,0.65), 0 0 0 1px rgba(106,173,184,0.08);
}"""

html = html.replace(OLD_LOADER_CSS, NEW_LOADER_CSS)

# ──────────────────────────────────────────────────────────
# 2. LOADER HTML: add spinner div inside exec-loader-inner
# ──────────────────────────────────────────────────────────
OLD_LOADER_HTML = """<div id="exec-loader">
  <div class="exec-loader-inner">
    <div class="jupyter-cell-indicator">"""

NEW_LOADER_HTML = """<div id="exec-loader">
  <div class="exec-loader-inner">
    <div class="ldr-ring"></div>
    <div class="jupyter-cell-indicator">"""

html = html.replace(OLD_LOADER_HTML, NEW_LOADER_HTML)

# ──────────────────────────────────────────────────────────
# 3. progress-fill: wider track, better colors
# ──────────────────────────────────────────────────────────
html = html.replace(
    '.exec-progress-track {\n  width: 260px; height: 3px;',
    '.exec-progress-track {\n  width: 300px; height: 4px;'
)

# ──────────────────────────────────────────────────────────
# 4. exec-status: bigger and white
# ──────────────────────────────────────────────────────────
html = html.replace(
    '.exec-status {\n  font-size: 12px; color: var(--text-secondary);',
    '.exec-status {\n  font-size: 13px; color: rgba(255,255,255,0.85);'
)

# Make jupyter-cell-indicator white too
html = html.replace(
    '.cell-bracket { color: var(--text-muted); }',
    '.cell-bracket { color: rgba(255,255,255,0.5); }'
)

# ──────────────────────────────────────────────────────────
# 5. JS: status messages more descriptive
# ──────────────────────────────────────────────────────────
OLD_STATUS = """  // Step type → loader status message
  const STATUS_MESSAGES = {
    'code':   'Executando célula Python...',
    'output': 'Processando output...',
    'chart':  'Renderizando visualização...',
  };"""

NEW_STATUS = """  // Step type → loader status message
  const STATUS_MESSAGES = {
    'code':    'Executando célula Python...',
    'output':  'Processando output...',
    'chart':   'Renderizando visualização...',
    'concept': '',   // skips loader entirely
  };"""

html = html.replace(OLD_STATUS, NEW_STATUS)

# ──────────────────────────────────────────────────────────
# 6. JS advance(): concept steps skip loader, instant reveal
# ──────────────────────────────────────────────────────────
OLD_ADVANCE = """    if (currentStep < maxSteps) {
      const nextStep = currentStep + 1;
      const stepType = getStepType(currentSlide, nextStep);
      isAnimating = true;
      showLoader(stepType, () => {
        currentStep = nextStep;
        revealStep(currentStep);
        isAnimating = false;
      });
    } else {"""

NEW_ADVANCE = """    if (currentStep < maxSteps) {
      const nextStep = currentStep + 1;
      const stepType = getStepType(currentSlide, nextStep);
      isAnimating = true;
      if (stepType === 'concept') {
        // Instant reveal — no fake execution loader
        currentStep = nextStep;
        revealStep(currentStep);
        isAnimating = false;
      } else {
        showLoader(stepType, () => {
          currentStep = nextStep;
          revealStep(currentStep);
          isAnimating = false;
        });
      }
    } else {"""

html = html.replace(OLD_ADVANCE, NEW_ADVANCE)

# ──────────────────────────────────────────────────────────
# 7. Add CSS for concept steps (instant fade-in, no loader)
# ──────────────────────────────────────────────────────────
STEP_CSS = """.step {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.5s ease, transform 0.5s ease;
  pointer-events: none;
}
.step.revealed {
  opacity: 1;
  transform: none;
  pointer-events: all;
}"""

STEP_CSS_NEW = """.step {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.5s ease, transform 0.5s ease;
  pointer-events: none;
}
.step.revealed {
  opacity: 1;
  transform: none;
  pointer-events: all;
}
/* Concept reveal box */
.concept-reveal {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent-blue);
  border-radius: 0 10px 10px 0;
  padding: 18px 22px;
  margin-top: 14px;
}
.concept-reveal.amber { border-left-color: var(--accent-amber); }
.concept-reveal.green { border-left-color: var(--accent-green); }
.concept-reveal h4 {
  font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--accent-blue);
  margin-bottom: 8px;
}
.concept-reveal.amber h4 { color: var(--accent-amber); }
.concept-reveal.green h4 { color: var(--accent-green); }
.concept-reveal p, .concept-reveal li {
  font-size: 13.5px; color: var(--text-secondary);
  line-height: 1.7;
}
.concept-reveal ul { padding-left: 16px; }
.concept-reveal ul li { margin-bottom: 4px; }
.edu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; }
.edu-grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-top: 14px; }
.edu-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px 18px;
}
.edu-card h4 {
  font-size: 12px; font-weight: 700; color: var(--text-primary);
  margin-bottom: 8px;
}
.edu-card p { font-size: 13px; color: var(--text-secondary); line-height: 1.65; }
.edu-card code { font-family: 'JetBrains Mono',monospace; font-size: 11.5px;
  background: rgba(106,173,184,0.12); padding: 1px 5px; border-radius: 3px;
  color: var(--accent-cyan); }
.key-finding {
  background: linear-gradient(135deg, rgba(106,173,184,0.12), rgba(255,75,40,0.06));
  border: 1px solid rgba(106,173,184,0.3);
  border-radius: 12px; padding: 18px 22px; margin-top: 14px;
}
.key-finding h4 { font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--accent-blue); margin-bottom: 6px; }
.key-finding p { font-size: 14px; color: var(--text-primary); line-height: 1.65; font-weight: 500; }
.implication-box {
  background: rgba(255,75,40,0.07); border: 1px solid rgba(255,75,40,0.2);
  border-radius: 10px; padding: 14px 18px; margin-top: 12px;
}
.implication-box h4 { font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--accent-amber); margin-bottom: 6px; }
.implication-box p { font-size: 13.5px; color: var(--text-secondary); line-height: 1.65; }"""

html = html.replace(STEP_CSS, STEP_CSS_NEW)

# ──────────────────────────────────────────────────────────
# 8. SLIDE CONTENT ADDITIONS
#    Strategy: find the <!-- ========== SLIDE N+1 --> comment
#    and insert before it. Use unique anchors per slide.
# ──────────────────────────────────────────────────────────

def insert_before(html, anchor, content):
    """Insert `content` immediately before `anchor`."""
    if anchor not in html:
        print(f"  [WARN] anchor not found: {anchor[:60]}")
        return html
    return html.replace(anchor, content + '\n' + anchor, 1)

def bump_steps(html, slide_num, extra_steps, extra_types):
    """Increase data-steps and append to data-step-types for a slide."""
    # Find the slide opening tag
    pattern = f'data-slide="{slide_num}" data-steps="(\\d+)"(.*?)data-step-types="([^"]*)"'
    def replacer(m):
        old_steps = int(m.group(1))
        new_steps = old_steps + extra_steps
        old_types = m.group(3)
        new_types = old_types + ',' + extra_types if old_types else extra_types
        return f'data-slide="{slide_num}" data-steps="{new_steps}"{m.group(2)}data-step-types="{new_types}"'
    new_html = re.sub(pattern, replacer, html)
    # Also handle slides with no data-step-types yet
    if new_html == html:
        pattern2 = f'data-slide="{slide_num}" data-steps="(\\d+)"([^>]*?)>'
        def replacer2(m):
            old_steps = int(m.group(1))
            new_steps = old_steps + extra_steps
            rest = m.group(2)
            return f'data-slide="{slide_num}" data-steps="{new_steps}"{rest} data-step-types="{extra_types}">'
        new_html = re.sub(pattern2, replacer2, html)
    return new_html


# ── SLIDE 2: Company Connection ──────────────────────────
# Add 1 concept step explaining what this means for our project
ANCHOR_S2 = '<!-- ========== SLIDE 3: O PROBLEMA =========='
STEP_S2 = """  <div class="step step-1">
    <div class="concept-reveal amber">
      <h4>Por que isso importa para o nosso projeto?</h4>
      <p>A Company Connection é uma startup de 2024 que cresceu via influenciadores digitais mas <strong>nunca analisou seus próprios dados</strong>. A base do produto Cap Mania tem 100.365 registros acumulados — todos geográficos — que nunca viraram inteligência de marketing. <em>É exatamente esse gap que nossa análise resolve.</em></p>
    </div>
  </div>"""
html = bump_steps(html, 2, 1, 'concept')
html = insert_before(html, ANCHOR_S2, STEP_S2)


# ── SLIDE 3: Decisão no Feeling ─────────────────────────
ANCHOR_S3 = '<!-- ========== SLIDE 4: A BASE DE DADOS =========='
STEP_S3 = """  <div class="step step-1">
    <div class="key-finding">
      <h4>A pergunta central do nosso projeto</h4>
      <p>Como usar dados geográficos e comportamentais para <strong>identificar, segmentar e priorizar</strong> os 82.875 participantes do Cap Mania no Rio de Janeiro — transformando 5 colunas brutas em um plano de marketing acionável?</p>
    </div>
    <div class="edu-grid" style="margin-top:12px;">
      <div class="edu-card"><h4>🎯 Segmentação</h4><p>Agrupar bairros em perfis de comportamento usando K-Means clustering.</p></div>
      <div class="edu-card"><h4>📍 Priorização</h4><p>Identificar os 10 bairros com maior potencial de reativação imediata.</p></div>
      <div class="edu-card"><h4>🌱 Expansão</h4><p>Detectar bairros emergentes com alta proporção de clientes recentes.</p></div>
      <div class="edu-card"><h4>📊 Interpretação</h4><p>Usar Árvore de Decisão para entender <em>quais variáveis geográficas</em> mais explicam o comportamento.</p></div>
    </div>
  </div>"""
html = bump_steps(html, 3, 1, 'concept')
html = insert_before(html, ANCHOR_S3, STEP_S3)


# ── SLIDE 4: A Base (O Que Esperávamos) ─────────────────
# Already has 1 step. Add another explaining LGPD context.
ANCHOR_S4 = '<!-- ========== SLIDE 5: O ACHADO =========='
STEP_S4 = """  <div class="step step-2">
    <div class="edu-grid">
      <div class="concept-reveal">
        <h4>Por que não temos dados pessoais?</h4>
        <p>A LGPD (Lei Geral de Proteção de Dados) exige anonimização. A Company Connection entregou apenas dados geográficos e temporais — sem nome, CPF ou telefone. <em>Isso não é limitação: é oportunidade para mostrar o poder da análise geográfica.</em></p>
      </div>
      <div class="concept-reveal amber">
        <h4>O que 5 colunas podem revelar</h4>
        <p>Com bairro + CEP + data da última compra, conseguimos calcular <strong>recência</strong> (quando comprou), <strong>localização granular</strong> (bairro exato) e <strong>macro-região</strong> (primeiros 3 dígitos do CEP). Suficiente para segmentação completa.</p>
      </div>
    </div>
  </div>"""
html = bump_steps(html, 4, 1, 'concept')
html = insert_before(html, ANCHOR_S4, STEP_S4)


# ── SLIDE 5: 99,7% no RJ ────────────────────────────────
# Already has 1 step. Add another with what this means.
ANCHOR_S5 = '<!-- ========== SLIDE 6: O PIPELINE =========='
STEP_S5 = """  <div class="step step-2">
    <div class="edu-grid">
      <div class="concept-reveal green">
        <h4>Decisão metodológica: foco no RJ</h4>
        <p>Em vez de uma análise nacional com dados esparsos (apenas ~200 registros fora do RJ), optamos por <strong>profundidade sobre amplitude</strong>. Analisamos 82.875 registros do RJ em detalhe — bairro por bairro — produzindo insights acionáveis em vez de médias nacionais sem significado.</p>
      </div>
      <div class="concept-reveal">
        <h4>Impacto na modelagem</h4>
        <p>Concentrar no RJ garante <strong>representatividade estatística</strong> por bairro. Com ~82 mil participantes em ~323 bairros, cada bairro tem em média 256 registros — massa suficiente para K-Means e Árvore de Decisão produzirem resultados confiáveis.</p>
      </div>
    </div>
  </div>"""
html = bump_steps(html, 5, 1, 'concept')
html = insert_before(html, ANCHOR_S5, STEP_S5)


# ── SLIDE 6: O Pipeline ─────────────────────────────────
# Add 1 concept step explaining what each group produces
ANCHOR_S6 = '<!-- ========== SLIDE 7: BLOCO 1 CARREGAMENTO =========='
STEP_S6 = """  <div class="step step-1">
    <div class="concept-reveal">
      <h4>O que cada etapa produz</h4>
    </div>
    <div class="edu-grid" style="margin-top:10px;">
      <div class="edu-card"><h4>🔵 Fundação (Blocos 0–1)</h4><p>DataFrame com 100.365 linhas brutas. Primeira inspeção: tipos, nulos, encoding.</p></div>
      <div class="edu-card"><h4>🟣 Preparação (Blocos 2–3)</h4><p>DataFrame limpo de 82.875 registros + 3 novas features: <code>recencia_dias</code>, <code>status_recente</code>, <code>cep3</code>.</p></div>
      <div class="edu-card"><h4>🔵 Exploração (Blocos 4–5)</h4><p>13 gráficos revelando distribuição geográfica, temporal e de dormência — base para hipóteses.</p></div>
      <div class="edu-card"><h4>🟡 Modelagem (Blocos 6–7)</h4><p>323 bairros agrupados em 4 clusters (K-Means) + Árvore identificando variável mais importante.</p></div>
      <div class="edu-card"><h4>🟢 Entrega (Blocos 8–10)</h4><p>3 listas priorizadas + plano de ação + 5 CSVs exportados prontos para o marketing.</p></div>
    </div>
  </div>"""
html = bump_steps(html, 6, 1, 'concept')
html = insert_before(html, ANCHOR_S6, STEP_S6)


# ── SLIDE 7: Bloco 1 Carregamento ──────────────────────
# Already has 2 steps (code + output). Add 1 concept step.
ANCHOR_S7 = '<!-- ========== SLIDE 8: BLOCO 2 LIMPEZA =========='
STEP_S7 = """  <div class="step step-3">
    <div class="concept-reveal">
      <h4>O que essa inspeção inicial nos revela</h4>
      <p>Antes de qualquer análise, precisamos entender a <strong>saúde da base</strong>: há valores nulos? Encodings corretos? Distribuição de UFs esperada? Este bloco responde essas perguntas e define o ponto de partida do pipeline.</p>
    </div>
    <div class="edu-grid" style="margin-top:10px;">
      <div class="edu-card"><h4>📋 100.365 registros</h4><p>Volume robusto. Em ciência de dados, bases com mais de 50 mil registros já permitem modelos estatisticamente confiáveis.</p></div>
      <div class="edu-card"><h4>⚠️ Dado bruto</h4><p>Nomes de bairros com acentos misturados ("COPACABANA" vs "COPACABÂNA"), UFs potencialmente inválidas, datas em formatos variados. Limpeza obrigatória antes de qualquer modelo.</p></div>
    </div>
  </div>"""
html = bump_steps(html, 7, 1, 'concept')
html = insert_before(html, ANCHOR_S7, STEP_S7)


# ── SLIDE 8: Bloco 2 Limpeza ───────────────────────────
# Already has 2 steps. Add 1 educational concept step.
ANCHOR_S8 = '<!-- ========== SLIDE 9: BLOCO 3 ENGENHARIA =========='
STEP_S8 = """  <div class="step step-3">
    <div class="concept-reveal">
      <h4>Por que normalizar com NFKD? O princípio GIGO</h4>
      <p><strong>GIGO — Garbage In, Garbage Out.</strong> Se dois registros do mesmo bairro têm grafias diferentes ("IPANEMA" e "IPÂNEMA"), o modelo trata como dois bairros distintos. O Unicode NFKD decompõe caracteres acentuados em letra-base + acento, permitindo remover o acento de forma sistemática e universal.</p>
    </div>
    <div class="edu-grid" style="margin-top:10px;">
      <div class="edu-card"><h4>🔤 Normalização NFKD</h4><p><code>"IPÂNEMA"</code> → decompõe em <code>"IPANEMA" + acento</code> → remove acento → <code>"IPANEMA"</code>. Mesmo resultado para qualquer variação tipográfica.</p></div>
      <div class="edu-card"><h4>🗺️ Filtro UF válida</h4><p>Valida contra a lista oficial de 26 estados + DF do IBGE. Remove registros com UF inválida (erros de digitação) antes de filtrar para RJ.</p></div>
      <div class="edu-card"><h4>📉 100.365 → 82.875</h4><p>Redução de 17.490 registros (17,4%). Todos de outros estados ou com UF inválida. <em>Nenhum dado útil foi perdido — apenas ruído.</em></p></div>
    </div>
  </div>"""
html = bump_steps(html, 8, 1, 'concept')
html = insert_before(html, ANCHOR_S8, STEP_S8)


# ── SLIDE 9: Bloco 3 Engenharia ─────────────────────────
# Already has 2 steps. Add 1 educational step.
ANCHOR_S9 = '<!-- ========== SLIDE 10: EDA ONDE ESTÃO =========='
STEP_S9 = """  <div class="step step-3">
    <div class="concept-reveal">
      <h4>O que é Engenharia de Features — e por que importa</h4>
      <p>Dados brutos raramente falam diretamente com modelos de ML. A engenharia de features transforma informação bruta em variáveis com poder explicativo. Aqui transformamos <strong>1 coluna de data</strong> em <strong>2 variáveis analíticas ricas</strong>.</p>
    </div>
    <div class="edu-grid-3" style="margin-top:10px;">
      <div class="edu-card">
        <h4>📅 <code>recencia_dias</code></h4>
        <p>Dias desde a última compra. Calculado como <code>data_máx − data_compra</code>. Quanto maior, mais "esquecido" o cliente. Feature contínua — ideal para K-Means e Árvore.</p>
      </div>
      <div class="edu-card">
        <h4>🔴 <code>status_recente</code></h4>
        <p>Variável binária: <code>RECENTE</code> ≤ 365 dias, <code>ANTIGO</code> &gt; 365 dias. Simplifica a análise e torna campanhas acionáveis: um grupo comprou no último ano, o outro não.</p>
      </div>
      <div class="edu-card">
        <h4>📮 <code>cep3</code></h4>
        <p>3 primeiros dígitos do CEP = macro-região postal. <code>CEP 220xx</code> → Zona Sul. <code>CEP 215xx</code> → Zona Norte. Granularidade ideal para segmentação sem precisar do CEP completo.</p>
      </div>
    </div>
  </div>"""
html = bump_steps(html, 9, 1, 'concept')
html = insert_before(html, ANCHOR_S9, STEP_S9)


# ── SLIDE 10: EDA — A Zona Oeste Domina ─────────────────
# Already has 2 chart steps. Add 1 concept step with interpretation.
ANCHOR_S10 = '<!-- ========== SLIDE 11: EDA QUANDO COMPRARAM =========='
STEP_S10 = """  <div class="step step-3">
    <div class="key-finding">
      <h4>O que esse padrão revela para o marketing</h4>
      <p>A concentração na Zona Oeste (Campo Grande, Guaratiba, Bangu) contraria a intuição de que clientes de sorteios se concentram na Zona Sul. <strong>Isso é um dado estratégico valioso</strong>: campanhas de mídia paga devem ser geo-segmentadas para Zona Oeste, não para os bairros mais "nobres".</p>
    </div>
    <div class="implication-box">
      <h4>Implicação prática</h4>
      <p>Meta Ads e Google Ads permitem segmentação por bairro/CEP. Com este mapa de concentração, o time de marketing pode alocar orçamento onde há mais participantes — reduzindo CAC e aumentando taxa de conversão.</p>
    </div>
  </div>"""
html = bump_steps(html, 10, 1, 'concept')
html = insert_before(html, ANCHOR_S10, STEP_S10)


# ── SLIDE 11: EDA Temporal ──────────────────────────────
# Already has 1 chart step. Add 1 interpretation step.
ANCHOR_S11 = '<!-- ========== SLIDE 12: EDA QUEM AINDA COMPRA =========='
STEP_S11 = """  <div class="step step-2">
    <div class="concept-reveal amber">
      <h4>O que a sazonalidade nos diz</h4>
      <p>O pico de 2024 seguido de queda brusca marca o momento em que o produto Cap Mania foi descontinuado. Isso explica diretamente os <strong>78% de clientes "antigos"</strong>: não saíram por insatisfação, mas porque o produto simplesmente parou. <em>Isso aumenta enormemente o potencial de reativação.</em></p>
    </div>
    <div class="edu-grid" style="margin-top:10px;">
      <div class="edu-card"><h4>📈 Crescimento 2022–2024</h4><p>Base construída organicamente via influenciadores. Crescimento saudável indica que o produto funcionava — havia demanda real.</p></div>
      <div class="edu-card"><h4>📉 Queda em 2024</h4><p>Descontinuação do produto, não abandono voluntário dos clientes. Diferença crucial: cliente que saiu por escolha é harder to reactivate; cliente que "ficou dormindo" é receptivo.</p></div>
    </div>
  </div>"""
html = bump_steps(html, 11, 1, 'concept')
html = insert_before(html, ANCHOR_S11, STEP_S11)


# ── SLIDE 12: EDA — 77% Dormentes ───────────────────────
# Already has 2 steps. Add 1 concept step.
ANCHOR_S12 = '<!-- ========== SLIDE 13: HEATMAPS =========='
STEP_S12 = """  <div class="step step-3">
    <div class="concept-reveal">
      <h4>Como calculamos dormência — e o que fazer com 77%</h4>
      <p>Um cliente é classificado como <code>ANTIGO</code> se sua última compra foi há mais de 365 dias. Com 82.875 registros no RJ, isso significa <strong>~63.800 clientes dormentes</strong> — uma base enorme para campanha de reativação.</p>
    </div>
    <div class="edu-grid-3" style="margin-top:10px;">
      <div class="edu-card"><h4>🔴 Estratégia: Reativar</h4><p>Top 10 bairros com maior volume de ANTIGOS. Campanha urgente: oferta exclusiva para quem participou mas parou. 5.435 dormentes identificados nos top 10.</p></div>
      <div class="edu-card"><h4>🟢 Estratégia: Manter</h4><p>Top 10 bairros com maior proporção de RECENTES. Investimento em fidelização: manter quem está ativo ativo. 2.808 clientes recentes protegidos.</p></div>
      <div class="edu-card"><h4>🔵 Estratégia: Expandir</h4><p>Top 10 bairros emergentes: baixo volume mas alta % de recentes. Teste A/B com investimento pequeno para validar potencial. 682 participantes-semente.</p></div>
    </div>
  </div>"""
html = bump_steps(html, 12, 1, 'concept')
html = insert_before(html, ANCHOR_S12, STEP_S12)


# ── SLIDE 13: Heatmaps ──────────────────────────────────
# Already has 3 chart steps. Add 1 interpretation step.
ANCHOR_S13 = '<!-- ========== SLIDE 14: K-MEANS A PERGUNTA =========='
STEP_S13 = """  <div class="step step-4">
    <div class="key-finding">
      <h4>O que o heatmap revela que gráficos simples não revelam</h4>
      <p>Um gráfico de barras mostra <em>volume</em>. O heatmap mostra <strong>padrão comportamental</strong>: quais bairros têm alta concentração de ANTIGOS mesmo sendo populosos. Bairros no canto direito-inferior do heatmap (alto volume, baixa % recentes) são os alvos prioritários de reativação.</p>
    </div>
    <div class="implication-box">
      <h4>Implicação para o K-Means</h4>
      <p>O heatmap confirma que há heterogeneidade comportamental entre bairros — alguns têm clientes mais engajados que outros. Isso justifica a clusterização: os bairros não são todos iguais, e o K-Means vai quantificar essas diferenças.</p>
    </div>
  </div>"""
html = bump_steps(html, 13, 1, 'concept')
html = insert_before(html, ANCHOR_S13, STEP_S13)


# ── SLIDE 14: K-Means — A Pergunta ──────────────────────
# Currently 0 steps. Add 2 concept steps explaining K-Means deeply.
ANCHOR_S14 = '<!-- ========== SLIDE 15: K-MEANS COTOVELO =========='
STEP_S14A = """  <div class="step step-1">
    <div class="concept-reveal">
      <h4>O que é K-Means? Como funciona matematicamente?</h4>
      <p>K-Means é um algoritmo de <strong>aprendizado não supervisionado</strong> — encontra grupos nos dados <em>sem saber de antemão o que cada grupo significa</em>. O algoritmo escolhe K centróides aleatórios, atribui cada ponto ao centróide mais próximo, recalcula os centróides, e repete até convergência.</p>
    </div>
    <div class="edu-grid-3" style="margin-top:10px;">
      <div class="edu-card"><h4>1️⃣ Inicialização</h4><p>K centróides posicionados aleatoriamente no espaço de features.</p></div>
      <div class="edu-card"><h4>2️⃣ Atribuição</h4><p>Cada ponto é atribuído ao centróide mais próximo (distância Euclidiana).</p></div>
      <div class="edu-card"><h4>3️⃣ Atualização</h4><p>Centróides recalculados como médias dos pontos atribuídos. Repete até estabilizar.</p></div>
    </div>
  </div>
  <div class="step step-2">
    <div class="edu-grid">
      <div class="concept-reveal">
        <h4>Por que clusterizamos bairros, não pessoas?</h4>
        <p>Com produto descontinuado, indivíduos têm variabilidade comportamental baixa — quase todos são "antigos". Mas <strong>bairros preservam diferenças significativas</strong>: volume, recência média, proporção de ativos. Agregar por bairro amplifica o sinal e reduz ruído individual.</p>
      </div>
      <div class="concept-reveal amber">
        <h4>Por que usamos StandardScaler?</h4>
        <p>As 3 features têm escalas muito diferentes: volume (10–2000), recência (0–1000 dias), % recentes (0–1). Sem normalização, o K-Means seria dominado pela feature de maior escala. O StandardScaler transforma cada feature para média=0, desvio=1 — equalizando a influência de cada variável.</p>
      </div>
    </div>
  </div>"""
html = bump_steps(html, 14, 2, 'concept,concept')
html = insert_before(html, ANCHOR_S14, STEP_S14A)


# ── SLIDE 15: Cotovelo ──────────────────────────────────
# Already has 1 chart step. Add 1 interpretation step.
ANCHOR_S15 = '<!-- ========== SLIDE 16: K-MEANS 4 TIERS =========='
STEP_S15 = """  <div class="step step-2">
    <div class="concept-reveal">
      <h4>Por que K=4? O trade-off inércia vs. interpretabilidade</h4>
      <p>O Método do Cotovelo plota a <strong>inércia</strong> (soma das distâncias quadráticas de cada ponto ao seu centróide) para diferentes valores de K. A curva "dobra" em K=4 — adicionar o 5º cluster reduziria pouco a inércia mas aumentaria muito a complexidade de interpretação. K=4 maximiza o equilíbrio entre <em>qualidade da segmentação</em> e <em>acionabilidade para o marketing</em>.</p>
    </div>
  </div>"""
html = bump_steps(html, 15, 1, 'concept')
html = insert_before(html, ANCHOR_S15, STEP_S15)


# ── SLIDE 16: K-Means — 4 Tiers ─────────────────────────
# Already has 2 chart steps. Add 1 strategy step.
ANCHOR_S16 = '<!-- ========== SLIDE 17: ÁRVORE A PERGUNTA =========='
STEP_S16 = """  <div class="step step-3">
    <div class="concept-reveal green">
      <h4>O que fazer com cada cluster?</h4>
    </div>
    <div class="edu-grid" style="margin-top:10px;">
      <div class="edu-card"><h4>🏆 Núcleo Estratégico (6 bairros)</h4><p><strong>Ação: Manter e proteger.</strong> Mega-bairros com volume gigante. Qualquer churn aqui tem impacto enorme. Investimento em fidelização e presença constante de marca.</p></div>
      <div class="edu-card"><h4>🎯 Engajado (69 bairros)</h4><p><strong>Ação: Nutrir e converter.</strong> Melhor taxa de recentes (29,4%). São os candidatos a subir para Núcleo Estratégico. Campanhas de upsell e indicação.</p></div>
      <div class="edu-card"><h4>📊 Massa Padrão (162 bairros)</h4><p><strong>Ação: Eficiência de custo.</strong> Perfil médio — campanhas padronizadas. Monitorar para não deixar cair para Em Declínio.</p></div>
      <div class="edu-card"><h4>⚠️ Em Declínio (86 bairros)</h4><p><strong>Ação: Reativar urgente.</strong> Pior recência (19,6% recentes). Candidatos a campanhas de recuperação com oferta especial. Se não reagirem, reclassificar como perdidos.</p></div>
    </div>
  </div>"""
html = bump_steps(html, 16, 1, 'concept')
html = insert_before(html, ANCHOR_S16, STEP_S16)


# ── SLIDE 17: Árvore — A Pergunta ───────────────────────
# Currently 0 steps. Add 2 concept steps.
ANCHOR_S17 = '<!-- ========== SLIDE 18: ÁRVORE VISUALIZAÇÃO =========='
STEP_S17 = """  <div class="step step-1">
    <div class="concept-reveal">
      <h4>O que é Aprendizado Supervisionado? Como difere do K-Means?</h4>
      <p>K-Means é <strong>não supervisionado</strong>: descobre grupos sem rótulos. A Árvore de Decisão é <strong>supervisionada</strong>: usa rótulos conhecidos (os clusters do K-Means) para aprender <em>regras de decisão</em>. Em vez de descobrir grupos, aprende a explicar por que cada ponto pertence a cada grupo.</p>
    </div>
    <div class="edu-grid" style="margin-top:10px;">
      <div class="edu-card"><h4>🔀 Fluxo de dados</h4><p>K-Means cria labels (cluster 0, 1, 2, 3) para cada bairro → Árvore usa esses labels como variável-alvo para aprender regras geográficas.</p></div>
      <div class="edu-card"><h4>🌳 Como a árvore funciona</h4><p>Divide os dados em splits binários: "recência_dias ≤ 365?" → sim/não. Cada divisão maximiza a separação entre clusters. Max_depth=5 limita a profundidade para evitar overfitting.</p></div>
    </div>
  </div>
  <div class="step step-2">
    <div class="edu-grid">
      <div class="concept-reveal amber">
        <h4>Parâmetros que usamos e por quê</h4>
        <ul>
          <li><code>max_depth=5</code> — Árvore com no máximo 5 níveis. Mais profundo = mais complexo, menos interpretável.</li>
          <li><code>class_weight='balanced'</code> — Compensa o desbalanceamento entre clusters (6 vs 162 bairros). Garante que o cluster menor não seja ignorado.</li>
          <li><code>random_state=42</code> — Reproducibilidade. Mesmos dados → mesmo resultado.</li>
          <li>Split 70/30 com <code>stratify=y</code> — Mantém proporção de cada cluster em treino e teste.</li>
        </ul>
      </div>
      <div class="concept-reveal">
        <h4>O que o modelo entrega</h4>
        <p>A Árvore não é usada para <em>prever</em> clusters — ela é usada para <em>entender</em> quais variáveis geográficas mais distinguem os clusters. O valor é <strong>interpretativo</strong>, não preditivo. Acurácia baixa é esperada e aceitável nesse contexto.</p>
      </div>
    </div>
  </div>"""
html = bump_steps(html, 17, 2, 'concept,concept')
html = insert_before(html, ANCHOR_S17, STEP_S17)


# ── SLIDE 19: Árvore — O Achado ─────────────────────────
# Already has 1 chart step. Add 1 critical analysis step.
ANCHOR_S19 = '<!-- ========== SLIDE 20: AS TRÊS LISTAS =========='
STEP_S19 = """  <div class="step step-2">
    <div class="concept-reveal amber">
      <h4>Por que acurácia baixa não invalida o modelo — análise crítica</h4>
      <p>Com 4 clusters e base majoritariamente "antiga" (produto descontinuado), prever cluster individual é estruturalmente difícil. Uma acurácia aleatória seria 25%. Qualquer resultado acima disso já agrega valor — e o ganho aqui é <strong>interpretativo</strong>: saber que <em>bairro importa mais que CEP-3</em> é uma decisão estratégica de segmentação.</p>
    </div>
    <div class="edu-grid" style="margin-top:10px;">
      <div class="edu-card"><h4>📏 Baseline: 25%</h4><p>Com 4 classes balanceadas, um chute aleatório acertaria 25% das vezes. Qualquer acurácia acima disso é aprendizado real.</p></div>
      <div class="edu-card"><h4>🎯 Valor real: importância</h4><p>O <code>feature_importances_</code> da scikit-learn revela quais variáveis a árvore usou mais para splits. Esse é o insight estratégico que importa.</p></div>
      <div class="edu-card"><h4>💡 Conclusão</h4><p>Segmentar campanhas por <strong>bairro</strong> (não cidade, não CEP completo) é a decisão mais fundamentada em dados que a Company Connection pode tomar.</p></div>
    </div>
  </div>"""
html = bump_steps(html, 19, 1, 'concept')
html = insert_before(html, ANCHOR_S19, STEP_S19)


# ── SLIDE 20: As Três Listas ─────────────────────────────
# Currently 0 steps. Add 3 concept steps (one per list, revealed progressively).
ANCHOR_S20 = '<!-- ========== SLIDE 21: PLANO DE AÇÃO =========='
STEP_S20 = """  <div class="step step-1">
    <div class="concept-reveal green">
      <h4>🟢 Top 10 Estrela — MANTER (2.808 clientes recentes)</h4>
      <p>Bairros com alto volume E alta % de recentes. São os bairros âncora — onde a base ainda está ativa. <strong>Estratégia: manutenção + upsell.</strong> Campanhas de fidelização, programa de indicação, investimento contínuo em mídia geo-segmentada.</p>
      <p style="margin-top:8px;font-size:13px;color:var(--text-muted);">Exemplos: Copacabana, Ipanema, Tijuca — alta densidade, clientes recentes.</p>
    </div>
  </div>
  <div class="step step-2">
    <div class="concept-reveal" style="border-left-color:var(--accent-amber);">
      <h4 style="color:var(--accent-amber);">🔴 Top 10 Em Risco — REATIVAR (5.435 clientes dormentes)</h4>
      <p>Bairros com alto volume MAS baixa % de recentes. Maior potencial de retorno imediato — são clientes que <em>já compraram antes</em> e pararam quando o produto foi descontinuado. <strong>Estratégia: campanha de reativação urgente</strong> com oferta especial via Meta Ads + WhatsApp.</p>
      <p style="margin-top:8px;font-size:13px;color:var(--text-muted);">Centro, Guaratiba, Campo Grande, Santa Cruz, Bangu — Zona Oeste domina esta lista.</p>
    </div>
  </div>
  <div class="step step-3">
    <div class="concept-reveal">
      <h4>🔵 Top 10 Emergentes — EXPANDIR (682 participantes)</h4>
      <p>Bairros com baixo volume MAS alta % de recentes. São mercados inexplorados com alta propensão a comprar. <strong>Estratégia: testes A/B</strong> com investimento pequeno — validar se o potencial se confirma antes de comprometer orçamento maior.</p>
      <p style="margin-top:8px;font-size:13px;color:var(--text-muted);">Volume baixo = menos histórico, mais risco. Por isso: testar antes de escalar.</p>
    </div>
    <div class="key-finding" style="margin-top:12px;">
      <h4>Total acionável via as 3 listas</h4>
      <p><strong>8.925 clientes</strong> identificados, priorizados e segmentados com estratégia específica para cada grupo. Entregue como 3 CSVs prontos para importar no Meta Ads.</p>
    </div>
  </div>"""
html = bump_steps(html, 20, 3, 'concept,concept,concept')
html = insert_before(html, ANCHOR_S20, STEP_S20)


# ── SLIDE 21: Plano de Ação ──────────────────────────────
# Currently 0 steps. Add 1 step with budget framework.
ANCHOR_S21 = '<!-- ========== SLIDE 22: ENCERRAMENTO =========='
STEP_S21 = """  <div class="step step-1">
    <div class="key-finding">
      <h4>Lógica de alocação de orçamento baseada em dados</h4>
      <p><strong>50% Reativação · 35% Manutenção · 15% Expansão.</strong> A distribuição reflete o potencial dimensionado de cada grupo: 5.435 dormentes &gt; 2.808 ativos &gt; 682 emergentes. O único parâmetro que o marketing precisa definir é o orçamento total — o script calcula automaticamente o custo por bairro.</p>
    </div>
    <div class="edu-grid" style="margin-top:12px;">
      <div class="edu-card"><h4>📊 CAC estimado</h4><p>Com Meta Ads geo-segmentado, custo por resultado em bairros mapeados tende a ser 20–40% menor do que campanhas nacionais genéricas.</p></div>
      <div class="edu-card"><h4>🔄 Reutilizável</h4><p>Quando a Company Connection lançar um novo produto, basta trocar o CSV e rodar o notebook. Em minutos, novas listas priorizadas prontas para o marketing.</p></div>
      <div class="edu-card"><h4>📈 Mensurabilidade</h4><p>Cada bairro tem baseline de clientes e % recentes documentados. Após a campanha, comparar com novo CSV para medir conversão real por bairro.</p></div>
    </div>
  </div>"""
html = bump_steps(html, 21, 1, 'concept')
html = insert_before(html, ANCHOR_S21, STEP_S21)


# ──────────────────────────────────────────────────────────
# 9. Update TOTAL_SLIDES count  (kept at 22 — we didn't add new slides)
# ──────────────────────────────────────────────────────────
# No change needed

# ──────────────────────────────────────────────────────────
# 10. Write result
# ──────────────────────────────────────────────────────────
with open('/home/user/PAD/apresentacao.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done! {len(html):,} chars written.")

# Quick sanity checks
ok = []
ok.append(('fullscreen loader', 'position: fixed; inset: 0;' in html))
ok.append(('spinner ring', 'ldr-ring' in html))
ok.append(('concept skip', "stepType === 'concept'" in html))
ok.append(('GIGO explanation', 'GIGO' in html))
ok.append(('K-Means concept', 'StandardScaler' in html))
ok.append(('árvore critical', 'acurácia baixa' in html))
ok.append(('3 listas steps', 'Top 10 Estrela' in html))

for label, passed in ok:
    print(f"  {'✓' if passed else '✗'} {label}")

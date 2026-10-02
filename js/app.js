// ============================================================
// FUNCIONALIDADES DO SITE — Compreendendo a Bíblia
// ============================================================

// ============ UTILITÁRIOS ============

function getElement(id) {
  return document.getElementById(id);
}

function createElement(tag, className, content) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (content) el.innerHTML = content;
  return el;
}

// ============ HEADER MOBILE ============

function initNavToggle() {
  const toggle = getElement('navToggle');
  const nav = getElement('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
  }
}

// ============ PÁGINA INICIAL ============

function renderHomePage() {
  const app = getElement('app');
  if (!app) return;

  const licaoAtual = LICOES[0];
  // Capítulos do estudo "A Bíblia" (mesma fonte do tema-biblia.html)
  const fonte = (window.TEMA_BIBLIA && window.TEMA_BIBLIA.capitulos)
    ? window.TEMA_BIBLIA
    : (window.DataLoader && DataLoader.getCapitulos && DataLoader.getCapitulos()) || {};
  const capitulosDestaque = (fonte.capitulos || []).filter(c => c && c.secoes && c.secoes.length > 0);


  app.innerHTML = `
    <section class="hero">
      <div class="hero-content">
        <h1>Compreendendo a Bíblia</h1>
        <p>Estudos bíblicos por temas, lições da Escola Sabatina e perguntas e respostas para aprofundar sua fé.</p>
        <div class="hero-cta">
          <a href="licoes.html" class="btn btn-primary">Lição da Semana</a>
          <a href="tema-biblia.html" class="btn btn-outline">Estudos por Tema</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="licao-destaque">
          <span class="badge">Lição da Semana</span>
          <h2>${licaoAtual.titulo}</h2>
          <div class="versiculo">${licaoAtual.versiculo}</div>
          <p>${licaoAtual.resumo}</p>
          <a href="licoes.html" class="btn btn-primary">Estudar Agora</a>
        </div>

        <div class="section-title">
          <h2>Estudos em Destaque</h2>
          <p>Capítulos do estudo A Bíblia — perguntas e respostas</p>
        </div>

                <div class="cards-grid">
          ${capitulosDestaque.length ? capitulosDestaque.map(capitulo => {
            const capId = capitulo.id || 'capitulo';
            const nSecoes = capitulo.secoes.length;
            const nPerg = capitulo.secoes.reduce((acc, s) => acc + (s.perguntas ? s.perguntas.length : 0), 0);
            const primeiraSecao = capitulo.secoes[0].titulo || '';
            return `
            <div class="card">
              <span class="card-badge">A Bíblia</span>
              <h3>${capitulo.titulo || capId}</h3>
              <div class="versiculo">${primeiraSecao}</div>
              <p>${nSecoes} seções · ${nPerg} perguntas</p>
              <div class="card-footer">
                <a href="tema-biblia.html#${capId}" class="btn btn-primary btn-small">Estudar</a>
              </div>
            </div>
          `}).join('') : `
            <div class="card">
              <h3>Em breve</h3>
              <p>Novos capítulos deste estudo estarão disponíveis em breve.</p>
            </div>
          `}
        </div>
      </div>
    </section>
  `;
}

// ============ PÁGINA DE LIÇÕES ============

// Verificar se a lição está disponível (baseado no site da CPB)
function isLicaoAvailable(licao) {
  // Data atual
  const hoje = new Date();
  
  // Data de início da lição (extraída do campo data)
  // Formato esperado: "28 de Setembro de 2026"
  const dataLicao = parseDataLicao(licao.data);
  
  if (!dataLicao) return true; // Se não conseguir parsear, mostra a lição
  
  // A lição está disponível se a data atual for >= data da lição
  return hoje >= dataLicao;
}

// Parse da data da lição
function parseDataLicao(dataStr) {
  const meses = {
    'janeiro': 0, 'fevereiro': 1, 'março': 2, 'abril': 3,
    'maio': 4, 'junho': 5, 'julho': 6, 'agosto': 7,
    'setembro': 8, 'outubro': 9, 'novembro': 10, 'dezembro': 11
  };
  
  // Formato: "28 de Setembro de 2026"
  const match = dataStr.match(/(\d+)\s+de\s+(\w+)\s+de\s+(\d{4})/i);
  if (!match) return null;
  
  const dia = parseInt(match[1]);
  const mes = meses[match[2].toLowerCase()];
  const ano = parseInt(match[3]);
  
  if (mes === undefined) return null;
  
  return new Date(ano, mes, dia);
}

function renderLicoesPage() {
  const app = getElement('app');
  if (!app) return;

  // Filtrar lições disponíveis
  const licoesDisponiveis = LICOES.filter(licao => isLicaoAvailable(licao));

  app.innerHTML = `
    <section class="section" style="padding-top: 40px;">
      <div class="container">
        <div class="section-title">
          <h2>Lições da Escola Sabatina</h2>
          <p>Estude a lição de cada semana e aprofunde-se na Palavra de Deus</p>
        </div>

        <div class="cards-grid">
          ${licoesDisponiveis.map((licao, index) => `
            <div class="card">
              <span class="card-badge">Lição ${LICOES.indexOf(licao) + 1} - 4º Trimestre 2026</span>
              <h3>${licao.titulo}</h3>
              <div class="versiculo">${licao.versiculo}</div>
              <p>${licao.resumo}</p>
              <div class="card-footer">
                <span class="card-date">${licao.data}</span>
                <a href="estudo-detalhe.html?tipo=licao&id=${licao.id}" class="btn btn-primary btn-small">Estudar</a>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    </section>
  `;
}

// ============ PÁGINA DE ESTUDOS ============

function renderEstudosPage() {
  const app = getElement('app');
  if (!app) return;

  app.innerHTML = `
    <section class="section" style="padding-top: 40px;">
      <div class="container">
        <div class="section-title">
          <h2>Estudos Bíblicos</h2>
          <p>Estudos organizados por temas para sua edificação espiritual</p>
        </div>

        <div class="cards-grid">
          <div class="card estudo-card" onclick="window.location.href='tema-biblia.html'">
            <span class="card-badge">A Bíblia</span>
            <h3>${TEMA_BIBLIA.titulo}</h3>
            <div class="versiculo">${TEMA_BIBLIA.descricao}</div>
            <p>Estudo completo sobre como estudar e compreender as Escrituras Sagradas.</p>
            <div class="card-footer">
              <a href="tema-biblia.html" class="btn btn-primary btn-small">Estudar</a>
            </div>
          </div>
        </div>
      </div>
    </section>
  `;
}

function renderEstudosCards(estudos) {
  if (estudos.length === 0) return '';
  return estudos.map(estudo => `
    <div class="card">
      <span class="card-badge">${estudo.tema}</span>
      <h3>${estudo.titulo}</h3>
      <div class="versiculo">${estudo.versiculo}</div>
      <p>${estudo.resumo}</p>
      <div class="card-footer">
        <a href="estudo-detalhe.html?id=${estudo.id}" class="btn btn-primary btn-small">Ler Estudo</a>
      </div>
    </div>
  `).join('');
}

function initEstudosFilters() {
  const searchInput = getElement('searchInput');
  const filterTags = getElement('filterTags');
  const grid = getElement('estudosGrid');
  const emptyState = getElement('emptyState');

  let temaAtual = 'Todos';
  let buscaAtual = '';

  function filtrar() {
    let resultados = ESTUDOS;

    if (temaAtual !== 'Todos') {
      resultados = resultados.filter(e => e.tema === temaAtual);
    }

    if (buscaAtual) {
      const termo = buscaAtual.toLowerCase();
      resultados = resultados.filter(e =>
        e.titulo.toLowerCase().includes(termo) ||
        e.resumo.toLowerCase().includes(termo) ||
        e.versiculo.toLowerCase().includes(termo)
      );
    }

    grid.innerHTML = renderEstudosCards(resultados);
    emptyState.style.display = resultados.length === 0 ? 'block' : 'none';
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      buscaAtual = e.target.value;
      filtrar();
    });
  }

  if (filterTags) {
    filterTags.addEventListener('click', (e) => {
      if (e.target.classList.contains('filter-tag')) {
        filterTags.querySelectorAll('.filter-tag').forEach(tag => tag.classList.remove('active'));
        e.target.classList.add('active');
        temaAtual = e.target.dataset.tema;
        filtrar();
      }
    });
  }
}

// ============ PÁGINA DE DETALHE ============

function renderDetalhePage() {
  const app = getElement('app');
  if (!app) return;

  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id')) || 1;
  const tipo = params.get('tipo') || 'estudo';

  let item;
  let tipoLabel;

  if (tipo === 'licao') {
    item = LICOES.find(l => l.id === id) || LICOES[0];
    tipoLabel = 'Lição da Escola Sabatina';
  } else {
    item = ESTUDOS.find(e => e.id === id) || ESTUDOS[0];
    tipoLabel = 'Estudo Bíblico';
  }

  const isLicao = tipo === 'licao';
  const lista = isLicao ? LICOES : ESTUDOS;
  const currentIndex = lista.findIndex(i => i.id === item.id);
  const prevItem = currentIndex > 0 ? lista[currentIndex - 1] : null;
  const nextItem = currentIndex < lista.length - 1 ? lista[currentIndex + 1] : null;

  const detalheUrl = (item) => {
    return isLicao
      ? `estudo-detalhe.html?tipo=licao&id=${item.id}`
      : `estudo-detalhe.html?id=${item.id}`;
  };

  // Verificar se é lição e tem abertura
  const abertura = isLicao && item.abertura ? item.abertura : null;

  app.innerHTML = `
    <div class="detalhe-header">
      <span class="card-badge" style="background: var(--secondary); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">${tipoLabel}</span>
      <h1>${item.titulo}</h1>
      <div class="versiculo">${item.versiculo}</div>
    </div>

    <div class="detalhe-content">
      ${abertura ? `
        <div class="abertura-licao">
          <div class="abertura-versiculo">${abertura.versiculo}</div>
          <div class="abertura-periodo">Período: ${abertura.periodo}</div>
          <div class="abertura-resumo">${abertura.resumo}</div>
          <div class="abertura-reflexao">${abertura.reflexao}</div>
        </div>
      ` : `
        <div class="texto-biblico">
          ${item.texto}
          <span class="ref">${item.versiculo}</span>
        </div>
      `}

      ${isLicao ? `
        <div style="text-align: center; margin: 24px 0;">
          <a href="estudo-professor.html" class="btn btn-primary" style="background: var(--secondary);">
            📚 Estudo para Professores
          </a>
        </div>
      ` : ''}

      <div class="perguntas-section">
        <h2>Perguntas e Respostas</h2>
        ${item.perguntas.map((p, i) => `
          <div class="pergunta-card" id="pergunta-${i}">
            <div class="pergunta-header">
              <span class="pergunta-numero">${i + 1}</span>
              <span class="pergunta-texto">${p.pergunta}</span>
            </div>
            <div class="pergunta-content">
              <div class="resposta-biblia">
                <button class="btn-resposta" onclick="toggleResposta(${i})">
                  <span class="icone-resposta">+</span>
                  Ver Resposta
                </button>
                <div class="resposta-conteudo" id="resposta-${i}">
                  <strong>Resposta:</strong> ${p.resposta}
                </div>
              </div>
            </div>
          </div>
        `).join('')}
      </div>

      ${isLicao && item.estudoProfessor ? `
        <div style="text-align: center; margin: 32px 0;">
          <a href="estudo-professor.html?id=${item.id}" class="btn btn-primary" style="font-size: 1.1rem; padding: 16px 32px;">
            Estudo para Professores
          </a>
        </div>
      ` : ''}

      <div class="navegacao-licoes">
        ${prevItem
          ? `<a href="${detalheUrl(prevItem)}" class="nav-licao">← ${prevItem.titulo}</a>`
          : `<span class="nav-licao disabled">← Anterior</span>`
        }
        <a href="${isLicao ? 'licoes.html' : 'estudos.html'}" class="btn btn-outline" style="color: var(--primary); border-color: var(--primary);">Voltar à Lista</a>
        ${nextItem
          ? `<a href="${detalheUrl(nextItem)}" class="nav-licao">${nextItem.titulo} →</a>`
          : `<span class="nav-licao disabled">Próximo →</span>`
        }
      </div>
    </div>

    <button class="back-to-top" id="backToTop" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">↑</button>
  `;
}

// ============ PÁGINA TEMA BÍBLIA (nova versão) ============
// Estado: capítulo/seção/seleção atuais e tradução escolhida
let temaBibliaState = {
  capitulo: 0,
  secao: 0,
  versao: 'naa'
};

// Monta uma única seção (capítulo e índice) com o seletor de tradução
function renderSecaoHTML(capitulo, secaoIndex) {
  const secoes = capitulo.secoes || [];
  const secao = secoes[secaoIndex] || {};
  const versao = temaBibliaState.versao;
  const perguntas = secao.perguntas || [];

  const tabs = ['naa', 'ntlh', 'nvi', 'acf'].map(v =>
    `<button class="versao-tab ${v === versao ? 'active' : ''}" onclick="trocarVersaoTema('${v}')">${v.toUpperCase()}</button>`
  ).join('');

  return `
    <div class="versao-global">
      <div class="versao-global-titulo">${capitulo.titulo} — ${limparTituloSecao(secao.titulo)}</div>
      <div class="versao-global-tabs">${tabs}</div>
    </div>

    <div class="perguntas-section">
      ${perguntas.map((p, i) => {
        const texto = (p.versoes && p.versoes[versao]) ? p.versoes[versao] : (p.texto || '');
        return `
          <div class="biblia-pergunta" id="pergunta-${secaoIndex}-${i}">
            <div class="pergunta-header">
              <span class="pergunta-numero">${p.numero}</span>
              <span class="pergunta-texto">${p.pergunta}</span>
            </div>
            <div class="pergunta-content">
              <div class="versiculo-biblia">
                <strong>${p.versiculo} (${versao.toUpperCase()})</strong>
                <p>${texto}</p>
              </div>
              <div class="resposta-biblia">
                <button class="btn-resposta" onclick="toggleRespostaCapitulo(${secaoIndex}, ${i})">
                  <span class="icone-resposta">+</span> Ver Resposta
                </button>
                <div class="resposta-conteudo" id="resposta-${secaoIndex}-${i}">
                  <strong>Resposta:</strong> ${p.resposta}
                </div>
              </div>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

// Renderiza a página (cabeçalho + conteúdo da seção atual no centro)
function renderTemaBibliaPage() {
  const app = getElement('app');
  if (!app) return;

  const fonte = (typeof TEMA_BIBLIA !== 'undefined' && TEMA_BIBLIA && TEMA_BIBLIA.capitulos)
    ? TEMA_BIBLIA
    : (DataLoader.getCapitulos && DataLoader.getCapitulos()) || {};

  const capitulos = fonte.capitulos || [];

  if (capitulos.length === 0) {
    app.innerHTML = `
      <div class="detalhe-header">
        <span class="card-badge">Tema</span>
        <h1>${fonte.titulo || 'Tema'}</h1>
        <div class="versiculo">Nenhum capítulo encontrado.</div>
      </div>
      <div class="detalhe-content">
        <a href="estudos.html" class="nav-licao">← Voltar aos Estudos</a>
      </div>
    `;
    renderTemaSidebar(capitulos);
    initTemaSidebarToggle();
    return;
  }

  const hashCap = window.location.hash.replace('#', '');
  const porHash = capitulos.findIndex(c => c && c.id === hashCap);
  const primeiroReal = capitulos.findIndex(c => c && c.secoes && c.secoes.length > 0);
  temaBibliaState.capitulo = porHash >= 0 ? porHash : (primeiroReal >= 0 ? primeiroReal : 0);
  temaBibliaState.secao = 0;

  app.innerHTML = `
    <div class="detalhe-header">
      <span class="card-badge" style="background: var(--secondary); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">Tema</span>
      <h1>${fonte.titulo}</h1>
      <div class="versiculo">${fonte.descricao}</div>
    </div>

    <div class="detalhe-content" id="tema-conteudo">
      ${renderSecaoHTML(capitulos[0], 0)}
    </div>

    <div class="navegacao-licoes">
      <a href="estudos.html" class="nav-licao">← Voltar aos Estudos</a>
    </div>

    <button class="back-to-top" id="backToTop" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">↑</button>
  `;

  renderTemaSidebar(capitulos);
  initTemaSidebarToggle();
}

// Limpa o título da seção para o padrão "2.1 Título"
function limparTituloSecao(titulo) {
  if (!titulo) return '';
  let t = String(titulo).trim();
  // Remove sufixos: "- estudado dia 20/06/2020", "- 27/06/2020", "- Estudo em casa"
  t = t.replace(/\s*-\s*[Ee]studado\s+(?:dia\s+)?[\d/]+\s*$/, '');
  t = t.replace(/\s*-\s*\d{1,2}\/\d{1,2}\/\d{2,4}\s*$/, '');
  t = t.replace(/\s*-\s*[Ee]studo\s+em\s+casa\s*$/i, '');
  // Padroniza "N.M - Título" -> "N.M Título"
  t = t.replace(/^(\d+\.\d+)\s*-\s*(.+)$/, '$1 $2');
  return t.trim();
}


// Aba lateral com capítulos expansíveis (acordeão)
function renderTemaSidebar(capitulos) {
  const nav = getElement('temaSidebarNav');
  if (!nav) return;
  let html = '';
  let qtVazios = 0;
  capitulos.forEach((capitulo, i) => {
    const secoes = (capitulo && capitulo.secoes) || [];
    if (secoes.length === 0) { qtVazios++; return; }
    const secaoAtiva = (i === temaBibliaState.capitulo);
    html += `
      <div class="tema-capitulo ${secaoAtiva ? 'open' : ''}">
        <button class="tema-capitulo-btn" onclick="toggleTemaCapitulo(${i}, this)">
          <span class="tema-capitulo-seta">${secaoAtiva ? '▾' : '▸'}</span>
          ${capitulo.titulo}
        </button>
        <div class="tema-secoes ${secaoAtiva ? 'aberto' : ''}">
          ${secoes.map((secao, s) => `
            <button class="tema-secao-btn ${i === temaBibliaState.capitulo && s === temaBibliaState.secao ? 'active' : ''}"
                    onclick="abrirSecaoTema(${i}, ${s})">${limparTituloSecao(secao.titulo)}</button>
          `).join('')}
        </div>
      </div>`;
  });
  if (qtVazios > 0) {
    html += `<div class="tema-em-breve">⏳ Em breve teremos mais capítulos deste estudo.</div>`;
  }
  nav.innerHTML = html;
}


// Expande/recolhe um capítulo; abre a 1ª seção se ainda não houver nenhuma aberta
function toggleTemaCapitulo(c, btn) {
  const item = btn.closest('.tema-capitulo');
  if (!item) return;
  const aberto = item.classList.contains('open');
  // Fecha todos e abre só o clicado (acordeão)
  document.querySelectorAll('.tema-capitulo').forEach(el => {
    el.classList.remove('open');
    el.querySelector('.tema-capitulo-seta').textContent = '▸';
    el.querySelector('.tema-secoes').classList.remove('aberto');
  });
  if (!aberto) {
    item.classList.add('open');
    btn.querySelector('.tema-capitulo-seta').textContent = '▾';
    item.querySelector('.tema-secoes').classList.add('aberto');
  }
}



// Ao clicar numa seção da lateral: guarda o estado e re-renderiza o centro
function abrirSecaoTema(c, s) {
  temaBibliaState.capitulo = c;
  temaBibliaState.secao = s;

  const capitulos = (typeof TEMA_BIBLIA !== 'undefined' && TEMA_BIBLIA && TEMA_BIBLIA.capitulos)
    ? TEMA_BIBLIA.capitulos
    : (DataLoader.getCapitulos && DataLoader.getCapitulos().capitulos) || [];

  const capitulo = capitulos[c] || {};
  const conteudo = getElement('tema-conteudo');
  if (conteudo) conteudo.innerHTML = renderSecaoHTML(capitulo, s);

  renderTemaSidebar(capitulos); // atualiza o "active" na lateral
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Troca a tradução (NAA/NTLH/NVI/AFC) e re-renderiza a seção atual
function trocarVersaoTema(novaVersao) {
  temaBibliaState.versao = novaVersao;

  const capitulos = (typeof TEMA_BIBLIA !== 'undefined' && TEMA_BIBLIA && TEMA_BIBLIA.capitulos)
    ? TEMA_BIBLIA.capitulos
    : (DataLoader.getCapitulos && DataLoader.getCapitulos().capitulos) || [];

  const capitulo = capitulos[temaBibliaState.capitulo] || {};
  const conteudo = getElement('tema-conteudo');
  if (conteudo) conteudo.innerHTML = renderSecaoHTML(capitulo, temaBibliaState.secao);
}

// Mostra/oculta a resposta de uma pergunta
function toggleRespostaCapitulo(secaoIdx, perguntaIdx) {
  const el = getElement(`resposta-${secaoIdx}-${perguntaIdx}`);
  if (!el) return;
  el.classList.toggle('aberta');
}



function scrollToCapituloSecao(capituloIndex, secaoIndex, event) {
  if (event) event.preventDefault();
  
  const secao = getElement(`capitulo-${capituloIndex}-secao-${secaoIndex}`);
  if (secao) {
    secao.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Atualizar link ativo
  const links = document.querySelectorAll('.tema-sidebar-nav a');
  links.forEach(link => link.classList.remove('active'));
  if (event && event.target) {
    event.target.classList.add('active');
  }

  // Fechar menu no celular
  const nav = getElement('temaSidebarNav');
  if (nav && nav.classList.contains('open')) {
    nav.classList.remove('open');
  }
}



function initTemaSidebarToggle() {
  const toggle = getElement('temaSidebarToggle');
  const nav = getElement('temaSidebarNav');
  
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
  }
}

function toggleRespostaSecao(secaoIndex, perguntaIndex) {
  const resposta = getElement(`secao-${secaoIndex}-resposta-${perguntaIndex}`);
  if (resposta) {
    resposta.classList.toggle('aberta');
  }
}

function toggleResposta(index) {
  const resposta = getElement(`resposta-${index}`);
  if (resposta) {
    resposta.classList.toggle('aberta');
  }
}

function trocarVersaoGlobal(versao, btn) {
  const capitulos = TEMA_BIBLIA.capitulos;
  
  capitulos.forEach((capitulo, c) => {
    capitulo.secoes.forEach((secao, s) => {
      secao.perguntas.forEach((p, i) => {
        const texto = document.querySelector(`#capitulo-${c}-secao-${s}-pergunta-${i} .versiculo-biblia p`);
        if (texto) {
          texto.textContent = p.versoes[versao];
        }
      });
    });
  });
  
  const tabs = btn.parentElement.querySelectorAll('.versao-tab');
  tabs.forEach(tab => tab.classList.remove('active'));
  btn.classList.add('active');
}

// ============ PÁGINA DE ESTUDO DO PROFESSOR ============

function renderEstudoProfessorPage() {
  const app = getElement('app');
  if (!app) return;

  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id')) || 1;

  const licao = LICOES.find(l => l.id === id) || LICOES[0];
  const estudo = licao.estudoProfessor;

  if (!estudo) {
    app.innerHTML = `
      <div class="container" style="padding: 60px 24px; text-align: center;">
        <h2>Estudo para Professores</h2>
        <p style="color: var(--text-light); margin-top: 16px;">Estudo não disponível para esta lição.</p>
        <a href="estudo-detalhe.html?tipo=licao&id=${licao.id}" class="btn btn-primary" style="margin-top: 24px;">Voltar à Lição</a>
      </div>
    `;
    return;
  }

  app.innerHTML = `
    <div class="professor-header">
      <div class="container">
        <span class="professor-badge">Material para Professores</span>
        <h1>${estudo.titulo}</h1>
        <p class="professor-subtitulo">${estudo.subtitulo}</p>
        <div class="professor-licao">
          <strong>Lição:</strong> ${licao.titulo} — ${licao.semana}
        </div>
      </div>
    </div>

    <div class="container" style="padding: 40px 24px;">
      <div class="professor-objetivo">
        <h3>Objetivo da Lição</h3>
        <p>${estudo.objetivo}</p>
      </div>

      <div class="professor-versiculo">
        <h3>Verso para Memorização</h3>
        <p>"${estudo.versoChave}"</p>
      </div>

      <div class="professor-orientacoes">
        <h3>Orientações Pedagógicas e Andragógicas</h3>
        <ul>
          ${estudo.orientacoes.map(o => {
            const parts = o.split(':');
            if (parts.length > 1) {
              return `<li><strong>${parts[0]}:</strong>${parts.slice(1).join(':')}</li>`;
            }
            return `<li>${o}</li>`;
          }).join('')}
        </ul>
      </div>

      <div class="professor-slides">
        <h3>Estrutura da Apresentação</h3>
        ${estudo.slides.map((slide, i) => `
          <div class="slide-card">
            <div class="slide-header">
              <span class="slide-number">${i + 1}</span>
              <h4>${slide.titulo}</h4>
            </div>
            <ul class="slide-topicos">
              ${slide.topicos.map(t => {
                const parts = t.split(':');
                if (parts.length > 1) {
                  return `<li><strong>${parts[0]}:</strong>${parts.slice(1).join(':')}</li>`;
                }
                return `<li>${t}</li>`;
              }).join('')}
            </ul>
            ${slide.nota ? `<div class="slide-nota"><strong>Nota Didática:</strong> ${slide.nota}</div>` : ''}
          </div>
        `).join('')}
      </div>

      <div class="professor-aprofundamento">
        <h3>Aprofundamento Teológico (Para o Professor)</h3>
        ${estudo.aprofundamentos.map(ap => `
          <div class="aprofundamento-card">
            <h4>${ap.titulo}</h4>
            <p>${ap.texto}</p>
          </div>
        `).join('')}
      </div>

      <div class="navegacao-licoes">
        <a href="estudo-detalhe.html?tipo=licao&id=${licao.id}" class="nav-licao">← Voltar à Lição</a>
        <a href="licoes.html" class="btn btn-outline" style="color: var(--primary); border-color: var(--primary);">Todas as Lições</a>
      </div>
    </div>
  `;
}

// ============ TOGGLE PERGUNTA ============

function togglePergunta(index) {
  const card = getElement(`pergunta-${index}`);
  if (card) {
    card.classList.toggle('aberta');
  }
}

// ============ BOTÃO VOLTAR AO TOPO ============

function initBackToTop() {
  const btn = getElement('backToTop');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  });
}

// ============ INICIALIZAÇÃO ============

document.addEventListener('DOMContentLoaded', () => {
  initNavToggle();
  initBackToTop();

  const path = window.location.pathname;

  if (path.includes('licoes.html')) {
    renderLicoesPage();
  } else if (path.includes('estudos.html')) {
    renderEstudosPage();
  } else if (path.includes('tema-biblia.html')) {
    renderTemaBibliaPage();
  } else if (path.includes('estudo-professor.html')) {
    renderEstudoProfessorPage();
  } else if (path.includes('estudo-detalhe.html')) {
    renderDetalhePage();
  } else {
    renderHomePage();
  }
});

// ===== TEMA BÍBLIA — Gaveta lateral no mobile (versão robusta) =====
(function () {
  var overlay = document.querySelector('.tema-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'tema-overlay';
    document.body.appendChild(overlay);
  }

  function abrir() {
    var sidebar = document.querySelector('.tema-sidebar');
    if (!sidebar) return;
    sidebar.classList.add('aberta');
    overlay.classList.add('ativa');
    document.body.style.overflow = 'hidden';
  }
  function fechar() {
    var sidebar = document.querySelector('.tema-sidebar');
    if (sidebar) sidebar.classList.remove('aberta');
    overlay.classList.remove('ativa');
    document.body.style.overflow = '';
  }

  // Delegação de eventos: funciona mesmo com itens criados depois pelo app.js
  document.addEventListener('click', function (e) {
    var alvo = e.target;

    // Botão "☰ Capítulos"
    if (alvo.closest('.tema-abrir-gaveta')) {
      e.preventDefault();
      abrir();
      return;
    }

    // X do cabeçalho da sidebar
    if (alvo.closest('.tema-sidebar-toggle')) {
      e.preventDefault();
      fechar();
      return;
    }

    // Fundo escuro
    if (alvo.closest('.tema-overlay')) {
      fechar();
      return;
    }

    // Clicou numa seção (ex.: 1.2, 1.3, 2.2) -> fecha a gaveta no mobile
    if (alvo.closest('.tema-secao-btn')) {
      if (window.innerWidth <= 768) fechar();
      return;
    }

    // Clicou num capítulo -> deixa o acordeão abrir/fechar normalmente
    if (alvo.closest('.tema-capitulo-btn')) {
      return;
    }
  });

  // Cria o botão "☰ Capítulos" assim que a sidebar existir
  function criarBotao() {
    if (document.querySelector('.tema-abrir-gaveta')) return;
    var main = document.querySelector('.tema-main');
    if (!main) return;
    var btn = document.createElement('button');
    btn.className = 'tema-abrir-gaveta';
    btn.type = 'button';
    btn.textContent = '☰ Capítulos';
    main.insertBefore(btn, main.firstChild);
  }

  // Se a sidebar já existe, cria o botão agora
  if (document.querySelector('.tema-sidebar')) {
    criarBotao();
  } else {
    // Senão, espera o app.js renderizar (MutationObserver)
    var obs = new MutationObserver(function () {
      if (document.querySelector('.tema-sidebar')) {
        criarBotao();
        obs.disconnect();
      }
    });
    obs.observe(document.body, { childList: true, subtree: true });
  }

  // Fecha a gaveta se a tela for redimensionada para desktop
  window.addEventListener('resize', function () {
    if (window.innerWidth > 768) fechar();
  });
})();



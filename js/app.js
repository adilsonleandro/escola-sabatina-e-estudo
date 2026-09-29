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
  // Estudos mais visitados (últimos 3 adicionados)
  const estudosDestaque = ESTUDOS.slice(-3).reverse();

  app.innerHTML = `
    <section class="hero">
      <div class="hero-content">
        <h1>Compreendendo a Bíblia</h1>
        <p>Estudos bíblicos por temas, lições da Escola Sabatina e perguntas e respostas para aprofundar sua fé.</p>
        <div class="hero-cta">
          <a href="licoes.html" class="btn btn-primary">Lição da Semana</a>
          <a href="estudos.html" class="btn btn-outline">Estudos por Tema</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="stats">
          <a href="licoes.html" class="stat-card stat-card-link">
            <div class="stat-number">${LICOES.length}</div>
            <div class="stat-label">Lições Disponíveis</div>
            <i class="fas fa-arrow-right stat-arrow"></i>
          </a>
          <a href="estudos.html" class="stat-card stat-card-link">
            <div class="stat-number">${ESTUDOS.length}</div>
            <div class="stat-label">Estudos Bíblicos</div>
            <i class="fas fa-arrow-right stat-arrow"></i>
          </a>
          <a href="estudos.html" class="stat-card stat-card-link">
            <div class="stat-number">${TEMAS.length - 1}</div>
            <div class="stat-label">Temas de Estudo</div>
            <i class="fas fa-arrow-right stat-arrow"></i>
          </a>
        </div>

        <div class="licao-destaque">
          <span class="badge">Lição da Semana</span>
          <h2>${licaoAtual.titulo}</h2>
          <div class="versiculo">${licaoAtual.versiculo}</div>
          <p>${licaoAtual.resumo}</p>
          <a href="licoes.html" class="btn btn-primary">Estudar Agora</a>
        </div>

        <div class="section-title">
          <h2>Estudos em Destaque</h2>
          <p>Aprofunde-se na Palavra de Deus</p>
        </div>

        <div class="cards-grid">
          ${estudosDestaque.map(estudo => `
            <div class="card">
              <span class="card-badge">${estudo.tema}</span>
              <h3>${estudo.titulo}</h3>
              <div class="versiculo">${estudo.versiculo}</div>
              <p>${estudo.resumo}</p>
              <div class="card-footer">
                <a href="estudo-detalhe.html?id=${estudo.id}" class="btn btn-primary btn-small">Ler Estudo</a>
              </div>
            </div>
          `).join('')}
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
          <h2>Estudos Bíblicos por Tema</h2>
          <p>Encontre estudos organizados por temas para sua edificação espiritual</p>
        </div>

        <div class="search-section">
          <div class="search-box">
            <input type="text" class="search-input" id="searchInput" placeholder="Buscar estudos...">
          </div>
          <div class="filter-tags" id="filterTags">
            ${TEMAS.map((tema, i) => `
              <button class="filter-tag ${i === 0 ? 'active' : ''}" data-tema="${tema}">${tema}</button>
            `).join('')}
          </div>
        </div>

        <div class="cards-grid" id="estudosGrid">
          ${renderEstudosCards(ESTUDOS)}
        </div>

        <div class="empty-state" id="emptyState" style="display: none;">
          <div class="icon">📖</div>
          <h3>Nenhum estudo encontrado</h3>
          <p>Tente buscar por outro termo ou tema.</p>
        </div>
      </div>
    </section>
  `;

  initEstudosFilters();
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
            <button class="pergunta-header" onclick="togglePergunta(${i})">
              <span class="icon">+</span>
              <span>${p.pergunta}</span>
            </button>
            <div class="pergunta-body">
              <div class="pergunta-body-inner">
                ${p.resposta}
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
  `;
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

// ============ INICIALIZAÇÃO ============

document.addEventListener('DOMContentLoaded', () => {
  initNavToggle();

  const path = window.location.pathname;

  if (path.includes('licoes.html')) {
    renderLicoesPage();
  } else if (path.includes('estudos.html')) {
    renderEstudosPage();
  } else if (path.includes('estudo-professor.html')) {
    renderEstudoProfessorPage();
  } else if (path.includes('estudo-detalhe.html')) {
    renderDetalhePage();
  } else {
    renderHomePage();
  }
});

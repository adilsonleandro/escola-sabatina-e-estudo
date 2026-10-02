# -*- coding: utf-8 -*-
# ============================================================
# Gerador da estrutura "Compreendendo a Bíblia"
# Cria:
#   - Pasta js/dados/ com os 20 arquivos de capítulo
#   - data.js atualizado (registro dos capítulos)
#   - Adiciona os <script> dos capítulos nos HTML
# Rode com: python gerar_estrutura.py
# ============================================================
import os
import pathlib
import re

# ------------------------------------------------------------------
# 1) CONFIGURAÇÕES
# ------------------------------------------------------------------
TOTAL_CAPITULOS = 20
PASTA_DADOS = os.path.join("js", "dados")

# Arquivos HTML que devem receber os <script> dos capítulos (antes do data.js)
HTMLS = [
    "tema-biblia.html",
    "secao-biblia.html",
]

# Nome/título de cada capítulo (ajuste os textos depois, se quiser)
def titulo_capitulo(n):
    return f"Capítulo {n} — [TÍTULO DO CAPÍTULO {n}]"

TEMPLATE_CAPITULO_SEM_SECOES = """// ============================================================
// Capítulo {n} — carregado via <script> antes do data.js
// ============================================================
const CAPITULO_{n} = {{
  id: "capitulo-{n}",
  titulo: "{titulo}",
  secoes: []
}};
"""

# Modelo completo (exemplo) para o Capítulo 2
TEMPLATE_CAPITULO_2 = """// ============================================================
// Capítulo 2 — carregado via <script> antes do data.js
// Estrutura padrão: secoes -> perguntas -> versoes (4 traduções)
// ============================================================
const CAPITULO_2 = {{
  id: "capitulo-2",
  titulo: "Capítulo 2 — [TÍTULO DO CAPÍTULO]",
  secoes: [
    {{
      id: "2-1",
      titulo: "2.1 [TÍTULO DA PRIMEIRA SEÇÃO]",
      perguntas: [
        {{
          numero: 1,
          pergunta: "[Texto da pergunta]",
          versiculo: "[Referência do versículo, ex.: Gênesis 1:1]",
          versoes: {{
            naa: "[Texto do versículo em NAA]",
            ntlh: "[Texto do versículo em NTLH]",
            nvi: "[Texto do versículo em NVI]",
            afc: "[Texto do versículo em AFC]"
          }},
          resposta: "[Resposta da pergunta]"
        }}
      ]
    }}
  ]
}};
"""

# ------------------------------------------------------------------
# 2) CRIA OS ARQUIVOS DE CAPÍTULO
# ------------------------------------------------------------------
def criar_capitulos():
    pathlib.Path(PASTA_DADOS).mkdir(parents=True, exist_ok=True)
    criados = []

    for n in range(1, TOTAL_CAPITULOS + 1):
        nome_arquivo = os.path.join(PASTA_DADOS, f"dados-capitulo-{n}.js")

        if n == 2:
            conteudo = TEMPLATE_CAPITULO_2  # capítulo 2 vem com exemplo completo
        else:
            conteudo = TEMPLATE_CAPITULO_SEM_SECOES.format(
                n=n, titulo=titulo_capitulo(n)
            )

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)

        criados.append(nome_arquivo)

    return criados

# ------------------------------------------------------------------
# 3) GERA O DATA.JS (registro dos capítulos)
# ------------------------------------------------------------------
def gerar_data_js():
    linhas = []
    linhas.append("// ============================================================")
    linhas.append("// DADOS — Compreendendo a Bíblia")
    linhas.append("// Registro central do tema \"A Bíblia\".")
    linhas.append("// Cada capítulo vive em um arquivo próprio em js/dados/ e é")
    linhas.append("// carregado via <script> ANTES deste arquivo.")
    linhas.append("// ============================================================")
    linhas.append("")
    linhas.append("const TEMA_BIBLIA = {")
    linhas.append("  id: \"biblia\",")
    linhas.append("  titulo: \"A Bíblia: Como estudá-la e compreendê-la\",")
    linhas.append("  descricao: \"Estudo completo sobre como estudar e compreender as Escrituras Sagradas.\",")
    linhas.append("  capitulos: []")
    linhas.append("};")
    linhas.append("")
    linhas.append("// Registra cada capítulo que tiver um arquivo próprio carregado")

    for n in range(1, TOTAL_CAPITULOS + 1):
        linhas.append(f"if (typeof CAPITULO_{n} !== 'undefined') TEMA_BIBLIA.capitulos.push(CAPITULO_{n});")

    linhas.append("")

    conteudo = "\n".join(linhas)

    with open(os.path.join("js", "data.js"), "w", encoding="utf-8") as f:
        f.write(conteudo)

    return conteudo

# ------------------------------------------------------------------
# 4) ATUALIZA OS HTML (insere os <script> dos capítulos antes do data.js)
# ------------------------------------------------------------------
def gerar_bloco_scripts():
    blocos = []
    for n in range(1, TOTAL_CAPITULOS + 1):
        blocos.append(f'  <script src="js/dados/dados-capitulo-{n}.js"></script>')
    return "\n".join(blocos) + "\n"

def atualizar_html():
    bloco = gerar_bloco_scripts()
    atualizados = []

    for arquivo in HTMLS:
        if not os.path.exists(arquivo):
            print(f"  [aviso] {arquivo} não encontrado, pulando.")
            continue

        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Remove blocos antigos de capítulo se já existirem (evita duplicar)
        conteudo = re.sub(r"(\s*<script src=\"js/dados/dados-capitulo-\d+\.js\"></script>)+\n?", "\n", conteudo)

        # Insere os <script> dos capítulos logo antes de js/data.js
        if '<script src="js/data.js"></script>' in conteudo:
            conteudo = conteudo.replace(
                '  <script src="js/data.js"></script>',
                bloco + '  <script src="js/data.js"></script>'
            )
        else:
            print(f"  [aviso] {arquivo}: tag de js/data.js não encontrada.")

        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)

        atualizados.append(arquivo)

    return atualizados

# ------------------------------------------------------------------
# 5) EXECUÇÃO PRINCIPAL
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("Criando arquivos de capítulos...")
    arquivos = criar_capitulos()
    print(f"  {len(arquivos)} arquivos criados em {PASTA_DADOS}/")

    print("Gerando data.js...")
    gerar_data_js()
    print("  js/data.js atualizado")

    print("Atualizando HTML...")
    atualizados = atualizar_html()
    for a in atualizados:
        print(f"  {a} atualizado")

    print()
    print("Concluído! Estrutura pronta para receber o conteúdo dos capítulos.")

    
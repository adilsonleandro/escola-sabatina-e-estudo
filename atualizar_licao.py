#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atualizar_licao.py — fonte: CPB (mais.cpb.com.br)
------------------------------------------------------------
Encontra a lição da SEMANA (pela data de hoje), baixa a página da
lição no site da CPB e gera:

    js/licoes/licao-{ano}-{trimestre}t-{numero}.js

Como encontra a lição atual (sem depender de cálculos de calendário):
  1. Lê o sitemap do site e junta TODAS as URLs de lições
     (ex.: /licao/o-criador-fala-4o-trimestre-2026/).
  2. Abre cada página (com cache) e lê o período escrito nela
     ("26 de setembro a 02 de outubro").
  3. Escolhe a lição cujo período contém a data de hoje.
  Se preferir, passe a URL direto: --url "https://...".

USO:
  python atualizar_licao.py                     # gera a lição da semana
  python atualizar_licao.py --json              # só confere (não gera)
  python atualizar_licao.py --url "https://mais.cpb.com.br/licao/o-criador-fala-4o-trimestre-2026/"
  python atualizar_licao.py --salvar-html       # salva HTML p/ debug
  python atualizar_licao.py --instalar-agendamento
  python atualizar_licao.py --remover-agendamento

DEPENDÊNCIAS:
  pip install requests beautifulsoup4
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date, datetime, timedelta

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Faltam dependências. Rode:  pip install requests beautifulsoup4")
    sys.exit(1)

PASTA_SAIDA = "js/licoes"
ARQUIVO_CACHE = "cache_licoes.json"
TEMPO_LIMITE = 20
SITEMAPS = [
    "https://mais.cpb.com.br/wp-sitemap.xml",
    "https://mais.cpb.com.br/sitemap_index.xml",
    "https://mais.cpb.com.br/sitemap.xml",
]
ANOS_ALVO = [date.today().year, date.today().year + 1]

MESES_PT = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
MES_NUM = {m: i + 1 for i, m in enumerate(MESES_PT)}

PALAVRAS_MSG_SUBSCRICAO = ("Garanta o conteúdo completo", "Assine a lição",
                           "Faça aqui a sua assinatura", "Banner CPB Play")


# ---------- UTILITÁRIOS ----------
def normalizar(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def limpar_texto(s):
    return re.sub(r"\s+", " ", (s or "")).replace("\xa0", " ").strip()


def baixar(url, salvar_html=False, nome="pagina"):
    r = requests.get(url, timeout=TEMPO_LIMITE,
                     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"
    if salvar_html:
        with open(f"debug_{nome}.html", "w", encoding="utf-8") as f:
            f.write(r.text)
    return r.text


def eh_mensagem_assinatura(t):
    return any(p in t for p in PALAVRAS_MSG_SUBSCRICAO)


# ---------- DATAS / PERÍODO ----------
def datas_do_periodo(texto, ano):
    """Extrai (data_inicio, data_fim) de texto como
    '26 de setembro a 02 de outubro'. Lida com virada de ano."""
    m = re.search(r"(\d{1,2})\s+de\s+([a-zç]+)\s+[aà]\s+(\d{1,2})\s+de\s+([a-zç]+)",
                  texto, re.I)
    if not m:
        return None, None
    try:
        d1 = date(ano, MES_NUM[normalizar(m.group(2).lower())], int(m.group(1)))
        d2 = date(ano, MES_NUM[normalizar(m.group(4).lower())], int(m.group(3)))
    except KeyError:
        return None, None
    if d2 < d1:  # período atravessa o ano (ex.: dezembro a janeiro)
        # tenta no ano seguinte
        try:
            d2 = date(ano + 1, MES_NUM[normalizar(m.group(4).lower())], int(m.group(3)))
        except ValueError:
            pass
    return d1, d2


# ---------- SITEMAP / DESCOBERTA DE URLS ----------
def _urls_do_sitemap(xml_texto, prof=0):
    urls = []
    soup = BeautifulSoup(xml_texto, "xml")
    for loc in soup.find_all("loc"):
        u = loc.get_text(strip=True)
        if u.endswith(".xml") and prof < 2:
            try:
                urls += _urls_do_sitemap(baixar(u), prof + 1)
            except Exception:
                continue
        else:
            urls.append(u)
    return urls


def coletar_urls_licoes():
    """Retorna todas as URLs /licao/...-Nº-trimestre-ANO/ do site."""
    urls = set()
    for sm in SITEMAPS:
        try:
            for u in _urls_do_sitemap(baixar(sm)):
                if "/licao/" in u and re.search(r"-\d{1,2}o-trimestre-\d{4}/?$", u):
                    urls.add(u.rstrip("/"))
        except Exception:
            continue
    return sorted(urls)


def ano_e_trimestre_da_url(url):
    m = re.search(r"-(\d{1,2})o-trimestre-(\d{4})/?$", url)
    if m:
        return int(m.group(2)), int(m.group(1))
    return None, None


# ---------- EXTRAÇÃO DA PÁGINA ----------
def achar_container(soup):
    """Escolhe o elemento que contém o período e o conteúdo da lição."""
    candidatos = []
    for sel in ("article", "main", ".entry-content", ".post-content",
                ".et_pb_post_content", ".content-area"):
        el = soup.select_one(sel)
        if el:
            candidatos.append(el)
    if not candidatos:
        candidatos.append(soup)
    melhor = None
    melhor_pontos = -1
    for el in candidatos:
        txt = el.get_text(" ", strip=True)
        pontos = 0
        if re.search(r"\d{1,2} de [a-zç]+ a \d{1,2} de [a-zç]+", txt, re.I):
            pontos += 3
        if re.search(r"Li[cç][aã]o\s+(\d+)", txt):
            pontos += 2
        if re.search(r"[Vv]erso.*[Mm]emorizar|[Mm]emorizar|VERSO PARA", txt, re.I):
            pontos += 2
        pontos += min(len(txt) // 1000, 5)
        if pontos > melhor_pontos:
            melhor_pontos = pontos
            melhor = el
    return melhor or soup


RE_DIA_CABECALHO = re.compile(
    r"^(S[aá]bado(?:\s+à\s+tarde)?|Domingo|Segunda[- ]feira?|Ter[cç]a[- ]feira?|"
    r"Quarta[- ]feira?|Quinta[- ]feira?|Sexta[- ]feira?)([,:]?\s+|$)",
    re.I)


def extrair_pagina_cpb(html, ano, url):
    soup = BeautifulSoup(html, "html.parser")
    conteudo = achar_container(soup)
    texto_geral = limpar_texto(conteudo.get_text(" ", strip=True))

    # --- Título (prioriza og:title, depois .entry-title, depois <title>) ---
    titulo = ""
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        titulo = limpar_texto(og["content"])
    if not titulo:
        et = soup.select_one(".entry-title")
        if et:
            titulo = limpar_texto(et.get_text(" ", strip=True))
    if not titulo:
        t = soup.find("title")
        if t:
            titulo = limpar_texto(t.get_text(" ", strip=True))
    titulo = re.sub(r"\s*\|\s*CPB mais.*$", "", titulo, flags=re.I)
    titulo = re.sub(r"\s*\|\s*.*CPB.*$", "", titulo, flags=re.I).strip()
    if not titulo:
        titulo = "Li\u00e7\u00e3o"

    # --- Ano / trimestre vindos da URL ---
    ano_url, trim_url = ano_e_trimestre_da_url(url)
    ano = ano_url or ano

    # --- Número da lição e período (no texto do container) ---
    numero = None
    m_num = re.search(r"Li[cç][aã]o\s+(\d+)", texto_geral)
    if m_num:
        numero = int(m_num.group(1))

    data_ini = data_fim = None
    data_ini, data_fim = datas_do_periodo(texto_geral, ano)

    # --- Versículo (aspas + referência entre parênteses) ---
    versiculo, versiculo_ref = "", ""
    m = re.search(r"[“\"]([^”\"]{15,})[”\"]\s*\(([^)]{3,40})\)", texto_geral)
    if m:
        versiculo, versiculo_ref = m.group(1).strip(), m.group(2).strip()

    # --- Seções diárias + perguntas/respostas ---
    secoes = []
    sec_atual = None
    bloco_comecou = False

    for el in conteudo.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
        t = limpar_texto(el.get_text(" ", strip=True))
        if not t or eh_mensagem_assinatura(t):
            continue

        # Cabeçalho de dia ("Domingo, 27 de setembro" / "Sábado à tarde")
        m_dia = RE_DIA_CABECALHO.match(t)
        eh_cabecalho_dia = bool(
            m_dia and (re.search(r"\d{1,2} de [a-zç]+", t, re.I) or "à tarde" in t))
        if eh_cabecalho_dia:
            bloco_comecou = True
            sec_atual = {"dia": m_dia.group(1).strip(),
                         "titulo": t, "texto": [], "perguntas": []}
            secoes.append(sec_atual)
            continue

        # Para ao chegar em "Resumo da Lição"/"Aplicação" (fim das seções)
        if re.search(r"^Resumo da Li[cç][aã]o|^APLICA[CÇ]|^Aplica[cç][aã]o", t, re.I):
            break
        if not bloco_comecou or sec_atual is None:
            continue

        # Pergunta numerada ("5. Eles revelam ...?")
        m_q = re.match(r"^(\d{1,2})[\.\)]\s*(.+)", t)
        if m_q:
            pergunta = t
            sec_atual["perguntas"].append({"pergunta": pergunta, "resposta": ""})
            continue

        # Resposta da última pergunta
        if sec_atual["perguntas"] and not sec_atual["perguntas"][-1]["resposta"]:
            sec_atual["perguntas"][-1]["resposta"] = t
            continue

        # Texto normal da seção
        sec_atual["texto"].append(t)

    for sec in secoes:
        sec["texto"] = limpar_texto(" ".join(sec["texto"]))
        for q in sec["perguntas"]:
            q["resposta"] = limpar_texto(q["resposta"])

    return {"fonte": "cpb", "titulo": titulo, "numero": numero,
            "ano": ano, "trimestre": trim_url,
            "versiculo": versiculo, "versiculo_ref": versiculo_ref,
            "data_inicio": data_ini, "data_fim": data_fim,
            "url": url, "secoes": secoes}


# ---------- CACHE ----------
def carregar_cache():
    if os.path.exists(ARQUIVO_CACHE):
        try:
            with open(ARQUIVO_CACHE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def salvar_cache(cache):
    with open(ARQUIVO_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def achar_licao_atual(data_alvo, salvar_html):
    """Escaneia as páginas da CPB e devolve a lição cujo período
    contém data_alvo. Usa cache para não repetir downloads."""
    urls = coletar_urls_licoes()
    urls = [u for u in urls
            if ano_e_trimestre_da_url(u)[0] in ANOS_ALVO]
    cache = carregar_cache()
    achadas = []

    for u in urls:
        info = cache.get(u)
        if not (info and info.get("periodo")):
            try:
                html = baixar(u, salvar_html, "licao_cpb")
                dados = extrair_pagina_cpb(html, date.today().year, u)
                if not (dados["data_inicio"] and dados["data_fim"]):
                    continue
                info = {"periodo": [dados["data_inicio"].isoformat(),
                                    dados["data_fim"].isoformat()],
                        "numero": dados["numero"],
                        "titulo": dados["titulo"],
                        "trimestre": dados["trimestre"],
                        "ano": dados["ano"]}
                cache[u] = info
            except Exception:
                continue
        if not (info and info.get("periodo")):
            continue
        d1 = date.fromisoformat(info["periodo"][0])
        d2 = date.fromisoformat(info["periodo"][1])
        if d1 <= data_alvo <= d2:
            achadas.append((u, info))

    salvar_cache(cache)

    if not achadas:
        return None, cache
    # Prefere a lição com maior sobreposição ao período alvo
    achadas.sort(key=lambda par: (par[1].get("ano") or 0, par[1].get("trimestre") or 0))
    return achadas[-1], cache


# ---------- GERAÇÃO DO JAVASCRIPT ----------
def js_str(s):
    return json.dumps(s if s is not None else "", ensure_ascii=False)


def formato_periodo_pt(d_ini, d_fim):
    return (f"{d_ini.day} de {MESES_PT[d_ini.month-1]} a "
            f"{d_fim.day} de {MESES_PT[d_fim.month-1]} de {d_fim.year}")


def gerar_js(ano, trim, numero, dados, data_ini, data_fim):
    titulo = dados["titulo"]
    periodo = formato_periodo_pt(data_ini, data_fim)
    versiculo = dados.get("versiculo", "")
    ref = dados.get("versiculo_ref", "")
    texto_resumo = " ".join(s["texto"] for s in dados.get("secoes", []) if s.get("texto"))
    resumo = [texto_resumo[:600]] if texto_resumo else []

    L = []
    L.append("// ============================================================")
    L.append(f"// Lição {numero} - {titulo} | {trim}º Trimestre {ano}")
    L.append(f"// Fonte: CPB (mais.cpb.com.br) | Em: {datetime.now():%d/%m/%Y %H:%M}")
    L.append("// Gerado por atualizar_licao.py — NÃO edite manualmente.")
    L.append("// ============================================================")
    L.append(f"const LICAO_{ano}_{trim}T_{numero} = {{")
    L.append(f"  id: {js_str(f'licao-{ano}-{trim}t-{numero}')},")
    L.append(f"  ano: {ano},")
    L.append(f"  trimestre: {trim},")
    L.append(f"  numero: {numero},")
    L.append(f"  titulo: {js_str(titulo)},")
    L.append(f"  versiculo: {js_str(versiculo)},")
    L.append(f"  versiculo_ref: {js_str(ref)},")
    L.append(f"  periodo: {js_str(periodo)},")
    L.append(f"  data_inicio: {js_str(data_ini.isoformat() if data_ini else '')},")
    L.append(f"  data_fim: {js_str(data_fim.isoformat() if data_fim else '')},")
    L.append(f"  fonte: {js_str('cpb')},")
    L.append("  abertura: {")
    L.append(f"    versiculo: {js_str(versiculo)},")
    L.append(f"    versiculo_ref: {js_str(ref)},")
    L.append(f"    periodo: {js_str(periodo)},")
    L.append(f"    resumo: {js_str(resumo)},")
    L.append(f"    reflexao: {js_str('Que Deus nos fale por meio desta lição.')}")
    L.append("  },")
    L.append("  estudo: {")
    L.append(f"    titulo: {js_str(titulo)},")
    L.append(f"    versiculo: {js_str(versiculo)},")
    L.append(f"    versiculo_ref: {js_str(ref)},")
    L.append(f"    periodo: {js_str(periodo)},")
    L.append(f"    resumo: {js_str(resumo)},")
    L.append("    secoes: [")
    for sec in dados.get("secoes", []):
        L.append("      {")
        L.append(f"        dia: {js_str(sec.get('dia', ''))},")
        L.append(f"        titulo: {js_str(sec.get('titulo', ''))},")
        L.append(f"        texto: {js_str(sec.get('texto', ''))},")
        L.append("        perguntas: [")
        for q in sec.get("perguntas", []):
            L.append("          {")
            L.append(f"            pergunta: {js_str(q.get('pergunta', ''))},")
            L.append(f"            resposta: {js_str(q.get('resposta', ''))}")
            L.append("          },")
        L.append("        ]")
        L.append("      },")
    L.append("    ]")
    L.append("  }")
    L.append("};")
    L.append("")
    return "\n".join(L)


# ---------- AGENDAMENTO NO WINDOWS ----------
def instalar_agendamento(caminho_script):
    atalho = os.path.abspath(caminho_script)
    comando = ("schtasks /Create /F /TN \"AtualizarLicaoSabatina\" "
               f"/TR \"python \\\"{atalho}\\\"\" /SC WEEKLY /D SAT /ST 07:00")
    print("Criando tarefa 'AtualizarLicaoSabatina' (todo sábado às 07:00)...")
    try:
        r = subprocess.run(comando, shell=True, capture_output=True, text=True)
        print(r.stdout or r.stderr)
        print("Pronto! Ajuste o horário no Agendador de Tarefas se quiser.")
    except Exception as e:
        print("Não foi possível criar automaticamente:", e)
        print(f"Crie manualmente no Agendador de Tarefas: bastão no sábado, comando: python {atalho}")


def remover_agendamento():
    subprocess.run('schtasks /Delete /F /TN "AtualizarLicaoSabatina"',
                   shell=True, capture_output=True, text=True)
    print("Tarefa 'AtualizarLicaoSabatina' removida.")


# ---------- MAIN ----------
def main():
    ap = argparse.ArgumentParser(description="Atualiza a Lição da Escola Sabatina (fonte: CPB)")
    ap.add_argument("--data", help="Data AAAA-MM-DD (padrão: hoje)")
    ap.add_argument("--url", help="Link direto da lição no site da CPB")
    ap.add_argument("--json", action="store_true", help="Mostra o JSON de conferência")
    ap.add_argument("--salvar-html", action="store_true", help="Salva o HTML baixado (debug)")
    ap.add_argument("--instalar-agendamento", action="store_true")
    ap.add_argument("--remover-agendamento", action="store_true")
    args = ap.parse_args()

    if args.instalar_agendamento:
        instalar_agendamento(__file__)
        return
    if args.remover_agendamento:
        remover_agendamento()
        return

    data_alvo = date.fromisoformat(args.data) if args.data else date.today()
    print(f"Data alvo : {data_alvo:%d/%m/%Y}")

    # 1) Descobrir a lição atual
    url_licao = args.url
    trim, numero = None, None
    if not url_licao:
        print("\n[1/3] Procurando a lição ativa no site da CPB (pode levar alguns instantes)...")
        par, _ = achar_licao_atual(data_alvo, args.salvar_html)
        if par:
            url_licao, info = par
            numero = info.get("numero")
            trim = info.get("trimestre")
            print(f"  Encontrada: Lição {numero} | {info.get('titulo','')} | "
                  f"({info['periodo'][0]} a {info['periodo'][1]})")
        else:
            print("  Não achei nenhuma lição cujo período cubra a data de hoje.")
            print("  Copie o link da lição da semana no site da CPB e rode com:")
            print('  python atualizar_licao.py --url "https://mais.cpb.com.br/licao/..."')
            sys.exit(1)
    print(f"  URL: {url_licao}")

    # 2) Baixar e extrair
    print("[2/3] Baixando e extraindo a lição da CPB...")
    html = baixar(url_licao, args.salvar_html, "licao_cpb")
    dados = extrair_pagina_cpb(html, data_alvo.year, url_licao)

    if not dados["numero"]:
        dados["numero"] = numero or 1
    if not dados["trimestre"]:
        _, dados["trimestre"] = ano_e_trimestre_da_url(url_licao)
        if not dados["trimestre"]:
            dados["trimestre"] = trim or ((dados["data_inicio"].month - 1) // 3 + 1
                                          if dados["data_inicio"] else 1)
    if not dados["data_inicio"]:
        print("  ERRO: não encontrei o período da lição na página.")
        print("  Rode com --salvar-html e me envie o arquivo debug_licao_cpb.html")
        print("  (ou me cole a saída de --json) para eu ajustar o parser.")
        sys.exit(1)

    numero = dados["numero"]
    trim = dados["trimestre"]
    ano = dados["ano"] or data_alvo.year
    print(f"  Título   : {dados['titulo']}")
    print(f"  Lição    : {numero} | {trim}º trimestre {ano}")
    print(f"  Período  : {dados['data_inicio']:%d/%m/%Y} a {dados['data_fim']:%d/%m/%Y}")
    print(f"  Seções   : {len(dados['secoes'])}")
    print(f"  Perguntas: {sum(len(s['perguntas']) for s in dados['secoes'])}")

    if args.json:
        saida = {k: (v.isoformat() if isinstance(v, date) else v)
                 for k, v in dados.items()}
        print("\n" + json.dumps(saida, ensure_ascii=False, indent=2))
        return

    # 3) Gerar o arquivo JS
    print("[3/3] Gerando arquivo JavaScript...")
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    caminho = os.path.join(PASTA_SAIDA, f"licao-{ano}-{trim}t-{numero}.js")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(gerar_js(ano, trim, numero, dados, dados["data_inicio"], dados["data_fim"]))
    print(f"  -> {caminho}")
    print("\nConcluído!")


if __name__ == "__main__":
    main()
        
 # python atualizar_licao.py

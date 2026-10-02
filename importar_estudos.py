# -*- coding: utf-8 -*-
# ============================================================
# Importador de Estudos v3 — Compreendendo a Bíblia
# Lê estudos/importar_estudo.txt, busca as 4 versões (NAA,
# NTLH, NVI, ACF) nos arquivos JSON locais da pasta biblia/
# e gera js/dados/dados-capitulo-N.js
#
# Fonte: JSONs de https://github.com/damarals/biblias
# (baixar 1x: naa.json, ntlh.json, nvi.json, acf.json)
#
# Uso:
#   python importar_estudos.py                 (usa estudos/importar_estudo.txt)
#   python importar_estudos.py --teste         (só lê/interpreta, sem buscar)
# ============================================================
import json, os, re, sys, unicodedata

# ----- CONFIGURAÇÃO -----
ARQUIVO_ENTRADA = "estudos/importar_estudo.txt"
PASTA_SAIDA = "js/dados"
PASTA_BIBLIA = "biblia"
VERSOES = ["naa", "ntlh", "nvi", "acf"]

# ----- MAPA DE LIVROS: nome normalizado -> (slug, numero 1-66) -----
LIVROS = {
    "genesis": ("gn", 1), "gn": ("gn", 1),
    "exodo": ("ex", 2), "ex": ("ex", 2),
    "levitico": ("lv", 3), "lv": ("lv", 3),
    "numeros": ("nm", 4), "nm": ("nm", 4),
    "deuteronomio": ("dt", 5), "dt": ("dt", 5),
    "josue": ("js", 6), "js": ("js", 6),
    "juizes": ("jz", 7), "jz": ("jz", 7),
    "rute": ("rt", 8), "rt": ("rt", 8),
    "1samuel": ("1sm", 9), "1sm": ("1sm", 9),
    "2samuel": ("2sm", 10), "2sm": ("2sm", 10),
    "1reis": ("1rs", 11), "1rs": ("1rs", 11),
    "2reis": ("2rs", 12), "2rs": ("2rs", 12),
    "1cronicas": ("1cr", 13), "1cr": ("1cr", 13),
    "2cronicas": ("2cr", 14), "2cr": ("2cr", 14),
    "esdras": ("ed", 15), "ed": ("ed", 15),
    "neemias": ("ne", 16), "ne": ("ne", 16),
    "ester": ("et", 17), "et": ("et", 17),
    "job": ("jó", 18),
    "salmos": ("sl", 19), "sal": ("sl", 19), "salmo": ("sl", 19), "sl": ("sl", 19),
    "proverbios": ("pv", 20), "pv": ("pv", 20),
    "eclesiastes": ("ec", 21), "ec": ("ec", 21),
    "canticos": ("ct", 22), "cantares": ("ct", 22), "ct": ("ct", 22),
    "isaias": ("is", 23), "is": ("is", 23),
    "jeremias": ("jr", 24), "jr": ("jr", 24),
    "lamentacoes": ("lm", 25), "lm": ("lm", 25),
    "ezequiel": ("ez", 26), "ez": ("ez", 26),
    "daniel": ("dn", 27), "dn": ("dn", 27),
    "oseias": ("os", 28), "os": ("os", 28),
    "joel": ("jl", 29), "jl": ("jl", 29),
    "amos": ("am", 30), "am": ("am", 30),
    "obadias": ("ob", 31), "ob": ("ob", 31),
    "jonas": ("jn", 32), "jn": ("jn", 32),
    "miqueias": ("mq", 33), "mq": ("mq", 33),
    "naum": ("na", 34), "na": ("na", 34),
    "habacuque": ("hc", 35), "hc": ("hc", 35),
    "sofonias": ("sf", 36), "sf": ("sf", 36),
    "ageu": ("ag", 37), "ag": ("ag", 37),
    "zacarias": ("zc", 38), "zc": ("zc", 38),
    "malaquias": ("ml", 39), "ml": ("ml", 39),
    "mateus": ("mt", 40), "mt": ("mt", 40),
    "marcos": ("mc", 41), "mc": ("mc", 41),
    "lucas": ("lc", 42), "lc": ("lc", 42),
    "joao": ("jo", 43), "jo": ("jo", 43),
    "atos": ("atos", 44), "at": ("atos", 44),
    "romanos": ("rm", 45), "rm": ("rm", 45),
    "1corintios": ("1co", 46), "1co": ("1co", 46),
    "2corintios": ("2co", 47), "2co": ("2co", 47),
    "galatas": ("gl", 48), "gl": ("gl", 48),
    "efesios": ("ef", 49), "ef": ("ef", 49),
    "filipenses": ("fp", 50), "fp": ("fp", 50),
    "colossenses": ("cl", 51), "cl": ("cl", 51),
    "1tessalonicenses": ("1ts", 52), "1ts": ("1ts", 52),
    "2tessalonicenses": ("2ts", 53), "2ts": ("2ts", 53),
    "1timoteo": ("1tm", 54), "1tm": ("1tm", 54),
    "2timoteo": ("2tm", 55), "2tm": ("2tm", 55),
    "tito": ("tt", 56), "tt": ("tt", 56),
    "filemom": ("fm", 57), "fm": ("fm", 57),
    "hebreus": ("hb", 58), "hb": ("hb", 58),
    "tiago": ("tg", 59), "tg": ("tg", 59),
    "1pedro": ("1pe", 60), "1pe": ("1pe", 60),
    "2pedro": ("2pe", 61), "2pe": ("2pe", 61),
    "1joao": ("1jo", 62), "1jo": ("1jo", 62),
    "2joao": ("2jo", 63), "2jo": ("2jo", 63),
    "3joao": ("3jo", 64), "3jo": ("3jo", 64),
    "judas": ("jd", 65), "jd": ("jd", 65),
    "apocalipse": ("ap", 66), "ap": ("ap", 66),
}

# Palavras/descritores removidos das referências
DESCRITORES = [
    "última parte", "ultima parte", "primeira parte", "parte",
    "a bíblia de jerusalém", "a biblia de jerusalem", "bíblia de jerusalém",
    "arc", "acf", "naa", "ntlh", "nvi", "ara", "kjv",
    "ver também", "ver tambem", "ver", "cf.", "cf",
]

# ----- UTILITÁRIOS -----
def js_str(s):
    return json.dumps(s if s is not None else "", ensure_ascii=False)

def normalizar(s):
    s = s.lower().strip()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[\s\.]+", "", s)
    return s

# ----- CARGA DOS JSONS LOCAIS (só 1x por rodada) -----
BIBLIAS = {}

def carregar_biblias():
    """Lê os 4 JSONs da pasta biblia/."""
    for versao in VERSOES:
        caminho = os.path.join(PASTA_BIBLIA, f"{versao}.json")
        if not os.path.exists(caminho):
            raise FileNotFoundError(
                f"Arquivo não encontrado: {caminho}\n"
                f"Baixe-o de https://github.com/damarals/biblias/releases/latest/download/{versao.upper()}.json "
                f"e salve em biblia/{versao}.json")
        with open(caminho, encoding="utf-8") as f:
            BIBLIAS[versao] = json.load(f)
        print(f"  carregada: {caminho} ({len(BIBLIAS[versao])} livros)")

def texto_versiculo(versao, num_livro, capitulo, versiculo):
    """Texto do versículo na versão dada, ou '' se não existir."""
    try:
        livros = BIBLIAS[versao]                      # lista com 66 livros
        livro = livros[num_livro - 1]                 # índice 0 = Gênesis
        cap = livro["chapters"][capitulo - 1]         # índice 0 = cap. 1
        if 1 <= versiculo <= len(cap):
            return cap[versiculo - 1].strip()
    except (IndexError, KeyError, TypeError):
        pass
    return ""

# ----- PARSER DE REFERÊNCIA -----
def parse_referencia(ref):
    """Retorna (slug, numero_livro, capitulo, [versiculos]) ou None."""
    ref = ref.strip()
    ref = re.sub(r"(?<![A-Za-z])ls(?=\s+\d)", "is", ref, flags=re.I)
    ref = ref.split(";")[0]
    for d in DESCRITORES:
        ref = re.sub(r"[,;]\s*" + re.escape(d) + r"\s*$", "", ref, flags=re.I)
        ref = re.sub(r"\s+" + re.escape(d) + r"\s*$", "", ref, flags=re.I)
    m = re.match(r"^\s*(.+?)\s+(\d+)\s*:\s*(\d+)(.*)$", ref)
    if not m:
        return None
    nome, cap_s, ver_s, resto = m.group(1), m.group(2), m.group(3), m.group(4)
    # "Jó" com acento só pode ser o livro de Jó — decide antes de normalizar
    if nome.strip().lower() == "jó":
        slug, num_livro = "jó", 18
    else:
        chave = normalizar(nome)
        if chave not in LIVROS:
            return None
        slug, num_livro = LIVROS[chave]
    capitulo = int(cap_s)
    versiculos = [int(ver_s)]
    for v in re.findall(r"\d+", resto):
        n = int(v)
        if n not in versiculos:
            versiculos.append(n)
    versiculos.sort()
    return slug, num_livro, capitulo, versiculos

# ----- EXTRAÇÃO DO VERSÍCULO DA LINHA -----
def extrair_versiculo(linha):
    m = re.search(r"\(([^()]*\d+\s*:\s*\d+[^()]*)\)", linha)
    ref = m.group(1).strip() if m else ""
    for d in DESCRITORES:
        ref = re.sub(r",?\s*" + re.escape(d) + r"\s*$", "", ref, flags=re.I)
    # Resposta: colchetes que NÃO sejam anotações
    respostas = []
    for m2 in re.finditer(r"\[([^\]]+)\]", linha):
        t = m2.group(1).strip()
        if t and not re.match(r"(em torno|obs\.?|observa|nota|cf\.?|ver\b|ver também)", t.lower()):
            respostas.append(t)
    return ref, "; ".join(respostas)

# ----- PREENCHIMENTO DAS 4 VERSÕES -----
def preencher_versoes(pergunta, avisos):
    ref = pergunta.get("versiculo", "")
    if not ref:
        return
    dado = parse_referencia(ref)
    if dado is None:
        avisos.append(f"referência não reconhecida: {ref!r}")
        return
    slug, num_livro, capitulo, versiculos = dado
    for versao in VERSOES:
        partes = [texto_versiculo(versao, num_livro, capitulo, v) for v in versiculos]
        partes = [p for p in partes if p]
        pergunta["versoes"][versao] = " ".join(partes).strip()
        if not partes:
            avisos.append(f"{versao.upper()} {ref}: texto não encontrado no JSON")

# ----- PARSER DO TXT (com dedupe de seções) -----
def parse_importacao(texto):
    capitulos = {}
    cap_atual = None
    secao_atual = None
    pergunta_atual = None

    for linha_bruta in texto.splitlines():
        linha = linha_bruta.strip()
        if not linha:
            continue

        m_sec = re.match(r"^(\d+)\.(\d+)\s+(.+)$", linha)
        if m_sec:
            num_cap = int(m_sec.group(1))
            num_sec = int(m_sec.group(2))
            titulo_sec = m_sec.group(3).strip()
            sec_id = f"{num_cap}-{num_sec}"

            if num_cap not in capitulos:
                capitulos[num_cap] = {"titulo": f"Capítulo {num_cap}", "secoes": []}
            cap_atual = capitulos[num_cap]

            existente = next((s for s in cap_atual["secoes"] if s["id"] == sec_id), None)
            if existente is not None:
                if not existente["perguntas"]:
                    existente["titulo"] = f"{num_cap}.{num_sec} {titulo_sec}"
                secao_atual = existente
            else:
                secao_atual = {
                    "id": sec_id,
                    "titulo": f"{num_cap}.{num_sec} {titulo_sec}",
                    "perguntas": [],
                }
                cap_atual["secoes"].append(secao_atual)
            pergunta_atual = None
            continue

        m_q = re.match(r"^(\d+)\.\s+(.+)$", linha)
        if m_q and secao_atual is not None:
            num_q = int(m_q.group(1))
            texto_q = m_q.group(2).strip().rstrip("?").strip()
            pergunta_atual = {
                "numero": num_q,
                "pergunta": texto_q,
                "versiculo": "",
                "versoes": {v: "" for v in VERSOES},
                "resposta": "",
            }
            secao_atual["perguntas"].append(pergunta_atual)
            # Pergunta e versículo na MESMA linha? Extrai na hora.
            tem_ref_ml = re.search(r"\([^()]*\d+\s*:\s*\d+[^()]*\)", texto_q)
            if tem_ref_ml or any(c in texto_q for c in ('"', "“", "”")):
                ref, resposta = extrair_versiculo(texto_q)
                if ref:
                    pergunta_atual["versiculo"] = ref
                if resposta:
                    pergunta_atual["resposta"] = resposta
            continue

        if pergunta_atual is not None:
            tem_aspas = any(c in linha for c in ('"', "“", "”"))
            tem_ref = re.search(r"\([^()]*\d+\s*:\s*\d+[^()]*\)", linha)
            if tem_aspas or tem_ref:
                ref, resposta = extrair_versiculo(linha)
                if ref:
                    pergunta_atual["versiculo"] = ref
                if resposta:
                    pergunta_atual["resposta"] = resposta

    return capitulos

# ----- GERAÇÃO DO ARQUIVO JS -----
def gerar_arquivo(n_cap, dados):
    L = []
    L.append("// ============================================================")
    L.append(f"// Capítulo {n_cap} — gerado por importar_estudos.py v3 (JSON local)")
    L.append("// ============================================================")
    L.append(f"const CAPITULO_{n_cap} = {{")
    L.append(f"  id: {js_str(f'capitulo-{n_cap}')},")
    L.append(f"  titulo: {js_str(dados['titulo'])},")
    L.append("  secoes: [")
    for sec in dados["secoes"]:
        L.append("    {")
        L.append(f"      id: {js_str(sec['id'])},")
        L.append(f"      titulo: {js_str(sec['titulo'])},")
        L.append("      perguntas: [")
        for p in sec["perguntas"]:
            L.append("        {")
            L.append(f"          numero: {p['numero']},")
            L.append(f"          pergunta: {js_str(p['pergunta'])},")
            L.append(f"          versiculo: {js_str(p['versiculo'])},")
            L.append("          versoes: {")
            for v in VERSOES:
                L.append(f"            {v}: {js_str(p['versoes'][v])},")
            L.append("          },")
            L.append(f"          resposta: {js_str(p['resposta'])}")
            L.append("        },")
        L.append("      ]")
        L.append("    },")
    L.append("  ]")
    L.append("};")
    return "\n".join(L)

# ----- MAIN -----
def main():
    args = sys.argv[1:]
    so_teste = "--teste" in args
    args = [a for a in args if a != "--teste"]
    arquivo = args[0] if args else ARQUIVO_ENTRADA

    if not os.path.exists(arquivo):
        print(f"Arquivo não encontrado: {arquivo}")
        sys.exit(1)

    with open(arquivo, "r", encoding="utf-8") as f:
        texto = f.read()

    print("Lendo e interpretando o arquivo...")
    capitulos = parse_importacao(texto)
    if not capitulos:
        print("Nenhuma seção (ex.: '1.2 Título') encontrada. Veja o formato.")
        sys.exit(1)

    total = sum(len(s["perguntas"]) for c in capitulos.values() for s in c["secoes"])
    print(f"Capítulos: {sorted(capitulos)} | Perguntas: {total}")
    for n_cap, dados in sorted(capitulos.items()):
        print(f"  Capítulo {n_cap}: {len(dados['secoes'])} seções, "
              f"{sum(len(s['perguntas']) for s in dados['secoes'])} perguntas")

    if so_teste:
        print("\n[modo --teste] Não vou buscar versículos.")
        print("Referências que serão buscadas:")
        for n_cap, dados in sorted(capitulos.items()):
            for sec in dados["secoes"]:
                for p in sec["perguntas"]:
                    status = "OK " if parse_referencia(p["versiculo"]) else "?? "
                    print(f"  {status} {sec['id']} P{p['numero']}: {p['versiculo']}")
        return

    print("\nCarregando Bíblias locais...")
    carregar_biblias()

    avisos = []
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    for n_cap, dados in sorted(capitulos.items()):
        print(f"\n[Capítulo {n_cap}]")
        for sec in dados["secoes"]:
            print(f"  {sec['titulo']} ({len(sec['perguntas'])} perguntas)")
            for p in sec["perguntas"]:
                preencher_versoes(p, avisos)
        caminho = os.path.join(PASTA_SAIDA, f"dados-capitulo-{n_cap}.js")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(gerar_arquivo(n_cap, dados))
        print(f"  -> {caminho} gerado")

    if avisos:
        print("\nAVISOS:")
        for a in avisos[:30]:
            print("  " + a)
        if len(avisos) > 30:
            print(f"  ... e mais {len(avisos) - 30} avisos")
    print("\nConcluído!")

if __name__ == "__main__":
    main()


# python importar_estudos.py
# python importar_estudos.py --teste 
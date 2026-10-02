# inspecionar_biblia.py — mostra a estrutura interna dos JSONs baixados
import json, os

def mostrar(obj, prefixo="", prof=0):
    if prof > 3:
        return
    if isinstance(obj, dict):
        for chave in list(obj.keys())[:6]:
            valor = obj[chave]
            print(f"{prefixo}{chave}: {type(valor).__name__} ({len(valor)} itens)" if isinstance(valor, (list, dict)) else f"{prefixo}{chave}: {type(valor).__name__}")
            mostrar(valor, prefixo + "  ", prof + 1)
    elif isinstance(obj, list) and obj:
        print(f"{prefixo}[lista com {len(obj)} itens]")
        mostrar(obj[0], prefixo + "  ", prof + 1)

for nome in ["naa", "ntlh", "nvi", "acf"]:
    caminho = os.path.join("biblia", f"{nome}.json")
    if not os.path.exists(caminho):
        print(f"NAO ENCONTRADO: {caminho}")
        continue
    print("=" * 55)
    print("ARQUIVO:", nome)
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    mostrar(dados)
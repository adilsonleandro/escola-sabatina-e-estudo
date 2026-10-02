# -*- coding: utf-8 -*-
# ============================================================
# Restaurador do data.js (v2)
# Lê um data.js ANTIGO (backup), extrai as constantes globais
# que não são TEMA_BIBLIA (ex.: LICOES, ESTUDOS — que são arrays)
# e reconstrói o data.js atual mantendo essas constantes + o
# registro dos capítulos em arquivos separados (js/dados/).
#
# Uso: python restaurar_data.py "CAMINHO_DO_BACKUP\js\data.js"
# ============================================================
import os
import sys
import re
import shutil

TOTAL_CAPITULOS = 20
ARQUIVO_DESTINO = os.path.join("js", "data.js")

def extrair_constantes(texto):
    """Extrai blocos 'const/let/var NOME = { ... };' OU '= [ ... ];'."""
    constantes = {}
    # aceita const, let ou var, e abertura com { ou [
    padrao = re.compile(r'\b(const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*([\[{])', re.S)

    for match in padrao.finditer(texto):
        nome = match.group(2)
        abridor = match.group(3)
        inicio = match.start(1)
        pos = texto.index(abridor, match.start(3))

        stack = []
        i = pos
        in_str = None
        while i < len(texto):
            c = texto[i]
            if in_str:
                if c == '\\':
                    i += 2
                    continue
                if c == in_str:
                    in_str = None
                i += 1
                continue
            if c in '"\'':
                in_str = c
                i += 1
                continue
            if c in '{[':
                stack.append(c)
            elif c in '}]':
                if stack and ((c == '}' and stack[-1] == '{') or (c == ']' and stack[-1] == '[')):
                    stack.pop()
                    if not stack:
                        fim = i + 1
                        if fim < len(texto) and texto[fim] == ';':
                            fim += 1
                        constantes[nome] = texto[inicio:fim].strip()
                        break
            i += 1
    return constantes

def montar_novo_data(blocos_preservados):
    linhas = []
    linhas.append("// ============================================================")
    linhas.append("// DADOS — Compreendendo a Bíblia")
    linhas.append("// Constantes de listagem (LICOES, ESTUDOS...) restauradas do")
    linhas.append("// data.js antigo + registro dos capítulos em js/dados/.")
    linhas.append("// ============================================================")
    linhas.append("")

    for bloco in blocos_preservados:
        linhas.append(bloco)
        linhas.append("")

    linhas.append("// --- Registro dos capítulos (cada um em js/dados/) ---")
    linhas.append("const TEMA_BIBLIA = {")
    linhas.append('  id: "biblia",')
    linhas.append('  titulo: "A Bíblia: Como estudá-la e compreendê-la",')
    linhas.append('  descricao: "Estudo completo sobre como estudar e compreender as Escrituras Sagradas.",')
    linhas.append("  capitulos: []")
    linhas.append("};")
    linhas.append("")
    linhas.append("// Registra cada capítulo que tiver um arquivo próprio carregado")
    for n in range(1, TOTAL_CAPITULOS + 1):
        linhas.append(f"if (typeof CAPITULO_{n} !== 'undefined') TEMA_BIBLIA.capitulos.push(CAPITULO_{n});")
    linhas.append("")

    return "\n".join(linhas)

def main():
    if len(sys.argv) < 2:
        print("Erro: informe o caminho do data.js antigo (backup).")
        print('Exemplo: python restaurar_data.py "C:\\backup\\js\\data.js"')
        sys.exit(1)

    caminho_backup = sys.argv[1]
    if not os.path.exists(caminho_backup):
        print(f"Erro: arquivo não encontrado: {caminho_backup}")
        sys.exit(1)

    with open(caminho_backup, "r", encoding="utf-8") as f:
        texto_antigo = f.read()

    constantes = extrair_constantes(texto_antigo)

    preservar = {nome: bloco for nome, bloco in constantes.items() if nome != "TEMA_BIBLIA"}

    if not preservar:
        print("Aviso: nenhuma constante além de TEMA_BIBLIA encontrada.")
        print("Constantes detectadas no arquivo:", list(constantes.keys()) or "nenhuma")
        print("Verifique se o backup realmente contém LICOES/ESTUDOS.")
    else:
        print("Constantes encontradas e que serão preservadas:")
        for nome in preservar:
            print(f"  - {nome}")

    if os.path.exists(ARQUIVO_DESTINO):
        backup_local = ARQUIVO_DESTINO + ".bak"
        shutil.copy2(ARQUIVO_DESTINO, backup_local)
        print(f"Backup do data.js atual salvo em: {backup_local}")

    novo_conteudo = montar_novo_data(list(preservar.values()))

    with open(ARQUIVO_DESTINO, "w", encoding="utf-8") as f:
        f.write(novo_conteudo)

    print(f"\nConcluído! Novo data.js gerado em: {ARQUIVO_DESTINO}")

if __name__ == "__main__":
    main()
    
 # python restaurar_data.py "C:\Users\adilson.rosa\OneDrive - Adventistas\01_projetos\compreendendo_a_biblia\backup\2026-09-30T13-48-05\js\data.js"   
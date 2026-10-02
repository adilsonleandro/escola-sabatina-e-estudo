# -*- coding: utf-8 -*-
# ============================================================
# Script de BACKUP do projeto "Compreendendo a Bíblia"
# Copia a pasta do projeto para backup/<data-hora>/
# Uso: python fazer_backup.py
# ============================================================
import os
import sys
import shutil
from datetime import datetime

# ------------------------------------------------------------------
# 1) CONFIGURAÇÃO
# ------------------------------------------------------------------
# Pasta onde ficam os backups (criada automaticamente)
PASTA_BACKUP = "backup"

# Arquivos/pastas que NÃO devem ser copiados (evita backup dentro de backup)
IGNORAR = {
    "backup",               # não copia backups antigos
    "__pycache__",
    ".git",
    ".vscode",
    "node_modules",
}

# ------------------------------------------------------------------
# 2) FUNÇÃO DE CÓPIA
# ------------------------------------------------------------------
def copiar_projeto(origem, destino):
    """Copia o conteúdo da pasta origem para destino, ignorando IGNORAR."""
    if not os.path.exists(destino):
        os.makedirs(destino)

    itens = os.listdir(origem)
    copiados = 0

    for item in itens:
        caminho_origem = os.path.join(origem, item)
        caminho_destino = os.path.join(destino, item)

        if item in IGNORAR:
            print(f"  [ignorado] {item}")
            continue

        try:
            if os.path.isdir(caminho_origem):
                shutil.copytree(caminho_origem, caminho_destino)
            else:
                shutil.copy2(caminho_origem, caminho_destino)
            copiados += 1
        except Exception as e:
            print(f"  [erro] {item}: {e}")

    return copiados

# ------------------------------------------------------------------
# 3) EXECUÇÃO PRINCIPAL
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Pasta atual do projeto (onde o script está)
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))

    # Nome do backup com data e hora
    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pasta_destino = os.path.join(pasta_projeto, PASTA_BACKUP, agora)

    print(f"Projeto: {pasta_projeto}")
    print(f"Backup em: {pasta_destino}")
    print("Copiando arquivos...")

    total = copiar_projeto(pasta_projeto, pasta_destino)

    print(f"\nConcluído! {total} itens copiados.")
    print(f"Backup salvo em: {pasta_destino}")

#     python fazer_backup.py
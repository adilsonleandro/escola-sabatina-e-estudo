# Instruções de Backup e Restauração

Este guia explica como fazer backup e restaurar o site "Compreendendo a Bíblia".

---

## Fazer Backup

### Comando

```bash
node backup.js
```

### O que acontece

1. Cria uma pasta em `backup/` com data e hora
2. Copia todos os arquivos importantes
3. Mostra o resultado

### Exemplo de saída

```
========================================
BACKUP DO SITE — Compreendendo a Bíblia
========================================
Data: 29/09/2026, 21:14:12
Pasta: backup\2026-09-30T00-14-12
----------------------------------------
✓ index.html
✓ licoes.html
✓ estudos.html
✓ estudo-detalhe.html
✓ estudo-professor.html
✓ tema-biblia.html
✓ css
✓ js
----------------------------------------
Backup concluído: 8 itens, 0 erros
========================================
```

---

## Listar Backups Disponíveis

### Comando

```bash
dir backup
```

### Ou pelo explorador de arquivos

Abra a pasta `backup/` no explorador de arquivos.

---

## Restaurar Backup

### Passo 1: Escolher o backup

Liste os backups disponíveis e escolha qual restaurar.

### Passo 2: Pedir restauração

Diga ao assistente:

> "Restaurar backup de [data/hora]"

Exemplo:

> "Restaurar backup de 2026-09-30T00-14-12"

### Passo 3: Confirmação

O assistente vai:

1. Mostrar o que será restaurado
2. Pedir confirmação
3. Copiar os arquivos de volta

---

## Estrutura de Pastas

```
compreendendo_a_biblia/
├── backup/                    ← Pasta de backups
│   ├── 2026-09-30T00-14-12/  ← Backup 1
│   │   ├── index.html
│   │   ├── licoes.html
│   │   ├── estudos.html
│   │   ├── estudo-detalhe.html
│   │   ├── estudo-professor.html
│   │   ├── tema-biblia.html
│   │   ├── css/
│   │   └── js/
│   └── 2026-09-30T00-15-30/  ← Backup 2
│       └── ...
├── index.html
├── licoes.html
├── estudos.html
├── estudo-detalhe.html
├── estudo-professor.html
├── tema-biblia.html
├── css/
└── js/
```

---

## Quando Fazer Backup

| Situação | Fazer backup? |
|----------|---------------|
| Antes de alterações grandes | Sim |
| Depois de adicionar conteúdo | Sim |
| Antes de atualizar o site | Sim |
| Semanalmente | Recomendado |

---

## Dicas

| Dica | Beneficio |
|------|-----------|
| **Backup antes de editar** | Segurança extra |
| **Backup sempre que adicionar conteúdo** | Não perde trabalho |
| **Manter pelo menos 3 backups** | Opções de restauração |
| **Nomear backups pela data** | Fácil de identificar |

---

## Solução de Problemas

| Problema | Solução |
|----------|---------|
| `node backup.js` não funciona | Verifique se Node.js está instalado |
| Pasta backup não foi criada | Verifique permissões da pasta |
| Arquivo não foi copiado | Verifique se o arquivo existe |

---

## Contato

Dúvidas ou problemas: adilsonrosa2@educadventista.org.br

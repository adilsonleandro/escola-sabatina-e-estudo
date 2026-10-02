# Arquivos para Publicar no GitHub

## Estrutura que deve ser enviada ao repositório

```
compreendendo-a-biblia/
├── index.html
├── licoes.html
├── estudos.html
├── estudo-detalhe.html
├── estudo-professor.html
├── tema-biblia.html
├── secao-biblia.html
├── css/
│   └── style.css
├── js/
│   ├── app.js
│   ├── data.js
│   ├── data-loader.js
│   ├── respostas.js
│   └── dados/
│       ├── dados-capitulo-1.js
│       ├── dados-capitulo-2.js
│       ├── dados-capitulo-3.js
│       ├── dados-capitulo-4.js
│       ├── dados-capitulo-5.js
│       ├── dados-capitulo-6.js
│       ├── dados-capitulo-7.js
│       ├── dados-capitulo-8.js
│       ├── dados-capitulo-9.js
│       ├── dados-capitulo-10.js
│       ├── dados-capitulo-11.js
│       ├── dados-capitulo-12.js
│       ├── dados-capitulo-13.js
│       ├── dados-capitulo-14.js
│       ├── dados-capitulo-15.js
│       ├── dados-capitulo-16.js
│       ├── dados-capitulo-17.js
│       ├── dados-capitulo-18.js
│       ├── dados-capitulo-19.js
│       └── dados-capitulo-20.js
├── data/
│   ├── capitulo-1.json
│   └── capitulo-2.json
├── img/
│   └── (imagens do site, se houver)
├── README.md
└── .gitignore
```

## Arquivos que NÃO devem ser enviados

- `backup/` — cópias de segurança
- `estudos/` — arquivos de desenvolvimento (.docx, .py, .txt)
- `prompts/` — arquivos de prompts
- `biblia/` — arquivos de inspeção
- `*.py` — scripts Python de desenvolvimento
- `*.txt` — arquivos temporários
- `*.bak` — backups
- `verificar.vbs` — script de verificação

## Como publicar

1. Crie um repositório no GitHub chamado `compreendendo-a-biblia`
2. Faça upload de todos os arquivos listados acima
3. Ative o GitHub Pages em Settings → Pages → main branch
4. Aguarde 2-3 minutos e acesse `https://SEU-USUARIO.github.io/compreendendo-a-biblia/`

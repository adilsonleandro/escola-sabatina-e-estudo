# Guia Completo: Publicar no GitHub Pages

Este guia explica passo a passo como publicar o site "Compreendendo a Bíblia" no GitHub Pages.

---

## Pré-requisitos

- Conta no GitHub (gratuita)
- Todos os arquivos do projeto organizados

---

## Passo 1: Criar conta no GitHub

1. Acesse: https://github.com
2. Clique em **"Sign up"**
3. Informe seu e-mail, crie uma senha e nome de usuário
4. Confirme o e-mail
5. **Importante:** Anote seu nome de usuário (ex: `adilsonrosa`)

---

## Passo 2: Criar um repositório

1. No GitHub, clique no botão **"+"** (canto superior direito)
2. Selecione **"New repository"**
3. Preencha:
   - **Repository name:** `compreendendo-a-biblia`
   - **Description:** `Site de estudos bíblicos e lições da Escola Sabatina`
   - **Public** (selecione esta opção)
   - Marque **"Add a README file"**
4. Clique em **"Create repository"**

---

## Passo 3: Fazer upload dos arquivos

### Opção A: Upload pelo site (mais fácil)

1. No repositório criado, clique em **"uploading an existing file"**
2. Arraste todos os arquivos do projeto:
   ```
   index.html
   licoes.html
   estudos.html
   estudo-detalhe.html
   estudo-professor.html
   css/
   └── style.css
   js/
   ├── data.js
   └── app.js
   ```
3. Clique em **"Commit changes"**

### Opção B: Usar Git (avançado)

```bash
git init
git add .
git commit -m "Primeiro commit"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/compreendendo-a-biblia.git
git push -u origin main
```

---

## Passo 4: Ativar GitHub Pages

1. No repositório, clique em **"Settings"** (menu superior)
2. No menu lateral esquerdo, clique em **"Pages"**
3. Em **"Build and deployment"**:
   - **Source:** Select `Deploy from a branch`
   - **Branch:** Selecione `main`
   - **Folder:** Selecione `/ (root)`
4. Clique em **"Save"**

---

## Passo 5: Aguardar e acessar

1. Aguarde 2-3 minutos (o GitHub está construindo o site)
2. Atualize a página de Settings → Pages
3. Você verá uma mensagem verde: **"Your site is live at..."**
4. Clique no link para acessar

---

## URL do site

```
https://SEU-USUARIO.github.io/compreendendo-a-biblia/
```

**Exemplo:**
```
https://adilsonrosa.github.io/compreendendo-a-biblia/
```

---

## Como atualizar o site

Sempre que fizer alterações nos arquivos:

1. Acesse o repositório no GitHub
2. Clique no arquivo que deseja editar
3. Clique no ícone de lápis (✏️) para editar
4. Ou clique em **"Add file"** → **"Upload files"** para novos arquivos
5. Clique em **"Commit changes"**
6. Aguarde 1-2 minutos para o site atualizar

---

## Estrutura final no GitHub

```
compreendendo-a-biblia/
├── index.html
├── licoes.html
├── estudos.html
├── estudo-detalhe.html
├── estudo-professor.html
├── css/
│   └── style.css
├── js/
│   ├── data.js
│   └── app.js
├── README.md
└── .gitignore
```

---

## Solução de problemas

| Problema | Solução |
|----------|---------|
| Site não carrega | Aguarde 5 minutos e atualize a página |
| CSS não carrega | Verifique se o caminho está correto (`css/style.css`) |
| JS não funciona | Verifique se o caminho está correto (`js/data.js`, `js/app.js`) |
| Página 404 | Verifique se o arquivo `index.html` está na raiz |
| Erro de permissão | Verifique se o repositório é **Public** |

---

## Domínio personalizado (opcional)

Se quiser um domínio personalizado (ex: `compreendendoabiblia.com.br`):

1. Compre o domínio em qualquer registrador (Registro.br, GoDaddy, etc.)
2. Em Settings → Pages → Custom domain, informe o domínio
3. Configure o DNS conforme instruções do GitHub

---

## Contato

Dúvidas ou problemas: adilson.rosa2@gmail.com

# Instruções de Publicação e Gerenciamento

Este guia explica como publicar, visualizar e gerenciar o site no GitHub Pages.

---

## 1. Publicar o site (primeira vez)

### Passo 1: Criar conta no GitHub
- Acesse: https://github.com
- Clique em **"Sign up"**
- Informe e-mail, senha e nome de usuário
- Confirme o e-mail

### Passo 2: Criar repositório
- Clique no botão **"+"** (canto superior direito)
- Selecione **"New repository"**
- Nome: `compreendendo-a-biblia` (ou outro de sua preferência)
- Marque **"Public"**
- Marque **"Add a README file"**
- Clique em **"Create repository"**

### Passo 3: Fazer upload dos arquivos
- No repositório, clique em **"uploading an existing file"**
- Arraste todos os arquivos do projeto:
  - `index.html`
  - `licoes.html`
  - `estudos.html`
  - `estudo-detalhe.html`
  - `estudo-professor.html`
  - `css/style.css`
  - `js/data.js`
  - `js/app.js`
- Clique em **"Commit changes"**

### Passo 4: Ativar GitHub Pages
- Vá em **Settings** → **Pages**
- Em **"Build and deployment"**:
  - **Source:** `Deploy from a branch`
  - **Branch:** `main`
  - **Folder:** `/ (root)`
- Clique em **"Save"**

### Passo 5: Aguardar e acessar
- Aguarde 2-3 minutos
- Atualize a página Settings → Pages
- Você verá a mensagem verde: **"Your site is live at..."**
- Clique no link para acessar

---

## 2. Visualizar o link do site

### Opção 1: Pelo GitHub
1. Acesse seu repositório
2. Vá em **Settings** → **Pages**
3. O link aparece no topo da página

### Opção 2: Pelo navegador
- O link sempre terá este formato:
  ```
  https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/
  ```

### Exemplo
```
https://adilsonrosa2.github.io/compreendendo-a-biblia/
```

---

## 3. Enviar o link para outras pessoas

Basta copiar o link e enviar por:
- WhatsApp
- E-mail
- Redes sociais
- Mensagens

---

## 4. Atualizar o site (depois de publicado)

### Alterar um arquivo existente
1. Acesse o repositório
2. Clique no arquivo que deseja editar
3. Clique no ícone de lápis (✏️)
4. Faça as alterações
5. Clique em **"Commit changes"**
6. Aguarde 1-2 minutos para o site atualizar

### Adicionar novo arquivo
1. Acesse o repositório
2. Clique em **"Add file"** → **"Upload files"**
3. Arraste o novo arquivo
4. Clique em **"Commit changes"**
5. Aguarde 1-2 minutos

### Adicionar nova pasta
1. Clique em **"Add file"** → **"Create new file"**
2. Nomeie: `nome-da-pasta/nome-do-arquivo.extensao`
3. O GitHub cria a pasta automaticamente
4. Cole o conteúdo do arquivo
5. Clique em **"Commit changes"**

---

## 5. Trocar o link do site

### Trocar o nome do repositório
1. Vá em **Settings**
2. Em **"Repository name"**, apague o nome atual
3. Digite o novo nome
4. Clique em **"Rename"**
5. O link muda automaticamente

### Trocar o nome de usuário
1. Clique na sua **foto** (canto superior direito)
2. Vá em **Settings**
3. No menu lateral, clique em **"Account"**
4. Clique em **"Change username"**
5. Digite o novo nome
6. Clique em **"Change username"**
7. O link muda automaticamente

---

## 6. Solução de problemas

| Problema | Solução |
|----------|---------|
| Site não carrega | Aguarde 5 minutos e atualize a página |
| Página 404 | Verifique se `index.html` está na raiz do repositório |
| CSS não carrega | Verifique se o caminho está correto (`css/style.css`) |
| JS não funciona | Verifique se os arquivos estão em `js/` |
| Site não atualiza | Aguarde 2-3 minutos e atualize com Ctrl+F5 |
| Erro de permissão | Verifique se o repositório é **Public** |
| Link não funciona após renomear | Aguarde 5 minutos e atualize a página |

---

## 7. Estrutura do site

```
compreendendo-a-biblia/
├── index.html              (página inicial)
├── licoes.html             (lições da Escola Sabatina)
├── estudos.html            (estudos por tema)
├── estudo-detalhe.html     (detalhe de estudo/lição)
├── estudo-professor.html   (estudo para professores)
├── css/
│   └── style.css           (estilos)
├── js/
│   ├── data.js             (dados dos estudos)
│   └── app.js              (funcionalidades)
├── README.md
└── .gitignore
```

---

## 8. Checklist de publicação

- [ ] Conta no GitHub criada
- [ ] Repositório criado
- [ ] Arquivos enviados
- [ ] GitHub Pages ativado
- [ ] Site acessível pelo link
- [ ] Link testado no celular
- [ ] Link enviado para outras pessoas

---

## Contato

Dúvidas ou problemas: adilson.rosa2@gmail.com

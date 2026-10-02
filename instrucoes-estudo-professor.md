# Instruções para Estudo do Professor

Este arquivo contém as instruções para adicionar o estudo do professor à lição da Escola Sabatina.

---

## Como usar

1. **Toda semana**, envie o material do estudo para professores no chat
2. Diga: **"Segue as instruções do estudo do professor"**
3. Eu adiciono automaticamente ao `data.js` e o estudo fica disponível na página da lição

---

## Passo a passo que eu sigo

### 1. Receber o material

O material pode ser enviado como:
- Texto colado diretamente no chat
- Arquivo PDF ou DOCX

### 2. Identificar a estrutura

Extrair do material:
- **Título do estudo**
- **Subtítulo**
- **Verso-chave**
- **Objetivo da lição**
- **Orientações pedagógicas**
- **Slides** (tópicos de cada slide)
- **Aprofundamentos teológicos**

### 3. Adicionar ao data.js

Adicionar o campo `estudoProfessor` na lição correspondente:

```javascript
estudoProfessor: {
  titulo: "Título do Estudo",
  subtitulo: "Subtítulo do Estudo",
  versoChave: "Verso-chave",
  objetivo: "Objetivo da lição",
  orientacoes: [
    "Orientação 1",
    "Orientação 2"
  ],
  slides: [
    {
      titulo: "Título do Slide",
      topicos: [
        "Tópico 1",
        "Tópico 2"
      ],
      nota: "Nota didática (opcional)"
    }
  ],
  aprofundamentos: [
    {
      titulo: "Título do Aprofundamento",
      texto: "Texto do aprofundamento"
    }
  ]
}
```

### 4. Validar

- Validar o `data.js` com Node.js
- Confirmar que não há erros de sintaxe

### 5. Confirmar

- Informar ao usuário que o estudo foi adicionado
- Mostrar resumo do que foi done

---

## Formato do material enviado

O material deve conter:
- Título e subtítulo
- Verso-chave
- Objetivo da lição
- Orientações pedagógicas
- Slides com tópicos
- Aprofundamentos teológicos

---

## Formato de exibição

O estudo é exibido na página com:

| Seção | Formato |
|-------|---------|
| **Objetivo da Lição** | Card com gradiente verde e ícone 🎯 |
| **Verso para Memorização** | Card com gradiente amarelo e ícone 📖 |
| **Orientações Pedagógicas** | Cards verdes com barra superior gradiente |
| **Estrutura da Apresentação** | Slides com header azul e cards para tópicos |
| **Aprofundamento Teológico** | Cards com borda lateral azul e ícone 📖 |

### Negrito automático

Palavras antes dos dois pontos (`:`) são automaticamente exibidas em **negrito** nos tópicos dos slides e nas orientações pedagógicas.

---

## Onde aparece

O estudo aparece:
- Na página da lição (estudo-detalhe.html), através do botão **"Estudo para professores"**
- Na página estudo-professor.html, com o conteúdo completo

---

## Observações importantes

- O estudo é específico para cada lição
- Os slides devem ser organizados em ordem didática
- As orientações pedagógicas são importantes para o professor
- Os aprofundamentos teóricos ajudam na preparação da aula
- Palavras antes dos dois pontos ficam em negrito automaticamente

---

## Estrutura do site

```
compreendendo_a_biblia/
├── index.html              (página inicial)
├── licoes.html             (lições da Escola Sabatina)
├── estudos.html            (estudos por tema)
├── estudo-detalhe.html     (detalhe de estudo/lição)
├── estudo-professor.html   (estudo para professores)
├── tema-biblia.html        (tema: A Bíblia)
├── secao-biblia.html       (seções do tema A Bíblia)
├── css/
│   └── style.css           (estilos)
├── js/
│   ├── data.js             (dados dos estudos)
│   ├── respostas.js        (respostas extraídas)
│   └── app.js              (funcionalidades)
├── COMO-PUBLICAR.md        (guia de publicação)
├── instrucoes-licao-abertura.md (instruções para lição abertura)
├── instrucoes-estudo-professor.md (este arquivo)
└── instrucoes_estudo_bíblico.md   (instruções para novos estudos)
```

---

## Contato

Dúvidas ou problemas: adilson.rosa2@gmail.com

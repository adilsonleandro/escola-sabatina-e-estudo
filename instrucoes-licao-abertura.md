# Instruções para Lição Abertura

Este arquivo contém as instruções para popular automaticamente a lição da Escola Sabatina (abertura + estudo completo).

---

## Como usar

1. **Toda sábado de manhã**, eu vou no site da CPB e busco a lição da semana
2. Eu crio automaticamente a **abertura** e o **estudo completo** da lição
3. O conteúdo aparece na página da lição

---

## Passo a passo que eu sigo

### 1. Acessar o site da CPB

Acesse: https://mais.cpb.com.br/licao-adultos/

### 2. Identificar a lição da semana

- Buscar a lição que está ativa no momento
- Identificar: título, versículo principal, data de início e data de término

### 3. Extrair informações da abertura

Extrair do site:
- **Título da lição**
- **Versículo principal**
- **Data de início** (ex: "26 de setembro")
- **Data de término** (ex: "02 de outubro")
- **Resumo da lição** (texto introdutório do site)
- **Reflexão inicial** (poucas palavras resumindo a lição)

### 4. Extrair o estudo completo

Extrair do site:
- **Título da lição**
- **Versículo principal**
- **Período** (data início e fim)
- **Resumo da lição**
- **Reflexão inicial**
- **Estudo completo** (tópicos, perguntas, respostas)

### 5. Criar a abertura

Criar uma abertura com:
- Título da lição
- Versículo principal
- Período: "26 de setembro a 02 de outubro"
- Resumo da lição (2-3 parágrafos)
- Reflexão inicial (poucas palavras)

### 6. Criar o estudo

Criar o estudo com:
- Título da lição
- Versículo principal
- Período
- Resumo
- Reflexão inicial
- Estudo completo (tópicos, perguntas, respostas)

### 7. Formato da abertura

```
[Versículo principal]

Período: [data início] a [data término]

[Resumo da lição - 2-3 parágrafos]

[Reflexão inicial - poucas palavras]
```

### 8. Formato do estudo

```
[Versículo principal]

Período: [data início] a [data término]

[Resumo da lição]

[Reflexão inicial]

[Estudo completo - tópicos, perguntas, respostas]
```

### 9. Onde aparece

- A abertura aparece **somente na página da lição** (licao-detalhe.html)
- O estudo aparece **na página da lição** após clicar em "Estudar"

---

## Exemplo de abertura

```
"Antigamente, Deus falou, muitas vezes e de muitas maneiras, aos pais, pelos profetas, mas, nestes últimos dias, nos falou pelo Filho, a quem constituiu herdeiro de todas as coisas e pelo qual também fez o Universo" — Hebreus 1:1, 2

Período: 26 de setembro a 02 de outubro

A lição desta semana aborda como Deus se comunica com a humanidade, desde o Éden até os dias atuais, através dos profetas, da Bíblia e de Jesus Cristo.

Veremos que a Bíblia é a Palavra de Deus, inspirada pelo Espírito Santo, e que através dela Deus revela Seu amor e Sua vontade para a humanidade.

Que esta semana possamos aprender mais sobre como Deus fala conosco.
```

---

## Quando executar

**Toda sábado de manhã**, criar a abertura e o estudo da próxima lição.

---

## Observações importantes

- A abertura deve ser curta e objetiva (2-3 parágrafos)
- A reflexão inicial deve ser breve (poucas palavras)
- As datas devem ser exatamente como estão no site da CPB
- O versículo deve ser o mesmo do site da CPB
- A abertura aparece somente na página da lição
- O estudo deve ser completo (tópicos, perguntas, respostas)

---

## Estrutura do site

```
compreendendo_a_biblia/
├── index.html              (página inicial)
├── licoes.html             (lições da Escola Sabatina)
├── estudos.html            (estudos por tema)
├── tema-biblia.html        (tema: A Bíblia)
├── secao-biblia.html       (seções do tema A Bíblia)
├── css/
│   └── style.css           (estilos)
├── js/
│   ├── data.js             (dados dos estudos)
│   ├── respostas.js        (respostas extraídas)
│   └── app.js              (funcionalidades)
├── COMO-PUBLICAR.md        (guia de publicação)
├── INSTRUCAES-LICAO-PROFESSOR.md (este arquivo)
└── instrucoes_estudo_bíblico.md   (instruções para novos estudos)
```

---

## Contato

Dúvidas ou problemas: adilson.rosa2@gmail.com

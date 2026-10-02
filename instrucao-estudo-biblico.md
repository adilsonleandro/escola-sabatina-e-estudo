# Instruções para Adicionar Novo Estudo

Este guia explica como adicionar novas seções ao tema "A Bíblia" (ou outros temas).

---

## Como usar

1. Envie o texto do estudo no formato abaixo
2. Diga: **"Adicionar novo estudo"**
3. Eu processo e adiciono ao `data.js`
4. Validamos juntos

---

## Formato do texto

```
ESTUDO
Seção: [número e título da seção]
Perguntas:
1. [pergunta] (versículo) [resposta]
2. [pergunta] (versículo) [resposta]
3. [pergunta] (versículo) [resposta]
...
```

**Ordem correta:**
1. Pergunta
2. Versículo entre parênteses
3. Resposta entre colchetes

---

## Exemplo completo

```
ESTUDO
Seção: 1.2 O Estudo das Escrituras
Perguntas:
1. Qual é o conselho do profeta Isaías, referente às Escrituras? (Is 34:16) [Buscai no livro do SENHOR e ledes]
2. Por que os bereanos foram louvados? (At 17:11) [examinando as Escrituras todos os dias para ver se as coisas eram de fato assim]
3. Que comparação indica que algumas porções da Palavra de Deus são mais difíceis de ser compreendidas? (Hb 5:12) [quais são os princípios elementares dos oráculos de Deus]
4. De que modo é mais bem explicada esta comparação? (Hb 5:13) [porque é criança]
5. Que escritos são especificamente mencionados como contendo pontos difíceis de entender? (2Pe 3:16) [Paulo vos escreveu, segundo a sabedoria que lhe foi dada]
```

---

## Regras importantes

| Regra | Exemplo |
|-------|---------|
| **Pergunta** | Texto antes do primeiro `(` |
| **Versículo** | Texto entre `(` e `)` |
| **Resposta** | Texto entre `[` e `]` |
| **Número** | Sempre sequencial (1, 2, 3...) |

---

## Ordem correta

```
1. [pergunta] (versículo) [resposta]
   ↑          ↑            ↑
   Pergunta   Versículo     Resposta
```

---

## O que eu faço

1. **Extraio** perguntas, respostas e versículos
2. **Corrijo** o português (gramática, ortografia, clareza)
3. **Busco** as 4 versões bíblicas (NAA, NTLH, NVI, AFC)
4. **Adiciono** ao `data.js` na seção correta
5. **Valido** a sintaxe
6. **Testo** no navegador

---

## Correção do português

| Aspecto | Orientação |
|---------|------------|
| **Gramática** | Corrigir erros de concordância, regência e pontuação |
| **Ortografia** | Corrigir erros de ortografia |
| **Clareza** | Garantir que o texto seja claro e fácil de entender |
| **Padronização** | Usar a mesma forma de escrita em todo o texto |

### Exemplos de correção

| Antes | Depois |
|-------|--------|
| "Os céus por Sua palavra se fizeram" | "Os céus foram feitos pela palavra de Deus" |
| "Ele falou, e tudo se fez" | "Ele falou, e tudo foi feito" |
| "A palavra de Deus é viva" | "A Palavra de Deus é viva e eficaz" |

---

## Estrutura no data.js

```javascript
{
  id: "1-2",
  titulo: "1.2 O Estudo das Escrituras",
  perguntas: [
    {
      numero: 1,
      pergunta: "...",
      resposta: "...",
      versiculo: "...",
      texto: "...",
      versoes: {
        naa: "...",
        ntlh: "...",
        nvi: "...",
        afc: "..."
      }
    }
  ]
}
```

---

## Seções existentes

| Seção | Título | Status |
|-------|--------|--------|
| 1.1 | As Escrituras Sagradas | Existe |
| 1.2 | O Estudo das Escrituras | Pendente |
| 1.3 | O Poder da Palavra de Deus | Pendente |
| 1.4 | A Palavra Vivificante | Existe |
| 1.5 | Cristo em Toda a Escritura Sagrada | Existe |

---

## Dicas

| Dica | Beneficio |
|------|-----------|
| **Cole o texto direto** | Não precisa formatar muito |
| **Mantenha a ordem** | Perguntas numeradas sequencialmente |
| **Versículos completos** | Facilita a busca das versões |

---

## Solução de problemas

| Problema | Solução |
|----------|---------|
| Formato não reconhecido | Verifique se está seguindo o exemplo |
| Versículo não encontrado | Escreva o versículo completo |
| Erro no data.js | Eu corrijo automaticamente |

---

## Contato

Dúvidas ou problemas: adilsonrosa2@educadventista.org.br

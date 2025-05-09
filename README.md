# Projeto Casa da Moeda

## Objetivo

O objetivo é a construção de uma aplicação que faça um controle das finanças pessoais do usuário, utilizando um chat bot no Telegram e registrando esses gastos numa planilha do Google Sheets. A construção das funcionalidades é feita com python e está prevista pelo menos 4 etapas de projeto.

### Etapas

**1° Etapa:**

Feita diretamente no chat usando os comandos /gasto e /litar

- [x] Registro de gastos
- [x] Listagem de dados

**2° Etapa:**

- [x] Criação de botões de gasto e listagem
- [ ] Criação de botões de categorias
- [ ] Separação de gastos no Débito e Crédito

**3° Etapa:**

- [ ] Criação dos alertas
- [ ] Soma de total gasto por categoria
- [ ] Filtros de listagem para o mês (Algo no formato de /listar Mês)

**4° Etapa:** (Se possível, usando Docling)

- [ ] Processamento de imagens de comprovantes
- [ ] Chat simples com IA para análise dos gastos
  
## Como configurar o Chat no telegram

1. Acesse o BotFather
   1. Siga as etapas descritas no Bot para a criação de um seu.
2. Guarde o Token.

## Como configurar o Google Sheets

1. Você pode acompanhar o passo a passo a partir do vídeo da Assimov Academy
   1. [Como integrar a API do Google Sheets com Python - básico ao avançado](https://www.youtube.com/watch?v=6XaF4ZF7LW0&ab_channel=AsimovAcademy) a partir do minuto 8:50.

## Como usar o projeto localmente

- Clone o repositório

    ~~~git
     git clone https://github.com/BelleVimercati/CasaDaMoeda 
     ~~~

- Crie um arquivo .env e adicione as seguintes variáveis:

    ~~~bash
        TOKEN_BOT = "Adicione o token do seu bot"
        PLANILHA_ID = "Adicione o Id da sua planilha"
        ARQUIVO_CREDENCIAIS = "Adicione as credenciais do arquivo"
    ~~~~

- Instale as dependências descritas no arquivo requirements.txt
- Rode o arquivo main.py

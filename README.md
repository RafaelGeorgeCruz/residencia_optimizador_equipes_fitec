# Formador de Equipes Automáticas com Otimização e IA

## Descrição do Projeto

Este projeto visa desenvolver uma ferramenta automática para a formação de equipes dentro da empresa Fitec. A solução utiliza um modelo matemático de otimização para alocar colaboradores em equipes com base em suas características, funções e performance. Após a alocação, agentes de Inteligência Artificial, utilizando o modelo Google Gemini 2.0 Flash, serão empregados para gerar um resumo dos currículos dos candidatos selecionados e um resumo do projeto.

O objetivo principal é otimizar o processo de formação de equipes, garantindo a melhor combinação de habilidades e expertises para cada projeto, além de fornecer resumos informativos para o gerenciamento.

## Arquivos do Projeto

A estrutura básica do projeto inclui os seguintes arquivos:

- `README.md`: Este arquivo, contendo a descrição e instruções do projeto.
- `requirements.txt`: Lista das bibliotecas Python necessárias para executar o projeto.
- `.env`: Arquivo para armazenar variáveis de ambiente sensíveis, como chaves de API.
- `.gitignore`: Especifica arquivos e diretórios que o Git deve ignorar.
- `data/`: Diretório para armazenar os dados dos colaboradores e informações do projeto.
- `src/`: Diretório responsável pelo código da API

## Requisitos

Antes de executar o projeto, certifique-se de ter instalado o Python e o pip (gerenciador de pacotes do Python).

### Dependências

As bibliotecas Python no requirements.tx são necessárias:

Para instalar as dependências em uma venv (recomendado), execute o seguinte comando:

```bash
python -m venv .venv
```

```bash
activate .venv/Scripts/acivate
```

```bash
pip install -r requirements.txt
```

### Variáveis de ambiente

Cheque se as variáveis de ambiente estão devidamentes configuradas, para esse projeto é necessário uma chave de API do gemini, para conseguir uma, entre em:
[Gemini_API_KEY](https://aistudio.google.com/apikey)

no arquivo env

```bash
GOOGLE_GEMINI_API_KEY="<sua_chave_de_api_gemini_aqui>"
```

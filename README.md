# 💸 Agente Financeiro Pessoal com Azure AI

Este projeto é uma solução completa (Full-Stack) de um assistente de Inteligência Artificial capaz de analisar transações financeiras pessoais e responder perguntas em linguagem natural.

O sistema é dividido em duas partes principais:

1. **Back-End (Cérebro):** Configurado no Azure AI Foundry + Azure AI Search.

2. **Front-End (Interface):** Aplicação web interativa feita em Streamlit e hospedada no Azure App Service.

### 🎯 Objetivo do Projeto

Demonstrar como criar um **Assistente Financeiro Pessoal** seguro e escalável utilizando a nuvem da Microsoft. O projeto resolve o problema de analisar planilhas financeiras complexas, permitindo que o usuário faça perguntas simples como *"Quanto gastei com transporte?"* e receba respostas baseadas em seus próprios dados.

O foco técnico é a implementação da arquitetura **RAG (Retrieval-Augmented Generation),** onde o Agente de IA consulta uma base de dados real (CSV) antes de responder, garantindo precisão e evitando alucinações.

### 📂 Estrutura do Projeto

* [📄 Guia do Back-End (Infraestrutura)](back-end/README.md)

    * Como criar os recursos no Azure (Resource Group, Storage, AI Search).

    * Como configurar o agente "cérebro" no Azure Foundry.

    * Como indexar os dados (CSV) na "memória" da IA.

* [💻 Guia do Front-End (Interface)](front-end/README.md)

    * Como rodar o chat no seu computador.

    * Como publicar o site na nuvem (Azure Web App).

    * Configuração de segurança e conexão com o agente.

### 🚀 Como Gerar os Dados de Teste (Passo Zero)

Antes de configurar a nuvem ou o site, você precisa criar o arquivo de transações bancárias fictícias `(mock_transactions.csv).`

#### 1. Pré-requisitos

Você precisa ter o [Python](https://www.python.org/downloads/) instalado.

#### 2. Instalar bibliotecas 

Abra seu terminal na pasta raiz do projeto e instale as ferramentas de dados:

```bash
   pip install pandas faker
```

#### 3. Gerar o arquivo

Execute o script de geração (certifique-se de ter o arquivo `generate_data.py` na pasta):

```bash
   python generate_data.py
```
✅ **Resultado:** Um arquivo chamado `mock_transactions.csv` será criado. Você usará este arquivo para alimentar a "memória" do seu Agente no Azure.

---

### 🛠️ Tecnologias Utilizadas

* **Cloud:** Microsoft Azure

* **IA:** Azure OpenAI (GPT-4o)

* **Busca Vetorial:** Azure AI Search

* **Linguagem:** Python 3.11

* **Interface:** Streamlit

---

### ⚠️ Aviso de Custos

Este projeto utiliza recursos de nuvem que podem gerar cobranças (especialmente o **Azure AI Search).** Lembre-se de excluir o Grupo de Recursos no portal do Azure ao finalizar seus testes para evitar custos indesejados.
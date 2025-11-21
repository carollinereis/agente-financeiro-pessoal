# Agente Financeiro com Azure Foundry 🤖

Este documento detalha o processo de construção de um agente de IA capaz de responder a perguntas sobre dados financeiros pessoais.

O projeto utiliza o **Azure Foundry** para o "cérebro" (o LLM e as instruções) e o **Azure AI Search** para a "memória" (os dados das transações). O teste final é realizado diretamente no painel de teste do Azure Foundry.

**O processo consiste em 4 passos de criação:** 

* Dados brutos via **script** no terminal
* **Azure Storage Account (Armazenamento):** Contém o `mock_transactions.csv` com os dados brutos.
* **Azure AI Search (Memória):** Um serviço que indexa o CSV para torná-lo pesquisável em alta velocidade.
* **Azure Foundry (Cérebro):** Onde o agente de IA (LLM + Instruções) é configurado para usar o AI Search como sua fonte de conhecimento ("Knowledge").

---

### 🚀 Fase 1: Criação dos Dados (CSV)

O primeiro passo é criar nossos dados fictícios.

1.  Salve o script `generate_data.py` no seu computador.

2.  Abra seu terminal e instale as dependências:

    ```bash
       pip install pandas faker
    ```

3.  Execute o script para gerar o seu arquivo de transações:

    ```bash
       python generate_data.py
    ```

4.  **Resultado:** Um novo arquivo, `mock_transactions.csv`, será criado. Este é o nosso "extrato bancário".

---

### ☁️ Fase 2: Configuração da Infraestrutura (Azure)

#### 1. Criar Resource Group (Grupo de Recursos)

1.  No Portal do Azure, navegue até **Resource Groups** > **+ Criar**.
    * [Ver Imagem: Pesquisar Resource Group](img/create-resource-group.png)
    * [Ver Imagem: Clicar em Criar Resource Group](img/click-criar-resource.png)
2.  Preencha os detalhes:
    * **Resource group name:** Escolha um nome da sua preferência (ex: `AgenteFinanceiro-`)
    * **Region:** Dê preferência à região **'Sweden Central'**.
3.  Clique em **Review + create** e depois em **Create**.
    * [Ver Imagem: Review e Create Resource Group](img/review-create-resource.png)
    * [Ver Imagem: Resource Group Criado](img/resource-created.png)

#### 2. Criar Storage Account (Conta de Armazenamento)

1.  No Portal do Azure, procure e selecione **Storage Accounts**.
    * [Ver Imagem: Procurar Storage Accounts](img/portal-search-storage-accounts.png)
2.  Clique em **+ Create**.
    * [Ver Imagem: Clicar em Criar Storage Account](img/create-storage-acct.png)
3.  Preencha os detalhes:
    * **Resource Group:** Selecione o grupo criado anteriormente (ex: `AgenteFinanceiro-`).
    * **Name:** Um nome único global (ex: `financeagentstorageacct`).
    * **Region:** Sweden Central
    * [Ver Imagem: Inserir informações do Storage Account](img/insert-info-storage-acct.png)
4.  Clique em **Review + create** e depois em **Create**.
    * [Ver Imagem: Deployment Storage Account](img/deployment-storage-acct1.png)

#### 3. Criar o Hub do AI Foundry

1.  No Portal do Azure, procure e selecione **AI Foundry**.
    * [Ver Imagem: Clicar em Azure AI Foundry](img/click-foundry.png)
2.  Clique em **+ Criar um recurso**.
    * [Ver Imagem: Clicar em Criar Recurso Foundry](img/click-create-resource-foundry.png)
3.  Preencha os detalhes:
    * **Resource Group:** Escolha o recurso criado anteriormente (`AgenteFinanceiro`).
    * **Name:** Escolha um nome (ex: `FrontierAgenteFinanceiro`)
    * **Region:** Sweden Central
    * [Ver Imagem: Informações para criar Foundry](img/info-create-foundry.png)
4.  Siga o assistente de criação clicando em "Avançar" (Next) até o fim e clique em "Criar" (Create).
    * [Ver Imagem: Foundry Deployment](img/create-foundry-deployment.png)

---

### ⬆️ Fase 3: Upload dos Dados (CSV para a Nuvem)

1.  No Portal do Azure, navegue até a sua **Storage Account** criada na Fase 2.
    * [Ver Imagem: Clicar em Storage Account](img/click-storage-acct.png)
2.  No menu à esquerda, em "Armazenamento de dados" (Data storage), clique em **"Contêineres" (Containers)**.
    * [Ver Imagem: Clicar em Containers](img/click-containers-storage-acct.png)
3.  Clique em **"+ Contêiner"** e crie um novo contêiner chamado `dados` (com acesso privado).
    * [Ver Imagem: Adicionar Container](img/add-container.png)
    * [Ver Imagem: Dar nome ao Container](img/give-name-container.png)
4.  Clique no contêiner `dados` para entrar nele.
    * [Ver Imagem: Clicar no container 'dados'](img/click-dados-container.png)
5.  Clique em **"Carregar" (Upload)** e selecione o seu arquivo `mock_transactions.csv`.
    * [Ver Imagem: Adicionar arquivo mock](img/add-mockfile-dados.png)
    * [Ver Imagem: Clicar em Upload](img/click-upload-file.png)
    * [Ver Imagem: Arquivo carregado](img/mockfile-upload-in-dados.png)

---

### 🧠 Fase 4: Criação da "Memória" (Azure AI Search)

Esta é uma fase crítica. Os assistentes do AI Foundry podem falhar com arquivos CSV. Precisamos construir o índice de busca manualmente usando o serviço de AI Search.

#### 4.1. Criar o Serviço de AI Search

1.  No Portal do Azure, dentro do seu Resource Group, clique em **"+ Criar" (+ Create)**.
    * [Ver Imagem: Clicar em Criar AI Search](img/click-create-AI-search.png)
2.  Procure por **"Azure AI Search"** e clique em "Create".
    * [Ver Imagem: Digitar Azure Search](img/type-azure-search.png)
    * [Ver Imagem: Clicar em Criar](img/clique-create.png)
3.  Preencha os detalhes:
    * **Resource Group:** Selecione seu grupo (ex: `AgenteFinanceiro`).
    * **Service Name:** Um nome único global (ex: `search-agente-financeiro`).
    * **Location:** Sweden Central
    * **Pricing tier:** Escolha **"Basic" (Básico)**.
        * *(Isto é crucial e tem custos associados. O plano "Free" não suporta as funcionalidades necessárias.)*
    * [Ver Imagem: Review e Create Search](img/review-create-search.png)
4.  Clique em **"Revisar + criar"** e depois em **"Criar"**.
   
5.  Após a conclusão, clique em **"Go to resource"**.
    * [Ver Imagem: AI Search Deployment](img/AI-search-deployment-made.png)
#### 4.2. Indexar o CSV 

1.  Na página do seu serviço de AI Search, clique no botão **"Import data"**.
    * [Ver Imagem: Importar arquivo](img/import-agente-financeiro.png)

#### A. Em "Connect to your data"

1.  **Data Source:** Selecione `Azure Blob Storage`.
    * [Ver Imagem: Azure Blob Storage Import](img/azure-blob-storage-import.png)
2.  **Data source name:** Dê um nome como ex: `fonte-dados-csv`
3.  **Parsing mode (Modo de Análise):** Mude de "Default" para **"Delimited text" (Texto delimitado)**.
    * [Ver Imagem: Delimited Text](img/delimited-text-import-data.png)
4.  **Header (Cabeçalho):** Marque a caixa **"First line contains header" (A primeira linha contém cabeçalho)**.
5.  **Connection (Conexão):** Clique em "Escolher uma conexão existente", selecione sua conta de armazenamento e o contêiner `dados`.
    * [Ver Imagem: Escolher conexão existente](img/clique-choose-existing-connection-import-data.png)
    * [Ver Imagem: Escolher container 'dados'](img/choose-container-dados.png)
6.  Clique em "Next" (Avançar).
    * [Ver Imagem: Clicar em Next](img/click-next-next.png)

#### B. Add skills (Adicionar Habilidades)

1.  Clique no botão **"Skip to: Customize target index"** (Pular para: Personalizar índice de destino).

#### C. Customize target index (Personalizar índice de destino)

1.  **Index name (Nome do Índice):** `azureblob-indexer`
2.  **Fields (Campos):** Configure as caixas de seleção:
    * `Date`: Marque **"Retrievable"** (Recuperável)
    * `Description`: Marque **"Retrievable"** E **"Searchable"**
    * `Category`: Marque **"Retrievable"** E **"Searchable"** 
    * `Amount`: Marque **"Retrievable"** E **"Searchable"** 
    * `Account`: Marque **"Retrievable"** E **"Searchable"**
    * [Ver Imagem: Configuração dos campos do índice](img/indexr-searchable-retrievable.png)
3.  Clique em "Avançar" (Next).

#### D. Create an Indexer (Criar um Indexador)

1.  **Name (Nome):** `azureblob-indexer`
2.  **Schedule (Agendamento):** Mude para **"Once" (Uma vez)**.
3.  Clique em **"Submit" (Enviar)**.
4.  Aguarde o indexador rodar. Na aba "Indexers", o status deve mudar para "Success" (Sucesso) e "Documentos Concluídos" deve mostrar 500.
    * [Ver Imagem: Sucesso do Indexador](img/success-indexer.png)

---

### 🤖 Fase 5: Criação do "Cérebro" (O Agente no AI Foundry)

#### 5.1. Iniciar o AI Foundry e Implementar o Modelo

1.  Volte ao Portal do Azure > seu Resource Group > seu recurso **AI Foundry**.
    * [Ver Imagem: Procurar AI Foundry](img/search-portal-AI-Foundry.png)
    * [Ver Imagem: Criar Recurso Foundry](img/create-resource-foundry.png)
2.  Clique em **"Launch Azure AI Foundry" (Iniciar o Azure AI Foundry)**.
    * [Ver Imagem: Ir para o portal Foundry](img/go-to-foundry-portal.png)
3.  No Azure Foundry, no menu à esquerda, vá para **"Agents" (Agentes)**.
    * [Ver Imagem: Clicar em Agents](img/click-agents-foundry.png)
4.  Clique em **"+ Create a new agent" (+ Criar um novo agente)**.
5.  O assistente pedirá para criar um modelo. Clique em **"+ Create new deployment"**.
6.  **Modelo:** Selecione `gpt-4o` (ou `gpt-4`).
    * [Ver Imagem: Escolher modelo](img/choose-model-create.png)
7.  Clique em **"Deploy"**.
    * [Ver Imagem: Deploy do modelo](img/deploy-model.png)

#### 5.2. Configurar o Agente

1.  Após o deployment, você será levado à tela "Create a new agent".
2.  **Agent name (Nome):** ``cerebro-gpt4o``
3.  **Agent instructions (Instruções):** Apague o texto padrão e cole seu prompt:

    > Você é um assistente financeiro pessoal, amigável e profissional. Seu nome é 'Assistente Financeiro'.
    >
    > Sua tarefa é APENAS responder perguntas sobre as transações financeiras do usuário. Todos os seus dados vêm de um arquivo de transações.
    >
    > SIGA ESTAS REGRAS ESTRITAMENTE:
    > 1.  SEMPRE responda em Português do Brasil.
    > 2.  SEMPRE use os dados do arquivo para responder. Na sua resposta, você deve citar as transações que usou para chegar ao número.
    > 3.  NUNCA invente informações. Se você não sabe a resposta ou ela não está nos dados, diga "Eu não tenho essa informação nos seus extratos."
    > 4.  NÃO RESPONDA a perguntas que não sejam sobre finanças (como "qual a previsão do tempo?"). Apenas diga: "Eu sou um assistente financeiro e só posso responder sobre suas transações."
    > 5.  Ao somar valores, seja preciso e mostre o total em Reais (R$).
4. **Agent Description:** Dê uma breve descrição do agente como ex: ``Assistente Pessoal Financeiro``
    * [Ver Imagem: Incluir instruções](img/include-instructions.png)

#### 5.3. Conectar a "Memória" ao "Cérebro"

1.  Na tela de "Setup" (Configuração) do seu `AssistenteFinanceiro`, encontre a seção **"Knowledge" (Conhecimento)** e clique em **"+ Add" (+ Adicionar)**.
    * [Ver Imagem: Clicar em Add Knowledge](img/click-add-knowledge.png)
2.  Selecione **"Azure AI Search"** como a fonte.
    * [Ver Imagem: Adicionar AI Search como Knowledge](img/add-search-knowledge.png)
3.  O assistente "Add knowledge" pode estar vazio. Se estiver:
    * Clique em **"Connect other Azure AI Search resource"**.
        * [Ver Imagem: Conectar outro recurso de Search](img/connect-search.png)
    * Clique em **"Add Connection"** > **"Connect"**.
        * [Ver Imagem: Adicionar Conexão](img/add-connection.png)
    * Preencha o **"Azure AI Search Index"** com seu índice criado (`searchagentefinanceiro`).
    * Dê um nome para o **"Display name"** (ex: `fonte-transacoes`).
    * **Search type:** `Simple`
    * Clique em **"Connect"** para adicionar a conexão ao seu serviço `search-agente-financeiro`.
    * [Ver Imagem: Conectar Azure AI Search](img/connect-Azure-AI-Search.png)

---

### ✅ Fase 6: Teste seu Agente

O seu back-end está 100% completo.

1.  Clique em **"Try in playground"**.
    * [Ver Imagem: Try in playground](img/try-playground.png)

2.  **Teste de Dados (Sucesso):**
    * `Quanto gastei no Amazon mês passado?`
        * [Ver Imagem: Teste Amazon](img/teste-Amazon.png)
    * `Quanto gastei em iFood?.`
        * [Ver Imagem: Teste iFood](img/teste-iFood.png)
    * *O agente deve responder corretamente e citar as fontes do seu CSV.* 🎉

3.  **Teste de Segurança (Falha Esperada):**
    * `Qual a temperatura esperada para hoje?`
    * *O agente deve se recusar a responder, conforme a Regra #4.*
        * [Ver Imagem: Teste de pergunta não respondida](img/falhar-teste.png)

#### 🎉 PARABÉNS, seu agente foi criado com sucesso!!

---

### 🛠️ Solução de Problemas Comuns (Troubleshooting)

#### Problema: Erro de "Quota Insuficiente" (Quota insufficient)

* **Sintoma:** Ao tentar implantar um modelo (Fase 5.1), você recebe um erro de "Quota".
* **Causa:** Sua conta do Azure não tem permissão para usar modelos de IA na região selecionada (provavelmente East US).
* **Solução:** Exclua o Grupo de Recursos. Recomece o projeto (Fase 2) e crie todos os novos recursos em uma região menos congestionada, como **Sweden Central (Suécia Central)**.

#### Problema: Agente Falha em Encontrar Informações (Índice com "0 Documentos")

* **Sintoma:** O agente sempre responde "Eu não tenho essa informação...", e seu Indexador no AI Search mostra "0 documentos concluídos".
* **Causa:** O assistente "Importar dados" (Fase 4.2) não foi configurado para ler CSV (padrão é .txt ou .pdf).
* **Solução:** Na Fase 4.2, Passo A ("Conectar aos seus dados"):
    1.  Mude **"Modo de Análise" (Parsing mode)** de "Default" para **"Texto delimitado" (Delimited text)**.
    2.  MARQUE a caixa **"A primeira linha contém cabeçalho" (First line contains header)**.
    3.  Exclua o índice/indexador antigo e execute novamente.

#### Problema: Agente Encontra o Documento, mas Não a Resposta (Campos Não-Pesquisáveis)

* **Sintoma:** O agente não encontra respostas, mas o índice tem 500 documentos.
* **Causa:** Na Fase 4.2, Passo C, as colunas (`Description`, `Category`) não foram marcadas como **"Searchable" (Pesquisável)**.
* **Solução:** Ao configurar o "Personalizar índice de destino", marque **"Searchable" (Pesquisável)** para os campos de texto que o agente precisará pesquisar. Outros campos (como `Amount`, `Date`) só precisam ser **"Retrievable" (Recuperável)**.

#### Problema: O AI Foundry não encontra seu Índice de Busca (Dropdown Vazio)

* **Sintoma:** Na Fase 5.3, ao adicionar "Knowledge" > "Azure AI Search", a lista de índices está vazia.
* **Causa:** A página do AI Foundry está desatualizada ou o "Projeto" do AI Foundry não tem uma "Conexão" formal com o serviço de AI Search.
* **Solução (Passo 1):** Dê um "Refresh" (F5) na página do AI Foundry e tente conectar novamente.
* **Solução (Passo 2):** Crie a conexão manualmente:
    1.  No AI Foundry, vá para o "Management center" (ícone ⚙️).
    2.  Vá para **Project (...)** > **"Connected resources" (Recursos conectados)**.
    3.  Clique em **"+ Create"** e selecione **"Azure AI Search"**.
    4.  Siga o assistente para adicionar uma conexão ao seu serviço de search (usando a Chave de API).
    5.  Volte para o seu Agente, atualize a página, e a conexão/índice agora aparecerá.

---

### ⚠️ AVISO DE CUSTO IMPORTANTE!

> Este projeto **NÃO É GRATUITO**.
>
> O serviço de **Azure AI Search** no plano **"Basic" (Básico)** gera custos por hora (aprox. R$ 20-30/dia) 24/7, mesmo que você não o esteja usando.
>
> **Quando terminar de testar:**
>
> 1.  Vá para o Portal do Azure.
> 2.  Encontre o seu **Grupo de Recursos** (ex: `AgenteFinanceiro-`).
> 3.  Clique em **"Excluir grupo de recursos" (Delete resource group)**.
> 4.  Confirme o nome e clique em "Excluir".
>
> Isto irá **PARAR TODAS AS COBRANÇAS**.

### 📚 Referências e Documentação Oficial

Abaixo estão os links para a documentação oficial das ferramentas utilizadas na construção do back-end e da inteligência do agente:

* **Azure AI Foundry (O Cérebro):**
    * [Documentação do Azure AI Foundry](https://learn.microsoft.com/pt-br/azure/ai-studio/)
    * [Como criar e implantar Agentes de IA](https://learn.microsoft.com/pt-br/azure/ai-studio/how-to/develop/assistants?tabs=python)
    * [Adicionando dados (Knowledge) aos Agentes](https://learn.microsoft.com/pt-br/azure/ai-studio/how-to/develop/assistants?tabs=python#add-knowledge-to-the-assistant)

* **Azure AI Search (A Memória):**
    * [O que é o Azure AI Search?](https://learn.microsoft.com/pt-br/azure/search/search-what-is-azure-search)
    * [Importando dados de CSV e Blob Storage](https://learn.microsoft.com/pt-br/azure/search/search-howto-indexing-azure-blob-storage)
    * [Entendendo Indexadores (Indexers)](https://learn.microsoft.com/pt-br/azure/search/search-indexer-overview)

* **Geração de Dados (Python):**
    * [Documentação do Pandas](https://pandas.pydata.org/docs/) (Usado para manipular o CSV).
    * [Documentação do Faker](https://faker.readthedocs.io/en/master/) (Usado para criar nomes e dados fictícios).

* **Azure Storage:**
    * [Criar uma conta de armazenamento](https://learn.microsoft.com/pt-br/azure/storage/common/storage-account-create)
    * [Upload de blobs/arquivos pelo Portal](https://learn.microsoft.com/pt-br/azure/storage/blobs/storage-quickstart-blobs-portal)
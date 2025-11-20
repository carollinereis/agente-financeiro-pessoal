# 🚀 Guia Completo: Seu Chatbot de Finanças com IA no Azure

Este guia documenta a criação de uma interface front-end segura e escalável para consumir um Agente de IA.

### 🎯 Objetivo do Projeto

O objetivo deste projeto é criar uma interface **front-end** interativa utilizando serviços do **Microsoft Azure** para conectar-se ao agente **back-end** ("Cérebro") desenvolvido no **Azure AI Foundry.**

**Serviços e Tecnologias Utilizados:**

* **Azure App Service (Web Apps):** Hospedagem da aplicação web em ambiente Linux.

* **Streamlit (Python):** Framework utilizado para criar a interface de chat.

* **Azure AI Foundry:** Plataforma onde o Agente e a inteligência residem.

* **Managed Identity (Identidade Gerenciada):** Para autenticação segura entre o Site e a IA, eliminando o uso de senhas ou chaves fixas no código (DefaultAzureCredential).

--- 

###  🛠️ Parte 1: Configuração e Desenvolvimento Local

#### 1. Preparar o Ambiente
* Instale o Python e o Visual Studio Code.
* Abra o terminal e instale as bibliotecas necessárias:

````bash
    pip install streamlit azure-ai-projects azure-identity
````
* Faça login no Azure pelo terminal:

````bash
    az login
````

#### 2. Criar o Código (`app.py`)

* Certifique-se de que seu código utiliza `DefaultAzureCredential()` para autenticação.

* Defina o `project_endpoint` e `agent_id` do seu agente criado no Foundry.

**3. Testar Localmente**

* No terminal, execute:

````bash
    streamlit run app.py
````

* O navegador abrirá. Teste o chat (Ex: "Quanto eu gastei no iFood?").

    [Veja imagem: LocalHost teste](img/local-host-teste.png)

* Funcionou? Ótimo. Pode fechar o teste local! (`Ctrl + C` no terminal).
---

### Parte 2: Preparação para a Nuvem

#### 1. Criar o arquivo de dependências

* Na mesma pasta do `app.py`, crie um arquivo chamado `requirements.txt.`com o seguinte conteúdo:

````plaintext
    streamlit
    azure-ai-projects
    azure-identity
````
#### 2. Registrar o Provedor de Web

* Execute este comando para garantir que sua assinatura do Azure aceita a criação de sites Linux:

````bash
    az provider register --namespace Microsoft.Web
````
*(Aguarde terminar antes de prosseguir).*

--- 

### ☁️ Parte 3: Publicação no Azure (Deploy)

Vamos subir o site para a nuvem.

#### 1. Comando de Criação e Upload** Substitua o `--name AgenteFinanceiroR-Frontend` se desejar mudar:

````bash
    az webapp up --name AgenteFinanceiroR-Frontend --resource-group [INSIRA SEU RESOURCE GROUP AQUI] --location swedencentral --sku B1 --os-type Linux --runtime "PYTHON:3.11"
````

*(Aguarde o JSON de sucesso aparecer no terminal).*

--- 

### ⚙️ Parte 4: Configurações do Servidor

O **Streamlit** precisa de configurações específicas que não vêm ativadas por padrão.

#### 1. Configurar Inicialização e WebSockets

````bash
    az webapp config set --name AgenteFinanceiroR-Frontend --resource-group AgenteFinanceiroR --startup-file "python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0" --web-sockets-enabled true
````

#### 2. Criar a Identidade. Gera um "crachá" para o site não precisar de senha.

````bash
    az webapp identity assign --name AgenteFinanceiroR-Frontend --resource-group [SEU RESOURCE GROUP AQUI]
````
***⚠️ Importante:** Copie o código `principalId` que aparecerá na saída deste comando.

[Veja imagem: Exemplo principalId](img/principalId.png)

### 🔐 Parte 5: Permissões de Acesso (IAM)

Agora autorizamos o site a falar com o cérebro de IA.

#### Opção Via Terminal (Recomendado): Substitua `COLE_SEU_PRINCIPAL_ID_AQUI` pelo ID copiado no passo anterior.

````
Bash
    az role assignment create --assignee "COLE_SEU_PRINCIPAL_ID_AQUI" --role "Azure AI Developer" --resource-group "SEU RESOURCE GROUP"
````
*(Alternativa Visual: No Portal Azure > Grupo de Recursos > IAM > Adicionar atribuição de função > Selecionar "Azure AI Developer" > Membros: Identidade Gerenciada > App Service > Seu App).*

[Veja imagem: Azure AI Developer](img/azure-dev.png)

[Veja imagem: App Service](img/controle-acesso-final.png)

---

### 🚀 Parte 6: Reiniciar e Acessar

A permissão de segurança pode levar até 5 minutos para propagar.

#### 1. Aguarde uns minutos.

#### 2. Reinicie o App:**

Substitua `AgenteFinanceiroR-Frontend`pelo nome do seu website e `AgenteFinanceiroR`por seu resource name.

````bash
    az webapp restart --name AgenteFinanceiroR-Frontend --resource-group AgenteFinanceiroR
````

#### 3. Acesse o link final:
https://agentefinanceiror-frontend.azurewebsites.net

[Veja imagem: Site no ar](img/site-rodando.png)

#### 🔍 Como recuperar o link do site?

Caso você tenha fechado o terminal e perdido o endereço, existem três formas de encontrá-lo:

#### 1. Padrão de URL 

O link sempre segue o formato do nome que você escolheu na criação:
`https://<NOME_DO_SEU_APP>.azurewebsites.net`

*(Exemplo: https://agentefinanceiror-frontend.azurewebsites.net)*

#### 2. Pelo Portal do Azure (Visual)
1. Acesse o [Portal do Azure](https://portal.azure.com).
2. Na barra de busca, digite o nome do seu app (ex: `AgenteFinanceiroR-Frontend`).
3. Clique no recurso do tipo **Serviço de Aplicativo** (ícone de globo azul).
4. Na tela de **Visão Geral (Overview)**, copie o link que aparece no campo **Domínio Padrão** (Default domain).

[Veja imagem: Domain Link](img/find-link.png)

#### 3. Pelo Terminal (Comando)**
Se estiver com o terminal aberto, rode este comando para o Azure te mostrar o link:

```bash
az webapp show --name AgenteFinanceiroR-Frontend --resource-group AgenteFinanceiroR --query defaultHostName --output tsv
```

### ❌ Solução de Problemas Comuns

| Erro | Causa Provável | Solução |
| :--- | :--- | :--- |
| **PermissionDenied / Lacks action** | O site não tem permissão no AI Foundry. | Refaça a **Parte 5** e reinicie o site. |
| **Application Error / Tela Cinza** | Streamlit não iniciou corretamente. | Verifique o comando na **Parte 4 (Passo 1)** e se WebSockets estão `true`. |
| **Lentidão na resposta** | Site e Agente em continentes diferentes. | Apague o Web App e recrie usando `--location swedencentral` (ou a mesma região do seu Agente). |

### 📚 Referências e Documentação Oficial

Abaixo estão os links da documentação da Microsoft utilizados para construir esta solução:

* **Azure CLI (Comandos de Linha de Comando):**
    * [Documentação Geral do Azure CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)
    * [Comando az webapp up](https://learn.microsoft.com/en-us/cli/azure/webapp?view=azure-cli-latest#az-webapp-up)

* **Azure App Service (Hospedagem):**
    * [Configurar aplicativos Python no App Service Linux](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python) (Essencial para entender o comando de inicialização).
    * [Visão geral do App Service no Linux](https://learn.microsoft.com/en-us/azure/app-service/overview)

* **Segurança e Identidade:**
    * [O que são Identidades Gerenciadas (Managed Identity)?](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)
    * [Biblioteca Azure Identity para Python (DefaultAzureCredential)](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python)

* **Azure AI Foundry (Inteligência):**
    * [Construindo apps de chat com o SDK do Azure AI](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/sdk-overview)
    * [Controle de Acesso (RBAC) no Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/rbac-ai-studio) (Explica as permissões como "Azure AI Developer").
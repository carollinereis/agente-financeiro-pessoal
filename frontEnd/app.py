import streamlit as st
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

# --- 1. Configuração do "Cérebro" (Agente do AI Foundry) ---
try:
    credential = DefaultAzureCredential()
    project_endpoint = "INSIRA SEU ENDPOINT AQUI" # exemplo: https://frontieragentefinanceiro.services.ai.azure.com/api/projects/proj-default
    agent_id = "INSIRA SEU agent_id" # exemplo: asst_6dfZ4ipfkWlQ7D9nRMk1xkvy
    
    project = AIProjectClient(
        credential=credential,
        endpoint=project_endpoint
    )
    agent = project.agents.get_agent(agent_id)

except Exception as e:
    st.error(f"Erro ao conectar com o Azure. Você executou 'az login'? Erro: {e}")
    st.stop()

# --- 2. Configuração da Página de Chat ---
st.title("Meu Assistente Financeiro 💸") # Dê o título conforme desejado
st.caption("Powered by Azure AI") # Modifique a frase se necessário

# --- NOVO: BARRA LATERAL COM BOTÃO DE RESET ---
with st.sidebar:
    st.write("### Opções de Conversa")
    if st.button("Iniciar Nova Conversa"):
        # Limpa o histórico da sessão e o ID da thread
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.rerun() # Força o recarregamento da página

# --- 3. Gerenciamento da Memória do Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# --- 4. Exibir Mensagens Antigas ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "citation" in message and message["citation"]:
            with st.expander("Ver fonte da resposta"):
                st.code(message["citation"])

# --- 5. Caixa de Pergunta (Onde o usuário digita) ---
if prompt := st.chat_input("Faça sua pergunta financeira..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 6. Lógica do Agente (A Mágica) ---
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Se for a primeira mensagem (thread_id está Nulo), crie um "thread"
                if st.session_state.thread_id is None:
                    thread = project.agents.threads.create()
                    st.session_state.thread_id = thread.id
                    
                    # Mensagem de "aquecimento" para o agente
                    project.agents.messages.create(
                        thread_id=st.session_state.thread_id,
                        role="user",
                        content="Olá Assistente Financeiro"
                    )

                # 1. Adiciona a pergunta do usuário ao thread
                project.agents.messages.create(
                    thread_id=st.session_state.thread_id,
                    role="user",
                    content=prompt
                )

                # 2. Manda o "Cérebro" (Agente) processar a conversa
                run = project.agents.runs.create_and_process(
                    thread_id=st.session_state.thread_id,
                    agent_id=agent.id
                )

                # 3. Verifica se o Agente teve sucesso
                if run.status == "failed":
                    st.error(f"O agente falhou: {run.last_error}")
                else:
                    # 4. Pega a lista de mensagens atualizada
                    messages_iterator = project.agents.messages.list(
                        thread_id=st.session_state.thread_id,
                        order=ListSortOrder.ASCENDING 
                    )
                    messages = list(messages_iterator)

                    # 5. Processa a resposta
                    if messages and messages[-1].role == "assistant" and messages[-1].text_messages:
                        
                        full_response = messages[-1].text_messages[-1].text.value
                        main_answer = full_response
                        citation = "" 

                        if "【" in full_response:
                            parts = full_response.split("【")
                            main_answer = parts[0].strip()
                            citation = "【" + "【".join(parts[1:])
                        
                        # 6. Mostra a resposta na tela
                        st.markdown(main_answer)
                        if citation:
                            with st.expander("Ver fonte da resposta"):
                                st.code(citation)
                        
                        # 7. Salva no histórico
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": main_answer,
                            "citation": citation
                        })
                        
                    else:
                        st.error("O agente processou, mas não recebi uma resposta final.")

            except Exception as e:
                st.error(f"Ocorreu um erro ao processar sua solicitação: {e}")
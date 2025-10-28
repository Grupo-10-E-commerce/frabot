import streamlit as st
import time
from rag import rag

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title="Chatbot | Frabot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS - TEMA DARK
st.markdown("""
<style>
    /* Configuração global dark mode */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Main */
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #0d1117;
    }
    
    /* Estilizando titulo */
    .custom-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4a90e2 0%, #7b68ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Subtitulo */
    .subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* Container da conversa */
    .chat-container {
        max-width: 900px;
        margin: 0 auto 3rem auto;
        padding: 1rem 2rem 2rem 2rem;
        background-color: #0d1117;
    }
    
    /* Container para mensagens - permite alinhamento */
    .message-container {
        display: flex;
        width: 100%;
        margin: 1rem 0;
    }
    
    .message-container.user {
        justify-content: flex-end;
    }
    
    .message-container.assistant {
        justify-content: flex-start;
    }
    
    /* Mensagem do usuário - DIREITA */
    .user-message {
        background: linear-gradient(135deg, #1e5a2e 0%, #2d7a39 100%);
        color: #e6f3e8;
        max-width: 70%;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        box-shadow: 0 4px 15px rgba(30, 90, 46, 0.3);
        animation: slideInRight 0.3s ease-out;
        word-wrap: break-word;
        border: 1px solid #30363d;
    }
    
    /* Mensagem do assistant - ESQUERDA */
    .assistant-message {
        background: linear-gradient(135deg, #1a4d8a 0%, #2563eb 100%);
        color: #e1f0ff;
        max-width: 70%;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        box-shadow: 0 4px 15px rgba(26, 77, 138, 0.3);
        animation: slideInLeft 0.3s ease-out;
        word-wrap: break-word;
        border: 1px solid #30363d;
    }
    
    /* Animação pensando - tema dark */
    .thinking {
        background: linear-gradient(135deg, #21262d 0%, #30363d 100%);
        color: #f0f6fc;
        max-width: 70%;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        box-shadow: 0 4px 15px rgba(33, 38, 45, 0.6);
        animation: pulse 1.5s ease-in-out infinite;
        border: 1px solid #30363d;
    }
    
    /* Animação de carregamento - cores dark */
    .loading-dots {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 20px;
    }
    
    .loading-dots div {
        position: absolute;
        top: 8px;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4a90e2;
        animation-timing-function: cubic-bezier(0, 1, 1, 0);
    }
    
    .loading-dots div:nth-child(1) {
        left: 8px;
        animation: lds-ellipsis1 0.6s infinite;
    }
    
    .loading-dots div:nth-child(2) {
        left: 8px;
        animation: lds-ellipsis2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(3) {
        left: 32px;
        animation: lds-ellipsis2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(4) {
        left: 56px;
        animation: lds-ellipsis3 0.6s infinite;
    }
    
    /* Animações */
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
    }
    
    @keyframes lds-ellipsis1 {
        0% {
            transform: scale(0);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes lds-ellipsis3 {
        0% {
            transform: scale(1);
        }
        100% {
            transform: scale(0);
        }
    }
    
    @keyframes lds-ellipsis2 {
        0% {
            transform: translate(0, 0);
        }
        100% {
            transform: translate(24px, 0);
        }
    }
    
    /* Estilização do input - tema dark - VERSÃO MAIS AGRESSIVA */
    .stChatInputContainer,
    .stChatInputContainer > div,
    .stChatInputContainer [data-testid="stChatInput"],
    .stChatInputContainer [data-testid="textInput"] {
        background: linear-gradient(135deg, #21262d 0%, #30363d 100%) !important;
        backdrop-filter: blur(10px);
        border-radius: 25px;
        border: 2px solid #30363d !important;
        background-clip: padding-box;
        transition: all 0.3s ease;
    }
    
    .stChatInputContainer:focus-within,
    .stChatInputContainer > div:focus-within {
        border: 2px solid #4a90e2 !important;
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.2);
    }
    
    /* OVERRIDE TOTAL - todos os elementos de input possíveis */
    .stChatInputContainer input,
    .stChatInputContainer textarea,
    .stChatInputContainer div[data-testid="stChatInput"] input,
    .stChatInputContainer div[data-testid="stChatInput"] textarea,
    .stChatInputContainer div[data-testid="textInput"] input,
    .stChatInputContainer div[data-testid="textInput"] textarea,
    .stChatInputContainer [data-baseweb="textarea"] textarea,
    .stChatInputContainer [data-baseweb="input"] input,
    .st-emotion-cache-1y4p8pa textarea,
    .st-emotion-cache-1y4p8pa input,
    div[data-testid="stChatInput"] input,
    div[data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] [data-baseweb="textarea"] textarea {
        color: #f0f6fc !important;
        background: #21262d !important;
        background-color: #21262d !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* PLACEHOLDER - todos os seletores possíveis */
    .stChatInputContainer input::placeholder,
    .stChatInputContainer textarea::placeholder,
    .stChatInputContainer div[data-testid="stChatInput"] input::placeholder,
    .stChatInputContainer div[data-testid="stChatInput"] textarea::placeholder,
    .stChatInputContainer div[data-testid="textInput"] input::placeholder,
    .stChatInputContainer div[data-testid="textInput"] textarea::placeholder,
    .stChatInputContainer [data-baseweb="textarea"] textarea::placeholder,
    .stChatInputContainer [data-baseweb="input"] input::placeholder,
    div[data-testid="stChatInput"] input::placeholder,
    div[data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] [data-baseweb="textarea"] textarea::placeholder {
        color: #c9d1d9 !important;
        opacity: 0.7 !important;
    }
    
    /* OVERRIDE UNIVERSAL - aplica em TUDO dentro do container */
    .stChatInputContainer *,
    div[data-testid="stChatInput"] * {
        background-color: transparent !important;
        color: #f0f6fc !important;
    }
    
    /* OVERRIDE para input específico baseado na imagem */
    .stChatInputContainer [data-baseweb="textarea"],
    .stChatInputContainer [data-baseweb="input"],
    div[data-testid="stChatInput"] [data-baseweb="textarea"],
    div[data-testid="stChatInput"] [data-baseweb="input"] {
        background-color: #21262d !important;
        background: #21262d !important;
        color: #f0f6fc !important;
        border: none !important;
    }
    
    /* Send button styling */
    .stChatInputContainer button {
        background: #1e5a2e !important;
        border: none !important;
        color: white !important;
    }
    
    .stChatInputContainer button:hover {
        background: #2d7a39 !important;
        transform: scale(1.05);
    }
    
    /* Sidebar dark mode */
    .css-1d391kg {
        background-color: #161b22;
    }
    
    /* Chat messages styling override */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar dark mode */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #484f58;
    }
            
    .st-emotion-cache-128upt6 {
        background-color: #0d1117;
        color: white;
    }
            
    /* Fundo da caixa de input e texto do usuário */
        div.st-emotion-cache-1c19b35.e1f1d6gn2 { /* Seletor para o background da caixa de texto */
        background-color: #21262d; /* Cor da caixa de input */
    }

    div.st-emotion-cache-1c19b35.e1f1d6gn2 textarea { /* Seletor para o texto digitado */
        color: #f0f6fc; /* Cor do texto digitado */
    }
            
    /* Garante que o fundo do ícone e da área arredondada seja escuro */
    div[data-testid="stChatInput"] > div:first-child {
        background-color: #21262d !important;
        border-radius: 25px; /* Mantém o arredondamento */
    }
</style>
""", unsafe_allow_html=True)

# Titulo customizado com cores gradientes dark
st.markdown('<h1 class="custom-title">Chatbot | Frabot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🤖 Seu assistente inteligente para respostas rápidas e precisas</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializar estados da sessão
if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "current_answer" not in st.session_state:
    st.session_state.current_answer = ""

# Container da conversa
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Mostrar histórico da conversa com novo layout
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'''
        <div class="message-container user">
            <div class="user-message">👤 {msg["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'''
        <div class="message-container assistant">
            <div class="assistant-message">🤖 {msg["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Mensagem inicial do assistente
if (len(st.session_state.messages) == 0):
    firstMessage = "Olá, sou o Frabot, um assistente digital, e estou aqui para tirar quaisquer dúvidas relacionadas á Fraux para você!<br>Como posso te ajudar?"
    st.markdown(f'''
    <div class="chat-container">
        <div class="message-container assistant">
            <div class="assistant-message">🤖 {firstMessage}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": firstMessage})

# Chat input
if prompt := st.chat_input("💭 Digite sua pergunta aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostrar mensagem do usuário na direita
    st.markdown(f'''
    <div class="message-container user">
        <div class="user-message">👤 {prompt}</div>
    </div>
    ''', unsafe_allow_html=True)

    # Mostrar indicador de pensamento na esquerda
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown('''
    <div class="message-container assistant">
        <div class="thinking">
            🤔 Analisando sua pergunta
            <div class="loading-dots">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Simula o tempo pensando
    time.sleep(2)
    
    try:
        response = rag(prompt, st.session_state.messages)
    except Exception as e:
        response = "Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente em alguns instantes."
    
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Limpar o indicador de pensamento
    thinking_placeholder.empty()
    
    # Mostrar resposta do assistente na esquerda
    st.markdown(f'''
    <div class="message-container assistant">
        <div class="assistant-message">🤖 {response}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Rerun para atualizar o estado
    st.rerun()
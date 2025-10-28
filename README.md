# Frabot - Chatbot da Fraux | 🤖

Este Chatbot tem como finalidade fornecer suporte e tirar dúvidas sobre o Projeto para os clientes, usuários finais do sistema,
utilizando da técnica de 
RAG em conjunto 
com o banco de dados 
vetorial ChromaDB, que 
utilizou como base de 
conhecimentos alguns 
documentos referentes ao Projeto.

Para desenvolvimento deste RAG foi utilizado a API da Gemini e HuggingFace para conseguir as **keys** necessárias para a utilização de modelos de LLMs e embeddings.


---
# Iniciando a aplicação | 💻

1. Verifique se possui o Python instalado em sua máquina,
utilizando em seu terminal o comando:
    ```bash
    python --version 
    # Versão do Python utilizada no Projeto: 3.13.5
    ```
2. Crie o ambiente virtual Python (Abre o terminal na pasta do Projeto):

    ```bash
    python -m venv .env
    ```
3. Ative o ambiente virtual:

    ```bash
    source .env/bin/activate   # Sistemas Linux/Mac
    # ou
    .env\Scripts\activate      # Sistemas Windows
    ```
4. Instale as dependências do projeto:

    ```bash
    pip install -r requirements.txt
    ```
5. Execute o aplicativo Streamlit:

    ```bash
    streamlit run main.py
    ```

---

# Configuração de Variáveis Ambiente | 🔑

Crie um arquivo .env no Projeto, nele você irá colocar as 
credenciais necessárias para o funcionamento do Projeto e setará em variáveis de ambiente para 
armazená-las de forma segura.

Segue o modelo abaixo:
```bash 
MODEL_NAME="NOME-DO-MODELO" 
API_KEY="CHAVE-DA-API"
EMBEDDING_MODEL="MODELO-DO-EMBEDDING"
DOCUMENTOS_ENTRADA="PASTA-DOS-DOCUMENTOS"
```

---

import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings


# CARREGA AS VARIAVEIS AMBIENTES DO .ENV

load_dotenv()


# PEGANDO AS VARIAVEIS AMBIENTE SETADAS NO .ENV PARA UTILIZA-LAS

MODEL = os.getenv('MODEL_NAME')
API_KEY = os.getenv('API_KEY')
PASTA = os.getenv('DOCUMENTOS_ENTRADA') 

os.environ["GOOGLE_API_KEY"] = API_KEY

# CRIANDO A VÁRIAVEL PARA GERAÇÃO DOS EMBEDDINGS E VÁRIAVEL PARA CHAMAR O MODELO PARA LLM

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

llm = ChatGoogleGenerativeAI(
    model=MODEL,   
    temperature=0.2
)


# CRIANDO O BANCO DE DADOS VETORIAL - CHROMADB

vector_store = Chroma (
    collection_name='chroma-database-01',
    embedding_function=embeddings,
    persist_directory='./CHROMA-DB'
)


# LINKS DOS DOCUMENTOS

pdf_links = {
    "Documentacao_fraudes_e-comerce.pdf": "https://bandteccom-my.sharepoint.com/shared?listurl=https%3A%2F%2Fbandteccom%2Esharepoint%2Ecom%2Fsites%2FGrupo10Semestre2%2FShared%20Documents&viewid=15bf6ac3%2Da460%2D4812%2Dad24%2D5be7fc887d23&login_hint=gabriel%2Epietro%40sptech%2Eschool&source=waffle&id=%2Fsites%2FGrupo10Semestre2%2FShared%20Documents%2FDocumenta%C3%A7%C3%A3o%2FDocumentacao%5Ffraudes%5Fe%2Dcomerce%2Epdf&parent=%2Fsites%2FGrupo10Semestre2%2FShared%20Documents%2FDocumenta%C3%A7%C3%A3o"
}


docs = [os.path.join(PASTA, arquivo) for arquivo in os.listdir(PASTA) if arquivo.endswith('.pdf')]

documents = []

for doc in docs:
    loader = PyPDFLoader(doc)
    loaded_docs = loader.load()

    # Nome do arquivo sem caminho
    filename = os.path.basename(doc)

    # Substitui o metadado "source" pelo link correspondente
    for d in loaded_docs:
        if filename in pdf_links:
            d.metadata["source"] = pdf_links[filename]

    documents.extend(loaded_docs)




# SPLITANDO/SEPARANDO OS DOCUMENTOS EM CHUNKS PARA MANDAR ESTES CHUNKS PARA O CHROMADB

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 500,
    add_start_index = True
)
all_splits = text_splitter.split_documents(documents)

documents_ids = vector_store.add_documents(documents = all_splits)


# INSTRUÇÃO PARA A LLM, TEMPLATE DE PROMPT PARA ELA SEGUIR, DE COMO ELA IRÁ RESPONDER A PERGUNTA DO USUÁRIO

template = PromptTemplate.from_template(
"""
Você é o Frabot 🤖, assistente da empresa Fraux.
Responda à pergunta do usuário com base no contexto abaixo.
Se não souber, diga: "Essa resposta foge da minha base de conhecimentos atuais!"

Contexto:
{contexto}

Pergunta:
{pergunta}
"""
)




# FUNÇÃO DO RAG, RESPONSÁVEL POR REALIZAR A CONSULTA NO CHROMA DB E CONSTRUIR A RESPOSTA, TENDO COMO PARÂMETROS A PERGUNTA DO USUÁRIO 
# E O HISTÓRICO DE CONVERSA DO CHATBOT (DO USUÁRIO COM ELE), ONDE ESSA RESPOSTA É CONSTRUIDA COM BASE EM UMA BUSCA FILTRADA 
# POR RELEVANCE SCORE, ONDE ELE TEM QUE SER MAIOR OU IGUAL A 0.7 (LEMBRANDO QUE QUANTO MAIS PRÓXIMO DE 1, MAIS PRÓXIMA DA PERGUNTA A RESPOSTA FICA)

def rag(user_query: str, chat_history: list[dict]) -> str:
    history_text = ""

    for m in chat_history:
        role = "Usuário" if m["role"] == "user" else "Frabot"
        history_text += f"{role}: {m['content']}\n"

    context = vector_store.similarity_search_with_relevance_scores(user_query)
    context = list(filter(lambda x: x[1] >= 0.1, context))

    context_text = ""

    if not context:
        docs = vector_store.similarity_search(user_query, k=3)
        for d in docs:
            context_text += f"{d.page_content}\nFonte: {d.metadata.get('source','')}\n\n"

    for doc, score in context:
        context_text += f"{doc.page_content}\nFonte: {doc.metadata.get('source','')}\n\n"

    # Criação do prompt manualmente
    prompt_text = template.format(
        contexto=context_text,
        pergunta=user_query,
        hist_conversa=history_text
    )

    # Envio ao modelo Gemini
    response = llm.invoke(prompt_text)
    result_text = response.content

    return result_text

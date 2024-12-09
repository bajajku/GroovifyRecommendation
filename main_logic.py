# main_logic.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import os
from dotenv import load_dotenv


def setup_chain():

    # load_dotenv()
    # HF_API_KEY = os.getenv("HF_API_KEY")
    # REPO_ID = os.getenv("REPO_ID")
    # DATA_FILE = os.getenv("DATA_FILE")
    # MODEL_NAME = os.getenv("MODEL_NAME")

    HF_API_KEY = os.environ.get("HF_API_KEY")
    REPO_ID = os.environ.get("REPO_ID")
    DATA_FILE = os.environ.get("DATA_FILE")
    MODEL_NAME = os.environ.get("MODEL_NAME")
    
    # 1. Set up the Hugging Face API
    llm = HuggingFaceEndpoint(
        repo_id=REPO_ID,
        max_length=50,
        temperature=0.1,
        huggingfacehub_api_token=HF_API_KEY
    )

    # 2. Load and process documents
    loader = TextLoader(DATA_FILE)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # 3. Create embeddings and a vector store
    embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore = FAISS.from_documents(texts, embedding_model)

    # 4. Set up the retriever
    retriever = vectorstore.as_retriever()

    # 5. Create the RAG chain
    template = '''
    <s>[INST] 
    Use the context {context} and recommend only 3 genres to the user based on the user's mood input. Do not provide anything else. 
    Make sure these genres are present in the context. 
    User Input: {input} 

    Your output MUST only provide genres and nothing else. 
    Output should follow this format:
    Genre: [put genres here]
    [/INST]
    '''

    prompt = PromptTemplate(template=template)

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    return chain
# # Not using this file for now, just for testing purposes

# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEndpoint
# from langchain.prompts import PromptTemplate
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.document_loaders import TextLoader
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# # from langchain_core.prompts import ChatPromptTemplate
# from langchain.vectorstores import FAISS # Vector Database store data in form of vectors


# llm = HuggingFaceEndpoint(
#     repo_id=repo_id,
#     max_length=50,
#     temperature=0.1,
#     huggingfacehub_api_token=hf_api_key
# )

# # 2. Load and process documents
# loader = TextLoader("sample.txt")  # Replace with your data file
# documents = loader.load()

# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
# texts = text_splitter.split_documents(documents)

# # 3. Create embeddings and a vector store
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# vectorstore = FAISS.from_documents(texts, embedding_model)

# # 4. Set up the retriever
# retriever = vectorstore.as_retriever()

# # # 5. Create the RAG chain
# template = '''
#     <s>[INST] 
# Use the context {context} and recommend only 3 genres to the user based on the user's mood input. Do not provide anything else. 
# Make sure these genres are present in the context. 
# User Input: {input} 

# Your output MUST only provide genres and nothing else. 
# Output should follow this format:
# Genre: [put genres here]
# [/INST]
#     '''

# prompt = PromptTemplate(template=template)

# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# chain = create_retrieval_chain(retriever, question_answer_chain)

# query = "I am feeling romantic"

# result = chain.invoke({"input": query})

# print(result['answer'])
#main.py
# following this tutorial:
#https://blog.nextideatech.com/chat-with-documents-using-langchain-gpt-4-python/

#also good video I'm watching: https://www.youtube.com/watch?v=3yPBVii7Ct0





import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import backoff
import openai


os.environ['OPENAI_API_KEY'] =  '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'



#---load the document(s). This can be commented out after storage is completed
# loader = DirectoryLoader("./venv/TrainingDocuments/BhamRealestateMarket", glob="./*.pdf", loader_cls=PyMuPDFLoader)
# documents = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
# texts = text_splitter.split_documents(documents)

#initialize the directory TrainingDocuments location and instanciate an embeddings object
persist_directory = "./storage"
embeddings = OpenAIEmbeddings()


# #Create and store the vector database This section can be commented out after storage is completed
# vectordb = Chroma.from_documents(documents=texts,
#                                  embedding=embeddings,
#                                  persist_directory=persist_directory)
# vectordb.persist()

#get from disk
vectordb = None
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)


retriever = vectordb.as_retriever(search_kwargs={"k": 4})
llm = ChatOpenAI(model_name='gpt-3.5-turbo')
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)


# while True:
#         user_input = input("Enter a query: ")
#         if user_input == "exit":
#             break
#
#         query = f"###Prompt {user_input}"
#         try:
#             llm_response = qa(query)
#             print(llm_response["result"])
#             # print('\n\nSources:')
#             # for source in llm_response["source_documents"]:
#             #     print(source.metadata['source'])
#         except Exception as err:
#             print('Exception occurred. Please try again', str(err))

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def QueryLLM(query):
    qry = f"###Prompt {query}"
    llm_response = qa(qry)
    return llm_response["result"]


#print (QueryLLM("Who is Frederick?"))
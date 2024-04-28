from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from redundant_filter_retriever import RedundantFilterRetriever

load_dotenv()

chat = ChatOpenAI()
embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory="emb", embedding_function=embeddings)
retriever = RedundantFilterRetriever(embeddings=embeddings, chroma=db)
"""
retriever는 다양한 db를 지원하기 위한 인터페이스
문자열을 받아 관련있는 도큐먼트들을 리턴하는 get_relevant_documents 함수가 있음
"""

chain = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff",  # take some context from the vector store and stuff it into prompt(SystemMessagePromptTemplate)
)

result = chain.run("what is interesting facts about the English language?")
print(result)

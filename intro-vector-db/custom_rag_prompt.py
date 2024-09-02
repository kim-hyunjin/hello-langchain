import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

"""
https://wikidocs.net/231393

RAG(Retrieval-Augmented Generation) 파이프라인은 기존의 언어 모델에 검색 기능을 추가하여, 
주어진 질문이나 문제에 대해 더 정확하고 풍부한 정보를 기반으로 답변을 생성할 수 있게 해줍니다. 
이 파이프라인은 크게 데이터 로드, 텍스트 분할, 인덱싱, 검색, 생성의 다섯 단계로 구성됩니다. 
"""
if __name__ == '__main__':
    print("Retrieving...")
    query = "What is Pinecone in machine learning?"

    llm = ChatOpenAI()
    embeddings = OpenAIEmbeddings()
    vector_store = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"], embedding=embeddings
    )

    template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    User three sentences maximum and keep the answer as concise as possible.
    Always say "Thanks for asking!" at the end of the answer.
    Answer any use questions based solely on the context below:
    
    {context}
    
    Question: {question}
    
    Helpful Answer:
    """
    custom_rag_prompt = PromptTemplate.from_template(template=template)
    rag_chain = (
            {"context": vector_store.as_retriever() | format_docs, "question": RunnablePassthrough()}
            | custom_rag_prompt | llm
    )
    result = rag_chain.invoke(query)
    print(result)

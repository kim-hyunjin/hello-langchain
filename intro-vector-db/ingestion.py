from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os

load_dotenv()

if __name__ == '__main__':
    print("Ingesting...")
    # input - text
    # blackbox (Embedding model)
    # output - vector

    # 현재 파일의 디렉토리 경로
    current_directory = os.path.dirname(os.path.abspath(__file__))
    textfile = os.path.join(current_directory, 'medium-blog1.txt')

    loader = TextLoader(textfile)
    document = loader.load()

    print("Splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    embeddings = OpenAIEmbeddings()
    PineconeVectorStore.from_documents(texts, embeddings, index_name=os.environ["INDEX_NAME"])
    print("finish")
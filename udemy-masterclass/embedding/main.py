from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()
"""
emb = embeddings.embed_query("hi there")
print(emb)
"""
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=0)
loader = TextLoader("facts.txt")
docs = loader.load_and_split(text_splitter=text_splitter)

# instantly, calculate embeddings with openai - it cost fraction of penny
db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory="emb",
)

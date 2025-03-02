from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_TOKEN")
MONGODB_COLLECTION = os.getenv("COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")
MONGODB_NAME = os.getenv("DB_NAME")
MONGODB_ATLAS_CLUSTER_URI = os.getenv("MONGODB_ATLAS_CLUSTER_URI")

client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
mongo_collection = client[MONGODB_NAME][MONGODB_COLLECTION]

text_loader_kwargs={'autodetect_encoding': True}
txt_loader = DirectoryLoader('./documents', 
                             glob="**/*.txt",
                             loader_cls = TextLoader,
                             loader_kwargs=text_loader_kwargs
                            )

documents_loader = txt_loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,
                                                chunk_overlap=512)

chunks = text_splitter.split_documents(documents_loader)

embeddings = HuggingFaceEmbeddings(
    model_name='hiieu/halong_embedding',
    model_kwargs={'device': 'cpu'},
    encode_kwargs= {'normalize_embeddings': False}
    )

vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection=mongo_collection,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

print("Tạo vector database thành công!")
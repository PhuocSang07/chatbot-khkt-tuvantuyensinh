from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.MODEL_EMBEDDING_NAME = os.getenv('MODEL_EMBEDDING_NAME') or 'bkai-foundation-models/vietnamese-bi-encoder'
        self.MONGODB_ATLAS_CLUSTER_URI = os.getenv('MONGODB_ATLAS_CLUSTER_URI')
        self.DB_NAME = os.getenv('DB_NAME') or 'langchain_db'
        self.COLLECTION_NAME = os.getenv('COLLECTION_NAME') or 'vector_db'
        self.ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv('ATLAS_VECTOR_SEARCH_INDEX_NAME') or 'vector_search_index'
        self.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        self.GROQ_API_KEY = os.getenv('GROQ_API_KEY')
        
        # Set Google API key
        os.environ["GOOGLE_API_KEY"] = self.GOOGLE_API_KEY
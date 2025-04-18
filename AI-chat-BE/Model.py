from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
import torch

class LanguageModelPipeline:
    def __init__(self, model_embedding_name):
        self.model_embedding_name = model_embedding_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.embeddings = self.create_embedding_model()

    def get_embedding(self):
        return self.embeddings

    def create_embedding_model(self):
        model_kwargs = {'device': self.device}
        encode_kwargs = {'normalize_embeddings': False}
        embeddings = HuggingFaceEmbeddings(
            model_name=self.model_embedding_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        return embeddings
    
    def create_chain(self, llm, prompt, retriever_db, return_source_documents=True):
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=retriever_db,
            return_source_documents=return_source_documents,
            chain_type_kwargs={
                'prompt': prompt,
                'document_variable_name': 'context',  
            },
        )
        return chain
    
    def retrieve_documents(self, retriever, question, is_web_search=False):
        docs = retriever.invoke(question)
        if len(docs) < 10:
            is_web_search = True
        return docs, is_web_search
from langchain_community.retrievers import WikipediaRetriever
from langchain.retrievers import EnsembleRetriever
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
    
    def create_chain(self, llm, prompt, retriever_db, top_k_documents=3, return_source_documents=True):
                
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
    
    # def custom_chain(self, llm, retriever_db, top_k_documents=3, return_source_documents=True, query=None, history=None):
    #     docs = retriever_db.similarity_search_with_score(query, k=top_k_documents)
    #     docs_content = "\n".join([doc['content'] for doc in docs])

    #     prompt = f"""
    #         Bạn là một trợ lí tư vấn tuyển sinh của trường THPT Ung Văn Khiêm bằng Tiếng Việt nhiệt tình và trung thực.
    #         Câu trả lời của bạn không nên chứa bất kỳ nội dung gây hại, phân biệt độc hại hoặc bất hợp pháp nào.
    #         Nếu bạn không biết câu trả lời cho một câu hỏi, hãy chỉ trả lời là bạn không biết thông tin và trả lời người dùng cần liên hệ với nhà trường để được giải đáp.
    #         Các câu trả lời đưa ra số liệu phải đi kèm thời gian của số liệu đó, đảm bảo không hiểu lầm số liệu quá khứ là số liệu của hiện tại và lựa chọn thông tin được sửa đổi mới nhất.Câu trả lời phải được định dạng chuẩn Markdown.
    #         Dựa vào đoạn chat trước đó: {history}
    #         Dựa vào thông tin sau để trả lời: 
    #         {docs_content}.
    #         Câu hỏi: {query}"""

    #     result = llm.invoke(prompt)

        
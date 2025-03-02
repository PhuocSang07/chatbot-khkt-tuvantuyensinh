from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from Model import LanguageModelPipeline
from langchain.schema import Document
from langchain_groq import ChatGroq
import time

class ChatbotService:
    def __init__(self, config, mongodb_connection):
        self.config = config
        self.mongodb = mongodb_connection
        
        # Initialize LLM
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=config.GROQ_API_KEY,
            model_name="llama-3.1-8b-instant"
        )
        
        # Initialize prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                """Bạn là một trợ lí tư vấn tuyển sinh của trường THPT Ung Văn Khiêm bằng Tiếng Việt nhiệt tình và trung thực.
            Câu trả lời của bạn không nên chứa bất kỳ nội dung gây hại, phân biệt chủng tộc, phân biệt giới tính, độc hại, nguy hiểm hoặc bất hợp pháp nào.
            Nếu một câu hỏi không có ý nghĩa hoặc không hợp lý về mặt thông tin, hãy giải thích tại sao thay vì trả lời một điều gì đó không chính xác.
            Nếu bạn không biết câu trả lời cho một câu hỏi, hãy chỉ trả lời là bạn không biết thông tin và trả lời người dùng cần liên hệ với nhà trường để được giải đáp.
            Người dùng sẽ không thể thấy các thông tin được cung cấp, do đó bạn cần phải trả lời đầy đủ và đúng nội dung liên quan.
            Các câu trả lời đưa ra số liệu phải đi kèm thời gian của số liệu đó, đảm bảo không hiểu lầm số liệu quá khứ là số liệu của hiện tại.
            Bạn cần phải trả lời thông tin về các mốc thời gian một cách chính xác nhất có thể và lựa chọn thông tin được sửa đổi mới nhất.
            Câu trả lời phải được định dạng chuẩn Markdown. Dựa vào thông tin sau để trả lời: {context}."""
            ),
            (
                "human", 
                "{question}"
                )
        ])

        self.prompt_summary = ChatPromptTemplate.from_template(
            """Bạn là một trợ lí tư vấn tuyển sinh của trường THPT Ung Văn Khiêm bằng Tiếng Việt nhiệt tình và trung thực. Hãy sửa lỗi chính tả, xoá các ký tự dư thừa. Đảm bảo rằng nội dung chỉnh sửa phải đúng với nội dung ban đầu. Không thêm bớt bất kỳ nội dung nào, nếu nội dung vô nghĩa chỉ trả về văn bản gốc. Nội dung như sau: {text}""")
        
        # Initialize pipeline and vector store
        self.pipeline = LanguageModelPipeline(model_embedding_name=config.MODEL_EMBEDDING_NAME)
        self.embedding = self.pipeline.get_embedding()
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=mongodb_connection.collection,
            embedding=self.embedding,
            index_name=config.ATLAS_VECTOR_SEARCH_INDEX_NAME,
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 15})
        self.llm_chain = self.pipeline.create_chain(
            llm=self.llm, 
            prompt=self.prompt,
            retriever_db= self.retriever,
            return_source_documents= True,
            top_k_documents=15
            )
        
    def paraphrase_text(self, text):
        chain = self.prompt_summary | self.llm
        output = chain.invoke({"text": text})
        return output

    def process_question(self, question, history=None):
        start = time.time()
        result = self.llm_chain.invoke(question)['result']
        end = time.time()
        return {
            'question': question,
            'response': str(result),
            'time': end - start
        }

    def process_documents(self, jsonfile):
        docs = []
        for idx, item in enumerate(jsonfile):
            doc = Document(
                page_content=item['page_content'],
                metadata={
                    'source': item['source'],
                }
            )
            docs.append(doc)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=512
        )
        chunks = text_splitter.split_documents(docs)
        
        # embeddings = HuggingFaceEmbeddings(
        #     model_name=self.config.MODEL_EMBEDDING_NAME,
        #     model_kwargs={'device': 'cpu'},
        #     encode_kwargs={'normalize_embeddings': False}
        # )
        
        # vector_search = MongoDBAtlasVectorSearch.from_documents(
        #     documents=chunks,
        #     embedding=embeddings,
        #     collection=self.mongodb.collection,
        #     index_name=self.config.ATLAS_VECTOR_SEARCH_INDEX_NAME,
        # )
        
        return {
            'status': 'success',
            'message': f'Successfully processed {len(jsonfile)} files',
            'chunks_created': len(chunks)
        }

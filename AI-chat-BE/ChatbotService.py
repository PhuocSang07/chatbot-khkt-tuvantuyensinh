from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from Model import LanguageModelPipeline
from langchain.schema import Document
import time
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from datetime import datetime
class ChatbotService:
    def __init__(self, config, mongodb_connection):
        self.config = config
        self.mongodb = mongodb_connection
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-001",
            temperature=0.6,
            max_output_tokens=8192,
            top_p=0.95,
            top_k=40,
            n=3,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        
        # Initialize prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                """
                Bạn là một trợ lí tư vấn tuyển sinh của trường THPT Ung Văn Khiêm bằng Tiếng Việt nhiệt tình và trung thực.
                Bạn cần phải trả lời đầy đủ và đúng nội dung liên quan.
                Các câu trả lời đưa ra số liệu phải đi kèm thời gian của số liệu đó, đảm bảo không hiểu lầm số liệu quá khứ là số liệu của hiện tại.
                Bạn cần phải trả lời thông tin về các mốc thời gian một cách chính xác nhất có thể và lựa chọn thông tin được sửa đổi mới nhất.
                **Nếu học sinh cần hỏi đáp, hay giải bài tập gì đó, bạn hãy giải đáp giúp học sinh một cách rõ ràng và dễ hiểu nhất có thể.
                Câu trả lời phải được định dạng chuẩn Markdown.
                *Thời gian hiện tại: {current_time} *
                Nội dung đoạn hội thoại (nếu có): {history}
                Dựa vào thông tin sau để trả lời: {context}."""
            ),
            (
                "human", 
                "{question}"
                )
        ])
        
        self.pipeline = LanguageModelPipeline(model_embedding_name=config.MODEL_EMBEDDING_NAME)
        self.embedding = self.pipeline.get_embedding()

        self.vector_store = MongoDBAtlasVectorSearch(
            collection=mongodb_connection.collection,
            embedding=self.embedding,
            index_name=config.ATLAS_VECTOR_SEARCH_INDEX_NAME,
        )
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={
                "k": 20,
                "score_threshold": 0.6,
                }
            )
        
    def process_question(self, question, history=None):
        docs, is_websearch = self.pipeline.retrieve_documents(
            retriever= self.retriever,
            question= question
        )
        
        prompt_chat = self.prompt.format_prompt(
            question=question,
            context=docs,
            history=str(history),
            current_time=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        start = time.time()            

        result = self.llm.invoke(prompt_chat).content
        end = time.time()
        return {
            'question': question,
            'response': str(result),
            'search_web': is_websearch,
            'time': end - start
        }

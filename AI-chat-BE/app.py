from flask import Flask, request, jsonify
from Config import Config
from MongoDBConnection import MongoDBConnection
from ChatbotService import ChatbotService
from semantic_router.sample import chatbotSample, chitchatSample
from semantic_router import SemanticRouter, Route
from langchain_huggingface import HuggingFaceEmbeddings
import torch
from langchain_google_genai import ChatGoogleGenerativeAI
from Config import Config
from reflection import Reflection
from flask_cors import CORS
# Initialize Flask app
app = Flask(__name__)
CORS(app)  
config = Config()

mongodb_connection = MongoDBConnection(config)
chatbot_service = ChatbotService(config, mongodb_connection)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
config = Config()

#--- Embeddings ---#
model_kwargs = {'device': device}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=config.MODEL_EMBEDDING_NAME,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

#--- Route ---#
PRODUCT_ROUTE_NAME = 'chatbot'
CHITCHAT_ROUTE_NAME = 'chitchat'

productRoute = Route(name=PRODUCT_ROUTE_NAME, samples=chatbotSample)
chitchatRoute = Route(name=CHITCHAT_ROUTE_NAME, samples=chitchatSample)
semanticRouter = SemanticRouter(embeddings, routes=[productRoute, chitchatRoute])

#--- LLM ---#
llm_reflection = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-001",
        temperature=0.1,
        max_tokens=None,
        timeout=None,
        max_retries=3,
    )   

#--- Reflection ---#
reflection = Reflection(llm=llm_reflection)

@app.route('/', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('message')
        history = data.get('history')
        turn = data.get('turn')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        if not history:
            history = []
        if not turn:
            turn = 0
        elif turn > 4:        
            history = reflection(history)
        result = chatbot_service.process_question(question, history)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from Config import Config
from MongoDBConnection import MongoDBConnection
from ChatbotService import ChatbotService
from semantic_router.sample import chatbotSample, chitchatSample
from semantic_router import SemanticRouter, Route
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
import torch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from Config import Config
from reflection import Reflection

# Initialize Flask app
app = Flask(__name__)
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
        model="gemini-1.5-flash",
        temperature=0.1,
        max_tokens=None,
        timeout=None,
        max_retries=3,
    )   

#--- Reflection ---#
reflection = Reflection(llm=llm_reflection)

#--- Sub ---#
@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    try:
        data = request.json
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        result = chatbot_service.paraphrase_text(text)
        return jsonify({"text": result.content})
        
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/documents/check/<filename>', methods=['GET'])
def check_source_exists(filename):
    try:
        exists = mongodb_connection.collection.find_one({"source": filename}) is not None
        return jsonify({"exists": exists})
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/documents/<filename>', methods=['DELETE'])
def delete_documents_by_source(filename):
    try:
        result = mongodb_connection.collection.delete_many({"source": filename})
        if result.deleted_count > 0:
            return jsonify({
                'status': 'success',
                'message': f'Successfully deleted {result.deleted_count} documents with source: {filename}'
            })
        return jsonify({
            'status': 'warning',
            'message': f'No documents found with source: {filename}'
        })
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
    
@app.route('/documents', methods=['POST'])
def add_documents():
    try:
        data = request.json
        # print(data)
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        result = chatbot_service.process_documents(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
    
@app.route('/documents', methods=['GET'])
def get_sources():
    try:
        sources = mongodb_connection.collection.distinct("source")
        return jsonify({"sources": sources})
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('message')
        history = data.get('history')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        if not history:
            history = []
            
        result = chatbot_service.process_question(question, history)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
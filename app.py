from flask import Flask, request, jsonify
from flask_cors import CORS
import medibot

app = Flask(__name__)
CORS(app)


# @app.route('/submit', methods=['POST'])
# def submit_college():
#     data = request.get_json()
#     college = data.get('college')
#     vectordb = load_vectordb(college)
#     if college:
#         global chain
#         chain = get_rag_chain(vectordb)
#         return jsonify({'message': 'Vector database and RAG chain initialized successfully!'}), 200
#     else:
#         return jsonify({'error': 'Failed to initialize vector database and RAG chain'}), 500
#     # else:
#     #     return jsonify({'error': 'No college name provided'}), 400

@app.route('/')
def hello():
    return "Hello world"

@app.route('/chat/<query>')
def chat(query):
    
    return jsonify({'query':medibot.calling(query)})
    # # Here you would use the initialized RAG chain to process the query
    # # This is a placeholder for actual RAG logic
    # if college and query:
    #     response = generate_response(chain, query)
    #     print(f'You asked about {college}: {query}')
    #     return jsonify({'response': response}), 200
    # else:
    #     return jsonify({'error': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(debug=True)

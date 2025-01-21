@app.route('/submit', methods=['POST'])
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

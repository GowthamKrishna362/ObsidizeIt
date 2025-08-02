from flask import Flask, jsonify, request
from obsidizer import handle_obsidize
app = Flask(__name__)

@app.route('/obsidize', methods=['POST'])
def obsidize():
    data = request.json
    print("Received data: ", data)
    
    input_text = data['input']
    if 'target_file' in data:
        target_file = data['target_file']
    else:
        target_file = 'default'
    
    handle_obsidize(input_text, target_file)
    return jsonify({'message': 'Data received', 'target_file': target_file}), 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
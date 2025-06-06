from flask import Flask, jsonify, request

app = Flask(__name__)

# Przykładowy endpoint GET
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask backend!"})

# Przykładowy endpoint POST
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify({"you_sent": data})

if __name__ == '__main__':
    app.run(debug=True)

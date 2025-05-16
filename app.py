from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sensor-data', methods=['POST'])
def sensor_data():
    data = request.json
    print("Otrzymane dane:", data)
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)

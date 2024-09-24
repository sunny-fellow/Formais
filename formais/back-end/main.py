from flask_cors import CORS
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
CORS(app)  # Isso permite CORS para todas as rotas

@app.route("/verifyProduction", methods=["POST"])
def verifyProduction():
    data = request.get_json()
    print(data)
    return jsonify({"message": "Hello, World!"})



if __name__ == '__main__':
    app.run(debug=True)
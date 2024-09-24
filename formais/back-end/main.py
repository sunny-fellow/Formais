from flask_cors import CORS
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
CORS(app)  # Isso permite CORS para todas as rotas

@app.route("/verifyProduction")
def verifyProduction(){
    data = request.get_json()
}



if __name__ == '__main__':
    app.run(debug=True)
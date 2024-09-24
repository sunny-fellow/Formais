from flask_cors import CORS
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
CORS(app)  # Isso permite CORS para todas as rotas

@app.route("/verifyInput", methods=["POST"])
def verifyInput():
    # Essa rota eh responsavel por verificar se o input esta no estilo "letra: producao"
    texto = request.get_json()["entrada"]
    print(texto)
    return jsonify({"message": "verifyInput"})

@app.route("/verifyProduction", methods=["POST"])
def verifyProduction():
    # Essa rota deve ser responsavel por retornar se a producao e valida, e adicionar ao back essa producao
    data = request.get_json()
    print(data)
    return jsonify({"message": "verifyProduction"})

@app.route("/removeProduction", methods=["POST"])
def removeProduction():
    # Essa rota deve ser responsavel por retornar se a producao ja esta inserida, e remover do back essa producao
    data = request.get_json()
    print(data)
    return jsonify({"message": "removeProduction"})



if __name__ == '__main__':
    app.run(debug=True)

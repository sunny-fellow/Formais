from flask_cors import CORS
from flask import Flask, render_template, jsonify, request
import re # Importa os metodos de regex
from grammarThings.gram import Grammar

app = Flask(__name__)
CORS(app)  # Isso permite CORS para todas as rotas
gram = Grammar()


@app.route("/verifyInput", methods=["POST"])
def verifyInput():
    # Essa rota eh responsavel por verificar se o input esta no estilo "letra: producao"
    texto = request.get_json()["entrada"]
    pattern = r'[a-zA-Z]: [a-zA-Z0-9]*'
    if re.fullmatch(pattern, texto):
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})


@app.route("/verifyProduction", methods=["POST"])
def verifyProduction():
    data = request.get_json()
    variaveis = data["variaveis"]
    terminais = data["terminais"]
    producao = data["producao"]

    # print(variaveis, terminais, producao)
    if producao == "epsilon":
        return jsonify({"valid": True})

    for letter in producao:
        if not letter in variaveis and not letter in terminais:
            return jsonify({"valid": False})
    
    return jsonify({"valid": True})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"Error": "Nenhum arquivo enviado."})
    
    arquivo = request.files['file']
    print(arquivo)
    
    if arquivo.filename == '':
        return jsonify({"Error": "Nenhum arquivo selecionado."})
    
    try:
        conteudo = arquivo.read().decode('utf-8')

        arq_val = archive_validation(conteudo)
        if arq_val[0]:
            return jsonify({"Success": conteudo})
        else:
            return arq_val[1]
    
    except Exception as e:
        return jsonify({"Error": f"Ocorreu um erro: {e}"})


def archive_validation(content:str) -> bool:
    lines = content.split("\n")
    vars_pattern = r'[a-zA-Z]*:(A-Z, )*(A-Z)'
    ini_pattern = r'[a-zA-Z]*:(A-Z)'
    term_pattern = r'[a-zA-Z]*:(a-z, )*(a-z)'
    prod_pattern = r'(A-Z): [a-zA-Z0-1]*'

    if len(lines) < 5:
        return (False, jsonify({"Error": "Nao ha informacoes o suficiente para a gramatica"}))

    if not re.fullmatch(vars_pattern, lines[0]):
        return (False, jsonify({"Error": "Variaveis nao formatadas corretamente"}))
    elif not re.fullmatch(ini_pattern, lines[1]):
        return (False, jsonify({"Error": "Variavel inicial nao formatada corretamente"}))
    elif not re.fullmatch(term_pattern, lines[2]):
        return (False, jsonify({"Error": "Terminais nao formatadas corretamente"}))
    else:
        for i in range(4, len(lines)):
            if not re.fullmatch(prod_pattern, lines[i]):
                return (False, jsonify({"Error": f"Producao linha {i+1} formatada incorretamente"}))
    
    return (True, jsonify({"Success": "Tudo formatado corretamente"}))

@app.route('/verifyInputGrammar', methods=['POST'])
def verifyFormat():
    data = request.get_json()
    if not data:
        return {"valid": False, "message": "No JSON data received"}

    print(data)

    pattern_variables = r'([A-Z],\s)*[A-Z]'
    pattern_terminal = r'([a-z]+|epsilon)(, ([a-z]+|epsilon))*'
    pattern_inicial   = r'[A-Z]'

    if not re.fullmatch(pattern_variables, data.get("variaveis", "")):
        return jsonify({"valid": False, "message": "formato de variaveis invalido"})
    elif not re.fullmatch(pattern_terminal, data.get("terminais", "")):
        return jsonify({"valid": False, "message": "formato de terminais invalido"})
    elif not re.fullmatch(pattern_inicial, data.get("inicial", "")):
        return jsonify({"valid": False, "message": "formato de inicial invalido"})
    else:
        return jsonify({"valid": True, "message": "formato valido"})

def verifyProductions(producoes, variaveis, terminais):
    pattern = f"[{variaveis}*{terminais}*]*"
    for prod in producoes.keys():
        for p in producoes[prod]:
            if not re.fullmatch(pattern, p):
                return {"valid": False, "message": f"Producao {prod}: {p} invalida"}
            
    return {"valid": True, "message": "Producoes validas"}
            

@app.route('/receiveInputs', methods=['POST'])
def receive_inputs():
    data = request.get_json()
    print(data)

    # Verifica se as producoes sao validas
    verify = verifyProductions(data["producoes"], data["variaveis"], data["terminais"])
    if verify["valid"]:
        return jsonify(verify)
    else:
        print(verify)
        return jsonify(verify)
        

if __name__ == '__main__':
    app.run(debug=True)

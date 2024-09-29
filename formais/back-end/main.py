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

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'valid': False, 'message': "Nenhum arquivo enviado."})
    
    archive = request.files['file']
    print(archive)
    
    content = archive.read().decode("utf-8")
    validation = archive_validation(content)

    if not validation[0]:
        return jsonify({'valid': False, 'message': validation[1]["Error"]})
    
    ret = {
        "variaveis": content.split("\n")[0].strip().split(":")[1],
        "inicial": content.split("\n")[1].strip().split(":")[1],
        "terminais": content.split("\n")[2].strip().split(":")[1],
        "producoes": getProductions(content)
    }

    # print("Retorno:", ret)
    return jsonify({'valid': True, 'return': ret})

def getProductions(content:str) -> dict:
    # Pega as producoes do arquivo
    prods = {}

    # Insere as variaveis como chaves
    for var in content.split("\n")[0].split(":")[1].strip().split(","):
        prods[var] = []

    # Adiciona as producoes que cada variavel possui
    for i in range(4, len(content.split("\n"))):
        prod = content.split("\n")[i].strip().split(": ")
        prods[prod[0]].append(prod[1])
    

    return prods

def archive_validation(content:str) -> bool:
    lines = content.split("\n")
    if len(lines) < 4:
        return (False, {"Error": "Nao ha informacoes o suficiente para a gramatica"})
    
    vars_pattern = r'variaveis:([A-Z],)*[A-Z]'
    ini_pattern = r'inicial:[A-Z]'
    term_pattern = r'terminais:([a-z0-9],)*[a-z0-9]'
    prod_pattern = r'[A-Z]: [a-zA-Z0-9]*'

    # Validacao das variaveis
    if not re.fullmatch(vars_pattern, lines[0].strip()):
        for char in lines[0]:
            print("caracter", char)
        return (False, {"Error": "Variaveis nao formatadas corretamente"})
    
    # Validacao da variavel inicial
    elif not re.fullmatch(ini_pattern, lines[1].strip()):
        print(lines[1])
        return (False, {"Error": "Variavel inicial nao formatada corretamente"})
    
    # Validacao dos terminais
    elif not re.fullmatch(term_pattern, lines[2].strip()):
        print(lines[2])
        return (False, {"Error": "Terminais nao formatadas corretamente"})
    
    # Validacao das producoes
    else:
        for i in range(5, len(lines)):
            # Verifica se a producao esta formatada corretamente
            if not re.fullmatch(prod_pattern, lines[i].strip()):
                return (False, {"Error": f"Producao {lines[i].strip()} formatada incorretamente"})
            
            # Verifica se a producao contem simbolos nao aceitos
            if lines[i].split(": ")[1].strip() == "epsilon":
                continue

            for letter in lines[i].strip().split(": ")[1]:
                if not letter in lines[0].split(":")[1] and not letter in lines[2].split(":")[1]:
                    return (False, {"Error": f"Producao {lines[i].strip()} contem simbolos nao aceitos"})
    
    return (True, {"Success": "Tudo formatado corretamente"})


@app.route('/receiveInputs', methods=['POST'])
def receive_inputs():
    data = request.get_json()
    print("GRAMÁTICA: " + str(data))

    validation = verifyFormat(data)
    if not validation["valid"]:
        return validation
    
    gram.set_grammar(data)
    return jsonify({"valid": True, "message": "Gramática recebida com sucesso"})
        
def verifyFormat(data):
    if not data:
        return {"valid": False, "message": "No JSON data received"}

    pattern_variables = r'([A-Z],\s)*[A-Z]'
    pattern_terminal = r'([a-z]+|epsilon)(, ([a-z]+|epsilon))*'
    pattern_inicial   = r'[A-Z]'

    variaveis = str(data["variaveis"]).replace(",", ", ")
    terminais = str(data["terminais"]).replace(",", ", ")


    if not re.fullmatch(pattern_variables, variaveis):
        return jsonify({"valid": False, "message": "formato de variaveis invalido"})
    elif not re.fullmatch(pattern_terminal, terminais):
        return jsonify({"valid": False, "message": "formato de terminais invalido"})
    elif not re.fullmatch(pattern_inicial, data["inicial"]):
        return jsonify({"valid": False, "message": "formato de inicial invalido"})
    else:
        return jsonify({"valid": True, "message": "formato valido"})

if __name__ == '__main__':
    app.run(debug=True)

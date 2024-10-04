from flask_cors import CORS
from flask import Flask, render_template, jsonify, request
import re # Importa os metodos de regex
from grammarThings.gram import Grammar
from grammarThings.dataStructures.chainTree import Tree


app = Flask(__name__)
CORS(app)  # Isso permite CORS para todas as rotas
gram = Grammar()
chainTree = None


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
        return (False, {"Error": "Variaveis não formatadas corretamente"})
    
    # Validacao da variavel inicial
    elif not re.fullmatch(ini_pattern, lines[1].strip()):
        print(lines[1])
        return (False, {"Error": "Variavel inicial não formatada corretamente"})
    
    # Validacao dos terminais
    elif not re.fullmatch(term_pattern, lines[2].strip()):
        print(lines[2])
        return (False, {"Error": "Terminais não formatados corretamente"})
    
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
        return jsonify(validation)
    
    gram.dict_to_grammar(data)
    return jsonify({"valid": True, "message": "Gramática recebida com sucesso", "allTrap": gram.check_grammar()["allTrap"]})
        
def verifyFormat(data):
    if not data:
        return {"valid": False, "message": "No JSON data received"}

    pattern_variables = r'([A-Z],\s)*[A-Z]'
    pattern_terminal = r'([a-z0-9]+|epsilon)(, ([a-z0-9]+|epsilon))*'
    pattern_inicial   = r'[A-Z]'

    variaveis = ', '.join(data["variaveis"])
    terminais = ', '.join(data["terminais"])

    print("variaveis:", variaveis, "terminais:", terminais)

    if not re.fullmatch(pattern_variables, variaveis):
        return {"valid": False, "message": "Formato de variaveis invalido ou não preenchido"}
    elif not re.fullmatch(pattern_terminal, terminais):
        return {"valid": False, "message": "Formato de terminais invalido ou não preenchido"}
    elif not re.fullmatch(pattern_inicial, data["inicial"]):
        return {"valid": False, "message": "Formato de inicial invalido ou não preenchido"}
    elif not data['inicial'] in variaveis:
        return {'valid': False, 'message': "Símbolo inicial  [ " + data["inicial"] + " ]  não presente nas variáveis"}
    else:
        return {"valid": True, "message": "formato valido"}


@app.route('/setFastMode')
def setFastMode():
    # gram.setFastMode()
    return jsonify({"valid": True, "message": "Modo rápido ativado", "allTrap": gram.check_grammar()["allTrap"]})


@app.route('/setDetailedMode')
def setDetailedMode():
    return jsonify({"valid": True, "initial": gram.initial, "allTrap": gram.check_grammar()["allTrap"]})


@app.route('/getProductionsOf', methods=['POST'])
def getProductionsOf():
    data = request.get_json()
    print("Solicitou producoes para a variavel: " + data['variavel'])

    # salva as producoes para a variavel recebida como parametro
    prods = gram.productions[data['variavel']]
    traps = []
    
    # para cada producao nessa lista de producoes
    for prod in prods:

        # verificando cada varaivel armadilha
        for trap in gram.traps:
            # se se houver pelo menos uma trap na producao em questao, adiciona essa producao a lista de producoes trap
            if trap in prod:
                traps.append(prod)
                break

    return jsonify({"productions": prods, "traps": traps})
    

@app.route('/derivate', methods=['POST'])
def derivate():
    data = request.get_json()

    print("\n\n" + str(data) + "\n\n")	

    chain = data["cadeia"]
    var = data["variavel"]
    opt = data["opcao"]

    if opt != gram.E:
        # percorrendo os caracteres da cadeia a derivar  
        for i in range(len(chain)):
            # se o caractere for igual ao simbolo 
            if chain[i] == var:
                # no caso da variavel nao estar no fim da cadeia
                if i < len(chain)-1:
                    chain = chain[0:i-1] + opt + chain[i+1:len(chain)]
                    print(chain)
                else:
                    chain = chain[0:i] + opt
                
                break
    else:
        chain = chain.replace(var, "")

    finished = True
    isTrap = False
    toDerivate = ''
    
    if opt != gram.E:
        for c in chain:
            print(f"{chain}: {c}")
            if c in gram.nonTermSymbols:
                finished = False
                toDerivate = c
                break
            
        for c in chain:
            if c in gram.traps:
                isTrap = True
                break
        
        
    
    return jsonify({"variable": var,
            "result": chain,
            "finished": finished,
            "isTrap": isTrap,
            "toDerivate": toDerivate})

@app.route('/cleanGrammar')
def cleanGrammar():
    gram.clean_grammar()

@app.route('/getVariableToDerivate', methods=['POST'])
def getVariablesToDerivate():
    data = request.get_json()
    print(data)

    prod = data['producao']

    for c in prod:
        if c in gram.nonTermSymbols:
            return jsonify({'variable': c})
    
    return jsonify({'variable': None})


# Variaveis utilizadas para a funcao getFastChain:
chainTree:Tree = None
depth = 1
alreadysent = []
retorno = []

@app.route('/generateFastChain')
def getFastChain():
    global chainTree, depth, alreadysent, retorno

    # Se ja tiver algo a espera de ser enviado, envia, tirando-a da fila
    if len(retorno) > 0:
        print("Enviando cadeia: ", retorno[0])
        return jsonify({"chain": retorno.pop(0)})
    
    # Se nao tiver nada a espera de ser enviado, cria a arvore
    else:
        chainTree = Tree(gram.initial, gram, depth)
        
        # Pega a lista de cadeias
        retorno = chainTree.getChainList()
        print("Retorno: ", retorno)
        depth += 1

        canContinue = False
        # Para cada sequencia de producoes, verifica se a cadeia gerada eh valida, ou seja, se nao contem variaveis
        print("NonTermSymbols: ", gram.nonTermSymbols)
        for elem in retorno:
            print("Analisando: ", elem)
            for car in elem[len(elem)-1]:
                if car in gram.nonTermSymbols:
                    canContinue = True
                    print("Removendo: ", elem)
                    retorno.remove(elem)
                    break
        
        # Agora, a retorno contem sequencias de producoes que geram cadeias validas, mas precisamos verificar se ja nao enviamos essas cadeias
        for elem in retorno:
            if elem in alreadysent:
                retorno.remove(elem)
            else:
                alreadysent.append(elem)

        # Se ainda houver algo a ser enviado, envia
        if len(retorno) > 0:
            print("Enviando cadeia: ", retorno[0])
            return jsonify({"chain": retorno.pop(0)})
        
        # Se nao houver mais nada a ser enviado, volta a tentar gerar
        elif canContinue:
            return getFastChain()
        
        # Se nao houver mais nada a ser enviado e nao houver mais nada a ser gerado, retorna uma mensagem de erro
        else:
            print("Nao ha mais cadeias a serem geradas")
            return jsonify({"chain": []})

    


# Roda o servidor
if __name__ == '__main__':
    app.run(debug=True)
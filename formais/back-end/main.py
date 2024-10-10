from flask_cors import CORS
from flask import Flask, jsonify, request
import re # Importa os metodos de regex
from grammarThings.gram import Grammar
from grammarThings.dataStructures.chainTree import Tree


# Inicialização de variáveis globais
chainTree = None
gram = Grammar()

# Criação da aplicação Flask
app = Flask(__name__)
CORS(app)


@app.route("/verifyInput", methods=["POST"])
def verifyInput():

    """
    Verifica se a entrada está no formato "letra: produção".

    Retorno:

    {

        JSON

        "valid": bool   # Indica se o formato da entrada é válido
    }
    """

    # Essa rota eh responsavel por verificar se o input esta no estilo "letra: producao"
    texto = request.get_json()["entrada"]
    pattern = r'[a-zA-Z]: [a-zA-Z0-9$&@#%\*\+\-/!?]*'
    if re.fullmatch(pattern, texto):
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})


# Rota para verificar se uma produção é válida
@app.route("/verifyProduction", methods=["POST"])
def verifyProduction():

    """
    Verifica se uma produção é composta apenas por variáveis e terminais válidos.

    Retorno:
    
    {
    
        JSON

        "valid": bool  #  Indica se a produção é válida
    }
    """

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


# Rota para fazer upload de um arquivo de gramática
@app.route('/uploadFile', methods=['POST'])
def upload_file():

    """
    Faz o upload de um arquivo de gramática e valida seu conteúdo.

    
    Retorno:

    {
        
        JSON

        "valid": bool,  # Indica se o upload e validação foram bem-sucedidos

        "message": str, # Mensagem de erro ou sucesso

        "return": dict  # Contém variáveis, inicial, terminais e produções, se válido
    }
    """

    if 'file' not in request.files:
        return jsonify({'valid': False, 'message': "Nenhum arquivo enviado."})
    
    archive = request.files['file']
    # print(archive)
    
    content = ""
    for line in archive.read().decode("utf-8").split("\n"):
        if line.strip():
            content += line + "\n"
    content = content.strip()
    print(content)
            
    # for i in range(len(content)):
    #     if content[i] == "":
    #         content.pop(i)
    
    # content = content.split("\n")
    # content = content[0:2].append(content[4:])
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
    """
        Retorna o dict de produções obtidas a partir do arquivo informado como entrada
    """

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

# Função auxiliar para validar o conteúdo do arquivo
def archive_validation(content:str) -> bool:
    """
        Valida a formatação das informações no arquivo, através de regex, retornando se é válido.

        Caso não seja, também retorna uma mensagem informando qual tipo de dado não foi informado corretamente.

    """
    lines = content.split("\n")
    if len(lines) < 4:
        return (False, {"Error": "Nao ha informacoes o suficiente para a gramatica"})
    
    vars_pattern = r'variaveis:([A-Z],)*[A-Z]'
    ini_pattern = r'inicial:[A-Z]'
    term_pattern = r'terminais:([a-z0-9%$&@#\*\+\-/!?],)*[a-z0-9%$&@#\*\+\-/!?]*'
    prod_pattern = r'[A-Z]: [a-zA-Z0-9%$&@#\*\+\-\/!?]*'

    # Validacao das variaveis
    if not re.fullmatch(vars_pattern, lines[0].strip()):
        # for char in lines[0]:
        # print("caracter", char)
        return (False, {"Error": "Variaveis não formatadas corretamente"})
    # Validacao da variavel inicial
    elif not re.fullmatch(ini_pattern, lines[1].strip()):
        # print(lines[1])
        return (False, {"Error": "Variavel inicial não formatada corretamente"})
    
    # Validacao dos terminais
    elif not re.fullmatch(term_pattern, lines[2].strip()):
        # print(lines[2])
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


# Rota para receber gramáticas
@app.route('/receiveInputs', methods=['POST'])
def receive_inputs():

    """
    Recebe uma gramática e a valida.

    Retorno:

    {

        JSON

        "valid": bool,  # Indica se a gramática foi recebida e validada com sucesso

        "message": str, # Mensagem de erro ou sucesso

        "allTrap": bool # Indica se há variáveis armadilha
    }
    """

    data = request.get_json()
    print("GRAMÁTICA: " + str(data))

    validation = verifyFormat(data)
    if not validation["valid"]:
        return jsonify(validation)
    
    gram.dict_to_grammar(data)
    print(gram.traps)
    return jsonify({"valid": True, "message": "Gramática recebida com sucesso", "allTrap": gram.check_grammar()["allTrap"]})


# Função auxiliar para verificar o formato da gramática recebida    
def verifyFormat(data):
    """
        Verifica se o formato da gramática recebida está de acordo com os padrões
        regex definidos.

        As variáveis devem ser letras maiúsculas.

        O incial deve ser uma única letra maiúsculas.

        Os terminais podem ser letras, símbolos ou números.
    """

    if not data:
        return {"valid": False, "message": "No JSON data received"}

    pattern_variables = r'([A-Z],\s)*[A-Z]'
    pattern_terminal = r'([a-z0-9$&@#%\*\+\-/!?]+|epsilon)(, ([a-z0-9$&@#%\*\+\-/!?]+|epsilon))*'
    pattern_inicial   = r'[A-Z]'

    variaveis = ', '.join(data["variaveis"])
    terminais = ', '.join(data["terminais"])

    # print("variaveis:", variaveis, "terminais:", terminais)

    if not re.fullmatch(pattern_variables, variaveis):
        return {"valid": False, "message": "Formato de variaveis invalido ou não preenchido"}
    elif terminais != "" and not re.fullmatch(pattern_terminal, terminais):
        return {"valid": False, "message": "Formato de terminais invalido ou não preenchido"}
    elif not re.fullmatch(pattern_inicial, data["inicial"]):
        return {"valid": False, "message": "Formato de inicial invalido ou não preenchido"}
    elif not data['inicial'] in variaveis:
        return {'valid': False, 'message': "Símbolo inicial  [ " + data["inicial"] + " ]  não presente nas variáveis"}
    else:
        return {"valid": True, "message": "formato valido"}


# Rota para ativar o modo rápido
@app.route('/setFastMode')
def setFastMode():

    """
    Ativa o modo rápido para a gramática.

    Retorno:

    {

        JSON

        "valid": bool,   # Indica se o modo rápido foi ativado com sucesso

        "message": str,  # Mensagem de confirmação

        "allTrap": bool  # Indica se há variáveis armadilha
    }
    """

    # gram.setFastMode()
    return jsonify({"valid": True, "message": "Modo rápido ativado", "allTrap": gram.check_grammar()["allTrap"]})


# Rota para ativar o modo detalhado
@app.route('/setDetailedMode')
def setDetailedMode():

    """
    Ativa o modo detalhado para a gramática.

    Retorno:

    {

        JSON

        "valid": bool,   # Indica se o modo detalhado foi ativado com sucesso

        "initial": str,  # Variável inicial da gramática

        "allTrap": bool  # Indica se há variáveis armadilha
    }
    """

    return jsonify({"valid": True, "initial": gram.initial, "allTrap": gram.check_grammar()["allTrap"]})


# Rota para obter produções de uma variável específica
@app.route('/getProductionsOf', methods=['POST'])
def getProductionsOf():

    """
    Obtém as produções de uma variável específica e verifica se há armadilhas.

    Retorno:

    {

        JSON

        "productions": list,  # Lista de produções para a variável solicitada

        "traps": list          # Lista de produções que contêm variáveis armadilha
    }
    """

    data = request.get_json()
    # print("Solicitou producoes para a variavel: " + data['variavel'])

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
    

# Rota para derivar uma cadeia
@app.route('/derivate', methods=['POST'])
def derivate():

    """
    Realiza a derivação de uma cadeia com base na variável e produção fornecidas.

    Retorno:

    {

        JSON

        "variable": str,     # Variável que foi derivada

        "result": str,       # Resultado da derivação
        
        "finished": bool,    # Indica se a derivação foi concluída
        
        "isTrap": bool,      # Indica se a derivação resultou em uma variável armadilha
        
        "toDerivate": str    # Próxima variável a ser derivada, se houver 
    }
    """

    data = request.get_json()

    # print("\n\n" + str(data) + "\n\n")	

    chain = data["cadeia"]
    var = data["variavel"]
    opt = data["opcao"]

    if opt != gram.E:
        # substitui a primeira aparicao da variavel pela opcao 
        chain = chain.replace(var, opt, 1)
     
    else:
        chain = chain.replace(var, "", 1)

    finished = True
    isTrap = False
    toDerivate = ''
    
    # if opt != gram.E:
    for c in chain:
        # print(f"{chain}: {c}")
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


# Rota para limpar a gramática
@app.route('/cleanGrammar')
def cleanGrammar():

    """
    Limpa a gramática atual.

    Retorno:

    {
    
        JSON

        "valid": bool,   # Indica se a gramática foi limpa com sucesso
        "message": str   # Mensagem de confirmação
    }
    """

    cleanChainTree()
    gram.clean_grammar()
    return jsonify({"valid": True, "message": "Gramática limpa"})


# Rota para limpar a árvore de cadeias
@app.route('/cleanChainTree')
def cleanChainTree():

    """
    Limpa a árvore de cadeias atual.

    Retorno:

    {

        JSON

        "valid": bool,   # Indica se a árvore de cadeias foi limpa com sucesso
        
        "message": str   # Mensagem de confirmação
    }
    """

    global chainTree, depth, alreadysent, queue
    chainTree = None
    depth = 1
    alreadysent.clear()
    queue.clear()
    tree = None
    return jsonify({"valid": True, "message": "Árvore de cadeias limpa"})


# Rota para obter a próxima variável a derivar
@app.route('/getVariableToDerivate', methods=['POST'])
def getVariablesToDerivate():

    """
    Obtém a próxima variável a ser derivada a partir de uma produção.

    Retorno:

    {
    
        JSON

        "variable": str | None  # Próxima variável a ser derivada ou string vazia se não houver
    }
    """

    data = request.get_json()

    prod = data['producao']

    for c in prod:
        if c in gram.nonTermSymbols:
            return jsonify({'variable': c})
    
    return jsonify({'variable': None})


# Variaveis utilizadas para a funcao getFastChain:
chainTree:Tree = None
depth = 1
alreadysent = []
queue = []


# Rota para gerar uma cadeia rapidamente
@app.route('/generateFastChain')
def getFastChain():

    """
    Gera cadeias rapidamente a partir da gramática.

    
    Retorno:
    {
    
        JSON

        "chain": list | []  # Cadeia gerada ou lista vazia se não houver mais cadeias disponíveis
    }

    Se houver apenas um retorno possível:
    {
    
        JSON

        "chain": list | []      # Cadeia gerada ou lista vazia se não houver mais cadeias disponíveis
        "continue": bool        # Informa que não haverá mais cadeias possíveis de serem produzidas
    }
    """

    global chainTree, depth, alreadysent, queue

    # Se ja tiver algo a espera de ser enviado, envia, tirando-a da fila
    if len(queue) > 0:
        # print("Enviando cadeia: ", queue[0])
        return jsonify({"chain": queue.pop(0)})
    
    # Se nao tiver nada a espera de ser enviado, cria a arvore
    else:
        chainTree = Tree(gram.initial, gram, depth)
        
        # Pega a lista de cadeias
        retorno = chainTree.getChainList()
        depth += 1

        canContinue = False
        # Para cada sequencia de producoes, verifica se a cadeia gerada eh valida, ou seja, se nao contem variaveis
        # print("NonTermSymbols: ", gram.nonTermSymbols)
        print("Retorno: ", retorno) 


        queue = retorno
        print("Queue: ", queue)

        if queue != [] and type(queue[0]) == str:
            for char in queue[-1]:
                if char in gram.nonTermSymbols:
                    canContinue = True
                    queue = []
                    break
        else:
            for elem in queue[:]:
                if type(elem) == list:
                    for char in elem[len(elem)-1]:
                        if char in gram.nonTermSymbols:
                            canContinue = True
                            queue.remove(elem)
                            break
        
        # print("Queue: ", queue)
        
        
        # Agora, a queue contem sequencias de producoes que geram cadeias validas, mas precisamos verificar se ja nao enviamos essas cadeias
        if queue != [] and type(queue[0]) == str:
            if queue[-1] in alreadysent:
                queue = []
        else:
            for elem in queue[:]:
                if elem[-1] in alreadysent:
                    queue.remove(elem)
                else:
                    alreadysent.append(elem[-1])

        print("Queue: ", queue)
        print("Tamanho da queue: ", len(queue))

        # Se houver apenas um retorno possivel
        if queue != [] and type(queue[0]) == str:
            print("Caso 1")
            return jsonify({"chain": queue, "continue": canContinue})
        # Se ainda houver algo a ser enviado, envia
        elif len(queue) >= 1:
            print("Caso 2")
            return jsonify({"chain": queue.pop(0)})
        # Se nao houver mais nada a ser enviado, volta a tentar gerar
        elif canContinue:
            print("Caso 3")
            return getFastChain()
        # Se nao houver mais nada a ser enviado e nao houver mais nada a ser gerado, retorna uma mensagem de erro
        else:
            # print("Nao ha mais cadeias a serem geradas")
            print("Caso 4")
            return jsonify({"chain": []})

    
# # Rota para gerar cadeias por profundidade
# @app.route('/generateByDepth', methods=['POST'])
# def generateByDepth():

#     """
#     Gera cadeias limitadas por profundidade a partir da gramática.

#     Retorno:
    
#     {

#         JSON
    
#         "chain": list  # Lista de cadeias geradas

#     }
#     """

#     depth = int(request.get_json()["depth"])
#     # print("Profundidade: ", str(depth))
    
#     chainTree = Tree(gram.initial, gram, int(depth))
#     retorno = chainTree.get_limited_chainList(depth, 2**15)
#     # 2^17 = 131072

#     if retorno:
#         # Se for um array de strings, converte-o em array de arrays. Isso eh necessario para o front-end
#         if type(retorno[0]) == str:
#             retorno = [retorno]
        

#     # print("Retorno tratado: ", retorno)
#     return jsonify({"chain": retorno})
    

@app.route('/verifyDepth', methods=['POST'])
def verifyDepth():
    """
        Verifica se a profundidade informada é válida.

        Retorno:

            JSON
            "valid": bool,          # Indica se a profundidade é válida
            "message": str          # Mensagem de erro ou sucesso
            
        
    """
    depth = request.get_json()['depth']

    if depth == "":
        return jsonify({"valid": False, "message": "É necessário informar a profundidade desejada"})
    elif int(depth) < 1:
        return jsonify({"valid": False, "message": "A profundidade deve estar entre [0 - 15]"})
    elif int(depth) > 15:
        return jsonify({"valid": False, "message": "A profundidade deve estar entre [0 - 15]"})
    else:
        return jsonify({"valid": True, "message": ""})


tree = None
@app.route('/generateByDepth', methods=['POST'])
def generateByDepth():
    """
        Cria um objeto Tree e gera uma cadeia limitada por profundidade a partir da gramática.

        Retorno  JSON:

            "chain": list  # Lista de cadeias geradas

    """
    global tree
    depth = int(request.get_json()["depth"])

    tree = Tree(gram.initial, gram, depth)
    # print("numero de nos: ", tree.nNodes)
    tree.clearSent()
    result = tree.get_limited_chainList(depth)        

    if result == []:
        tree = None
    
    return jsonify({"chain": result, "qtdNodes": tree.nNodes})

@app.route("/getChainByDepth")
def getChainByDepth():
    """
        Retorna a cadeia gerada pela árvore de cadeias limitada por profundidade.

        Retorno JSON:

            "chain": list  # Lista de cadeias geradas
    """
    global tree

    result = tree.get_limited_chainList(tree.depth)
    if result == []:
        tree = None
    
    return jsonify({"chain": result})

# Roda o servidor
if __name__ == '__main__':
    app.run(debug=True, port=5001)
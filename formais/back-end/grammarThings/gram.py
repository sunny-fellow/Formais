from enum import Enum
from .dataStructures.tree import GramTree


class Key(Enum):
    variaveis = 1
    inicial = 2
    terminais = 3
    producoes = 4

class Grammar:

    def __init__(self):
        """
        Apos instanciar a gramatica, eh necessario escolher a forma de criacao dela.
        Dadas as possibilidades, escolha entre:

        GRAMATICA INTEIRA

            - archive_to_grammar(path: str) 
                limpa a gramatica 
                recebe o caminho do arquivo que contem a gramatica e reescreve esta gramatica
            - str_to_grammar(info:str)
                limpa a gramatica
                recebe a string que contem a gramatica e reescreve esta gramatica
            - dict_to_grammar(gram:dict)
                limpa a gramatica
                recebe um dicionario no modelo gramatica e reescreve esta gramatica
            
                
            ADICIONANDO PARTE POR PARTE:

            - add_to_grammar(value:str|list, key:str = None)
                * Recebe uma Key que deve ter um dentre os valores que se quer adicionar:
                    + key: [variaveis = 1, inicial = 2, terminais = 3, producoes = 4] onde, caso nao receba a key, 
                    por padrao adiciona nas producoes
                * E recebe um valor que, dependendo da chave, pode assumir tipos diferentes
                    + value:
                        - variaveis: str | list[str]
                        - terminais: str | list[str]
                        - producoes | None: dict {variavel: producao} 
        """

        # simbolos terminais e nao terminais
        self.nonTermSymbols:list = [] # array de simbolos nao-terminais (strings)
        self.termSymbols:list = []    # array de simbolos terminais (strings)
        self.initial:str = ""        # string que contem um simbolo nao-terminal que inicia a gramatica
        self.productions:dict = {}    # dicionario de producoes, onde a chave eh a variavel (nao-terminal) e o valor eh(sao) a(as) producao(oes)
        self.E = "epsilon"       # constante que indica o fim de producoes

        # para o auxilio na parte de geracao de cadeias, serao necessarias as 
        # listas de variaveis armadilhas e nao-armadilhas para evitar gerar 
        # cadeias derivando das variaveis aramdilha
        self.traps:list = []
        self.notTraps:list = []

        return

#####################################################################

    # adicionar partes individuais da gramatica 
    def add_to_grammar(self, value:str|list|dict, key:Key = None):

        """
            - add_to_grammar(value:str | list | dict, key:str = None)
                * Recebe uma Key que deve ter um dentre os valores que se quer adicionar:
                    + key: [variaveis = 1, inicial = 2, terminais = 3, producoes = 4] onde, caso nao receba a key, 
                    por padrao adiciona nas producoes

                * E recebe um valor que, dependendo da chave, pode assumir tipos diferentes
                    + value:
                        - variaveis: str | list[str]
                        - terminais: str | list[str]
                        - producoes | None: dict {variavel: producao} 

            
            - Retorno:
            
        """

        if key == Key.variaveis:
            if type(value) == list:
                    for val in value:
                        self.nonTermSymbols.append(val.removesuffix('\n'))
            else:
                self.nonTermSymbols.append(value)

        elif key == Key.inicial:
            if type(value) == str:
                self.initial = value
            else:
                self.initial = str(value)

        elif key == Key.terminais:
            if type(value) == list:
                    for val in value:
                        self.termSymbols.append(val.removesuffix('\n'))
            else:
                self.termSymbols.append(value)
        
        elif key == Key.producoes or key == None:
            if type(value) == dict:
                    for val in value.keys():
                        for prod in value.get(val):
                            self.productions.setdefault(val, []).append(prod)
            elif type(value) == list:
                for val in value:
                    self.productions.setdefault(self.initial, []).append(val)
            else:
                self.productions.setdefault(self.initial, []).append(value)
        else:
            return jsonify({"Error": "Invalid Key"})

        return self.check_grammar()

#####################################################################

    # recebe o caminho de um arquivo e converte-o a gramatica
    def archive_to_grammar(self, path:str):
        """
            Preenche as variaveis da classe Grammar com os valores lidos no arquivo cujo caminho eh passado como parametro

            retorno: dict da funcao check_grammar() para a gramatica inserida
            
        """
        #garante que as variaveis estarao vazias
        self.clean_grammar()

        file = open(path, 'r')
        if not file:
            print("Nao foi possivel abrir o arquivo da gramatica!\n")
            return

        # preenchendo os nao-terminais
        line = file.readline()
        nonTerminalS = line.split(":")[1].split(",")
        for symbol in nonTerminalS:
            #retirando a quebra de linha (se existir)
            symbol = symbol.removesuffix("\n")
            self.nonTermSymbols.append(symbol)
        
        # preechendo o inicial
        line = file.readline()
        self.initial = line.split(":")[1].removesuffix("\n") # removendo, ao mesmo tempo, a quebra de linha

        # preenchendo os terminais
        line = file.readline()
        terminalS = line.split(":")[1].split(",")
        for symbol in terminalS:
            #retirando a quebra de linha (se existir)
            symbol = symbol.removesuffix("\n")
            self.termSymbols.append(symbol)
        
        # preenchendo as producoes
        line = file.readline()  # pula a string "producoes"
        line = file.readline()
        while line:
            production = line.split(": ")
            # retirando a quebra de linha
            production[1] = production[1].removesuffix("\n")
            self.productions.setdefault(production[0], []).append(production[1])
    
            line = file.readline()

        return self.check_grammar()

#####################################################################

    def check_grammar(self) -> dict:
        """
            Responsavel por verificar se a gramatica eh valida.
            Algumas verificacoes a serem feitas:

                a. simbolo inicial esta contido na lista de nao-terminais
                b. verifica se todas as variaveis tem apenas 1 simbolo
                c. verifica as producoes e guarda quais sao armadilha, se houver armadilhas
                d. verifica se alguma producao nao eh armadilha. Se todas forem, o conjunto de cadeias geradas pela gramatica eh vazio 

            - Retorno:

            {

                dict

                "valid": bool,        # indica se a gramatica eh valida ou nao

                "message": str,       # mensagem indicando o erro, caso a gramatica nao seja valida

                "allTrap": bool      # indica se todas as producoes da gramatica sao armadilhas
            }
        """

        if not self.initial in self.nonTermSymbols:
            return {"valid": False, "message": "Simbolo inicial nao esta contido nas variaveis informadas", "allTrap": False}
        
        # no caso do nivel 2 da hierarquia de chompski, as variaveis devem conter apenas um simbolo ser derivado
        for var in self.nonTermSymbols:
            if len(var) > 1:
                return {"valid": False, "message": f"A variavel {var} tem mais do que um simbolo", "allTrap": False}
            elif len(var) < 1:
                return {"valid": False, "message": f"A variavel {var} tem menos do que um simbolo", "allTrap": False}

        if len(self.productions.keys()) == 0:
            return {"valid": False, "message": f"A gramática não possui nenhuma produção", "allTrap": False}

        # acessa a classe tree e recebe guarda um dicionario com a lista das variaveis armadilha e nao armadilha
        # {
        #     "traps" : ['A', 'C'],
        #     "notTraps": ['S', 'B']
        # }
        t = GramTree(self.initial, self.productions.get(self.initial))
        verification = t.check_variables(self.productions, self.nonTermSymbols)

        # atualiza esses valores na gramatica
        self.traps = (verification.get("traps"))
        self.notTraps = (verification.get("notTrap"))

       
        
        if self.initial in self.traps:
            # a gramatica eh valida, mas nao gera nenhuma cadeia
            return {"valid": True, "message": "Variavel inicial eh armadilha. Logo, esta gramatica nao gera cadeia nenhuma", "allTrap": True}

        # caso todos os casos acima nao ocorram, a gramatica eh valida
        return {"valid": True, "message": "Gramatica valida!", "allTrap": False}

#####################################################################

    def clean_grammar(self):
        """
            Reseta os valores de todas as variaveis da gramatica
        """
        self.nonTermSymbols = []   
        self.termSymbols = []       
        self.initial = ""               
        self.productions.clear()     

        self.traps = []
        self.notTraps = []

        return
    
#####################################################################

    def dict_to_grammar(self, gram:dict):
        """
            Preenche as variaveis da classe Grammar com os valores recebinos no dicionario gram

            retorno: dict da funcao check_grammar() para a gramatica inserida
            
        """

        self.clean_grammar()

        self.nonTermSymbols = gram["variaveis"]
        self.initial = gram.get("inicial")
        self.termSymbols = gram.get("terminais")
        self.productions = gram.get("producoes")

        # adicionar parte de checar armadilhas

        return self.check_grammar()

#####################################################################

    def grammar_to_dict(self, grammar = None):
        """
            Recebe como parametro uma Grammar e retorna um dicionario dos valores 
            dessa gramatica organizados por chave.
        """

        if grammar == None:
            grammar = self

        gram = {}           # dicionario que armazenarah as informacoes da gramatica

        # definindo as variaveis da gramatica
        for var in grammar.nonTermSymbols:
            gram.setdefault("variaveis", []).append(var)
        # definindo o nao-terminal inicial da gramatica   
        gram.setdefault("inicial", grammar.initial)   

        # definindo os terminais da gramatica
        for termn in grammar.termSymbols:
            gram.setdefault("terminais", []).append(termn)
        
        # definindo as producoes da gramatica
        gram.setdefault("producoes", grammar.productions)

        return gram

#####################################################################

    def grammar_to_str(self, gram = None) -> str:
        """
            Recebe como parametro uma Grammar e retorna uma str formatada de forma
            organizada, simulando a representacao de uma gramatica no papel.
        """

        if gram == None:
            gram = self.grammar_to_dict()   # dicionario com as informações da gramtica
        else: 
            gram = self.grammar_to_dict(gram)

        ARROW = "\u2192"                # seta no padrao unicode para facilitar a exibicao das transicoes
        gram_str = ""

        for var in gram.get("variaveis"):
            line = f"{var}  {ARROW}  "

            if type(gram.get("producoes").get(var)) == list:
                for prod in gram.get("producoes").get(var):
                    line += f"{prod} | "
            else:
                line += gram.get("producoes").get(var)

            if var == gram.get("initial"):
                gram_str = line.removesuffix(" | ") + "\n" + gram_str
            else:
                gram_str += line.removesuffix(" | ") + '\n'
        
        return gram_str

#####################################################################

    def str_to_grammar(self, content:str):
        """ 
            Espera-se uma string content do tipo:

                variaveis:S,A,B             # linha 0
                inicial:S                   # linha 1
                terminais:a,b,c,d           # linha 2
                (linha vazia opcional)      # linha (3)
                producoes                   # linha 3(4)
                S: aA                       # linha 4(5)
                S: bB                       # ...
                A: epsilon
                B: cS
                B: dS

            Preenche as variaveis da classe Grammar com os valores da string passada como parametro

            retorno: dict da funcao check_grammar() para a gramatica inserida
   
        """

        #garante que as variaveis estarao vazias
        self.clean_grammar()

        values = content.split('\n')
        
        # salva em vars os nao-terminais que foram digitados apos o ':' da primeira linha
        variables = values[0].split(":")[1].split(",") 
        for var in variables:
            #retira o '\n' do fim da string, se houver, e insere na lista de variaveis
            self.nonTermSymbols.append(var.removesuffix('\n'))
        
        # define initial como o nao-terminal escrito apos o ':' da segunda linha
        self.initial = values[1].split(":").removesuffix('\n') # removendo uma possivel quebra de linha

        # salva em vars os terminais que foram digitados apos o ':' da terceira linha
        variables = values[2].split(":")[1].split(",") 
        for var in variables:
            #retira o '\n' do fim da string, se houver, e insere na lista de variaveis
            self.termSymbols.append(var.removesuffix('\n'))

        i = 4
        # caso haja uma linha em braco na string
        if values[i-1] == "":
            i = 5
        # adiciona a chave ao dicionario se nao existir e, caso exista, atualiza seus valores
        for i in range(i, len(values)):
            prod = values[i].split(": ")
            # se a chave da producao ja existir:
                # Adiciona um novo valor (sem quebra de linha so final) a lista dessa chave
            # se nao
                # Adiciona a nova chave ao dicionario e o novo valor
            self.productions.setdefault(prod[0], []).append(prod[1].removesuffix('\n'))

        return self.check_grammar()

#####################################################################

    def setFastMode(self):
        self.mode = "fast"
        return
    
#####################################################################

    def setDetailedMode(self):
        self.mode = "detailed"
        return

#####################################################################

    def show_grammar(self):

        """
            Printa a gramatica no estilo de arquivo no terminal
        """

        print("Gramatica: \n")

        # mostrando os simbolos nao-terminais
        line = ""
        for symbol in self.nonTermSymbols:
            line += symbol
            line += ","
        line = line.removesuffix(",")
        print(f"variaveis: {line}")

        # mostrando o simbolo inicial
        print(f"inicial: {self.initial}")

        # mostrando os simbolos terminais
        line = ""
        for symbol in self.termSymbols:
            line += symbol
            line += ","
        line = line.removesuffix(",")
        print(f"terminais: {line}")
        print()

        # mostrando as producoes
        print("producoes:")
        for var in self.productions.keys():
            print(f"{var}  ->  {self.productions[var]}")

        return

g = Grammar()
# g.add_to_grammar(['S', 'A'], Key.variaveis)
# g.add_to_grammar('S', Key.inicial) # sobrescreve qualquer inicial que ja exista, se existir
# g.add_to_grammar(['a'], Key.terminais)
# g.add_to_grammar({ "S" : ['aA', "epsilon"] , "A": ["a", "epsilon"]}) # se nao passar nenhuma key, ele considera como producao
# g.add_to_grammar(['a', 'aa']) # ao passar apenas uma lista sem sua chave, ele adiciona todos os valores aas producoes do inicial
# print(g.grammar_to_str())

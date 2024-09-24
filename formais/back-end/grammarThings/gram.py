class Grammar:

    def __init__(self, path):
        self.gramPath = path     # caminho do arquivo que contém a gramática

        # símbolos terminais e não terminais
        self.nonTermSymbols = [] # array de símbolos não-terminais (strings)
        self.termSymbols = []    # array de símbolos terminais (strings)
        self.initial = ""        # string que contém um símbolo não-terminal que inicia a gramática
        self.E = "epsilon"       # constante que indica o fim de produções

        self.productions = []    # matriz de produções, onde o indice (primeira coluna) é o não-terminal e a segunda coluna é 
                                # a string gerada, contendo um terminal e/ou um não terminal

        # preencher a gramática
        self.fill_grammar()

        # checar gramática
        validation = self.check_grammar()
        if not validation[0]:
            print(validation[1])
            # mandar o objeto erro
            # ...
            return
        
        return

    """
        Responsável por verificar se a gramática é válida (Retorna True se for válida, False caso contrário).
        Algumas verificações a serem feitas:
            a. símbolo inicial está contido na lista de não-terminais
            b. existe alguma produção que resulte em epsilon ou símbolo terminal para que a gramática não seja um loop infinito
            c. todos as produções podem ser criadas, ou seja, há produções que resultem nessa segunda produção (não ter produções soltas do resto)
    """
    def check_grammar(self) -> tuple:
        if not self.initial in self.nonTermSymbols:
            return (False, "Simbolo inicial nao esta contido nas variaveis informadas")
        
        # como productions é:
        # [ 
        #     ["S", "aA"],
        #     ["A", "epsilon"]
        # ]
        
        hasTerminalSymb = False
        #verificar se há terminais nas produções
        for production in self.productions:
            # se encontrar um 'epsilon', então é possível terminar  uma cadeia de caracteres
            if production[1] == self.E:
                hasTerminalSymb = True
                break
            
            # se encontrar um único/apenas símbolo terminal na produção, então é possível ter cadeia val (11)
            for elem in production[1]:
                # se encontrar algum símbolo não-terminal
                if not elem in self.termSymbols:
                    hasTerminalSymb = False
                    break
            



        if not hasTerminalSymb:
            return (False, "Nao ha ponto de parada na gramatica")



        return (True, "Gramatica valida!")

    """
        Preenche as variaveis da classe Grammar com os valores lidos no arquivo passado como parâmetro do construtor
    """
    def fill_grammar(self):
        file = open(self.gramPath, 'r')
        if not file:
            print("Não foi possível abrir o arquivo da gramática!\n");
            return 

        # preenchendo os não-terminais
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
        
        # preenchendo as produções
        line = file.readline()  # pula a string "producoes"
        line = file.readline()
        while line:
            production = line.split(": ")
            # retirando a quebra de linha
            production[1] = production[1].removesuffix("\n")
            self.productions.append(production)
    
            line = file.readline()
        return
        

    def show_grammar(self):
        print("Gramática: \n")

        # mostrando os símbolos não-terminais
        line = ""
        for symbol in self.nonTermSymbols:
            line += symbol
            line += ", "
        line = line.removesuffix(", ")
        print(f"Símbolos não-terminais: {line}")

        # mostrando o símbolo inicial
        print(f"Símbolo inicial: {self.initial}")

        # mostrando os símbolos terminais
        line = ""
        for symbol in self.termSymbols:
            line += symbol
            line += ", "
        line = line.removesuffix(", ")
        print(f"Símbolos terminais: {line}")
        print()

        # mostrando as produções
        print("Produções:")
        for production in self.productions:
            print(f"{production[0]}  ->  {production[1]}")
            # print(f"{production}")
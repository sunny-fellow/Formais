from grammarThings.gram import Grammar
from queue import Queue
"""
    gram : {
        S : ['aA', 'bB', 'epsilon'],
        A : ['S', 'epsilon'],
        B : ['bB', 'S']
        }

    {
        data: S,
        gram: gram,
        children:
        [
            data: aS
            gram: gram
        ]
    }
"""
# infixo


class Tree:
    def __init__(self, data:str, gram:Grammar, depth:int):
        self.data = data                    # guardar a info do no
        self.gram = gram                    # gramatica para basear as informacoes
        self.depth = depth
        self.children:list[Tree] = []       # lista de filhos do no (subcadeias produzidas)
        self.var_check = self.checkVar_fromProd(self.data) 
        if self.var_check["hasVar"] and depth > 0:       # se tiver subcadeias e a altura nao tiver sido reduzida a 0 ainda
            self.fillChildren()             # preenche os filhos com as subcadeias geradas pelas producoes do campo data
            

    def fillChildren(self):
        # var_check guarda informacoes sobre a producao atual, tais como:
            # bool: tem variavel
            # bool: eh armadilha
            # str: variavel contida na cadeia

        # se nao tiver variavel ou caso a variavel que existir for armadilha 
        if self.var_check["isTrap"]:
            return

        # para cada producao da variavel checada
        for prod in self.gram.productions[self.var_check["variable"]]:
            # substitui (1 unica vez) na cadeia dessa arvore o valor da producao da variavel e salva esse retorno 
            if prod == "epsilon":
                nextChain = self.data.replace(self.var_check["variable"], "", 1)
            else:
                nextChain = self.data.replace(self.var_check["variable"], prod, 1)
            # adiciona na lista dos filhos dessa arvore uma arvore com cada subcadeia gerada pelas producoes
            # informa a gramatica, altura-1, se eh armadilha e se tem filhos (se tem uma variavel contida)
            self.children.append(Tree(nextChain, self.gram, self.depth - 1))


    def checkVar_fromProd(self, prod:str) -> dict:
        # para cada caractere na producao
        for c in prod:
            # se esse caracter estiver contido nas variaveis
            if c in self.gram.nonTermSymbols:
                # e estiver contido na lista das armadilhas
                if c in self.gram.traps:
                    # retorna os valores indicando que tem variavel, que eh armadilha e a variavel em si
                    return {"hasVar": True, "isTrap": True, "variable": c}
                # se nao estiver contido na lista das armadilhas
                else:
                    # retorna os mesmos valores acima, com excessao do booleano que indica se eh armadilha
                    return {"hasVar": True, "isTrap": False, "variable": c}
        
        # caso nao encontre uma variavel, entao todos os campos retornam "vazios"
        return {"hasVar": False, "isTrap": False, "variable": ""}
    

    # S: A , B 
    # A: epsilon
    # B: b, epsilon
    # prof1: [["S", "A"], ["S", "B"]]
    # prof2: [["S", "A", "epsilon"], ["S", "B", "b"], ["S", "B", "epsilon"]]

    
    # Versao Lael
    # OBS: NAO TA FUNCIONANDO COMO ALI NO EXEMPLO ACIMA
    def getChainList(self) -> list:
        chainList = []
        for child in self.children:
            if not child.children:
                continue
            childChains = child.getChainList()
            for chain in childChains:
                chainList.append(chain.insert(0, self.data))

        return chainList
    
    """
        Depois vou precisar que tenha uma funcao que transforme essas filas em suas progressoes de substituicao
        Exemplo:

        S -> aA | epsilon
        A -> bB | c
        B -> epsilon

        Seja a fila de producoes:
            ["S", "aA", "bB", "epsilon"]
        Retorne:
            ["S", "aA", "abB", "ab"]

        Seja a fila de producoes:
            ["S", "aA", "c"]
        Retorne:
            ["S", "aA", "ac"]
    
    """
from ...grammarThings.gram import Grammar
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
    def __init__(self, data:str, gram:Grammar, depth:int, isTrap = None, hasChildren:bool = None):
        self.data = data                    # guardar a info do no
        self.gram = gram                    # gramatica para basear as informacoes
        self.children:list[Tree] = []       # lista de filhos do no (subcadeias produzidas)
        self.isTrap = isTrap                # valor para dizer se tal no eh armadilha
        if hasChildren and depth > 0:       # se tiver subcadeias e a altura nao tiver sido reduzida a 0 ainda
            self.fillChildren()             # preenche os filhos com as subcadeias geradas pelas producoes do campo data
            

    def fillChildren(self):
        # guarda informacoes sobre a producao atual, tais como:
            # bool: tem variavel
            # bool: eh armadilha
            # str: variavel contida na cadeia
        var_check = self.checkVar_fromProd(self.data) 

        # se nao tiver variavel ou caso a variavel que existir for armadilha 
        if not var_check["hasVar"] or var_check["isTrap"]:
            
            return

        # para cada producao da variavel checada
        for prod in self.gram.productions[var_check["variable"]]:
            # substitui (1 unica vez) na cadeia dessa arvore o valor da producao da variavel e salva esse retorno 
            nextChain = self.data.replace(var_check["variable"], prod, 1)
            # adiciona na lista dos filhos dessa arvore uma arvore com cada subcadeia gerada pelas producoes
            # informa a gramatica, altura-1, se eh armadilha e se tem filhos (se tem uma variavel contida)
            self.children.append(Tree(nextChain, self.gram, self.depth - 1, var_check["isTrap"], var_check["hasVar"]))


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
    

    def getChainQueue(self) -> list:
        chainList = Queue()
        for child in self.children:
            chainList.push([self.data, child.getChainQueue()])
        
        return chainList

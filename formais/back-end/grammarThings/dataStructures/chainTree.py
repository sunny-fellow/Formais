from grammarThings.gram import Grammar
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
        self.data = data                                            # guardar a info do no
        self.gram = gram                                            # gramatica para basear as informacoes
        self.depth = depth                                          # Guarda o nivel do no em relacao a raiz
        self.children:list[Tree] = []                               # lista de filhos do no (subcadeias produzidas)
        self.var_check = self.checkVar_fromProd(self.data)          # Checa se a cadeia contem variaveis e se eh armadilha
        if self.var_check["hasVar"] and depth > 0:                  # se tiver subcadeias e a altura nao tiver sido reduzida a 0 ainda
            self.fillChildren()                                     # preenche os filhos com as subcadeias geradas pelas producoes do campo data
            

    def fillChildren(self):        

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
        """
            #### checkVar_fromProd verifica a producao atual, a fim de chegar a um diagnóstico sobre a producao dada:
            
                retorno:

                {

                    dict

                    "hasVar": bool  #  tem variavel

                    "isTrap": bool  #  eh armadilha

                    "variable": str #  variavel contida na cadeia

                }
        """
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

    def getChainList(self) -> list:
        """
            Retorna uma lista com todas as sequencias de producoes possiveis a partir do no inicial

            Parâmetros:
            
                self (Tree)                  # No inicial
            
            Retorno:

                result (list)                 # lista das cadeias desejadas
        """
        result = []

    # se o no nao possuir filhos, ele apenas retorna seu proprio valor 
        if not self.children:
            return [self.data]
        
    # se o no possuir apenas um filho, ele retorna uma lista com sua propria cadeia seguida pela de seu filho   
        elif len(self.children) == 1:
            return [self.data] + [self.children[0].data]
        
    # havendo multiplos filhos, a lista completa dos mesmos sera percorrida    
        else:
            for child in self.children:
                # recebe a lista equivalente do filho
                temp = child.getChainList()
                # print("Temp: " + str(temp))

                # Se for uma lista de listas, percorre-a
                # o que ocorreria dado que o no filho atual tenha multiplos filhos
                if type(temp[0]) == list:
                    for t in temp:
                        appd = [self.data]
                        appd.extend(t)
                        result.append(appd)
                    
                # Se for uma lista de strings, apenas adiciona o valor
                # pois sabe-se que possui apenas um elemento (a cadeia do filho)
                else:
                    appd = [self.data]
                    appd.extend(temp)
                    result.append(appd)
            return result
    
    
    def get_limited_chainList(self, n):
        """
            Retorna uma lista com todas as sequencias de producoes possiveis a partir do no inicial,
            no nível da profundidade limitada

            Parâmetros:
            
                self (Tree)                  # No inicial
                n    (int)                   # Profundidade (limite da busca)
            
            Retorno:

                result (list)                 # lista das cadeias desejadas
        """

        result = []

        # percorre os filhos do no, apenas retornando diretamente a lista de producoes
        # no caso em que a profundidade desejada seja 1
        # se nao, a funcao eh chamada recursivamente para cada filho
        for child in self.children:
            if n > 1:
                if child.var_check["hasVar"] and not child.var_check["isTrap"]:
                    temp = child.get_limited_chainList(n-1)

                    # Se for uma lista de listas, percorre-a
                    if temp and type(temp[0]) == list:
                        # Se a lista de producoes for muito grande, retorna o que tem
                        if len(result) > 150000:
                            return result
                        for t in temp:
                            appd = [self.data]
                            appd.extend(t)
                            result.append(appd)
                        
                    # Se for uma lista de strings, apenas adiciona o valor
                    elif temp:
                        appd = [self.data]
                        appd.extend(temp)
                        result.append(appd)
                
            elif not child.var_check["hasVar"]:
                temp = [child.data]
                appd = [self.data]
                appd.extend(temp)
                result.append(appd)

        return result
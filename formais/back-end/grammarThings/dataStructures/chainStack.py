from grammarThings.gram import Grammar

class ChainStack:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.alreadySent = []
        self.canContinue = False
    
    def get_chainStack(self, n: int, prod: str):
        """
            Retorna uma lista (pilha) com uma producao de profundidade n,
            verificando se esta producao ja nao foi enviada anteriormente

            Parâmetros:

                n: int          # Profundidade da producao
                prod: str       # Producao a ser verificada
            
            Retorno:
                
                list            # Lista com a producao de profundidade n
            
            Exemplo:
                
                Seja a gramatica:
                    S -> aS | A | a
                    A -> b

                E a chamada:
                    get_chainStack(2, 'S')
                    Resultado: ['S', 'aS', 'aa']        # Caso seja a primeira chamada desse objeto
                    Resultado: ['S', 'A', 'b']          # Segunda chamada
                    Nao ha mais producoes possiveis para a profundidade 2, 
                    considerando que a profundidade dita quantas derivacoes serao feitas a partir do no inicial
        """

        # Guardara o resultado da iteracao da funcao
        result = []

        # Encontra qual variavel deve ser derivada
        var_to_derivate = ''
        for char in prod:
            if char in self.grammar.nonTermSymbols:
                var_to_derivate = char
                break
        
       
        # Encontra as producoes que derivam a variavel
        children = []
        for option in self.grammar.productions[var_to_derivate]:
            if option not in self.alreadySent and option not in self.grammar.traps:
                if option != self.grammar.E:
                    children.append(prod.replace(var_to_derivate, option, 1))
                else:
                    children.append(prod.replace(var_to_derivate, "", 1))

        for child in children:
            # Se a profundidade for maior que 1, chama a funcao recursivamente
            if n > 1:
                # Captura apenas as producoes que contem variaveis nao-armadilhas, pois queremos apenas da profundidade n
                if self.hasVar(child) and child not in self.grammar.traps:
                    temp = self.get_chainStack(n-1, child)
                    if temp == []:
                        continue

                    # Se houve producoes uteis, adiciona o caminho conforme as interacoes na pilha, e retorna
                    appd = [prod]
                    appd.extend(temp)
                    return appd
            
            # Se a profundidade for 1, captura apenas as producoes que nao possuem variaveis
            elif not self.hasVar(child):
                temp = [child]

                # Se a producao ja foi enviada, ignora
                if temp in self.alreadySent:
                    continue

                # Caso contrario, adiciona a producao na lista de producoes ja enviadas e a retorna
                self.alreadySent.append(temp)
                appd = [prod]
                appd.extend(temp)
                return appd
            
            # Se a profundidade for 1 e existirem producoes com variaveis, significa que a proxima profundidade ainda pode gerar producoes possiveis
            else:
                self.canContinue = True
    
        return []

    def hasVar(self, prod: str):
        """
            Verifica se a producao possui alguma variavel

            Parâmetros:

                prod: str       # Producao a ser verificada
            
            Retorno:

                bool            # True se a producao possui variaveis, False caso contrario
        """

        for char in prod:
            if char in self.grammar.nonTermSymbols:
                return True
        
        return False
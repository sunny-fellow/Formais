class Node:
    
    def __init__(self, data=None, children=None):
        self.data = data
        self.node_Children = []
        if children is not None:
            for child in children:
                self.node_Children.append(Node(child))

    
class GramTree:    
    checked_vars = []

    def __init__(self, initial:str = None, children:list = None):
        if initial != None and children != None:
            self.root = Node(initial, children)
        else:
            self.root = None

    #printar a arvore
    def print_tree(self):
        if self.root != None:
            self.print_tree_aux(self.root)   
        else:
            print("Arvore vazia") 
    def print_tree_aux(self, root:Node):
        print(f"{root.data} ")
        for child in  root.node_Children:
            self.print_tree_aux(child)



    # checar quais variaveis podem chegar a algum ponto final
    def check_variables(self, productions:dict, variables:list) -> dict:
        self.traps = []
        self.notTraps = []

        for var in productions.keys():
            # limpa as variaveis checadas
            self.checked_vars.clear()
            # se a variavel nao for armadilha
            if self.check_tree(var, productions):
                self.notTraps.append(var)
            # se for armadilha
            else:
                self.traps.append(var)

        for var in variables:
            if var not in productions.keys():
                # limpa as variaveis checadas
                self.checked_vars.clear()
                # se a variavel nao for armadilha
                if self.check_tree(var, productions):
                    self.notTraps.append(var)
                # se for armadilha
                else:
                    self.traps.append(var)

        # retorna um dicionario para previnir o acesso a armadilha na geracao de cadeias futuras
        return {"traps": self.traps, "notTraps": self.notTraps}


    def check_tree(self, initial:str,  productions:dict) -> bool:
        # se a variavel nao foi checada, agora sera
        if initial not in self.checked_vars:
            # se a variavel esta na lista de variaveis que nao sao armadinha, retorna true
            if initial in self.notTraps:
                return True
            # se a variavel esta nas lista das variaveis armadilha, retorna False
            elif initial in self.traps:
                return False

            # adiciona a variavel na lista de variaveis checadas, para evitar loop
            self.checked_vars.append(initial)

            # se nenhuma producao derivar dessa variavel, ela eh armadilha
            if not initial in productions.keys():
                return False

            # Verifica se ha transicao sem variaveis, ou seja, terminal
            for prod in productions.get(initial):
    
                hasTerminal = True
                # para cada chave (variavel) na lista de chaves do dicionario (variaveis)
                for var in productions.keys():
                    # se houver uma variavel na producao
                    if var in prod:
                        hasTerminal = False
                        break

                # se houver pelo menos uma producao terminal, a variavel nao e armadilha
                if hasTerminal:
                    return True
                
                
            # Verifica se as producoes, todas nao terminais, tem fim
            for prod in productions.get(initial):
                
                # para cada simbolo da producao
                for i in range(len(prod)): 

                    # se o simbolo esta na lista das variaveis que nao sao armadilha e for o ultimo simbolo, retorna True
                    if prod[i] in self.notTraps and i == (len(prod)-1):
                        return True
                    
                    # se o simbolo esta na lista das variaveis armadilha, toda a producao e armadilha. Retorna False
                    elif prod[i] in self.traps:
                        return False
        
                    isTerminal = True

                    # se o simbolo nao e variavel, pula a verificacao
                    if not prod[i] in productions.keys():
                        continue
                     
                    
                    # para cada chave (variavel) entre as chaves do dicionario (variaveis)
                    for var in productions.keys():
                        # se for a mesma variavel que a funcao esta verificando, a producao nao e terminal, pula a verificacao
                        if var == initial:
                            isTerminal = False
                            continue
                        
                        # se a variavel for igual ao simbolo da producao
                        if var == prod[i]:
                            # a producao nao e terminal
                            isTerminal = False
                            # checa se o simbolo nao e armadilha
                            if self.check_tree(var, productions):
                                # se nao for armadilha e se for o ultimo da producao, retorna True
                                if i == len(prod)-1:
                                    return True
                                # se nao for o ultimo, checa o proximo
                                else:
                                    continue
                            # se for armadilha, sai do for, com o conferidor isTerminal com valor False
                            else:
                                break        

                    # se encontrar uma variavel na producao e ela for armadilha
                    if isTerminal:
                        return True
                    else:
                        break

            # se chegar aqui, percorreu tudo e nao encontrou um fim    
            return False
        
                    
            

        
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################



# tree = Tree("S", {"S": ["aA", "bB"]})
# tree = GramTree()
# tree.print_tree()
# print("\n------------------------------------\n")
# print(tree.check_variables({"S": ["aA", "bB", "cC"],
#                             "A": ["epsilon"],
#                             "B": ["DA", "CB", "B", "AB", "ABA"],
#                             "C": ["DC", "AB"],
#                             "D" :["D", "C"]}))
# print("\n------------------------------------\n")

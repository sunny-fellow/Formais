class Node:
    
    def __init__(self, data=None, children=None):
        self.data = data
        self.node_Children = []
        if children is not None:
            for child in children:
                self.node_Children.append(Node(child))

            
    
class Tree:    
    checked_vars = []


    def __init__(self, key:str = None, children:dict = None):
        if key != None and children != None:
            self.root = Node(key, children[key])
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
    def check_variables(self, productions:dict) -> dict:
        self.traps = []
        self.notTraps = []

        for var in productions.keys():
            # limpa as variáveis checadas
            self.checked_vars.clear()
            # se a variável não for armadilha
            if self.check_tree(var, productions):
                self.notTraps.append(var)
            # se for armadilha
            else:
                self.traps.append(var)

        # retorna um dicionário para previnir o acesso a armadilha na geração de cadeias futuras
        return {"traps": self.traps, "notTraps": self.notTraps}


    def check_tree(self, initial:str,  productions:dict) -> bool:
        # se a variavel nao foi checada, agora será
        if initial not in self.checked_vars:
            # se a variável está na lista de variáveis que não são armadinha, retorna true
            if initial in self.notTraps:
                return True
            # se a variável está nas lista das variáveis armadilha, retorna False
            elif initial in self.traps:
                return False

            # adiciona a variável na lista de variáveis checadas, para evitar loop
            self.checked_vars.append(initial)

            # Verifica se há transição sem variáveis, ou seja, terminal
            for prod in productions.get(initial):
    
                hasTerminal = True
                # para cada chave (variável) na lista de chaves do dicionário (variáveis)
                for var in productions.keys():
                    # se houver uma variável na produção
                    if var in prod:
                        hasTerminal = False
                        break

                # se houver pelo menos uma produção terminal, a variável não é armadilha
                if hasTerminal:
                    return True
                
                
            # Verifica se as produções, todas não terminais, têm fim
            for prod in productions.get(initial):
                
                # para cada símbolo da produção
                for i in range(len(prod)): 

                    # se o símbolo está na lista das variáveis que não são armadilha e for o último símbolo, retorna True
                    if prod[i] in self.notTraps and i == (len(prod)-1):
                        return True
                    
                    # se o símbolo está na lista das variáveis armadilha, toda a produção é armadilha. Retorna False
                    elif prod[i] in self.traps:
                        return False
        
                    isTerminal = True

                    # se o símbolo não é variável, pula a verificação
                    if not prod[i] in productions.keys():
                        continue
                     
                    
                    # para cada chave (variável) entre as chaves do dicionário (variáveis)
                    for var in productions.keys():
                        # se for a mesma variável que a função está verificando, a produção não é terminal, pula a verificação
                        if var == initial:
                            isTerminal = False
                            continue
                        
                        # se a variável for igual ao símbolo da produção
                        if var == prod[i]:
                            # a produção não é terminal
                            isTerminal = False
                            # checa se o símbolo não é armadilha
                            if self.check_tree(var, productions):
                                # se não for armadilha e se for o último da produção, retorna True
                                if i == len(prod)-1:
                                    return True
                                # se não for o último, checa o próximo
                                else:
                                    continue
                            # se for armadilha, sai do for, com o conferidor isTerminal com valor False
                            else:
                                break        

                    # se encontrar uma variável na produção e ela for armadilha
                    if isTerminal:
                        return True
                    else:
                        break

            # se chegar aqui, percorreu tudo e não encontrou um fim    
            return False
        
                    
            

        
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################



# tree = Tree("S", {"S": ["aA", "bB"]})
tree = Tree()
tree.print_tree()
print("\n------------------------------------\n")
print(tree.check_variables({"S": ["aA", "bB", "cC"],
                            "A": ["epsilon"],
                            "B": ["DA", "CB", "B", "AB", "ABA"],
                            "C": ["DC", "AB"],
                            "D" :["D", "C"]}))
print("\n------------------------------------\n")

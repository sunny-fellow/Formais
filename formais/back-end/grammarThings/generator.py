from gram import Grammar
from .dataStructures.stack import Stack


"""
Algoritmo para gerar cadeias
    - Necessario: 
        Uma pilha para guardar o caminho, a subcadeia atual e uma gramatica completa

    - Passos:
        1. Derivar a variavel inicial em uma de suas producoes (nao armadilha)
        2. Seguir recursivamente ate o ponto de parada
    - Ponto de parada:
        Uma cadeia que nao contenha nenhuma das variaveis
    
    - O que a pilha deve conter:
        stack.top (node)
            - node:
                + str path (caminho que fez chegar do inicial ate a subcadeia atual)
                + str subChain (cadeia atual)
                + bool isDone (booleano que dira se ja chegou ao ponto final da gramatica)
                + node next ("ponteiro" para o proximo)
"""

"""
    TODAS as funcoes que o front vai solicitar:
    
        - Registrar a gramatica recebida pelo usuario
        
        - Setar o modo, rapido/detalhado
            Quando um novo modo eh setado, deve-se resetar a pilha. Para poupar memoria
            
        - Resetar quais cadeias ja foram geradas
        
        - (Fast) Gerar uma nova cadeia diferente das que ja foram geradas. Deve-se retornar:
            + A cadeia gerada
            + As producoes que geraram a cadeia
            + O novo estado da pilha
            
        - (Detailed) Comecar a gerar uma nova cadeia, deve ser retornado a cada iteracao:
            + A lista de producoes possiveis para a variavel atual 
            + A lista de quais dessas producoes sao armadilhas e nao armadilhas
            + A cadeia atual
            + A pilha atual

        - (Detailed) receber do front qual foi a producao escolhida, assim retornando:
            + A cadeia atual
            + A pilha atual

        DETAILED VAI FICAR COM LUIS (deus me ajude)

        - Como a arvore deve funcionar:
            S: aS | a | b | epsilon
            aS -> aa
            aS -> aaS -> aaa
            aS -> aaS -> aaaS -> aaaa
            aS -> aaS -> aaaS -> aaaaS -> aaaaa
            aS -> aaS -> aaaS -> aaaaS -> aaaaaS -> aaaaaa

            aS -> ab
            aS -> aaS -> aab
            aS -> a
            
            a
            
            b

            {}
"""

class ChainGenerator:
    def __init__(self, g:Grammar):
        self.grammar = g
        self.stack = Stack(g.initial)
        self.prodSeq = [[]]

        return
    
    def fast_generation(self) -> str:

        return
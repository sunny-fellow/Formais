class Node:
    def __init__(self, path:str, chain:str):
        self.path = path
        self.chain = chain
        self.isDone = False
        self.next:Node = None


class Stack:
    def __init__(self, chain:str):
        self.top:Node = None
        self.push(chain, True)
    
    def push(self, chain:str, hasVar:bool):
        """
            Recebe a nova cadeia derivada e um booleano que indica se ha variaveis nessa cadeia
        """
        if self.top.isDone: 
            print("A cadeia já está finalizada!")
            return

        if self.top != None:
            path = self.top.path + ";" + chain
        else:
            path = chain

        # preenche o no
        new = Node(path, chain)
        new.isDone = not hasVar

        #conecta o no na pilha
        new.next = self.top

        # modifica a pilha 
        self.top = new

        return

    def pop(self) -> bool:
        # enquanto houver mais do que 1 cadeia (eh necessario que haja pelo menos a variavel inicial na pilha)
        if self.top.next != None:
            self.top = self.top.next
            return True

        # se houver apenas a inicial na pilha, simplemente nao remove nada da pilha
        return False
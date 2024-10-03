class Node:
    # nos que recebem o valor, o anterior e o proximo, sendo que esses dois ultimos, caso nao passados, valem nulo
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.next = next
        self.prev = prev
    
class Queue:
    # inicio e fim nulos
    def __init__(self):
        self.begin = None
        self.end = None

    def push(self, data):
        # caso esteja vazia, insere no fim, igualando o fim e o inicio a este elemento
        if self.end == None:
            self.begin = self.end = Node(data)

        # se nao estiver vazia, insere no fim, passando o fim da fila como anterior do novo fim e o proximo valendo nulo
        else:
            self.end = Node(data, self.end, None)
    
    def pop(self):
        """
            Retorna o inicio da fila, removendo-o
        """

        # se o inicio e fim forem iguais
        if self.begin == self.end:
            # e iguais a nulo, a fila esta vazia, entao retorna nulo
            if self.begin == None:
                return None
            
            # caso contrario, retorna o unico elemento, fazendo a lista, agora, ficar vazia
            else:
                data = self.begin
                self.begin = self.end = None
                return data
            
        # caso contrario, salva o inicio da fila, o novo inicio passa a ser o 
        # proximo e o anterior do proximo eh igualado a nulo, retornando o 
        # valor guardado anteriormente
        else:
            data = self.begin
            self.begin = self.begin.next
            self.begin.prev = None
            return data
    
    def copy(self):
        aux = self.begin
        q = Queue()
        
        while aux != None:
            q.push(aux.data)
            aux = aux.next
        
        return q
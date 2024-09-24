class Node:
    node_Children = []

    def __init__(self):
        self.data = str()
        self.node_Children = []

    def __init__(self,data:str):
        self.data = data
        self.node_Children = []

    def __init__(self, data, *children):
        self.data = data
        for child in children:
            self.node_Children.append(Node(child))
    
class Tree:
    def __init__(self, initial:str, children:dict):
        self.root = Node(initial, children[initial])

    # def print_tree(self):
    #     print(f"{self.root.data}")
    #     print(" < ")
    #     if self.root.node_Children:
    #         for child in self.root.node_Children:
    #             self.print_tree(child)
    #     print(" > ")
                
    def print_tree(self, root:Node):
        print(f"{root.data}")
        print(" < ")
        if len(root.node_Children) > 0:
            for child in root.node_Children:
                self.print_tree(child)
        print(" > ")

    #####################################

    def print_tree_Luis(self):
        aux = self.root
        self.print_tree_aux(aux)

    def print_tree_aux(self, root:Node):
        print(f"{root.data}")
        if len(root.node_Children) > 0:
            self.print_tree_aux(root.node_Children)

tree = Tree("S", {"S": "1S", 
                  "S": "0S", 
                  "S": "epsilon"})
tree.print_tree(tree.root)
print("\n\n------------------------------------\n\n")
# tree.print_tree_Luis() 
        
                
        



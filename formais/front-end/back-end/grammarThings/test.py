from gram import Grammar
from ED.tree import Tree

g = Grammar("grammar.txt")
t = Tree("S", {"S": ["aA", "bB", "epsilon"]})
t.print_tree(t.root)
t.print_tree_Luis()

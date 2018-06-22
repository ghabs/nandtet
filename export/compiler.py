comparisons = {'not': 'not', 'or': 'or', 'and': 'and',
               '<': 'lt', '>': 'gt', '<=': 'lte', '>=': 'gte', '==': 'eq'}
op = {'+': 'add', '-': 'sub', '*': 'mult', '\\': 'div'}
branching = {'while': "_while", "if": "if"}


class Node:
    """
    Node to demonstrate abstract syntax tree
    """
    def __init__(self, val):
        self.val = val
        self.children = []

    def __str__(self):
        return self.val

def write_code(val):
    "Takes in a string, appends to file"
    "TODO: this should be refactored to batch to make more efficient, but since small files for POC nbd"
    with open('output.txt', 'w+') as o:
        o.writelines(val)
    return
    #TODO: use io.py

def _constants(node):
    return write_code('push constant {}'.format(node.val))
    

class Compiler():

    def tokenize(self, line):
        return line.replace('#', '').replace('(', ' ( ').replace(')', ' ) ').split()

    def _create_tree(self, tokens):
        token = tokens.pop(0)
        if tokens[0] == '(':
            tokens.pop(0)
            tree = Node(token)
            while tokens[0] != ')':
                tree.children.append(self._create_tree(tokens))
            tokens.pop(0)
            return tree
        else:
            return Node(token)

    def _while(self, node):
        """
        while loop requires two children, an eval operator that returns true false and a statement.
        true/false is child[0], statement is child*
        """
        write_code('label while')   
        self._eval_token(node.children[0])
        write_code('if-goto while_end')
        map(lambda x: self._eval_token(x), node.children[1:])
        write_code('goto while')
        return

    def _comp(self, node):
        """
        compariston operator takes in two children, pushes those values to the stack, and then pushes the comparison.
        """
        map(lambda x: self._eval_token(x), node.children)
        return write_code(node.val)


    def _eval_token(self, node):
        """Take in node for AST, output LVM code, call on children, and return"""
        action = node.val
        if action in comparisons:
            write_code(comparisons[action])
        elif action in op:
            write_code(action)
        elif action == 'while':
            self._while(node)
        elif action == 'define':
            self._func(node)
        else:
            write_code(node.val)
    
    def _func(self, node):
        """
        defines func
        First goes left, gets args and sets them as variables in this scope.
        Then calls statement. Then returns.
        """
        num_args = len(node.children[1].children)
        write_code('function {} {}').format(node.children[0].val, num_args)
        for i in range(num_args):
            write_code("push argument {}".format(i))
        #sets variables in scope so future calls can reference args
        for n in node.children[1].children:
            exec(n.val + " = " + n.children[1].val)
        self._eval_token(node.children[2])
        return write_code('return')

    def _call_func(self, node):
        write_code("call {} {}".format(node.val, len(node.children)))
        for n in node.children:
            self._eval_token(n.val)
        return

    def compile(self, lisp):
        tokens = self.tokenize(lisp)
        root = self._create_tree(tokens)
        self._eval_token(root)
        return

if __name__ == "__main__":
    pass
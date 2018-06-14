from copy import deepcopy
import operator
import math

Operators = {
    '+': {'value': operator.add, 'priority': 1},
    '-': {'value': operator.sub, 'priority': 1},
    '*': {'value': operator.mul, 'priority': 2},
    '/': {'value': operator.truediv, 'priority': 2},
    '**': {'value': operator.pow, 'priority': 3},
}

'''
TODO
'''
Functions = {
    'sqrt': {'value': math.sqrt, 'argNum': 1},
    'cos': {'value': math.cos, 'argNum': 1},
    'sin': {'value': math.sin, 'argNum': 1},
    'tan': {'value': math.tan, 'argNum': 1},
    'log': {'value': math.log, 'argNum': 2}
}

Delimiters = [
    ','
]


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.right = right
        self.left = left

    def __add__(self, node):
        return Node(operator.add, self, node)

    def __sub__(self, node):
        return Node(operator.sub, self, node)

    def __mul__(self, node):
        return Node(operator.mul, self, node)

    def __truediv__(self, node):
        return Node(operator.truediv, self, node)

    '''
    TODO
    '''

    def __copy__(self):
        pass

    def __neg__(self):
        return Node(operator.sub, Node('0'), self)

    def __pow__(self, power, modulo=None):
        return Node(operator.pow, self, power)

    def calcTree(self, x):
        if self.right is None and self.left is None:
            if str.isalpha(self.value):
                return x
            return float(self.value)
        elif self.right is None:
            return self.value(self.left.calcTree(x))
        else:
            return self.value(self.left.calcTree(x), self.right.calcTree(x))

    def isContainsVar(self):
        if self.right is None and self.left is None:
            if str.isalpha(self.value):
                return True
            return False
        elif self.right is None:
            return self.left.isContainsVar()
        else:
            return self.left.isContainsVar() or self.right.isContainsVar()


def expression(node: Node):
    expr = ''

    if node.right is None and node.left is None:
        return node.value
    elif node.right is None:
        func_name = ''
        if node.value is math.sqrt:
            func_name = 'sqrt '
        elif node.value is math.cos:
            func_name = ' cos '
        elif node.value is math.sin:
            func_name = ' sin '
        elif node.value is logn:
            func_name = ' ln '
        return func_name + ' ( ' + expression(node.left)
    else:
        func_name = ''
        if node.value is operator.add:
            func_name = ' + '
        elif node.value is operator.mul:
            func_name = ' * '
        elif node.value is operator.truediv:
            func_name = ' / '
        elif node.value is operator.sub:
            func_name = ' - '
        elif node.value is operator.pow:
            func_name = ' ** '
        return '( ' + expression(node.left) + func_name + expression(node.right) + ' )'

class Tree:
    def __init__(self, expr='', node=None):
        if node is None:
            self.expression = expr
            self.node = self._getAST()
        else:
            self.expression = expression(node)
            self.node = node

    def _getAST(self):
        stack = []
        result = []
        tokenList = self.expression.split()
        prevToken = ''
        for token in tokenList:
            if str.isalpha(token) and token not in Functions or str.isdigit(token):
                node = Node(token)
                result.append(node)
            elif token in Functions:
                stack.append(token)
            elif token in Operators:
                if prevToken is '' or prevToken is '(':
                    node = Node(0)
                    result.append(node)
                    continue
                while stack and (stack[-1] in Operators) and (
                            Operators[stack[-1]]['priority'] > Operators[token]['priority']):
                    op = stack.pop()
                    right = result.pop()
                    left = result.pop()
                    node = Node(Operators[op]['value'], left, right)
                    result.append(node)
                stack.append(token)
            elif token is '(':
                stack.append(token)
            elif token is ')':
                while stack[-1] is not '(' and stack:
                    op = stack.pop()
                    if op in Operators:
                        right = result.pop()
                        left = result.pop()
                        node = Node(Operators[op]['value'], left, right)
                        result.append(node)
                    elif op in Functions:
                        right = None
                        left = result.pop()
                        node = Node(Functions[op]['value'], left, right)
                        result.append(node)
                    if not stack:
                        raise ValueError(" пропущена открывающая скобка")
                stack.pop()
                if stack and stack[-1] in Functions:
                    node = Node(Functions[stack.pop()]['value'], result.pop(), None)
                    result.append(node)
            prevToken = token
        if '(' in stack:
            raise ValueError("Несбалансированные скобки '( )' ")
        while stack:
            op = stack.pop()
            if op in Operators:
                right = result.pop()
                left = result.pop()
                node = Node(Operators[op]['value'], left, right)
                result.append(node)
            elif op in Functions:
                right = None
                left = result.pop()
                node = Node(Functions[op]['value'], left, right)
                result.append(node)
        try:
            return result.pop()
        except IndexError:
            return Node(None)

    def __str__(self):
        return self.expression

    def __repr__(self):
        return self.expression

    def __add__(self, tree):
        first, second = deepcopy(self.node), deepcopy(tree.node)
        node = first + second
        expression = '( ' + self.expression + ' ) + ( ' + tree.expression + ' )'
        return Tree(expression, node)

    def __sub__(self, tree):
        first, second = deepcopy(self.node), deepcopy(tree.node)
        node = first - second
        expression = '( ' + self.expression + ' ) - ( ' + tree.expression + ' )'
        return Tree(expression, node)

    def __mul__(self, tree):
        first, second = deepcopy(self.node), deepcopy(tree.node)
        node = first * second
        expression = '( ' + self.expression + ' ) * ( ' + tree.expression + ' )'
        return Tree(expression, node)

    def __truediv__(self, tree):
        first, second = deepcopy(self.node), deepcopy(tree.node)
        node = first / second
        expression = '( ' + self.expression + ' ) / ( ' + tree.expression + ' )'
        return Tree(expression, node)

    def __neg__(self):
        buf = deepcopy(self.node)
        node = -buf
        expression = "- ( " + self.expression + " )"
        return Tree(expression, node)

    def __pow__(self, tree, modulo=None):
        first, second = deepcopy(self.node), deepcopy(tree.node)
        node = first ** second
        expr = '( ' + self.expression + ' ) ** ( ' + tree.expression + ' )'
        return Tree(expr, node)

    def __call__(self, x):
        value = self.node.calcTree(x)
        return round(value, 5)


def sqrt(x: Tree):
    node = Node(value=math.sqrt)
    node.left = x.node
    node.right = None
    expr = "sqrt (" + x.expression + " )"
    return Tree(expr=expr, node=node)


def cos(x: Tree):
    node = Node(value=math.cos)
    node.left = x.node
    node.right = None
    expr = "cos (" + x.expression + " )"
    return Tree(expr=expr, node=node)


def logn(x):
    return math.log(x, base=math.e)


def ln(x: Tree):
    node = Node(value=logn)
    node.left = x.node
    node.right = None
    expr = 'ln ( ' + x.expression + ' )'
    return Tree(expr=expr, node=node)


def diff(tree: Tree):
    if tree.node.value is operator.add:
        return diff(Tree(node=tree.node.left)) + diff(Tree(node=tree.node.right))
    elif tree.node.value is operator.sub:
        return diff(Tree(node=tree.node.left)) - diff(Tree(node=tree.node.right))
    elif tree.node.value is operator.mul:
        first = tree.node.left.isContainsVar()
        second = tree.node.right.isContainsVar()
        if first and second:
            return diff(Tree(node=tree.node.left)) * Tree(node=tree.node.right) + \
                   diff(Tree(node=tree.node.right)) * Tree(node=tree.node.left)
        elif first and not second:
            return diff(Tree(node=tree.node.left)) * Tree(node=tree.node.right)
        elif not first and second:
            return diff(Tree(node=tree.node.right)) * Tree(node=tree.node.left)
        elif not first and not second:
            return Tree('0', node=Node('0'))
    elif tree.node.value is operator.truediv:
        return (diff(tree.node.left) * tree.node.right - diff(tree.node.right) * tree.node.left) / \
               (tree.node.right * tree.node.right)
    elif tree.node.value is operator.pow:
        first = tree.node.left.isContainsVar()
        second = tree.node.right.isContainsVar()
        if first and second:
            return tree * (diff(Tree(node=tree.node.right)) * ln(Tree(node=tree.node.left)) +
                           Tree(node=tree.node.right) * diff(Tree(node=tree.node.left)) / Tree(node=tree.node.left))
        elif first and not second:
            return diff(Tree(node=tree.node.left)) * Tree(node=tree.node.right) * (Tree(node=tree.node.left) ** (Tree(node=tree.node.right) - Tree(node=Node('1'))))
        elif not first and second:
            return diff(Tree(node=tree.node.right)) * Tree(node=tree.node) * ln(Tree(node=tree.node.left))
        elif not first and not second:
            return Tree('0', node=Node('0'))

    elif str.isalpha(tree.node.value):
        return Tree('1', node=Node('1'))
    elif str.isalnum(tree.node.value):
        return Tree('0', node=Node('0'))


if __name__ == "__main__":
    f = Tree("x ** 2 + 2 ** x")
    g = diff(f)
    print(g)
    print(g.node.isContainsVar())

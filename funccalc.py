from copy import deepcopy
import operator
import math

Operators = {
    '+': {'value': operator.add, 'priority': 1},
    '-': {'value': operator.sub, 'priority': 1},
    '*': {'value': operator.mul, 'priority': 2},
    '/': {'value': operator.truediv, 'priority': 2},
    '^': {'value': operator.pow, 'priority': 3},
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

    def calcTree(self, x):
        if self.right is None and self.left is None:
            if str.isalpha(self.value):
                return x
            return float(self.value)
        elif self.right is None:
            return self.value(self.left.calcTree(x))
        else:
            return self.value(self.left.calcTree(x), self.right.calcTree(x))


class Tree:
    def __init__(self, expression='', node=None):
        self.expression = expression
        if node is None:
            self.node = self._getAST()
        else:
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
            prevToken = token
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

    def __call__(self, x):
        value = self.node.calcTree(x)
        return round(value, 5)


def sqrt(x: Tree):
    node = Node(value=math.sqrt)
    node.left = x.node
    node.right = None
    expression = "sqrt (" + x.expression + " )"
    return Tree(expression=expression, node=node)


# def makeTree(expression):
#     stack = []
#     result = []
#
#     tokenList = expression.split()
#     for token in tokenList:
#         if str.isalpha(token) and token not in Functions or str.isdigit(token):
#             node = Node(token)
#             result.append(node)
#         elif token in Functions:
#             stack.append(token)
#         elif token in Operators:
#             while stack and (stack[-1] in Operators) and (Operators[stack[-1]]['priority'] > Operators[token]['priority']):
#                 op = stack.pop()
#                 right = result.pop()
#                 left = result.pop()
#                 node = Node(Operators[op]['value'], left, right)
#                 result.append(node)
#             stack.append(token)
#         elif token is '(':
#             stack.append(token)
#         elif token is ')':
#             while stack[-1] is not '(' and stack:
#                 op = stack.pop()
#                 if op in Operators:
#                     right = result.pop()
#                     left = result.pop()
#                     node = Node(Operators[op]['value'], left, right)
#                     result.append(node)
#                 elif op in Functions:
#                     right = None
#                     left = result.pop()
#                     node = Node(Functions[op]['value'], left, right)
#                     result.append(node)
#                 if not stack:
#                     raise ValueError(" пропущена открывающая скобка")
#             stack.pop()
#             if stack and stack[-1] in Functions:
#                 op = stack.pop()
#                 right = None
#                 left = result.pop()
#                 node = Node(Functions[op]['value'], left, right)
#                 result.append(node)
#     while stack:
#         op = stack.pop()
#         if op in Operators:
#             right = result.pop()
#             left = result.pop()
#             node = Node(Operators[op]['value'], left, right)
#             result.append(node)
#         elif op in Functions:
#             right = None
#             left = result.pop()
#             node = Node(Functions[op]['value'], left, right)
#             result.append(node)
#     return result.pop()
#
#
# def calcTree(tree, x):
#     if tree.right is None and tree.left is None:
#         if str.isalpha(tree.value):
#             tree.value = x
#         return float(tree.value)
#     elif tree.right is None:
#         return tree.value(calcTree(tree.left, x))
#     else:
#         return tree.value(calcTree(tree.left, x), calcTree(tree.right, x))
#
# class MathFunctionClass:
#     def __init__(self, expression=None):
#         result = []
#         stack = []
#
#         if expression is not None:
#             tokenList = expression.split(" ")
#             for token in tokenList:
#                 if str.isalpha(token) and token not in Functions or str.isdigit(token):
#                     result.append(token)
#                 elif token in Functions:
#                     stack.append(token)
#                 elif token in Delimiters:
#                     if '(' not in stack:
#                         raise ValueError("Либо пропущена открывающая скобка, либо пропущен разделитель")
#                     while stack[-1] is not '(' and len(stack) != 0:
#                         result.append(stack.pop())
#                 elif token in Operators:
#                     if len(stack) != 0:
#                         while (stack[-1] in Operators) and (Operators[stack[-1]] > Operators[token]):
#                             result.append(stack.pop())
#                     stack.append(token)
#                 elif token is '(':
#                     stack.append(token)
#                 elif token is ')':
#                     while stack[-1] is not '(' and len(stack) != 0:
#                         result.append(stack.pop())
#                         if len(stack) == 0:
#                             raise ValueError(" пропущена открывающая скобка")
#                     stack.pop()
#             while len(stack) != 0:
#                 result.append(stack.pop())
#
#         self.postfix = result
#         self.expression = expression
#
#     # @property
#     def __str__(self):
#         return ' '.join(self.postfix)
#
#     def __add__(self, other):
#         buf = MathFunctionClass()
#         buf.postfix.extend(self.postfix)
#         buf.postfix.extend(other.postfix)
#         buf.postfix.append('+')
#         return buf


if __name__ == "__main__":
    f = Tree("- x")
    g = Tree("sin ( - x )")
    print(f)
    print(g(3.14 / 2))

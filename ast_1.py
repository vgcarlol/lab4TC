class Node:
    def __init__(self, value, left=None, right=None):
        # Inicializa un nodo en el AST.
        # 'value' es el valor del nodo (un operador o un operando).
        # 'left' y 'right' son referencias a los nodos hijos (izquierdo y derecho).
        self.value = value
        self.left = left
        self.right = right

class AST:
    def __init__(self, postfix):
        # Inicializa la clase AST con la expresión regular en notación postfix.
        self.postfix = postfix

    def build(self):
        # Construye el AST a partir de la expresión postfix.
        # Utiliza una pila para mantener los nodos a medida que se procesan los tokens.
        stack = []
        for token in self.postfix:
            if token.isalnum() or token == 'ε':
                # Si el token es un operando o epsilon, crea un nodo y lo apila.
                stack.append(Node(token))
            else:
                # Si el token es un operador, saca nodos de la pila y crea un nuevo nodo con ellos.
                if token in '*+':
                    left = stack.pop()
                    stack.append(Node(token, left))
                elif token in '|.':
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(Node(token, left, right))
        # Devuelve el nodo raíz del AST, que queda en la cima de la pila.
        return stack.pop()

class ShuntingYard:
    def __init__(self, expression):
        # Inicializa con la expresión regular en notación infix.
        self.expression = expression

    def to_postfix(self):
        # Convierte la expresión infix a postfix usando el algoritmo Shunting Yard.
        precedence = {'*': 3, '+': 2, '?': 2, '|': 1, '.': 1}
        stack = []
        output = []
        for token in self.expression:
            if token.isalnum() or token == 'ε':
                # Si el token es un operando o epsilon, lo agrega a la salida.
                output.append(token)
            elif token == '(':
                # Si es un paréntesis de apertura, lo apila.
                stack.append(token)
            elif token == ')':
                # Si es un paréntesis de cierre, desempila hasta encontrar el paréntesis de apertura.
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Elimina el '(' de la pila.
            else:
                # Para operadores, desempila según la precedencia y luego apila el operador actual.
                while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
        while stack:
            # Finalmente, vacía la pila en la salida.
            output.append(stack.pop())
        return ''.join(output)

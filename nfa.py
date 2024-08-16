class State:
    def __init__(self):
        # Cada estado tiene una lista de transiciones (edges) que son pares (símbolo, estado destino).
        self.edges = []

class NFA:
    def __init__(self, start, end):
        # Un NFA tiene un estado inicial y un estado final.
        self.start = start
        self.end = end

    @staticmethod
    def from_ast(node):
        # Método estático para construir un NFA a partir de un nodo del AST.
        if node.value.isalnum() or node.value == 'ε':
            # Si el nodo es un operando o epsilon, crea un NFA simple con una transición.
            start = State()
            end = State()
            start.edges.append((node.value, end))
            return NFA(start, end)
        elif node.value == '*':
            # Manejo de la cerradura de Kleene (cero o más repeticiones).
            nfa = NFA.from_ast(node.left)
            start = State()
            end = State()
            start.edges.append(('ε', nfa.start))
            nfa.end.edges.append(('ε', end))
            nfa.end.edges.append(('ε', nfa.start))
            start.edges.append(('ε', end))
            return NFA(start, end)
        elif node.value == '+':
            # Manejo de una o más repeticiones (como Kleene, pero al menos una vez).
            nfa = NFA.from_ast(node.left)
            start = State()
            end = State()
            start.edges.append(('ε', nfa.start))
            nfa.end.edges.append(('ε', end))
            nfa.end.edges.append(('ε', nfa.start))
            return NFA(start, end)
        elif node.value == '?':
            # Manejo de cero o una repetición (símbolo opcional).
            nfa = NFA.from_ast(node.left)
            start = State()
            end = State()
            start.edges.append(('ε', nfa.start))  # Opción de tomar el símbolo.
            start.edges.append(('ε', end))        # Opción de omitir el símbolo.
            nfa.end.edges.append(('ε', end))
            return NFA(start, end)
        elif node.value == '|':
            # Manejo del operador OR (alternativa entre dos expresiones).
            left_nfa = NFA.from_ast(node.left)
            right_nfa = NFA.from_ast(node.right)
            start = State()
            end = State()
            start.edges.append(('ε', left_nfa.start))
            start.edges.append(('ε', right_nfa.start))
            left_nfa.end.edges.append(('ε', end))
            right_nfa.end.edges.append(('ε', end))
            return NFA(start, end)
        elif node.value == '.':
            # Manejo de la concatenación de dos expresiones.
            left_nfa = NFA.from_ast(node.left)
            right_nfa = NFA.from_ast(node.right)
            left_nfa.end.edges.append(('ε', right_nfa.start))
            return NFA(left_nfa.start, right_nfa.end)

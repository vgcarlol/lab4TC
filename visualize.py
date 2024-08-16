from graphviz import Digraph

def visualize_nfa(nfa):
    # Crea un objeto Digraph de Graphviz para visualizar el NFA.
    dot = Digraph()
    visited = set()

    def traverse(state):
        # Función recursiva que recorre el NFA y dibuja las transiciones.
        if state in visited:
            return
        visited.add(state)
        for symbol, next_state in state.edges:
            # Dibuja una arista para cada transición del NFA.
            dot.edge(str(id(state)), str(id(next_state)), label=symbol)
            traverse(next_state)

    traverse(nfa.start)
    # Marca el estado inicial con un doble círculo verde y el estado final con un doble círculo rojo.
    dot.node(str(id(nfa.start)), shape='doublecircle', color='green')
    dot.node(str(id(nfa.end)), shape='doublecircle', color='red')
    return dot

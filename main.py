import os
import re
from shunting_yard import ShuntingYard
from ast_1 import AST
from nfa import NFA
from visualize import visualize_nfa

# Añade la ruta de Graphviz al PATH del sistema, en caso de que sea necesario.
os.environ["PATH"] += os.pathsep + os.path.abspath("Graphviz/bin")

def simulate_nfa(nfa, string):
    # Función que simula el funcionamiento de un NFA sobre una cadena de entrada.
    
    def dfs(state, idx, visited):
        # Función recursiva que implementa una búsqueda en profundidad (DFS) en el NFA.
        if (state, idx) in visited:
            return False
        visited.add((state, idx))
        
        # Imprime el estado actual y el índice para depuración.
        print(f"Estado actual: {id(state)}, Índice: {idx}, Caracter: {string[idx] if idx < len(string) else 'EOF'}")

        if idx == len(string):
            # Si se ha llegado al final de la cadena, verifica si el estado actual es de aceptación.
            if state == nfa.end:
                print("¡Cadena aceptada!")
                return True
            for symbol, next_state in state.edges:
                if symbol == 'ε':
                    # Continua con transiciones epsilon si es posible.
                    if dfs(next_state, idx, visited):
                        return True
            return False
        
        for symbol, next_state in state.edges:
            if symbol == 'ε':
                # Continua con transiciones epsilon si es posible.
                if dfs(next_state, idx, visited):
                    return True
            elif idx < len(string) and symbol == string[idx]:
                # Continua si el símbolo coincide con el carácter actual en la cadena.
                if dfs(next_state, idx + 1, visited):
                    return True
        
        return False

    visited = set()
    return dfs(nfa.start, 0, visited)

def clean_filename(filename):
    # Limpia el nombre del archivo de cualquier carácter no permitido en nombres de archivos.
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def process_file(file_path):
    # Procesa cada línea del archivo, que contiene una expresión regular.
    with open(file_path, 'r') as file:
        for line in file:
            regex = line.strip()
            postfix = ShuntingYard(regex).to_postfix()  # Convierte a postfix.
            ast = AST(postfix).build()  # Construye el AST.
            nfa = NFA.from_ast(ast)  # Genera el NFA desde el AST.
            dot = visualize_nfa(nfa)  # Visualiza el NFA.
            cleaned_filename = clean_filename(f'{regex}_nfa')
            dot.render(cleaned_filename, format='png', cleanup=True)  # Genera la imagen del NFA.
            cadena = input(f"Ingrese la cadena para la expresión regular '{regex}': ")
            resultado = simulate_nfa(nfa, cadena)  # Simula el NFA con la cadena.
            print(f"¿La cadena '{cadena}' es aceptada por el NFA de '{regex}'? {'Sí' if resultado else 'No'}")

if __name__ == "__main__":
    # Llama a la función para procesar el archivo cuando el programa se ejecuta.
    process_file('expresiones.txt')

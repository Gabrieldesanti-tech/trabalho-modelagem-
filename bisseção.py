"""
Implementação do Método da Bisseção para encontrar raízes de funções.
Inclui todos os testes de parada necessários e verificação do teorema de Bolzano.
O usuário fornece a função matemática e o intervalo [a,b].
"""

import math
import sys
from typing import Callable, List, Tuple, Dict, Union

def normalizar_expressao(expressao: str) -> str:
    """
    Normaliza uma expressão matemática para formato Python.
    Por exemplo: 
    - "x*2" -> "2*x"
    - "3x" -> "3*x"
    - "x^2" -> "x**2"
    """
    import re
    
    # Remove espaços
    expressao = expressao.replace(" ", "")
    
    # Substitui ^ por **
    expressao = expressao.replace("^", "**")
    
    # Adiciona * entre número e x
    expressao = re.sub(r'(\d)([x])', r'\1*\2', expressao)

    # Adiciona * entre número e pi (ex: 2pi -> 2*pi)
    expressao = re.sub(r'(\d)(pi)', r'\1*\2', expressao)
    
    # Adiciona * depois de x quando seguido de parênteses
    expressao = re.sub(r'x\(', r'x*(', expressao)
    
    # Adiciona * entre x e número
    expressao = re.sub(r'([x])(\d)', r'\1*\2', expressao)
    
    # Converte expressões como 3x para 3*x
    expressao = re.sub(r'(\d)x', r'\1*x', expressao)

    # Adiciona * entre número e e (constante de Euler) quando NÃO for notação científica
    # Exemplo: 2e -> 2*e  but 1e-3 (notação científica) deve permanecer
    expressao = re.sub(r"(\d)(e)(?![+\-]?\d)", r"\1*\2", expressao, flags=re.IGNORECASE)
    
    return expressao

def criar_funcao(expressao: str) -> Callable[[float], float]:
    """
    Cria uma função a partir de uma expressão matemática fornecida pelo usuário.
    
    Parâmetros:
    expressao: string contendo a expressão matemática em x
    """
    # Cria um dicionário com funções matemáticas permitidas
    funcoes_permitidas = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
        'abs': abs, 'pi': math.pi, 'e': math.e, 'E': math.e
    }
    
    # Normaliza a expressão
    expressao = normalizar_expressao(expressao)
    
    # Compila a expressão
    try:
        codigo = compile(expressao, '<string>', 'eval')
        
        def f(x: float) -> float:
            # Cria namespace local com x e funções matemáticas
            namespace = {'x': x, **funcoes_permitidas}
            return eval(codigo, {"__builtins__": {}}, namespace)
        
        return f
    except Exception as e:
        raise ValueError(f"Erro ao criar função: {str(e)}")

def bissecao(f: Callable[[float], float], a: float, b: float, tolerancia=0.0001, max_iteracoes=10):
    """
    Encontra uma raiz de f(x) = 0 no intervalo [a, b] usando o método da bisseção.
    
    Parâmetros:
    f: função contínua no intervalo [a, b]
    a: limite inferior do intervalo
    b: limite superior do intervalo
    tolerancia: erro máximo aceitável
    max_iteracoes: número máximo de iterações permitidas
    
    Retorna:
    x_medio: aproximação da raiz
    iteracoes: número de iterações realizadas
    convergiu: True se convergiu, False se não
    historico: lista com valores de x e f(x) em cada iteração
    erro: mensagem de erro se houver, None caso contrário
    """
    # Verifica se a < b
    if a >= b:
        return None, 0, False, [], "Erro: O limite inferior 'a' deve ser menor que o limite superior 'b'"
    
    # Calcula f(a) e f(b)
    try:
        fa = f(a)
        fb = f(b)
    except Exception as e:
        return None, 0, False, [], f"Erro ao avaliar f(a) ou f(b): {e}"

    # Verifica o teorema de Bolzano (se f(a)·f(b) < 0)
    if fa * fb > 0:
        return None, 0, False, [], "Erro: f(a) e f(b) devem ter sinais opostos"

    # Se f(a) = 0, a é a raiz
    if fa == 0:
        return a, 0, True, [(a, fa)], None

    # Se f(b) = 0, b é a raiz
    if fb == 0:
        return b, 0, True, [(b, fb)], None
    
    iteracoes = 0
    historico = [(a, fa), (b, fb)]
    
    while iteracoes < max_iteracoes:
        # Calcula o ponto médio
        x_medio = (a + b) / 2
        f_medio = f(x_medio)
        
        # Adiciona ao histórico
        historico.append((x_medio, f_medio))
        
        # Se f(x_medio) = 0, encontramos a raiz exata
        if f_medio == 0:
            return x_medio, iteracoes + 1, True, historico, None
        
        # Verifica a tolerância (critério de parada)
        if (b - a) < tolerancia:
            return x_medio, iteracoes + 1, True, historico, None
        
        # Atualiza o intervalo
        if f_medio * fa < 0:  # Raiz está entre a e x_medio
            b = x_medio
            fb = f_medio
        else:  # Raiz está entre x_medio e b
            a = x_medio
            fa = f_medio
        
        iteracoes += 1
    
    # Se chegou aqui, atingiu o número máximo de iterações
    return x_medio, iteracoes, False, historico, "Aviso: Atingiu o número máximo de iterações"

# Exemplo de uso
if __name__ == "__main__":
    print("Método da Bisseção - Calculadora")
    print("-" * 40)
    print("\nExemplos de funções que você pode digitar:")
    print("x^2 - 4        → x² - 4")
    print("3x^2 - 2x + 1  → 3x² - 2x + 1")
    print("2x - 5         → 2x - 5")
    print("x^3 - x - 2    → x³ - x - 2")
    print("sin(x) - 0.5   → seno(x) - 0.5")
    print("2x^2 + 3x - 4  → 2x² + 3x - 4")
    print("\nVocê pode escrever a função naturalmente:")
    print("- Use x^2 ou x**2 para x²")
    print("- Pode escrever 2x ao invés de 2*x")
    print("- Pode usar sin(x), cos(x), exp(x), etc.")
    print("\nFunções disponíveis: sin, cos, tan, exp, log, sqrt, abs")
    print("Constantes disponíveis: pi, e")
    
    # Entrada do usuário
    try:
        # Obtém a função do usuário
        print("\nDigite a função em termos de x:")
        expressao = input("f(x) = ")
        f = criar_funcao(expressao)
        
        # Testa se a função é válida
        try:
            f(0.0)  # Testa com um valor simples
        except Exception as e:
            raise ValueError(f"Função inválida: {str(e)}")
        
        # Obtém o intervalo: permite entrada em uma linha "a b" ou "a,b"
        print("\nDefina o intervalo [a, b]:")

        while True:
            entrada_intervalo = input("Digite a e b (separe por espaço ou vírgula) ou pressione Enter para digitar separadamente: ").strip()

            if entrada_intervalo:
                partes = [p for p in entrada_intervalo.replace(',', ' ').split() if p != '']
                if len(partes) != 2:
                    print("Entrada inválida para 'a b'. Vou pedir separadamente.")
                    try:
                        a = float(input("Digite o valor de a: "))
                        b = float(input("Digite o valor de b: "))
                    except ValueError:
                        print("Entrada inválida. Tente novamente.")
                        continue
                else:
                    try:
                        a = float(partes[0])
                        b = float(partes[1])
                    except ValueError:
                        print("Não consegui converter os valores para números. Tente novamente.")
                        continue
            else:
                # entrada separada
                try:
                    a = float(input("Digite o valor de a: "))
                    b = float(input("Digite o valor de b: "))
                except ValueError:
                    print("Entrada inválida. Tente novamente.")
                    continue

            if a >= b:
                print("O valor de 'a' deve ser menor que 'b'. Deseja tentar novamente? (s/n)")
                resp = input().strip().lower()
                if resp.startswith('s'):
                    continue
                else:
                    print("Encerrando.")
                    sys.exit(1)

            # Tenta avaliar f(a) e f(b)
            try:
                fa = f(a)
                fb = f(b)
            except Exception as e:
                print(f"Erro ao avaliar f(a) ou f(b): {e}")
                print("Deseja tentar outro intervalo? (s/n)")
                resp = input().strip().lower()
                if resp.startswith('s'):
                    continue
                else:
                    print("Encerrando.")
                    sys.exit(1)

            print(f"\nf({a}) = {fa:.6f}")
            print(f"f({b}) = {fb:.6f}")

            # Verifica o teorema de Bolzano
            if fa * fb >= 0:
                print("A função deve ter sinais opostos em a e b. Deseja tentar outro intervalo? (s/n)")
                resp = input().strip().lower()
                if resp.startswith('s'):
                    continue
                else:
                    print("Encerrando.")
                    sys.exit(1)

            # se chegou até aqui, intervalo válido
            break

        print("\nParâmetros do método:")
        tolerancia = float(input("Digite a tolerância (ex: 0.0001): ") or "0.0001")
        max_iter = int(input("Digite o número máximo de iterações (ex: 100): ") or "100")
        
        # Executa o método
        raiz, iter, convergiu, hist, erro = bissecao(f, a, b, tolerancia, max_iter)
        
        print("\n" + "=" * 40)
        if erro:
            print(f"Erro: {erro}")
        else:
            print(f"Raiz encontrada: {raiz:.6f}")
            print(f"Iterações realizadas: {iter}")
            print(f"Convergiu: {convergiu}")
            print("\nHistórico de iterações:")
            print("Iteração".ljust(10), "x".ljust(15), "f(x)")
            print("-" * 35)
            for i, (x, fx) in enumerate(hist):
                print(f"{i}".ljust(10), f"{x:.6f}".ljust(15), f"{fx:.6f}")
        
    except ValueError:
        print("\nErro: Por favor, insira apenas números válidos.")

"""
Implementação do Método de Newton-Raphson para encontrar raízes de funções.
Permite que o usuário insira sua própria função e utiliza derivada numérica.
"""

from derivada import derivada_numerica

def newton_raphson(f, x_inicial, tolerancia=0.0001, max_iteracoes=10):
    """
    Encontra a raiz de uma função usando o método de Newton-Raphson.
    
    Parâmetros:
    f: função para encontrar a raiz
    x_inicial: valor inicial para começar a busca
    tolerancia: erro máximo aceitável
    max_iteracoes: número máximo de iterações permitidas
    
    Retorna:
    x: aproximação da raiz
    iteracoes: número de iterações realizadas
    convergiu: True se convergiu, False se não
    historico: lista com valores de x em cada iteração
    """
    x = x_inicial
    iteracoes = 0
    historico = [x]
    
    while iteracoes < max_iteracoes:
        # Calcula f(x) e f'(x)
        fx = f(x)
        dx = derivada_numerica(f, x)
        
        # Verifica se a derivada é muito próxima de zero
        if abs(dx) < 1e-10:
            print(f"Aviso: Derivada muito próxima de zero em x = {x}")
            return x, iteracoes, False, historico
        
        # Calcula próximo x
        x_novo = x - fx/dx
        
        # Adiciona ao histórico
        historico.append(x_novo)
        
        # Verifica convergência
        if abs(x_novo - x) < tolerancia:
            return x_novo, iteracoes + 1, True, historico
        
        x = x_novo
        iteracoes += 1
    
    return x, iteracoes, False, historico

# Exemplo de uso
if __name__ == "__main__":
    print("Método de Newton-Raphson para encontrar raízes de funções")

    
    # Obtém a função do usuário
    print("\nExemplos de funções que você pode usar:")
    print("x**2 - 4        (para x² - 4)")
    print("x**3 - x - 2    (para x³ - x - 2)")
    print("math.sin(x)     (para seno de x)")
    print("\nObservação: você pode usar as funções do módulo math")
    
    import math
    
    # Entrada da função do usuário
    funcao_str = input("\nDigite a função f(x) = ")
    
    # Cria a função a partir da string
    try:
        # Cria uma função que pode usar o módulo math
        funcao = eval(f"lambda x: {funcao_str}")
        
        # Testa a função
        funcao(1.0)
    except Exception as e:
        print(f"\nErro ao criar a função: {e}")
        print("Verifique a sintaxe e tente novamente")
        exit(1)
    
    # Obtém o valor inicial
    try:
        x_inicial = float(input("\nDigite o valor inicial x0 = "))
    except ValueError:
        print("\nErro: O valor inicial deve ser um número")
        exit(1)
    
    # Obtém a tolerância (opcional)
    try:
        tolerancia = input("\nDigite a tolerância desejada (ou pressione Enter para usar 0.0001): ")
        tolerancia = float(tolerancia) if tolerancia.strip() else 0.0001
    except ValueError:
        print("\nErro: A tolerância deve ser um número")
        exit(1)
    
    # Obtém o número máximo de iterações (opcional)
    try:
        max_iter = input("\nDigite o número máximo de iterações (ou pressione Enter para usar 10): ")
        max_iter = int(max_iter) if max_iter.strip() else 10
    except ValueError:
        print("\nErro: O número de iterações deve ser um inteiro")
        exit(1)
    
    # Executa o método
    raiz, iter, convergiu, hist = newton_raphson(funcao, x_inicial, tolerancia, max_iter)
    
    # Imprime resultados
    print("\nResultados:")
    print("===========")
    print(f"Função: f(x) = {funcao_str}")
    print(f"Valor inicial: {x_inicial}")
    print(f"Raiz encontrada: {raiz:.10f}")
    print(f"f(raiz) = {funcao(raiz):.10f}")
    print(f"Iterações realizadas: {iter}")
    print(f"Convergiu: {'Sim' if convergiu else 'Não'}")
    
    print("\nHistórico de valores:")
    print("===================")
    for i, valor in enumerate(hist):
        print(f"Iteração {i}: x = {valor:.10f}")

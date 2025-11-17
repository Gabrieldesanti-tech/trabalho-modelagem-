import math
# Importa o módulo math, que contém funções matemáticas como sin, cos, exp, log etc.
# Se remover esta linha: qualquer chamada math.algo vai gerar erro (NameError).


def bissecao(funcao_str, a, b, tol=1e-6, max_iter=100):
    # Define a função principal do método da bisseção, usada pelo backend.
    # Se remover a função inteira, o backend não conseguirá calcular bisseção.

    """
    Método da Bisseção para a API:
    - funcao_str: string com f(x), ex: "x**3 - x - 1"
    - a, b: limites do intervalo [a, b]
    - tol: tolerância
    - max_iter: número máximo de iterações

    Retorna:
      - raiz (float) se deu certo
      - None se não atender condição de sinal oposto em f(a) e f(b)
    """
    # Este bloco é apenas documentação; removê-lo não afeta o funcionamento.


    def f(x):
        # Define uma função interna f(x) que avalia a expressão digitada pelo usuário.
        # Se remover essa função, você não teria como calcular f(a), f(b) nem f(c),
        # então o método de bisseção quebra completamente.

        contexto = {
            "x": x,         # variável usada na expressão; sem isso, 'x' seria indefinida.
            "math": math,   # permite usar math.sin, math.exp etc.
            "e": math.e,    # permite usar 'e' diretamente na expressão.
            "pi": math.pi,  # permite usar 'pi' diretamente.
            "sin": math.sin,  # permite usar sin(x); se remover, daria erro ao usar sin().
            "cos": math.cos,  # idem para cos(x).
            "tan": math.tan,  # idem para tan(x).
            "log": math.log,  # log natural.
            "exp": math.exp,  # exponencial e^x.
            "sqrt": math.sqrt, # raiz quadrada.
            "log10": math.log10, # log base 10.
        }
        # O contexto controla o que o usuário pode usar.
        # Sem isso, o usuário teria acesso a funções perigosas via eval.

        return eval(funcao_str, {"__builtins__": {}}, contexto)
        # Avalia a função digitada com segurança.
        # Se remover o segundo argumento {"__builtins__": {}}, o usuário pode rodar código malicioso.
        # Se remover o contexto, funções como sin, exp etc. não funcionariam.


    fa = f(a)
    # Calcula f(a). Necessário para testar mudança de sinal e atualizar o intervalo.
    # Se remover, você não tem como saber se existe raiz no intervalo.

    fb = f(b)
    # Calcula f(b). Mesma importância que f(a).
    # Se remover, a verificação de sinal e as atualizações bisseção quebram.


    # condição de existência de raiz (mudança de sinal)
    if fa * fb >= 0:
        # Testa se f(a) e f(b) têm sinais opostos.
        # O método de bisseção só funciona se houver mudança de sinal.
        # Se remover essa verificação, o método pode entrar em intervalo sem raiz ou divergir.
        
        # para a API, devolvemos None; o backend trata isso
        return None
        # Retorna None para indicar erro ao backend.


    for _ in range(1, max_iter + 1):
        # Loop principal da bisseção, repetindo até atingir max_iter.
        # Se remover o for, o algoritmo nunca calculará os passos da bisseção.

        c = (a + b) / 2
        # Calcula o ponto médio do intervalo [a, b].
        # Se remover, você não teria novo candidato à raiz.

        fc = f(c)
        # Avalia a função nesse ponto.
        # Sem isso, não pode aplicar o teste de parada nem atualizar intervalo.


        # critério de parada
        if abs(fc) < tol or (b - a) / 2 < tol:
            # Primeiro critério: |f(c)| < tolerância → ótimo, chegamos perto da raiz.
            # Segundo critério: tamanho do intervalo < tolerância.
            # Se remover isso, o método só pararia no limite de iterações.
            return c
            # Retorna a raiz aproximada.


        # atualiza intervalo
        if fa * fc < 0:
            # Se há mudança de sinal entre [a, c], a raiz está nesse intervalo.
            b = c       # Atualiza limite superior.
            fb = fc     # Atualiza f(b).
            # Se remover esta parte, o método não atualiza o intervalo corretamente.

        else:
            # Caso contrário, a raiz está entre [c, b].
            a = c       # Atualiza limite inferior.
            fa = fc     # Atualiza f(a).
            # Se remover esta parte, também quebra o método.


    # se estourar o número máximo de iterações,
    # devolve o meio do último intervalo
    return (a + b) / 2
    # Valor aproximado caso não tenha atingido o critério de parada antes.
    # Se remover, o método terminaria sem retorno (erro).

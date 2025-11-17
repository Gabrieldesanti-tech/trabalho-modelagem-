import math

def bissecao(funcao_str, a, b, tol=1e-6, max_iter=100):
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

    def f(x):
        contexto = {
            "x": x,
            "math": math,
            "e": math.e,
            "pi": math.pi,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,   # log natural
            "exp": math.exp,
            "sqrt": math.sqrt,
            "log10": math.log10,
        }
        return eval(funcao_str, {"__builtins__": {}}, contexto)

    fa = f(a)
    fb = f(b)

    # condição de existência de raiz (mudança de sinal)
    if fa * fb >= 0:
        # para a API, devolvemos None; o backend trata isso
        return None

    for _ in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)

        # critério de parada
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c

        # atualiza intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    # se estourar o número máximo de iterações,
    # devolve o meio do último intervalo
    return (a + b) / 2

import math

def bissecao(f_str, a, b, tol=1e-6, max_iter=100):
    """
    Método da Bisseção para encontrar uma raiz de f(x) no intervalo [a, b].
    O usuário informa a expressão de f(x) como string.
    """

    def f(x):
        # Ambiente seguro com funções matemáticas permitidas
        contexto = {
            "x": x,
            "math": math,
            "e": math.e,
            "pi": math.pi,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,      # log(x) = ln(x)
            "exp": math.exp,
            "sqrt": math.sqrt,
            "log10": math.log10,
        }
        return eval(f_str, contexto)

    # Verifica condição de existência de raiz (mudança de sinal)
    fa = f(a)
    fb = f(b)
    if fa * fb >= 0:
        print("Erro: f(a) e f(b) devem ter sinais opostos no intervalo [a, b].")
        return None

    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)

        print(
            f"Iteração {i:2d}: "
            f"a = {a:.6f}, b = {b:.6f}, x{i} = {c:.6f}, "
            f"f(a) = {fa:.6e}, f(b) = {fb:.6e}, f(x{i}) = {fc:.6e}"
        )

        # Testes de parada
        if abs(fc) < tol or (b - a) / 2 < tol:
            print(f"Raiz aproximada encontrada: {c:.6f}")
            return c

        # Atualiza intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    print("Número máximo de iterações atingido.")
    return (a + b) / 2


if __name__ == "__main__":
    print("MÉTODO DA BISSEÇÃO")
    f_str = input("Digite a função f(x) = ")

    a = float(input("Digite o limite inferior a: "))
    b = float(input("Digite o limite superior b: "))

    tol = float(input("Digite a tolerância (ex: 1e-6): "))

    raiz = bissecao(f_str, a, b, tol)

    if raiz is not None:
        print(f"Resultado final: raiz ≈ {raiz:.6f}")

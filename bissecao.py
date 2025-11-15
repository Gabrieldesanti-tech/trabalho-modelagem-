import math

def bissecao(f, a, b, tolerancia=1e-6, max_iteracoes=100):
    """
    Método da Bisseção adaptado para o BACK-END.
    Agora recebe a função f(x) já pronta, e retorna um dicionário JSON-friendly.
    """

    historico = []

    fa = f(a)
    fb = f(b)

    # Verifica mudança de sinal
    if fa * fb >= 0:
        return {
            "convergiu": False,
            "mensagem": "f(a) e f(b) devem ter sinais opostos.",
            "historico": [],
            "raiz": None,
            "iteracoes": 0
        }

    for i in range(1, max_iteracoes + 1):
        c = (a + b) / 2
        fc = f(c)

        historico.append({
            "iteracao": i,
            "a": a,
            "b": b,
            "x": c,
            "f(a)": fa,
            "f(b)": fb,
            "f(x)": fc
        })

        # Testes de parada
        if abs(fc) < tolerancia or abs(b - a) / 2 < tolerancia:
            return {
                "convergiu": True,
                "raiz": c,
                "iteracoes": i,
                "historico": historico
            }

        # Atualização do intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    # Se não convergiu
    return {
        "convergiu": False,
        "raiz": (a + b) / 2,
        "iteracoes": max_iteracoes,
        "historico": historico,
        "mensagem": "Número máximo de iterações atingido."
    }

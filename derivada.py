def derivada_numerica(f, x, h=1e-6):
    """
    Derivada numérica usando diferença central:
        f'(x) ≈ (f(x + h) - f(x - h)) / (2h)

    - f: função Python que recebe x e retorna f(x)
    - x: ponto onde quer a derivada
    - h: passo pequeno
    """
    return (f(x + h) - f(x - h)) / (2 * h)
# MÉTODO DA DERIVADA

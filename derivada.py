def derivada_numerica(f, x, h=1e-6):
    # Define a função derivada_numerica, que calcula a derivada aproximada de f(x).
    # - f: é a função original (ex: lambda x: x**2)
    # - x: ponto onde queremos derivar
    # - h: um valor pequeno usado para aproximar a derivada
    #
    # Se remover essa linha, a função não existiria e o método de Newton iria quebrar
    # com erro "NameError: derivada_numerica is not defined".

    """
    Derivada numérica usando diferença central:
        f'(x) ≈ (f(x + h) - f(x - h)) / (2h)

    - f: função Python que recebe x e retorna f(x)
    - x: ponto onde quer a derivada
    - h: passo pequeno
    """
    # Este bloco é apenas documentação (docstring).
    # Se você remover, nada muda no funcionamento.
    # Serve apenas para explicar a função.

    return (f(x + h) - f(x - h)) / (2 * h)
    # Retorna a fórmula da derivada numérica pela diferença central.
    #
    # (f(x + h) - f(x - h)) / (2h)
    #
    # Essa fórmula é muito precisa para valores pequenos de h.
    #
    # Se remover essa linha:
    #   - A função não retornaria nada
    #   - Newton-Raphson tentaria usar o valor None como derivada
    #   - Resultado: erro de divisão (TypeError) e ruptura total do método.

# MÉTODO DA DERIVADA
# Apenas um comentário explicando o tema.
# Pode remover que nada muda no funcionamento.

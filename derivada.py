"""
Módulo para cálculo de derivadas numéricas.
"""

def derivada_numerica(f, x, h=1e-7):
    """
    Calcula a derivada numérica de uma função em um ponto usando diferenças finitas.
    
    Parâmetros:
    f: função para calcular a derivada
    x: ponto onde calcular a derivada
    h: tamanho do passo para diferença finita
    
    Retorna:
    float: valor da derivada no ponto x
    """
    return (f(x + h) - f(x)) / h
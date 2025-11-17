from flask import Flask, request, jsonify
from flask_cors import CORS
import math

# módulos auxiliares que você já tem:
# - derivada.py  → função derivada_numerica(f, x)
# - eliminacao_gauss.py → funcoes eliminacao_gauss(matriz, usar_pivoteamento)
#                          e verificar_solucao(matriz, solucao)
from derivada import derivada_numerica
from eliminacao_gauss import eliminacao_gauss, verificar_solucao


app = Flask(__name__)
CORS(app)  # libera CORS para o front (index.html aberto no navegador)


# =========================
# FUNÇÃO BISSEÇÃO (direto no backend)
# =========================
def bissecao(funcao_str, a, b, tol=1e-6, max_iter=100):
    """
    Método da Bisseção:
    - funcao_str: string com f(x), ex: "x**3 - x - 1"
    - a, b: limites do intervalo [a, b]
    - tol: tolerância
    - max_iter: número máximo de iterações

    Retorna:
      - raiz (float) se der certo
      - None se f(a) e f(b) não tiverem sinais opostos
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


# =========================
# MÉTODO DE NEWTON-RAPHSON
# =========================
def newton_raphson(f, x_inicial, tolerancia=0.0001, max_iteracoes=10):
    x = x_inicial
    iteracoes = 0
    historico = [x]

    while iteracoes < max_iteracoes:
        fx = f(x)
        dx = derivada_numerica(f, x)

        if abs(dx) < 1e-10:
            return {
                "raiz": x,
                "iteracoes": iteracoes,
                "convergiu": False,
                "historico": historico,
                "mensagem": "Derivada muito próxima de zero"
            }

        x_novo = x - fx / dx
        historico.append(x_novo)

        if abs(x_novo - x) < tolerancia:
            return {
                "raiz": x_novo,
                "iteracoes": iteracoes + 1,
                "convergiu": True,
                "historico": historico
            }

        x = x_novo
        iteracoes += 1

    return {
        "raiz": x,
        "iteracoes": iteracoes,
        "convergiu": False,
        "historico": historico,
        "mensagem": "Não convergiu no número máximo de iterações"
    }


# =========================
# ROTA NEWTON
# =========================
@app.route("/newton", methods=["POST"])
def api_newton():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Nenhum JSON foi enviado."}), 400

    try:
        funcao_str = data["funcao"]
        x0 = float(data["x0"])
        tolerancia = float(data.get("tolerancia", 0.0001))
        max_iter = int(data.get("max_iter", 10))
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({
            "erro": "Dados inválidos no corpo da requisição.",
            "detalhe": str(e)
        }), 400

    contexto = {
        "math": math,
        "e": math.e,
        "pi": math.pi,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "sqrt": math.sqrt,
    }

    # monta a função f(x) a partir do texto
    try:
        ambiente = {"__builtins__": {}}
        ambiente.update(contexto)
        f = eval(f"lambda x: {funcao_str}", ambiente)
        f(1.0)  # teste rápido
    except Exception as e:
        return jsonify({"erro": f"Erro ao interpretar a função: {e}"}), 400

    try:
        resultado = newton_raphson(f, x0, tolerancia, max_iter)
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar método de Newton-Raphson: {e}"}), 400

    return jsonify({
        "metodo": "newton",
        "funcao": funcao_str,
        "x0": x0,
        "tolerancia": tolerancia,
        "max_iter": max_iter,
        **resultado
    }), 200


# =========================
# ROTA BISSEÇÃO
# =========================
@app.route("/bissecao", methods=["POST"])
def api_bissecao():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Nenhum JSON foi enviado."}), 400

    try:
        funcao_str = data["funcao"]
        a = float(data["a"])
        b = float(data["b"])
        tolerancia = float(data.get("tolerancia", 1e-6))
        max_iter = int(data.get("max_iter", 100))
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({
            "erro": "Dados inválidos no corpo da requisição.",
            "detalhe": str(e)
        }), 400

    # teste rápido de sintaxe da função
    contexto_teste = {
        "x": 1.0,
        "math": math,
        "e": math.e,
        "pi": math.pi,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "sqrt": math.sqrt,
    }
    try:
        eval(funcao_str, {"__builtins__": {}}, contexto_teste)
    except Exception as e:
        return jsonify({"erro": f"Erro ao interpretar a função: {e}"}), 400

    try:
        raiz = bissecao(funcao_str, a, b, tolerancia, max_iter)
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar método da bisseção: {e}"}), 400

    if raiz is None:
        return jsonify({
            "erro": "Não foi possível encontrar raiz nesse intervalo. "
                    "Verifique se f(a) e f(b) têm sinais opostos."
        }), 400

    resposta = {
        "metodo": "bissecao",
        "funcao": funcao_str,
        "a": a,
        "b": b,
        "tolerancia": tolerancia,
        "max_iter": max_iter,
        "raiz": raiz
    }

    return jsonify(resposta), 200


# =========================
# ROTA ELIMINAÇÃO DE GAUSS
# =========================
@app.route("/gauss", methods=["POST"])
def api_gauss():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Nenhum JSON foi enviado."}), 400

    matriz = data.get("matriz")
    usar_pivoteamento = bool(data.get("usar_pivoteamento", False))

    if matriz is None:
        return jsonify({"erro": "Matriz não informada."}), 400

    try:
        solucao, etapas, mensagem = eliminacao_gauss(matriz, usar_pivoteamento)
        residuos = verificar_solucao(matriz, solucao) if solucao is not None else None
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar eliminação de Gauss: {e}"}), 400

    return jsonify({
        "metodo": "gauss",
        "usar_pivoteamento": usar_pivoteamento,
        "mensagem": mensagem,
        "solucao": solucao,
        "etapas": etapas,
        "residuos": residuos
    }), 200


# =========================
# INICIAR SERVIDOR
# =========================
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import math

from derivada import derivada_numerica          # derivada numérica usada pelo Newton
from bissecao import bissecao                   # nossa versão adaptada para backend
from eliminacao_gauss import eliminacao_gauss, verificar_solucao

app = Flask(__name__)
CORS(app)  # libera CORS para todas as rotas


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

    funcao_str = data.get("funcao")
    x0 = float(data.get("x0"))
    tolerancia = float(data.get("tolerancia", 0.0001))
    max_iter = int(data.get("max_iter", 10))

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

    try:
        ambiente = {"__builtins__": None}
        ambiente.update(contexto)

        f = eval(f"lambda x: {funcao_str}", ambiente)
        f(1.0)  # teste rápido
    except Exception as e:
        return jsonify({"erro": f"Erro ao interpretar a função: {e}"}), 400

    resultado = newton_raphson(f, x0, tolerancia, max_iter)

    return jsonify({
        "metodo": "newton",
        "funcao": funcao_str,
        "x0": x0,
        "tolerancia": tolerancia,
        "max_iter": max_iter,
        **resultado
    })


# =========================
# ROTA BISSEÇÃO
# =========================
@app.route("/bissecao", methods=["POST"])
def api_bissecao():
    data = request.get_json()

    funcao_str = data.get("funcao")
    a = float(data.get("a"))
    b = float(data.get("b"))
    tolerancia = float(data.get("tolerancia", 0.0001))
    max_iter = int(data.get("max_iter", 50))

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

    try:
        ambiente = {"__builtins__": None}
        ambiente.update(contexto)

        f = eval(f"lambda x: {funcao_str}", ambiente)
        f(1.0)
    except Exception as e:
        return jsonify({"erro": f"Erro ao interpretar a função: {e}"}), 400

    resultado = bissecao(f, a, b, tolerancia, max_iter)

    return jsonify({
        "metodo": "bissecao",
        "funcao": funcao_str,
        "a": a,
        "b": b,
        "tolerancia": tolerancia,
        "max_iter": max_iter,
        **resultado
    })


# =========================
# ROTA ELIMINAÇÃO DE GAUSS
# =========================
@app.route("/gauss", methods=["POST"])
def api_gauss():
    data = request.get_json()

    # matriz aumentada [A|b], do jeitinho que seu código usa
    # ex para sistema: 2x + 3y = 8  ;  1x - 1y = 0
    # matriz = [[2, 3, 8],
    #           [1, -1, 0]]
    matriz = data.get("matriz")
    usar_pivoteamento = bool(data.get("usar_pivoteamento", False))

    if matriz is None:
        return jsonify({"erro": "Matriz não informada."}), 400

    # chama sua função
    solucao, etapas, mensagem = eliminacao_gauss(matriz, usar_pivoteamento)

    residuos = None
    if solucao is not None:
        residuos = verificar_solucao(matriz, solucao)

    return jsonify({
        "metodo": "gauss",
        "usar_pivoteamento": usar_pivoteamento,
        "mensagem": mensagem,
        "solucao": solucao,
        "etapas": etapas,
        "residuos": residuos
    })


if __name__ == "__main__":
    app.run(debug=True)

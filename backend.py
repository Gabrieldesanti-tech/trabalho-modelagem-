from flask import Flask, request, jsonify  # importa as classes/funções do Flask usadas no backend (servidor, acesso à requisição e resposta JSON). Se remover, qualquer uso de Flask, request ou jsonify vai dar erro NameError.
from flask_cors import CORS               # importa o CORS para liberar o acesso do front (HTML/JS) ao backend. Se remover, a função CORS não existirá e a linha CORS(app) vai quebrar.
import math                                # importa o módulo math, usado nas funções numéricas (exp, log, cos etc.). Se remover, qualquer chamada math.alguma_coisa dará erro.

# módulos auxiliares que você já tem:      # só comentário explicativo; removê-lo não muda nada no funcionamento.
# - derivada.py  → função derivada_numerica(f, x)  # comentário; sem efeito no código.
# - eliminacao_gauss.py → funcoes eliminacao_gauss(matriz, usar_pivoteamento)  # comentário; sem efeito.
#                          e verificar_solucao(matriz, solucao)
from derivada import derivada_numerica     # importa a função derivada_numerica usada no método de Newton. Se remover, newton_raphson não vai funcionar (NameError ao chamar derivada_numerica).
from eliminacao_gauss import eliminacao_gauss, verificar_solucao  # importa as funções de eliminação de Gauss e verificação de solução; se remover, a rota /gauss quebra ao tentar usá-las.

app = Flask(__name__)                      # cria a aplicação Flask (o servidor). Sem isso, não existe 'app' e nenhuma rota funciona.
CORS(app)  # libera CORS para o front (index.html aberto no navegador)  # aplica o CORS à aplicação, permitindo que o front (rodando em file:// ou outro host) chame a API; se remover, o navegador pode bloquear as requisições por CORS.

# =========================                # comentários de separação visual; sem impacto.
# FUNÇÃO BISSEÇÃO (direto no backend)
# =========================
def bissecao(funcao_str, a, b, tol=1e-6, max_iter=100):  # define a função de bisseção que recebe a função em texto, intervalo [a,b], tolerância e máximo de iterações. Se remover essa função, a rota /bissecao não conseguirá calcular a raiz.
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
    # docstring explicando a função; se remover, o código continua funcionando normalmente (é só documentação).

    def f(x):                               # define uma função interna f(x) que avalia a expressão que o usuário enviou. Se remover, não tem como calcular f(a), f(b) e f(c).
        contexto = {                        # cria um dicionário com as variáveis e funções permitidas dentro do eval. Sem isso, a expressão do usuário não teria acesso a math, e, pi, etc.
            "x": x,                         # disponibiliza a variável x dentro da expressão; sem isso, qualquer expressão que use x não funcionaria.
            "math": math,                   # permite usar math.alguma_coisa na expressão, se o usuário quiser.
            "e": math.e,                    # permite usar a constante 'e' diretamente; sem isso, 'e' não seria reconhecido.
            "pi": math.pi,                  # permite usar pi diretamente.
            "sin": math.sin,                # atalho para sin(x); sem isso, a expressão que usar sin vai falhar.
            "cos": math.cos,                # idem para cos(x).
            "tan": math.tan,                # idem para tan(x).
            "log": math.log,   # log natural # permite usar log(x) como ln(x).
            "exp": math.exp,                # permite exp(x) = e**x.
            "sqrt": math.sqrt,              # permite raiz quadrada.
            "log10": math.log10,            # permite log10(x).
        }
        return eval(funcao_str, {"__builtins__": {}}, contexto)  # avalia a string da função com um ambiente “seguro” (sem builtins) e o contexto definido. Se remover, a função não calcula nada e a bisseção não funciona.

    fa = f(a)                               # calcula f(a) no começo do algoritmo. Se remover, a condição de sinal e o laço não têm o valor de f(a).
    fb = f(b)                               # calcula f(b). Se remover, mesma coisa: a condição de existência de raiz não funciona.

    # condição de existência de raiz (mudança de sinal)
    if fa * fb >= 0:                        # verifica se f(a) e f(b) têm sinais opostos (produto < 0). Se remover, o método pode rodar em intervalos sem raiz ou com duas raízes, o que quebra a lógica.
        return None                         # se não tiver mudança de sinal, retorna None indicando erro. Sem esse return, cairia no laço e poderia dar resultados errados.

    for _ in range(1, max_iter + 1):        # laço que faz até max_iter iterações da bisseção. Se remover, o algoritmo nunca itera.
        c = (a + b) / 2                     # calcula o ponto médio do intervalo. Sem isso, não teria o novo candidato à raiz.
        fc = f(c)                           # calcula f(c). Sem isso, não consegue testar critério de parada nem atualizar o intervalo.

        # critério de parada
        if abs(fc) < tol or (b - a) / 2 < tol:  # verifica se f(c) está próximo de zero ou se o intervalo ficou suficientemente pequeno. Se remover, o método só pararia quando estourar max_iter.
            return c                        # retorna a raiz aproximada se o critério de parada for atingido. Se remover, o método não retorna quando deveria.

        # atualiza intervalo
        if fa * fc < 0:                     # se a raiz está entre a e c (mudança de sinal), atualiza o limite superior.
            b = c                           # novo limite superior passa a ser c.
            fb = fc                         # f(b) passa a ser f(c); sem isso, os testes seguintes usam valores velhos.
        else:
            a = c                           # caso contrário, a raiz está entre c e b, então atualiza o limite inferior.
            fa = fc                         # f(a) também passa a ser f(c).

    # se estourar o número máximo de iterações,
    # devolve o meio do último intervalo
    return (a + b) / 2                      # caso o laço termine sem atingir o critério de parada, retorna o meio do último intervalo como aproximação. Se remover, a função poderia terminar sem retorno (erro).

# =========================
# MÉTODO DE NEWTON-RAPHSON
# =========================
def newton_raphson(f, x_inicial, tolerancia=0.0001, max_iteracoes=10):  # define a função do método de Newton-Raphson; recebe f(x), chute inicial, tolerância e número máximo de iterações. Se remover, a rota /newton não tem como calcular nada.
    x = x_inicial                        # inicializa x com o valor inicial dado pelo usuário. Se remover, x não teria valor definido.
    iteracoes = 0                        # contador de iterações começa em 0. Se remover, o while não controla o número de passos corretamente.
    historico = [x]                      # guarda o primeiro valor de x no histórico. Se remover, você perde o registro dos valores usados.

    while iteracoes < max_iteracoes:     # laço que repete enquanto não atingir o máximo de iterações. Se remover, Newton não faria iterações.
        fx = f(x)                        # calcula f(x) no ponto atual. Sem isso, não tem como aplicar a fórmula de Newton.
        dx = derivada_numerica(f, x)     # calcula a derivada numérica em x. Se remover, não há dx pra dividir e a fórmula não funciona.

        if abs(dx) < 1e-10:              # verifica se a derivada está muito próxima de zero (risco de divisão por zero). Se remover, pode dividir por um número quase zero e explodir numericamente.
            return {
                "raiz": x,
                "iteracoes": iteracoes,
                "convergiu": False,
                "historico": historico,
                "mensagem": "Derivada muito próxima de zero"
            }                            # retorna um dicionário indicando que não convergiu por causa da derivada quase zero. Se remover esse return, o código continuaria e poderia dar erro.

        x_novo = x - fx / dx             # fórmula de Newton-Raphson para calcular a próxima aproximação. Se remover, x nunca é atualizado.
        historico.append(x_novo)         # adiciona o novo x no histórico. Se remover, você perde esse valor no registro.

        if abs(x_novo - x) < tolerancia:  # critério de parada: se a diferença entre x_novo e x for menor que a tolerância. Se remover, o método só pararia quando estourar o número de iterações.
            return {
                "raiz": x_novo,
                "iteracoes": iteracoes + 1,
                "convergiu": True,
                "historico": historico
            }                            # retorna o resultado quando converge. Se remover, o laço continuaria mesmo já tendo solução boa.

        x = x_novo                       # atualiza x para o novo valor e segue a próxima iteração. Se remover, x fica preso no mesmo valor e o método entra em loop ou não converge.
        iteracoes += 1                   # incrementa o contador de iterações. Se remover, o while nunca atinge o limite e pode entrar em loop infinito.

    return {
        "raiz": x,
        "iteracoes": iteracoes,
        "convergiu": False,
        "historico": historico,
        "mensagem": "Não convergiu no número máximo de iterações"
    }                                    # caso o laço termine por atingir o máximo de iterações, retorna o melhor x encontrado e indica que não convergiu totalmente. Se remover, a função pode acabar sem retorno.

# =========================
# ROTA NEWTON
# =========================
@app.route("/newton", methods=["POST"])  # define a rota /newton que responde a requisições HTTP POST. Se remover, o backend não terá endpoint para o método de Newton.
def api_newton():                       # função que será executada quando o front chamar /newton. Se remover, a rota não existe.
    data = request.get_json()           # lê o JSON enviado pelo front na requisição. Se remover, você não tem acesso aos dados da função, x0 etc.

    if not data:                        # verifica se nenhum JSON foi enviado.
        return jsonify({"erro": "Nenhum JSON foi enviado."}), 400  # retorna erro 400 se não veio nada. Se remover o if, vai dar erro mais pra frente tentando acessar campos de data None.

    try:
        funcao_str = data["funcao"]     # pega a string da função f(x) do JSON. Se remover, a função não será definida.
        x0 = float(data["x0"])          # pega o valor inicial x0 e converte para float. Se remover, x0 não existe pro Newton.
        tolerancia = float(data.get("tolerancia", 0.0001))  # lê a tolerância ou usa 0.0001 se não vier; se remover, sempre teria que usar um valor fixo ou dar erro.
        max_iter = int(data.get("max_iter", 10))            # lê max_iter ou usa 10 por padrão. Se remover, não controla o máximo de iterações.
    except (KeyError, TypeError, ValueError) as e:          # captura erros caso algum campo falte ou seja inválido.
        return jsonify({
            "erro": "Dados inválidos no corpo da requisição.",
            "detalhe": str(e)
        }), 400                      # retorna erro 400 dizendo que os dados são inválidos. Se remover o try/except, o servidor cai com erro 500 em vez de responder bonito.

    contexto = {                     # dicionário com funções e constantes matemáticas disponíveis para montar a função f(x).
        "math": math,
        "e": math.e,
        "pi": math.pi,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "sqrt": math.sqrt,
    }                                # se remover esse contexto, a expressão da função não teria acesso a essas funções/constantes.

    # monta a função f(x) a partir do texto
    try:
        ambiente = {"__builtins__": {}}  # cria um ambiente sem built-ins por segurança. Se remover, o eval teria acesso a funções perigosas.
        ambiente.update(contexto)        # adiciona o contexto de funções matemáticas nesse ambiente. Se remover, a expressão não conhece sin, cos, etc.
        f = eval(f"lambda x: {funcao_str}", ambiente)  # cria dinamicamente uma função lambda x: <expressão do usuário>. Se remover, não há f para passar ao Newton.
        f(1.0)  # teste rápido              # testa a função com x=1 pra garantir que a sintaxe é válida. Se remover, erros de expressão só vão aparecer dentro do Newton.
    except Exception as e:                  # captura qualquer erro de sintaxe ou execução da função.
        return jsonify({"erro": f"Erro ao interpretar a função: {e}"}), 400  # se der erro, responde com JSON de erro. Sem esse try, o servidor cai com 500.

    try:
        resultado = newton_raphson(f, x0, tolerancia, max_iter)  # chama o método de Newton-Raphson com os parâmetros convertidos. Se remover, a rota não calcula nada.
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar método de Newton-Raphson: {e}"}), 400  # se algo der errado dentro de newton_raphson, retorna erro amigável. Sem isso, o backend cai com 500.

    return jsonify({
        "metodo": "newton",          # informa no JSON qual método foi usado.
        "funcao": funcao_str,        # devolve a função usada.
        "x0": x0,                    # devolve o x inicial.
        "tolerancia": tolerancia,    # devolve a tolerância usada.
        "max_iter": max_iter,        # devolve o máximo de iterações.
        **resultado                  # espalha o dicionário retornado por newton_raphson (raiz, iteracoes, convergiu, historico, etc.). Se remover o **resultado, a resposta não teria os dados principais.
    }), 200                          # status HTTP 200 (sucesso). Se mudar pra outro código, o front pode interpretar como erro.

# =========================
# ROTA BISSEÇÃO
# =========================
@app.route("/bissecao", methods=["POST"])  # define a rota /bissecao para requisições POST. Se remover, o front não consegue chamar a bisseção.
def api_bissecao():                        # função que trata as requisições de bisseção. Se remover, a rota também some.
    data = request.get_json()              # lê o JSON enviado pelo front. Sem isso, não tem acesso a funcao, a, b etc.

    if not data:                           # verifica se não veio JSON.
        return jsonify({"erro": "Nenhum JSON foi enviado."}), 400  # responde erro 400 se estiver vazio. Sem isso, acesso a data[...] quebraria.

    try:
        funcao_str = data["funcao"]        # função como string.
        a = float(data["a"])               # limite inferior do intervalo.
        b = float(data["b"])               # limite superior do intervalo.
        tolerancia = float(data.get("tolerancia", 1e-6))  # tolerância, com padrão.
        max_iter = int(data.get("max_iter", 100))         # máximo de iterações, com padrão.
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({
            "erro": "Dados inválidos no corpo da requisição.",
            "detalhe": str(e)
        }), 400                            # trata erros de entrada. Sem o try/except, o servidor cai em erro 500.

    # teste rápido de sintaxe da função
    contexto_teste = {                     # contexto mínimo para testar a função (sem montar lambda).
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
        eval(funcao_str, {"__builtins__": {}}, contexto_teste)  # avalia só a expressão em x=1. Se remover, erros de sintaxe só aparecem dentro da bisseção.
    except Exception as e:
        return jsonify({"erro": f"Erro ao interpretar a função: {e}"}), 400  # devolve erro amigável se a expressão estiver errada.

    try:
        raiz = bissecao(funcao_str, a, b, tolerancia, max_iter)  # chama a função de bisseção implementada lá em cima. Se remover, a rota não calcula nada.
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar método da bisseção: {e}"}), 400  # captura erros internos e retorna JSON em vez de quebrar o servidor.

    if raiz is None:                       # verifica se a bisseção retornou None (intervalo inválido, sem mudança de sinal).
        return jsonify({
            "erro": "Não foi possível encontrar raiz nesse intervalo. "
                    "Verifique se f(a) e f(b) têm sinais opostos."
        }), 400                             # responde com erro explicando o problema. Se remover esse if, o front receberia raiz=None sem explicação.

    resposta = {
        "metodo": "bissecao",              # identifica o método usado.
        "funcao": funcao_str,              # devolve a função.
        "a": a,                            # devolve limite inferior.
        "b": b,                            # devolve limite superior.
        "tolerancia": tolerancia,          # devolve tolerância.
        "max_iter": max_iter,              # devolve máximo de iterações.
        "raiz": raiz                       # devolve a raiz encontrada.
    }

    return jsonify(resposta), 200          # responde com JSON e status 200. Se remover, a rota não retorna nada.

# =========================
# ROTA ELIMINAÇÃO DE GAUSS
# =========================
@app.route("/gauss", methods=["POST"])     # define a rota /gauss para requisições POST. Se remover, o método de Gauss não fica acessível.
def api_gauss():                           # função para tratar as chamadas de eliminação de Gauss. Se remover, a rota some.
    data = request.get_json()              # lê o JSON enviado com a matriz. Sem isso, não tem acesso aos dados do sistema.

    if not data:                           # verifica se o JSON veio vazio.
        return jsonify({"erro": "Nenhum JSON foi enviado."}), 400  # retorna erro 400 se não houver dados.

    matriz = data.get("matriz")            # lê a matriz aumentada [A|b] enviada pelo front.
    usar_pivoteamento = bool(data.get("usar_pivoteamento", False))  # flag para decidir se usa pivoteamento; padrão False (ou True, dependendo do front).

    if matriz is None:                     # se a matriz não foi enviada…
        return jsonify({"erro": "Matriz não informada."}), 400  # retorna erro informando o problema.

    try:
        solucao, etapas, mensagem = eliminacao_gauss(matriz, usar_pivoteamento)  # chama sua função de eliminação de Gauss. Se remover, a rota não resolve o sistema.
        residuos = verificar_solucao(matriz, solucao) if solucao is not None else None  # se houve solução, calcula os resíduos; se não, deixa None. Se remover, você perde essa verificação.
    except Exception as e:
        return jsonify({"erro": f"Erro ao executar eliminação de Gauss: {e}"}), 400  # trata qualquer erro interno da função de Gauss. Sem isso, o backend cai.

    return jsonify({
        "metodo": "gauss",                 # identifica o método usado.
        "usar_pivoteamento": usar_pivoteamento,  # informa se pivoteamento foi usado.
        "mensagem": mensagem,             # mensagem da função (sucesso, impossível, indeterminado, etc.).
        "solucao": solucao,               # vetor solução, se existir.
        "etapas": etapas,                 # lista de etapas textuais da eliminação.
        "residuos": residuos              # resíduos A·x - b para cada equação.
    }), 200                               # retorna JSON com status 200.

# =========================
# INICIAR SERVIDOR
# =========================
if __name__ == "__main__":                # garante que o servidor Flask só vai rodar se o arquivo for executado diretamente (e não importado de outro lugar). Se remover, ainda funciona ao rodar direto, mas é uma boa prática mantê-lo.
    app.run(debug=True)                   # inicia o servidor Flask em modo debug (recarrega sozinho e mostra erros detalhados). Se remover, nada sobe: o backend não inicia.

"""
Implementação do Método de Eliminação de Gauss para resolver sistemas de equações lineares.
Inclui as versões com e sem pivoteamento parcial.
"""

def criar_matriz(n):
    """
    Cria uma matriz n x n+1 preenchida com zeros.
    """
    return [[0.0] * (n + 1) for _ in range(n)]

def imprimir_matriz(matriz, nome="Matriz"):
    """
    Imprime uma matriz de forma organizada.
    """
    print(f"\n{nome}:")
    n = len(matriz)
    for i in range(n):
        print("[", end=" ")
        for j in range(n + 1):
            if j == n:
                print("|", end=" ")
            print(f"{matriz[i][j]:8.4f}", end=" ")
        print("]")

def copiar_matriz(matriz):
    """
    Cria uma cópia profunda de uma matriz.
    """
    return [linha[:] for linha in matriz]

def trocar_linhas(matriz, i, j):
    """
    Troca duas linhas de uma matriz.
    """
    matriz[i], matriz[j] = matriz[j], matriz[i]

def encontrar_pivo_maximo(matriz, i, n):
    """
    Encontra o maior elemento em valor absoluto na coluna i a partir da linha i.
    Retorna o índice da linha com o maior elemento.
    """
    max_i = i
    max_valor = abs(matriz[i][i])
    
    for k in range(i + 1, n):
        if abs(matriz[k][i]) > max_valor:
            max_valor = abs(matriz[k][i])
            max_i = k
    
    return max_i

def eliminacao_gauss(matriz, usar_pivoteamento=False):
    """
    Resolve um sistema de equações lineares usando o método de eliminação de Gauss.
    
    Parâmetros:
    matriz: matriz aumentada do sistema [A|b]
    usar_pivoteamento: se True, usa pivoteamento parcial
    
    Retorna:
    solucao: lista com as soluções do sistema
    etapas: lista com as etapas da eliminação
    status: mensagem indicando o status da resolução
    """
    n = len(matriz)
    etapas = []
    matriz_atual = copiar_matriz(matriz)
    etapas.append(copiar_matriz(matriz_atual))
    
    # Eliminação progressiva
    for i in range(n):
        if usar_pivoteamento:
            # Encontra o maior elemento na coluna atual
            max_i = encontrar_pivo_maximo(matriz_atual, i, n)
            if max_i != i:
                trocar_linhas(matriz_atual, i, max_i)
                etapas.append(copiar_matriz(matriz_atual))
        
        pivo = matriz_atual[i][i]
        if abs(pivo) < 1e-10:
            return None, etapas, "Sistema singular - sem solução única"
        
        # Eliminação dos elementos abaixo do pivô
        for j in range(i + 1, n):
            fator = matriz_atual[j][i] / pivo
            for k in range(i, n + 1):
                matriz_atual[j][k] -= fator * matriz_atual[i][k]
            
            if any(abs(matriz_atual[j][k]) > 1e-10 for k in range(n)):
                etapas.append(copiar_matriz(matriz_atual))
    
    # Retrosubstituição
    solucao = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(matriz_atual[i][j] * solucao[j] for j in range(i + 1, n))
        if abs(matriz_atual[i][i]) < 1e-10:
            return None, etapas, "Sistema singular - sem solução única"
        solucao[i] = (matriz_atual[i][n] - soma) / matriz_atual[i][i]
    
    return solucao, etapas, "Sistema resolvido com sucesso"

def analisar_matriz(matriz):
    """
    Analisa a matriz e sugere o melhor método de resolução.
    Retorna True se o pivoteamento parcial é recomendado.
    """
    n = len(matriz)
    max_elemento = 0
    min_diagonal = float('inf')
    
    for i in range(n):
        # Encontra o maior elemento em módulo na matriz
        for j in range(n):
            max_elemento = max(max_elemento, abs(matriz[i][j]))
        
        # Verifica o elemento da diagonal
        diag = abs(matriz[i][i])
        if diag < min_diagonal:
            min_diagonal = diag
    
    # Critérios para recomendar pivoteamento:
    # 1. Se houver elementos muito pequenos na diagonal
    # 2. Se houver grande diferença entre os elementos
    return min_diagonal < 1e-10 or min_diagonal < 0.01 * max_elemento

def verificar_solucao(matriz_original, solucao):
    """
    Verifica a solução calculada, computando os resíduos.
    """
    n = len(matriz_original)
    residuos = []
    
    for i in range(n):
        soma = sum(matriz_original[i][j] * solucao[j] for j in range(n))
        residuo = abs(soma - matriz_original[i][n])
        residuos.append(residuo)
    
    return residuos

if __name__ == "__main__":
    print("Resolução de Sistemas Lineares - Método de Eliminação de Gauss")
    
    
    try:
        # Entrada do tamanho do sistema
        n = int(input("\nDigite o número de equações do sistema: "))
        if n <= 0:
            raise ValueError("O número de equações deve ser positivo")
        
        # Escolha do método
        print("\nEscolha o método de resolução:")
        print("\n1 - Eliminação de Gauss com pivoteamento normal")
        print("   - Usa o primeiro elemento de cada coluna como pivô")
        print("   - Pivoteamento simples linha por linha")
        print("   - Adequado para a maioria dos sistemas")
        print("   - Processo mais direto de eliminação")
        
        print("\n2 - Eliminação de Gauss com pivoteamento parcial")
        print("   - Procura o maior elemento da coluna para usar como pivô")
        print("   - Mais estável numericamente")
        print("   - Minimiza erros de arredondamento")
        print("   - Recomendado para sistemas mal condicionados")
        print("   - Essencial quando há elementos muito pequenos na diagonal")
        
        opcao = int(input("\nDigite sua escolha (1 ou 2): "))
        if opcao not in [1, 2]:
            raise ValueError("Opção inválida")
        
        print("\nVocê escolheu:", end=" ")
        if opcao == 1:
            print("Eliminação de Gauss com pivoteamento normal")
            print("(Usa o primeiro elemento de cada coluna como pivô)")
        else:
            print("Eliminação de Gauss com pivoteamento parcial")
            print("(Procura o maior elemento da coluna para usar como pivô)")
        
        usar_pivoteamento = (opcao == 2)
        
        # Função auxiliar para mostrar a equação
        def mostrar_equacao(coeficientes):
            """Mostra a equação em formato matemático"""
            variaveis = ['x', 'y', 'z', 'w', 'v', 'u', 't', 's', 'r', 'p']  # para até 10 variáveis
            equacao = ""
            primeiro = True
            
            for i, coef in enumerate(coeficientes[:-1]):
                if coef == 0:
                    continue
                    
                if coef > 0 and not primeiro:
                    equacao += " + "
                elif coef < 0:
                    equacao += " - " if not primeiro else "-"
                    
                coef = abs(coef)
                if coef != 1 or i >= len(variaveis):
                    equacao += str(coef)
                if i < len(variaveis):
                    equacao += variaveis[i]
                else:
                    equacao += f"x{i+1}"
                    
                primeiro = False
                
            if not equacao:
                equacao = "0"
            
            equacao += f" = {coeficientes[-1]}"
            return equacao

        print("\nDigitação do Sistema de Equações")
     
        print("\nPara cada equação, digite os coeficientes separados por espaço")
        print("Exemplo: Para a equação 2x + 3y = 5, digite: 2 3 5")
        
        # Leitura da matriz aumentada [A|b]
        matriz = criar_matriz(n)
        print("\nSistema atual:")
        
        for i in range(n):
            print(f"\nEquação {i+1}:")
            if i > 0:
                print("\nEquações digitadas:")
                for j in range(i):
                    print(f"({j+1}) {mostrar_equacao(matriz[j])}")
            
            linha = input(f"\nDigite os coeficientes: ")
            valores = []
            
            try:
                valores = list(map(float, linha.split()))
                if len(valores) != n + 1:
                    raise ValueError(f"A equação deve ter {n+1} números (coeficientes + termo independente)")
                
                matriz[i] = valores
                print(f"Equação digitada: {mostrar_equacao(valores)}")
                
            except ValueError as e:
                print(f"\nErro: {e}")
                print("Digite novamente os coeficientes para esta equação.")
                i -= 1  # Repete a mesma equação
                continue
        
        print("\nSistema completo:")
     

        for i in range(n):
            print(f"({i+1}) {mostrar_equacao(matriz[i])}")
        
        # Análise da matriz e sugestão do método
        pivoteamento_recomendado = analisar_matriz(matriz)
        if pivoteamento_recomendado and not usar_pivoteamento:
            print("\nAVISO: Esta matriz pode se beneficiar do uso de pivoteamento parcial.")
            print("Você pode querer recomeçar e escolher a opção 2.")
            resposta = input("\nDeseja continuar mesmo assim? (s/n): ").lower()
            if resposta != 's':
                raise ValueError("Operação cancelada pelo usuário")
        
        # Resolve o sistema
        print("\nResolvendo o sistema...")
        solucao, etapas, mensagem = eliminacao_gauss(matriz, usar_pivoteamento)
        
        # Mostra os resultados
        print("\nEtapas da resolução:")
        for i, etapa in enumerate(etapas):
            imprimir_matriz(etapa, f"Etapa {i+1}")
        
        print(f"\n{mensagem}")
        
        if solucao is not None:
            print("\nSolução encontrada:")
            for i, xi in enumerate(solucao):
                print(f"x{i+1} = {xi:10.4f}")
            
            # Verifica a solução
            residuos = verificar_solucao(matriz, solucao)
            print("\nVerificação da solução :")
            for i, r in enumerate(residuos):
                print(f"Equação {i+1}: {r:10.4e}")
            
            if max(residuos) > 1e-10:
                print("\nAtenção: Resíduos grandes detectados!")
                if not usar_pivoteamento:
                    print("Sugestão: Tente usar o método com pivoteamento parcial")
        
    except ValueError as e:
        print(f"\nErro: {e}")
        print("Por favor, verifique os dados e tente novamente")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Por favor, tente novamente")

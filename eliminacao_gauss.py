"""
Implementação do Método de Eliminação de Gauss para resolver sistemas de equações lineares.
Inclui as versões com e sem pivoteamento parcial.
"""
# Comentário simples explicando o propósito do arquivo. Não afeta a execução.


def criar_matriz(n):                                      # Define a função que cria uma matriz n x (n+1)
    """
    Cria uma matriz n x n+1 preenchida com zeros.
    """
    return [[0.0] * (n + 1) for _ in range(n)]            # Gera a matriz aumentada [A|b] inicial cheia de 0


def imprimir_matriz(matriz, nome="Matriz"):               # Função que imprime a matriz formatada no terminal
    """
    Imprime uma matriz de forma organizada.
    """
    print(f"\n{nome}:")                                   # Imprime o nome da matriz (ex: Etapa 1)
    n = len(matriz)                                       # Obtém o número de linhas
    for i in range(n):                                    # Percorre cada linha
        print("[", end=" ")                               # Começo da linha visual
        for j in range(n + 1):                            # Percorre colunas, incluindo b (última)
            if j == n:                                    # Antes da última coluna...
                print("|", end=" ")                       # ...insere um separador visual "|"
            print(f"{matriz[i][j]:8.4f}", end=" ")        # Imprime cada elemento com 4 casas decimais
        print("]")                                        # Fecha a linha da impressão


def copiar_matriz(matriz):                                # Cria uma cópia profunda da matriz
    """
    Cria uma cópia profunda de uma matriz.
    """
    return [linha[:] for linha in matriz]                 # Copia cada linha isoladamente para evitar referência


def trocar_linhas(matriz, i, j):                          # Função que troca duas linhas da matriz
    """
    Troca duas linhas de uma matriz.
    """
    matriz[i], matriz[j] = matriz[j], matriz[i]           # Swap direto entre linhas i e j


def encontrar_pivo_maximo(matriz, i, n):                  # Localiza o maior elemento absoluto da coluna i
    """
    Encontra o maior elemento em valor absoluto na coluna i a partir da linha i.
    Retorna o índice da linha com o maior elemento.
    """
    max_i = i                                             # Começa assumindo que o maior valor está na linha atual
    max_valor = abs(matriz[i][i])                         # Valor absoluto do pivô inicial

    for k in range(i + 1, n):                             # Percorre as linhas abaixo da atual
        if abs(matriz[k][i]) > max_valor:                 # Se encontrar valor maior...
            max_valor = abs(matriz[k][i])                 # Atualiza o maior
            max_i = k                                     # Atualiza a linha onde está esse maior pivô

    return max_i                                          # Retorna o índice da linha com o maior pivô
def eliminacao_gauss(matriz, usar_pivoteamento=False):                       # Função principal que resolve o sistema pelo método de Gauss
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
    n = len(matriz)                                                          # Número de equações (n linhas da matriz)
    etapas = []                                                              # Lista onde serão salvas as matrizes de cada etapa do processo
    matriz_atual = copiar_matriz(matriz)                                    # Cria uma cópia da matriz original para não alterá-la diretamente
    etapas.append(copiar_matriz(matriz_atual))                              # Armazena a matriz inicial como primeira etapa
    
    # Eliminação progressiva
    for i in range(n):                                                      # Loop sobre as colunas/linhas pivotais (da linha 0 até n-1)
        if usar_pivoteamento:                                               # Se o pivoteamento parcial estiver ativado...
            # Encontra o maior elemento na coluna atual
            max_i = encontrar_pivo_maximo(matriz_atual, i, n)               # Procura a linha com o maior valor absoluto na coluna i
            if max_i != i:                                                  # Se essa linha não for a própria linha i...
                trocar_linhas(matriz_atual, i, max_i)                       # Troca a linha atual pela linha de maior pivô
                etapas.append(copiar_matriz(matriz_atual))                  # Registra essa troca como uma nova etapa
        
        pivo = matriz_atual[i][i]                                           # Pega o elemento da diagonal (pivô) na posição (i,i)
        if abs(pivo) < 1e-10:                                               # Se o pivô é praticamente zero...
            return None, etapas, "Sistema singular - sem solução única"     # Considera o sistema singular, sem solução única, e devolve as etapas feitas
        
        # Eliminação dos elementos abaixo do pivô
        for j in range(i + 1, n):                                           # Para cada linha abaixo da linha do pivô (i+1 até n-1)
            fator = matriz_atual[j][i] / pivo                               # Calcula o fator multiplicador para zerar o elemento da coluna i na linha j
            for k in range(i, n + 1):                                       # Percorre da coluna i até a última coluna (incluindo o termo independente)
                matriz_atual[j][k] -= fator * matriz_atual[i][k]            # Faz L_j = L_j - fator * L_i (operação típica de eliminação de Gauss)
            
            if any(abs(matriz_atual[j][k]) > 1e-10 for k in range(n)):      # Se ainda há algum elemento relevante na linha j (não virou tudo "quase zero")
                etapas.append(copiar_matriz(matriz_atual))                  # Registra a matriz após a eliminação dessa linha
    
    # Retrosubstituição
    solucao = [0.0] * n                                                     # Cria a lista que vai guardar a solução (x1, x2, ..., xn)
    for i in range(n - 1, -1, -1):                                          # Faz o loop de baixo para cima (da última linha até a primeira)
        soma = sum(matriz_atual[i][j] * solucao[j] for j in range(i + 1, n))# Calcula a soma dos termos já conhecidos na linha i (a_i,j * x_j para j > i)
        if abs(matriz_atual[i][i]) < 1e-10:                                 # Se o elemento da diagonal é quase zero nessa fase...
            return None, etapas, "Sistema singular - sem solução única"     # De novo considera sistema singular
        solucao[i] = (matriz_atual[i][n] - soma) / matriz_atual[i][i]       # Aplica a fórmula: x_i = (b_i - soma dos outros termos) / a_i,i
    
    return solucao, etapas, "Sistema resolvido com sucesso"                 # Retorna a solução, a lista de etapas e a mensagem de sucesso


def analisar_matriz(matriz):                                                # Função que analisa a matriz e sugere se é bom usar pivoteamento
    """
    Analisa a matriz e sugere o melhor método de resolução.
    Retorna True se o pivoteamento parcial é recomendado.
    """
    n = len(matriz)                                                         # Número de equações
    max_elemento = 0                                                        # Vai armazenar o maior valor absoluto encontrado na matriz
    min_diagonal = float('inf')                                             # Inicializa o menor valor da diagonal como infinito
    
    for i in range(n):                                                      # Percorre as linhas
        # Encontra o maior elemento em módulo na matriz
        for j in range(n):                                                  # Percorre as colunas (apenas A, não o termo independente)
            max_elemento = max(max_elemento, abs(matriz[i][j]))             # Atualiza o maior valor absoluto encontrado
        
        # Verifica o elemento da diagonal
        diag = abs(matriz[i][i])                                            # Valor absoluto do elemento diagonal a_i,i
        if diag < min_diagonal:                                             # Se for menor que o mínimo atual...
            min_diagonal = diag                                             # Atualiza o menor valor da diagonal
    
    # Critérios para recomendar pivoteamento:
    # 1. Se houver elementos muito pequenos na diagonal
    # 2. Se houver grande diferença entre os elementos
    return min_diagonal < 1e-10 or min_diagonal < 0.01 * max_elemento       # Retorna True se a diagonal for "fraca" em relação ao resto (pivoteamento recomendado)


def verificar_solucao(matriz_original, solucao):                            # Função que verifica quão boa é a solução calculando os resíduos
    """
    Verifica a solução calculada, computando os resíduos.
    """
    n = len(matriz_original)                                                # Número de equações
    residuos = []                                                           # Lista para guardar o resíduo de cada equação
    
    for i in range(n):                                                      # Para cada equação (linha i)
        soma = sum(matriz_original[i][j] * solucao[j] for j in range(n))    # Calcula A·x (lado esquerdo) para aquela equação
        residuo = abs(soma - matriz_original[i][n])                         # Resíduo = |A·x - b| para aquela linha
        residuos.append(residuo)                                            # Armazena o resíduo na lista
    
    return residuos                                                         # Retorna a lista de resíduos (um para cada equação)


if __name__ == "__main__":                                                 # Bloco que só é executado se rodar este arquivo diretamente (modo terminal)
    print("Resolução de Sistemas Lineares - Método de Eliminação de Gauss") # Mensagem inicial de apresentação
    
    
    try:                                                                    # Bloco try para capturar erros de entrada/execução
        # Entrada do tamanho do sistema
        n = int(input("\nDigite o número de equações do sistema: "))        # Pede ao usuário o número de equações (n)
        if n <= 0:                                                          # Se o usuário digitar zero ou negativo...
            raise ValueError("O número de equações deve ser positivo")      # Lança um erro de valor inválido
        
        # Escolha do método
        print("\nEscolha o método de resolução:")                           # Menu explicando as opções do método
        print("\n1 - Eliminação de Gauss com pivoteamento normal")          # Opção 1: Gauss sem pivoteamento parcial
        print("   - Usa o primeiro elemento de cada coluna como pivô")      # Explicação adicional
        print("   - Pivoteamento simples linha por linha")                  # Explicação adicional
        print("   - Adequado para a maioria dos sistemas")                  # Explicação adicional
        print("   - Processo mais direto de eliminação")                    # Explicação adicional
        
        print("\n2 - Eliminação de Gauss com pivoteamento parcial")         # Opção 2: Gauss com pivoteamento parcial
        print("   - Procura o maior elemento da coluna para usar como pivô")# Explicação adicional
        print("   - Mais estável numericamente")                            # Explicação adicional
        print("   - Minimiza erros de arredondamento")                      # Explicação adicional
        print("   - Recomendado para sistemas mal condicionados")           # Explicação adicional
        print("   - Essencial quando há elementos muito pequenos na diagonal") # Explicação adicional
        
        opcao = int(input("\nDigite sua escolha (1 ou 2): "))               # Lê a opção escolhida pelo usuário
        if opcao not in [1, 2]:                                             # Se a opção não for 1 nem 2...
            raise ValueError("Opção inválida")                              # Lança erro de valor inválido
        
        print("\nVocê escolheu:", end=" ")                                  # Começa a mostrar qual método foi escolhido (sem pular linha)
        if opcao == 1:                                                      # Se escolheu 1...
            print("Eliminação de Gauss com pivoteamento normal")            # Mostra a descrição da opção 1
            print("(Usa o primeiro elemento de cada coluna como pivô)")     # Detalhe adicional
        else:                                                               # Caso contrário, escolheu 2...
            print("Eliminação de Gauss com pivoteamento parcial")           # Mostra a descrição da opção 2
            print("(Procura o maior elemento da coluna para usar como pivô)") # Detalhe adicional
        
        usar_pivoteamento = (opcao == 2)                                    # Define a variável booleana com base na escolha do usuário
        
        # Função auxiliar para mostrar a equação
        def mostrar_equacao(coeficientes):                                  # Função interna que monta a equação em forma de texto
            """Mostra a equação em formato matemático"""
            variaveis = ['x', 'y', 'z', 'w', 'v', 'u', 't', 's', 'r', 'p']  # Nomes das variáveis para até 10 incógnitas
            equacao = ""                                                    # String que vai sendo montada com a equação
            primeiro = True                                                 # Flag para saber se é o primeiro termo (pra não colocar "+" indevido)
            
            for i, coef in enumerate(coeficientes[:-1]):                    # Percorre todos os coeficientes, menos o último (que é o termo independente)
                if coef == 0:                                               # Se o coeficiente for zero...
                    continue                                                # Pula, não escreve esse termo
                    
                if coef > 0 and not primeiro:                               # Se coeficiente positivo e não é o primeiro termo...
                    equacao += " + "                                        # Adiciona um " + "
                elif coef < 0:                                              # Se coeficiente negativo...
                    equacao += " - " if not primeiro else "-"               # Coloca sinal de menos, cuidando do caso se é o primeiro ou não
                    
                coef = abs(coef)                                            # Usa o valor absoluto para escrever o número (sinal já foi tratado)
                if coef != 1 or i >= len(variaveis):                        # Se o coeficiente não é 1, ou se já passou do número de variáveis padrão...
                    equacao += str(coef)                                    # Escreve o número do coeficiente
                if i < len(variaveis):                                      # Se ainda está dentro da lista de nomes padrão de variáveis...
                    equacao += variaveis[i]                                 # Adiciona o nome da variável correspondente (x, y, z, ...)
                else:                                                       # Se já passou do tamanho de 'variaveis'...
                    equacao += f"x{i+1}"                                    # Usa um nome genérico xN
                    
                primeiro = False                                            # Depois do primeiro termo, essa flag passa a False
                
            if not equacao:                                                 # Se nenhum termo foi adicionado (tudo zero)...
                equacao = "0"                                               # A equação é simplesmente "0"
            
            equacao += f" = {coeficientes[-1]}"                             # Adiciona o termo independente no formato "= b"
            return equacao                                                  # Retorna a string com a equação completa

        print("\nDigitação do Sistema de Equações")                         # Mensagem para início da digitação do sistema
     
        print("\nPara cada equação, digite os coeficientes separados por espaço") # Orientação de entrada
        print("Exemplo: Para a equação 2x + 3y = 5, digite: 2 3 5")         # Exemplo prático
        
        # Leitura da matriz aumentada [A|b]
        matriz = criar_matriz(n)                                            # Cria a matriz aumentada n x (n+1) preenchida com zeros
        print("\nSistema atual:")                                           # Cabeçalho
        
        for i in range(n):                                                  # Loop para cada equação
            print(f"\nEquação {i+1}:")                                      # Indica qual equação está sendo digitada
            if i > 0:                                                       # Se já houver equações anteriores digitadas...
                print("\nEquações digitadas:")                              # Cabeçalho para exibir equações já inseridas
                for j in range(i):                                         # Percorre as equações anteriores
                    print(f"({j+1}) {mostrar_equacao(matriz[j])}")          # Mostra cada equação anterior em formato bonito
            
            linha = input(f"\nDigite os coeficientes: ")                    # Pede ao usuário digitar os coeficientes da nova equação
            valores = []                                                    # Lista temporária para guardar os valores convertidos
            
            try:
                valores = list(map(float, linha.split()))                   # Converte cada valor digitado para float
                if len(valores) != n + 1:                                   # Se não tiver exatamente n+1 valores...
                    raise ValueError(f"A equação deve ter {n+1} números (coeficientes + termo independente)") # Erro de quantidade
                
                matriz[i] = valores                                         # Guarda a linha lida na matriz aumentada
                print(f"Equação digitada: {mostrar_equacao(valores)}")      # Mostra a mesma equação no formato matemático
                
            except ValueError as e:                                         # Trata erros de conversão ou de contagem de números
                print(f"\nErro: {e}")                                       # Mostra a mensagem de erro
                print("Digite novamente os coeficientes para esta equação.")# Pede para digitar de novo
                i -= 1                                                      # Faz o contador voltar uma unidade para repetir essa equação
                continue                                                    # Volta ao início do for para repetir a leitura
        
        print("\nSistema completo:")                                        # Mensagem final antes de exibir o sistema completo
     

        for i in range(n):                                                  # Percorre todas as equações
            print(f"({i+1}) {mostrar_equacao(matriz[i])}")                  # Mostra cada uma formatada
        
        # Análise da matriz e sugestão do método
        pivoteamento_recomendado = analisar_matriz(matriz)                  # Usa a função de análise para ver se pivoteamento parcial é recomendado
        if pivoteamento_recomendado and not usar_pivoteamento:              # Se pivoteamento é recomendado, mas o usuário não escolheu essa opção...
            print("\nAVISO: Esta matriz pode se beneficiar do uso de pivoteamento parcial.") # Aviso
            print("Você pode querer recomeçar e escolher a opção 2.")       # Sugestão
            resposta = input("\nDeseja continuar mesmo assim? (s/n): ").lower() # Pergunta se deseja continuar mesmo sem pivoteamento
            if resposta != 's':                                             # Se a resposta não for 's'...
                raise ValueError("Operação cancelada pelo usuário")         # Cancela a operação com um erro controlado
        
        # Resolve o sistema
        print("\nResolvendo o sistema...")                                  # Mensagem de status
        solucao, etapas, mensagem = eliminacao_gauss(matriz, usar_pivoteamento) # Chama a função principal de Gauss
        
        # Mostra os resultados
        print("\nEtapas da resolução:")                                     # Cabeçalho para as etapas
        for i, etapa in enumerate(etapas):                                  # Percorre as matrizes salvas em cada etapa
            imprimir_matriz(etapa, f"Etapa {i+1}")                          # Imprime cada matriz com um nome ("Etapa X")
        
        print(f"\n{mensagem}")                                              # Mostra a mensagem final (sucesso ou problema)
        
        if solucao is not None:                                             # Se existe solução (não é sistema singular)
            print("\nSolução encontrada:")                                  # Cabeçalho da solução
            for i, xi in enumerate(solucao):                                # Percorre cada variável
                print(f"x{i+1} = {xi:10.4f}")                               # Imprime x1, x2, ... xn com 4 casas decimais
            
            # Verifica a solução
            residuos = verificar_solucao(matriz, solucao)                   # Calcula os resíduos para cada equação
            print("\nVerificação da solução :")                             # Cabeçalho para a verificação
            for i, r in enumerate(residuos):                                # Percorre os resíduos
                print(f"Equação {i+1}: {r:10.4e}")                          # Imprime o resíduo em notação científica
            
            if max(residuos) > 1e-10:                                       # Se o maior resíduo for maior que um limite...
                print("\nAtenção: Resíduos grandes detectados!")            # Alerta de possível imprecisão
                if not usar_pivoteamento:                                   # Se não estava usando pivoteamento...
                    print("Sugestão: Tente usar o método com pivoteamento parcial") # Sugere tentar de novo com pivoteamento
        
    except ValueError as e:                                                 # Trata erros mais comuns (entrada inválida, cancelamento, etc.)
        print(f"\nErro: {e}")                                               # Mostra mensagem de erro
        print("Por favor, verifique os dados e tente novamente")            # Sugere revisar as entradas
    except Exception as e:                                                  # Captura qualquer erro inesperado
        print(f"\nErro inesperado: {e}")                                    # Mostra erro inesperado
        print("Por favor, tente novamente")                                 # Sugere tentar de novo

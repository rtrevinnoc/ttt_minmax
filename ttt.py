import random, time, signal, sys

# Declarar simbolos para el jugador y la ia
player, opponent = 'x', 'o' 
  
# Funcion para determinar si quedan casillas por rellenar
def isMovesLeft(board) : 
  
    for i in range(3) :
        for j in range(3) :
            if (board[i][j] == '_') :
                return True 
    return False
  
def evaluate(b) : 
    
    # Verificar si algun jugador ha llenado alguna de las filas
    for row in range(3) :     
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]) :        
            if (b[row][0] == player) :
                return 10
            elif (b[row][0] == opponent) :
                return -10
  
    # Verificar si algun jugador ha llenado alguna de las columnas
    for col in range(3) :
       
        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]) :
          
            if (b[0][col] == player) : 
                return 10
            elif (b[0][col] == opponent) :
                return -10
  
    # Verificar si algun jugador ha llenado alguna de las diagonales
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) :
      
        if (b[0][0] == player) :
            return 10
        elif (b[0][0] == opponent) :
            return -10
  
    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) :
      
        if (b[0][2] == player) :
            return 10
        elif (b[0][2] == opponent) :
            return -10

    return 0

# Profundidad maxima de minimax
MAX_DEPTH = 9
  
def minimax(board, depth, isMax) : 
    # print("###=>", depth)
    # Verificar el estado del tablero
    score = evaluate(board)
  
    # Regresar el puntaje calculado si hay un ganador o se ha llegado a la profundidad maxima
    if (score == 10) or (score == -10) or (depth == MAX_DEPTH): 
        return score
  
    # Empate si no hay ganador y ya no hay espacios disponibles
    if (isMovesLeft(board) == False) :
        return 0
  
    # Si se trata del jugador a maximizar
    if (isMax) :     
        best = -1000 
  
        # Recorrer todo el tablero
        for i in range(3) :         
            for j in range(3) :
               
                # Checar si la celda esta disponible
                if (board[i][j]=='_') :
                  
                    # Marcarla con el jugador a maximizar
                    board[i][j] = player 
  
                    # Volver a ejecutar Minimax desde este punto de forma recursiva 
                    best = max( best, minimax(board,
                                              depth + 1,
                                              not isMax) )
  
                    # Regresar el tablero a su valor anterior
                    board[i][j] = '_'
        return best
  
    # Para el jugador a minimizar
    else :
        best = 1000 
  
        # Recorrer todo el tablero
        for i in range(3) :         
            for j in range(3) :
               
                # Verificar la disponibilidad de la celda
                if (board[i][j] == '_') :
                  
                    # Ejecutar el movimiento con el jugador a minimizar
                    board[i][j] = opponent 
  
                    # Volver a ejecutar Minimax de forma recursiva a partir de este movimiento
                    best = min(best, minimax(board, depth + 1, not isMax))
  
                    # Deshacer el movimiento
                    board[i][j] = '_'
        return best
  
# Calcular el mejor movimiento para el tablero actual
def findBestMove(board) : 
    bestVal = -1000 
    bestMove = (-1, -1) 
  
    # Recorrer todo el tablero
    for i in range(3) :     
        for j in range(3) :
          
            # Verificar que la celda este disponible
            if (board[i][j] == '_') : 
              
                # Realizra el movimiento
                board[i][j] = player
  
                # Calcular el valor mediante el algoritmo de Minimax para ese movimiento
                moveVal = minimax(board, 0, False) 
  
                # Deshacer el movimiento
                board[i][j] = '_' 
  
                # Si el resultado obtenido supera lo conocido, actualizarlo
                if (moveVal > bestVal) :                
                    bestMove = (i, j)
                    bestVal = moveVal
  
    return bestMove
  
# Loop para obtener un movimiento del oponente
def get_move(board):
    while True:
        try:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter column (0-2): "))
            if board[row][col] != '_':
                print("That cell is already occupied. Try again.")
                continue
            return row, col
        except ValueError:
            print("Invalid input. Try again.")
        except IndexError:
            print("Row and column should be between 0 and 2. Try again.")

def print_board(board):
    for lst in board:
        print(*lst)

# Loop principal para la ejecucion del juego
def play_game():
    board = [
        [ '_', '_', '_' ], 
        [ '_', '_', '_' ], 
        [ '_', '_', '_' ] 
    ]
    times = []
    print_board(board)
    cur = opponent

    def results():
        print("######################################")
        print(times)
        print("IA movements: ", len(times))
        print("IA avg movement time: ", sum(times)/len(times))
        print("######################################")

    def signal_handler(_signal, _frame):
        results()
        sys.exit(0)

    while isMovesLeft(board):
        if cur == player:
            # it's the player X's turn
            print("Player X's turn")
            row, col = get_move(board)
            board[row][col] = player
            cur = opponent
        else:
            # it's the player O's turn
            print("Player O's turn")
            start = time.time()
            row, col = findBestMove(board)
            end = time.time()
            times.append(end - start)
            board[row][col] = opponent
            cur = player
        print_board(board)

        signal.signal(signal.SIGINT, signal_handler)
        
        if (evaluate(board) == 10):
            print("\nx wins")
            break
        elif (evaluate(board) == -10):
            print("\no wins")
            break

    results()

play_game()

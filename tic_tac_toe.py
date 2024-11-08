"""
Jogo da Veia
"""

class TicTacToe():

    def __init__(self, player_symbol):
        # Inicializa lista de simbolos
        self.symbol_list = []

        # Define todos os 9 simbolos. Todos começando em branco  
        for i in range(9):
            self.symbol_list.append(" ") 

        # Inicia o simbolo do player
        self.player_symbol = player_symbol


    def restart(self):
        # Limpa a matriz
        for i in range(9):
            self.symbol_list[i] = " "


    def draw_grid(self):
        # Mostra o cabeçalho das colunas
        print("\n       A   B   C\n")
        
        # Exibe a primeira linha
        row_one = "   1   " + self.symbol_list[0]
        row_one += " ║ " + self.symbol_list[1]
        row_one += " ║ " + self.symbol_list[2]
        print(row_one)

        print("      ═══╬═══╬═══")

        # Exibe a segunda linha 
        row_two = "   2   " + self.symbol_list[3]
        row_two += " ║ " + self.symbol_list[4]
        row_two += " ║ " + self.symbol_list[5]
        print(row_two)

        print("      ═══╬═══╬═══")

        # Exibe a terceira e ultima linha 
        row_three = "   3   " + self.symbol_list[6]
        row_three += " ║ " + self.symbol_list[7]
        row_three += " ║ " + self.symbol_list[8]
        print(row_three, "\n")

    def is_valid_move(self, grid_coord):
        # Troca as coordenadas de "1A" para "A1" se necessário
        if grid_coord[0].isdigit():
            grid_coord = grid_coord[1] + grid_coord[0]

        # Divide as coordenadas
        col = grid_coord[0].capitalize()
        row = grid_coord[1]

        # Converte "A1" para 0, "C3" para 8, e assim por diante
        grid_index = 0

        if row == "1":
            if col == "A":
                grid_index = 0
            elif col == "B":
                grid_index = 1
            elif col == "C":
                grid_index = 2
        elif row == "2":
            if col == "A":
                grid_index = 3
            elif col == "B":
                grid_index = 4
            elif col == "C":
                grid_index = 5
        elif row == "3":
            if col == "A":
                grid_index = 6
            elif col == "B":
                grid_index = 7
            elif col == "C":
                grid_index = 8
        else:
            return False  # Coordenada inválida

        # Verifica se a posição já está ocupada
        return self.symbol_list[grid_index] == " "

    def edit_square(self, grid_coord):
        # Troca as cordenadas de "1A" para "A1"
        if grid_coord[0].isdigit():
            grid_coord = grid_coord[1] + grid_coord[0]

        # Divide as cordenadas
        col = grid_coord[0].capitalize()
        row = grid_coord[1]

        # Converte "A1" para 0, "C3" para 8, e assim por diante 
        grid_index = 0

        if row == "1":
            if col == "A":
                grid_index = 0
            elif col == "B":
                grid_index = 1
            elif col == "C":
                grid_index = 2
        elif row == "2":
            if col == "A":
                grid_index = 3
            elif col == "B":
                grid_index = 4
            elif col == "C":
                grid_index = 5
        elif row == "3":
            if col == "A":
                grid_index = 6
            elif col == "B":
                grid_index = 7
            elif col == "C":
                grid_index = 8

        # Verifica se a posição já foi ocupada
        if self.symbol_list[grid_index] == " ":
            self.symbol_list[grid_index] = self.player_symbol
            return True  # Movimento bem sucedido
        else:
            return False  # Position already occupied


    def update_symbol_list(self, new_symbol_list):
        for i in range(9):
            self.symbol_list[i] = new_symbol_list[i]


    def did_win(self, player_symbol):
        # local variable to replace unweildy self.symbol_list
        g = []
        for i in range(9):
            g.append(self.symbol_list[i])

        # likewise to replace self.player_symbol 
        sym = player_symbol

        # check top row 
        if g[0] == sym and g[1] == sym and g[2] == sym:
            return True

        # check middle row
        elif g[3] == sym and g[4] == sym and g[5] == sym:
            return True
        
        # check bottom row 
        elif g[6] == sym and g[7] == sym and g[8] == sym:
            return True 

        # check left column 
        elif g[0] == sym and g[3] == sym and g[6] == sym:
            return True 

        # check middle column 
        elif g[1] == sym and g[4] == sym and g[7] == sym:
            return True 

        # check right column 
        elif g[2] == sym and g[5] == sym and g[8] == sym:
            return True

        # check top-right to bottom-left 
        elif g[2] == sym and g[4] == sym and g[6] == sym:
            return True 

        # check top-left to bottom-right 
        elif g[0] == sym and g[4] == sym and g[8] == sym:
            return True 

        # didn't win... yet! 
        return False


    def is_draw(self):
        # see if all the spaces are used up 
        num_blanks = 0
        for i in range(9):
                if self.symbol_list[i] == " ":
                    num_blanks += 1

        # if the player didn't win and no spaces are left, it's a draw
        if self.did_win(self.player_symbol) == False and num_blanks == 0:
            return True
        else:
            return False

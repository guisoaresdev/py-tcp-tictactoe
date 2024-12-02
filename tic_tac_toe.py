class TicTacToe:
    """
    Classe que representa o jogo da velha.
    """
    def __init__(self, player_symbol):
        self.symbol_list = [" "] * 9
        self.player_symbol = player_symbol

    def restart(self):
        self.symbol_list = [" "] * 9

    def draw_grid(self):
        print("\n       A   B   C\n")
        print(f"   1   {self.symbol_list[0]} ║ {self.symbol_list[1]} ║ {self.symbol_list[2]}")
        print("      ═══╬═══╬═══")
        print(f"   2   {self.symbol_list[3]} ║ {self.symbol_list[4]} ║ {self.symbol_list[5]}")
        print("      ═══╬═══╬═══")
        print(f"   3   {self.symbol_list[6]} ║ {self.symbol_list[7]} ║ {self.symbol_list[8]}\n")

    def is_valid_move(self, grid_coord):
        try:
            # Normaliza para aceitar "B2" ou "2B"
            if grid_coord[0].isdigit():  # Se o primeiro caractere for número, inverter
                row, col = int(grid_coord[0]), grid_coord[1].upper()
            else:
                col, row = grid_coord[0].upper(), int(grid_coord[1])

            # Valida a coordenada
            if 'A' <= col <= 'C' and 1 <= row <= 3:
                index = (row - 1) * 3 + (ord(col) - ord('A'))
                return self.symbol_list[index] == ' '
        except (IndexError, ValueError):
            return False

    def edit_square(self, grid_coord, symbol):
        index = self._convert_to_index(grid_coord)
        if self.symbol_list[index] == " ":
            self.symbol_list[index] = symbol
            return True
        return False

    def update_symbol_list(self, new_symbol_list):
        self.symbol_list = new_symbol_list[:]

    def did_win(self, player_symbol):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Linhas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Colunas
            (0, 4, 8), (2, 4, 6)              # Diagonais
        ]
        return any(all(self.symbol_list[i] == player_symbol for i in combo) for combo in combos)

    def is_draw(self):
        return " " not in self.symbol_list and not self.did_win(self.player_symbol)

    def _convert_to_index(self, grid_coord):
        try:
            if len(grid_coord) == 2:
                print(f"Coordenada recebida: {grid_coord}")
                # Verifica se a coordenada está no formato "A1" ou "1A"
                if grid_coord[0].isalpha() and grid_coord[1].isdigit():  # Formato "A1"
                    row = int(grid_coord[1]) - 1
                    col = ord(grid_coord[0].upper()) - ord('A')
                elif grid_coord[1].isalpha() and grid_coord[0].isdigit():  # Formato "1A"
                    row = int(grid_coord[0]) - 1
                    col = ord(grid_coord[1].upper()) - ord('A')
                else:
                    raise ValueError("Formato inválido")

                # Verifica se a coordenada está dentro dos limites (0-2 para linha e coluna)
                if 0 <= row < 3 and 0 <= col < 3:
                    print(f"Coluna: {col}, Linha: {row}")
                    index = row * 3 + col
                    print(f"Índice calculado: {index}")
                    return index
                else:
                    raise ValueError("Coordenadas fora do limite")
        except (IndexError, ValueError) as e:
            print(f"Erro ao converter coordenadas: {e}")
            return None

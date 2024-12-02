import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'
PORT = 12783

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Conectado ao servidor! Aguardando o início do jogo...")

# Recebe o símbolo do jogador (X ou O) do servidor
data = client_socket.recv(2048)
player_symbol = pickle.loads(data)
print(f"Recebido símbolo do servidor: {player_symbol}")
client_game = TicTacToe(player_symbol)  # Inicializa o jogo com o símbolo recebido

while True:
    try:
        data = client_socket.recv(2048)
        if not data:
            break

        message = pickle.loads(data)

        if isinstance(message, list):
            # Atualiza o tabuleiro se for uma lista de símbolos
            client_game.update_symbol_list(message)
            client_game.draw_grid()

        elif isinstance(message, str):
            # Lógica do que o cliente faz ao receber mensagens
            if message == "Sua vez":
                while True:
                    move = input("Sua jogada (exemplo: A1, B2): ")
                    if not client_game.is_valid_move(move):
                        print("Movimento inválido, tente novamente")
                        continue
                    client_socket.sendall(pickle.dumps(move))
                    resposta = pickle.loads(client_socket.recv(2048))

                    if resposta == "Movimento inválido, tente novamente":
                        print(resposta)
                    else:
                        break  # Sai do loop se o movimento for válido

            elif message in ["win", "lose", "draw"]:
                print(f"Resultado: {message.capitalize()}!")

            elif message == "rematch":
                # Pergunta se o jogador quer revanche
                rematch = input("Deseja uma revanche? (Y/N): ").upper()
                client_socket.sendall(pickle.dumps(rematch))

                if rematch == "Y":
                    print("Revanche iniciada!")
                    continue  # Continua o loop e reinicia o jogo
                else:
                    print("Obrigado por jogar!")
                    break  # Encerra o loop e fecha o jogo

    except Exception as e:
        print(f"Erro de conexão: {e}")
        break

# Fecha a conexão do cliente quando o jogo terminar
client_socket.close()

import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'
PORT = 12783

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Conectado ao servidor! Aguardando o início do jogo...")

client_game = None

while True:
    try:
        data = client_socket.recv(1024)
        if not data:
            break
        message = pickle.loads(data)

        if isinstance(message, list):
            if client_game is None:
                client_game = TicTacToe("X")
            client_game.update_symbol_list(message)
            client_game.draw_grid()

        elif isinstance(message, str):
            if message == "Sua vez":
                while True:
                    move = input("Sua jogada (exemplo: A1, B2): ")
                    client_socket.sendall(pickle.dumps(move))
                    
                    # Recebe a confirmação se o movimento foi válido ou não
                    resposta = pickle.loads(client_socket.recv(1024))
                    if resposta == "Movimento inválido, tente novamente":
                        print(resposta)
                    else:
                        client_game.edit_square(move)
                        client_game.draw_grid()
                        break

            elif message == "win":
                print("Parabéns! Você venceu!")
            
            elif message == "lose":
                print("Você perdeu. Boa sorte na próxima!")
            
            elif message == "draw":
                print("O jogo terminou em empate!")
            
            elif message == "rematch":
                print("Recebido pedido de revanche do servidor.")
                rematch = input("Deseja uma revanche? (Y/N): ").upper()
                print(f"Enviando resposta de rematch: {rematch}")
                client_socket.sendall(pickle.dumps(rematch))
                if rematch != "Y":
                    print("Obrigado por jogar!")
                    break
            else:
                print(message)
    except EOFError:
        print("Conexão com o servidor encerrada.")
        break

client_socket.close()

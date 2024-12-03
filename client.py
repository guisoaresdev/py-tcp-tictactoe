import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'
PORT = 12783


def recv_with_length(sock):
    length_data = sock.recv(4)
    if not length_data:
        return None
    length = int.from_bytes(length_data, byteorder='big')
    data = b""
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data += packet
    return pickle.loads(data)


def send_with_length(sock, message):
    data = pickle.dumps(message)
    length = len(data)
    sock.sendall(length.to_bytes(4, byteorder='big') + data)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Conectado ao servidor! Aguardando o início do jogo...")

player_symbol = recv_with_length(client_socket)
print(f"Recebido símbolo do servidor: {player_symbol}")
client_game = TicTacToe(player_symbol)

while True:
    try:
        message = recv_with_length(client_socket)
        if not message:
            break

        if isinstance(message, list):
            client_game.update_symbol_list(message)
            client_game.draw_grid()

        elif isinstance(message, str):
            if message == "Sua vez":
                while True:
                    move = input("Sua jogada (exemplo: A1, B2): ")
                    if not client_game.is_valid_move(move):
                        print("Movimento inválido, tente novamente")
                        continue
                    send_with_length(client_socket, move)
                    response = recv_with_length(client_socket)

                    if response == "Movimento inválido, tente novamente!":
                        print(response)
                    else:
                        break

            if message in ["win", "lose", "draw"]:
                print(f"Resultado: {message.capitalize()}!")

            if message == "rematch":
                rematch = input("Deseja uma revanche? (Y/N): ").upper()
                send_with_length(client_socket, rematch)

                if rematch == "Y":
                    print("Aguardando resposta do outro jogador...")
                    continue
                else:
                    print("Obrigado por jogar!")
                    break

    except Exception as e:
        print(f"Erro de conexão: {e}")
        break

client_socket.close()

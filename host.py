import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'
PORT = 12783

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

print("Aguardando jogadores...")
connections = []
addresses = []
players = ['X', 'O']


def send_with_length(conn, message):
    data = pickle.dumps(message)
    length = len(data)
    conn.sendall(length.to_bytes(4, byteorder='big') + data)


def receive_with_length(conn):
    length_data = conn.recv(4)
    if not length_data:
        return None
    length = int.from_bytes(length_data, byteorder='big')
    data = b""
    while len(data) < length:
        packet = conn.recv(length - len(data))
        if not packet:
            return None
        data += packet
    return pickle.loads(data)


while len(connections) < 2:
    conn, addr = server_socket.accept()
    connections.append(conn)
    addresses.append(addr)
    print(f"Jogador {len(connections)} conectado: {addr}")
    send_with_length(conn, players[len(connections) - 1])
    print(f"Jogador {len(connections)} atribuído ao símbolo: {players[len(connections) - 1]}")

game = TicTacToe(players[0])
current_player = 0


def send_to_all(message):
    for conn in connections:
        send_with_length(conn, message)


running = True

while running:
    send_to_all(game.symbol_list)

    current_conn = connections[current_player]
    send_with_length(current_conn, "Sua vez")

    move = receive_with_length(current_conn)
    if not move:
        print(f"Jogador {current_player + 1} desconectado.")
        running = False
        break

    if not game.is_valid_move(move):
        send_with_length(current_conn, "Movimento inválido, tente novamente!")
        continue

    valid_move = game.edit_square(move, players[current_player])
    if not valid_move:
        send_with_length(current_conn, "Movimento inválido, tente novamente!")
        continue
    send_to_all(game.symbol_list)

    if game.did_win(players[current_player]):
        send_to_all(game.symbol_list)
        send_with_length(current_conn, "win")
        send_with_length(connections[1 - current_player], "lose")
        send_to_all("rematch")

        rematch_responses = [receive_with_length(conn) == "Y" for conn in connections if conn]
        if all(rematch_responses):
            print("Revanche iniciada!")
            game.restart()
            current_player = 0
            continue
        else:
            print("Partida encerrada.")
            running = False
            break

    elif game.is_draw():
        send_to_all(game.symbol_list)
        send_to_all("draw")
        send_to_all("rematch")

        rematch_responses = [receive_with_length(conn) == "Y" for conn in connections if conn]
        if all(rematch_responses):
            print("Revanche iniciada!")
            game.restart()
            current_player = 0
            continue
        else:
            print("Partida encerrada.")
            running = False
            break

    current_player = 1 - current_player

server_socket.close()

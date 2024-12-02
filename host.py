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
players = ['X', 'O']  # Lista de símbolos para os jogadores

while len(connections) < 2:
    conn, addr = server_socket.accept()
    connections.append(conn)
    addresses.append(addr)
    print(f"Jogador {len(connections)} conectado: {addr}")
    conn.sendall(pickle.dumps(players[len(connections) - 1]))  # Envia o símbolo para o jogador
    print(f"Jogador {len(connections)} atribuído ao símbolo: {players[len(connections) - 1]}")

# Instanciar o jogo com o primeiro símbolo (jogador 1)
game = TicTacToe(players[0])  # 'X' para o primeiro jogador

current_player = 0


def send_to_all(message):
    for conn in connections:
        conn.sendall(pickle.dumps(message))


def receive_input(conn):
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            return data
        except:
            return None


running = True

while running:
    send_to_all(game.symbol_list)

    current_conn = connections[current_player]
    current_conn.sendall(pickle.dumps("Sua vez"))

    move = receive_input(current_conn)
    if not move:
        print(f"Jogador {current_player + 1} desconectado.")
        running = False
        break

    if not game.is_valid_move(move):
        current_conn.sendall(pickle.dumps("Movimento inválido. Use o formato A1, B2, etc..."))
        continue;
    valid_move = game.edit_square(move, players[current_player])
    current_conn.sendall(pickle.dumps("Movimento inválido, tente novamente" if not valid_move else "OK"))

    if game.did_win(players[current_player]) or game.is_draw():
        send_to_all(game.symbol_list)
        send_to_all("rematch")  # Send rematch message to both clients

        rematch_responses = []
        for conn in connections:
            response = receive_input(conn)
            if response is None:
                print(f"Jogador {connections.index(conn) + 1} desconectado.")
                running = False
                break  # Stop the game loop if a player disconnects
            rematch_responses.append(response == "Y")

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

        rematch_responses = []
        for conn in connections:
            response = receive_input(conn)
            rematch_responses.append(response == "Y")

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

import socket
import pickle
import time
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'
PORT = 12783

# Configura o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

print("Aguardando conexões dos dois jogadores...")

# Aceita as conexões dos dois jogadores
client1_socket, client1_address = server_socket.accept()
print(f"Jogador 1 conectado: {client1_address}")
client2_socket, client2_address = server_socket.accept()
print(f"Jogador 2 conectado: {client2_address}")

# Inicializa os jogos para os jogadores
player1_game = TicTacToe("X")
player2_game = TicTacToe("O")

def enviar_tabuleiro():
    client1_socket.sendall(pickle.dumps(player1_game.symbol_list))
    client2_socket.sendall(pickle.dumps(player1_game.symbol_list))

def enviar_para_ambos(mensagem):
    print(f"Enviando para ambos os clientes: {mensagem}")
    client1_socket.sendall(pickle.dumps(mensagem))
    client2_socket.sendall(pickle.dumps(mensagem))

rematch = True

while rematch:
    # Reinicia o jogo no início de uma nova partida
    player1_game.restart()
    player2_game.update_symbol_list(player1_game.symbol_list)
    enviar_tabuleiro()
    
    game_over = False
    turn = 0

    while not game_over:
        current_socket = client1_socket if turn == 0 else client2_socket
        other_socket = client2_socket if turn == 0 else client1_socket
        current_symbol = "X" if turn == 0 else "O"
        current_game = player1_game if turn == 0 else player2_game

        try:
            current_socket.sendall(pickle.dumps("Sua vez"))
        except Exception as e:
            print(f"Erro ao enviar mensagem ao jogador: {e}")
            game_over = True
            break

        while True:
            try:
                # Recebe o movimento do jogador
                move = pickle.loads(current_socket.recv(2048))  # Aumenta o buffer de recebimento

                # Verifica se o movimento é válido
                if not current_game.is_valid_move(move):
                    current_socket.sendall(pickle.dumps("Movimento inválido, tente novamente"))
                else:
                    current_game.edit_square(move)
                    break
            except Exception as e:
                print(f"Erro ao receber movimento do jogador: {e}")
                game_over = True
                break

        if game_over:
            break

        # Atualiza o tabuleiro para ambos os jogadores
        player1_game.update_symbol_list(current_game.symbol_list)
        player2_game.update_symbol_list(current_game.symbol_list)
        enviar_tabuleiro()

        # Verifica se há um vencedor ou empate
        if current_game.did_win(current_symbol):
            try:
                current_socket.sendall(pickle.dumps("win"))
                other_socket.sendall(pickle.dumps("lose"))
            except Exception as e:
                print(f"Erro ao enviar mensagem de vitória/derrota: {e}")
            game_over = True
        elif current_game.is_draw():
            enviar_para_ambos("draw")
            game_over = True

        turn = 1 - turn

    time.sleep(1)

    # Após o término do jogo, pergunta sobre revanche
    enviar_para_ambos("rematch")
    print("Perguntando sobre rematch...")  # Debug

    try:
        rematch_client1 = pickle.loads(client1_socket.recv(2048))  # Aumenta o buffer de recebimento
        rematch_client2 = pickle.loads(client2_socket.recv(2048))

        print(f"Respostas para rematch: Jogador 1 - {rematch_client1}, Jogador 2 - {rematch_client2}")

        rematch = rematch_client1.upper() == "Y" and rematch_client2.upper() == "Y"
    except EOFError:
        print("Um dos clientes encerrou a conexão. Encerrando o servidor.")
        break
    except Exception as e:
        print(f"Ocorreu um erro ao processar as respostas dos jogadores: {e}")
        break

print("Jogo encerrado.")
client1_socket.close()
client2_socket.close()
server_socket.close()

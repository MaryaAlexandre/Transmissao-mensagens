import socket

HOST =  'localhost'
TCP_PORT = 5050
UDP_PORT = 5051

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((HOST, TCP_PORT))
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', UDP_PORT))

print("Bem-vindo ao jogo de perguntas! 🧠\nResponda com A, B ou C.\n")


for i in range(1, 4):
    resposta = input(f"Sua resposta para a pergunta {i}: ").strip().upper()
    tcp_socket.send(resposta.encode())  

    resultado, _ = udp_socket.recvfrom(1024)
    print(f"Servidor diz: {resultado.decode()}")

print("\nObrigado por jogar! 🎉")
tcp_socket.close()
udp_socket.close()


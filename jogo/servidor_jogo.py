import socket

perguntas = {
    1: ("Qual a capital do Brasil?", "B", ["A) São Paulo", "B) Brasília", "C) Rio de Janeiro"]),
    2: ("Quanto é 5 + 3?", "C", ["A) 6", "B) 9", "C) 8"]),
    3: ("Qual disciplina incorpora esse projeto?", "A", ["A) Sistemas Distribuidos", "B) Programação", "C) Banco de dados"])
}

HOST = '0.0.0.0'
TCP_PORT = 5050
UDP_PORT = 5051

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((HOST, TCP_PORT))
tcp_socket.listen(1)
print(f"Servidor aguardando conexão TCP em {HOST}:{TCP_PORT}...")
conn, addr = tcp_socket.accept()
print(f"Cliente conectado: {addr}")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for num in perguntas:
    while True:
        data = conn.recv(1024).decode().strip()

        if data == "PEDIR_ENUNCIADO":
            pergunta, _, opcoes = perguntas[num]
            # Envia enunciado + opções concatenadas para o cliente
            mensagem = pergunta + "\n" + "\n".join(opcoes)
            conn.send(mensagem.encode())
        
        elif data in ["A", "B", "C", "-"]:
            _, resposta_correta, _ = perguntas[num]
            
            if data == resposta_correta:
                resultado = f"Pergunta {num}: Correta ✅"
            elif data == "-":
                resultado = f"Pergunta {num}: Tempo esgotado ❌ (Sem resposta)"
            else:
                resultado = f"Pergunta {num}: Incorreta ❌ (Certa: {resposta_correta})"
            
            # Envia feedback via UDP para o cliente
            udp_socket.sendto(resultado.encode(), (addr[0], UDP_PORT))
            break  # passa para próxima pergunta

        else:
            print(f"Comando desconhecido recebido: {data}")

print("\nJogo finalizado.")
conn.close()
tcp_socket.close()
udp_socket.close()

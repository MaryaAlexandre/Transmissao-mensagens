import socket

perguntas = {
    1: (
        "Qual a capital do Brasil?",
        "B",
        ["A) São Paulo", "B) Brasília", "C) Rio de Janeiro"],
    ),
    2: ("Quanto é 5 + 3?", "C", ["A) 6", "B) 9", "C) 8"]),
    3: (
        "Qual disciplina incorpora esse projeto?",
        "A",
        ["A) Sistemas Distribuidos", "B) Programação", "C) Banco de dados"],
    ),
    4: (
        "Quem pintou a Mona Lisa?",
        "B",
        ["A) Pablo Vittar", "B) Leonardo da Vinci", "C) Michelangelo"],
    ),
    5: (
        "Qual o melhor jogo?\nFortnite, LoL ou Roblox?",
        "B",
        ["A) Fortnite", "B) League of Legends", "C) Roblox"],
    ),
}

HOST = "0.0.0.0"
TCP_PORT = 5050
UDP_PORT = 5051

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((HOST, TCP_PORT))
tcp_socket.listen(1)
print(f"Servidor aguardando conexões TCP em {HOST}:{TCP_PORT}...")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    conn, addr = tcp_socket.accept()
    print(f"\nCliente conectado: {addr}")

    try:
        for num in sorted(perguntas): 
            while True:
                data = conn.recv(1024).decode().strip()

                if data == "PEDIR_ENUNCIADO":
                    pergunta, resposta_correta, opcoes = perguntas[num]
                    mensagem = pergunta + "\n" + "\n".join(opcoes)

                  
                    print(f"[{addr}] Enviando pergunta {num}: {pergunta}")
                    print(f"[{addr}] Resposta correta: {resposta_correta}")

                    conn.send(mensagem.encode())

                elif data in ["A", "B", "C", "-"]:
                    _, resposta_correta, _ = perguntas[num]

                    print(f"[{addr}] Resposta recebida: {data}")

                    if data == resposta_correta:
                        resultado = f"Pergunta {num}: Correta ✅"
                    elif data == "-":
                        resultado = f"Pergunta {num}: Tempo esgotado ❌ (Sem resposta)"
                    else:
                        resultado = (
                            f"Pergunta {num}: Incorreta ❌ (Certa: {resposta_correta})"
                        )

                    udp_socket.sendto(resultado.encode(), (addr[0], UDP_PORT))
                    break

                else:
                    print(f"[{addr}] Comando desconhecido recebido: {data}")

        print(f"Jogo finalizado para {addr}. Aguardando novo jogador...\n")
        conn.close()

    except Exception as e:
        print(f"Erro com cliente {addr}: {e}")
        conn.close()

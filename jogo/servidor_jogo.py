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
tcp_socket.bind(('0.0.0.0', TCP_PORT))
tcp_socket.listen(1)
print(f"Servidor aguardando conexão TCP em {HOST}:{TCP_PORT}...")
conn, addr = tcp_socket.accept()

print(f"Cliente conectado: {addr}")


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


for num, (pergunta, resposta_correta, opcoes) in perguntas.items():
    print(f"\nPergunta {num}: {pergunta}")
    for opcao in opcoes:
        print(opcao)
    
    
    resposta_cliente = conn.recv(1024).decode().strip().upper()
    print(f"Resposta recebida: {resposta_cliente}")
    
    
    if resposta_cliente == resposta_correta:
        resultado = f"Pergunta {num}: Correta ✅"
    else:
        resultado = f"Pergunta {num}: Incorreta ❌ (Certa: {resposta_correta})"
    
    
    udp_socket.sendto(resultado.encode(), (addr[0], UDP_PORT))

print("\nJogo finalizado.")
conn.close()
tcp_socket.close()
udp_socket.close()


import socket
import tkinter as tk
from tkinter import messagebox

# ------------------- CONFIGS -------------------
HOST = 'localhost'  # IP do servidor
TCP_PORT = 5050
UDP_PORT = 5051
TEMPO_RESPOSTA = 15  # segundos para responder cada pergunta

# ------------------ VARIÁVEIS GLOBAIS ------------------
jogador_nome = ""
pergunta_num = 1
pontuacao = 0
tcp_socket = None
udp_socket = None
timer_id = None
tempo_restante = TEMPO_RESPOSTA

# ------------------ DADOS ------------------
perguntas = {
    1: "Qual a capital do Brasil?\nA) São Paulo\nB) Brasília\nC) Rio de Janeiro",
    2: "Quanto é 5 + 3?\nA) 6\nB) 9\nC) 8",
    3: "Qual disciplina incorpora esse projeto?\nA) Sistemas Distribuídos\nB) Programação\nC) Banco de Dados",
    4: "Qual a principal diferença entre TCP e UDP?\nA) Ambos garantem entrega confiável\nB) TCP é mais rápido\nC) TCP garante ordem dos dados",
    5: "Qual comando é usado para o cliente TCP iniciar conexão?\nA) socket.connect()\nB) socket.bind()\nC) socket.listen()"
}

# ------------------ FUNÇÕES ------------------
def obter_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def iniciar_jogo():
    global jogador_nome, tcp_socket, udp_socket, pergunta_num, pontuacao
    nome = entrada_nome.get().strip()
    if not nome:
        messagebox.showwarning("Nome obrigatório", "Por favor, digite seu nome!")
        return

    jogador_nome = nome
    pergunta_num = 1
    pontuacao = 0

    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((HOST, TCP_PORT))

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(('', UDP_PORT))

        frame_inicio.pack_forget()
        frame_final.pack_forget()
        frame_jogo.pack()
        feedback.config(text="")
        carregar_pergunta()

    except Exception as e:
        messagebox.showerror("Erro de conexão", f"Erro ao conectar com o servidor: {e}")

def carregar_pergunta():
    global pergunta_num, tempo_restante, timer_id
    if pergunta_num > 5:
        encerrar_jogo()
        return

    tempo_restante = TEMPO_RESPOSTA
    atualizar_tempo()
    saudacao.config(text=f"{jogador_nome}, aqui vai sua pergunta {pergunta_num}:")
    enunciado.config(text=perguntas[pergunta_num])
    feedback.config(text="")
    botao_A.config(state="normal")
    botao_B.config(state="normal")
    botao_C.config(state="normal")
    iniciar_contador()

def iniciar_contador():
    global timer_id
    timer_id = root.after(1000, atualizar_tempo)

def atualizar_tempo():
    global tempo_restante, timer_id
    tempo_restante -= 1
    label_tempo.config(text=f"Tempo restante: {tempo_restante} segundos")

    if tempo_restante <= 0:
        # tempo esgotado, considera sem resposta e vai para próxima pergunta
        feedback.config(text="Tempo esgotado! Você não respondeu a tempo.", fg="red")
        desativar_botoes()
        root.after(1500, proxima_pergunta)
    else:
        timer_id = root.after(1000, atualizar_tempo)

def desativar_botoes():
    botao_A.config(state="disabled")
    botao_B.config(state="disabled")
    botao_C.config(state="disabled")

def proxima_pergunta():
    global pergunta_num
    pergunta_num += 1
    carregar_pergunta()

def responder(opcao):
    global pergunta_num, pontuacao, timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

    try:
        tcp_socket.send(opcao.encode())
        resultado, _ = udp_socket.recvfrom(1024)
        resultado_texto = resultado.decode()

        if "Correta" in resultado_texto:
            pontuacao += 1

        feedback.config(text=resultado_texto, fg="green" if "Correta" in resultado_texto else "red")
        desativar_botoes()
        root.after(1500, proxima_pergunta)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao enviar resposta: {e}")
        root.quit()

def encerrar_jogo():
    global pergunta_num, pontuacao
    frame_jogo.pack_forget()  # Oculta a tela do jogo
    mensagem_final.config(text=f"Parabéns, {jogador_nome}!\nVocê acertou {pontuacao} de 5 perguntas!")
    frame_final.pack()  # Mostra a tela final

def jogar_novamente():
    frame_final.pack_forget()
    entrada_nome.delete(0, tk.END)
    frame_inicio.pack()

def sair():
    if tcp_socket:
        tcp_socket.close()
    if udp_socket:
        udp_socket.close()
    root.destroy()

# ------------------ INTERFACE ------------------
root = tk.Tk()
root.title("Jogo Interativo 🎮")
root.geometry("600x400")
root.config(bg="#f0f8ff")

# --------- Tela Inicial ---------
frame_inicio = tk.Frame(root, bg="#f0f8ff")
tk.Label(frame_inicio, text="Bem-vindo ao Jogo de Perguntas!", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)
tk.Label(frame_inicio, text="Digite seu nome para começar:", bg="#f0f8ff").pack()

entrada_nome = tk.Entry(frame_inicio, font=("Arial", 12))
entrada_nome.pack(pady=5)

tk.Label(frame_inicio, text=f"Seu IP local é: {obter_ip_local()}", font=("Arial", 10), bg="#f0f8ff", fg="#555").pack(pady=5)

tk.Button(frame_inicio, text="Começar Jogo", bg="#4CAF50", fg="white", font=("Arial", 12),
          command=iniciar_jogo).pack(pady=10)

frame_inicio.pack()

# --------- Tela do Jogo ---------
frame_jogo = tk.Frame(root, bg="#f0f8ff")

saudacao = tk.Label(frame_jogo, text="", font=("Arial", 14, "bold"), bg="#f0f8ff")
saudacao.pack(pady=10)

enunciado = tk.Label(frame_jogo, text="", font=("Arial", 12), bg="#f0f8ff", wraplength=500, justify="left")
enunciado.pack(pady=10)

label_tempo = tk.Label(frame_jogo, text=f"Tempo restante: {TEMPO_RESPOSTA} segundos", font=("Arial", 12), bg="#f0f8ff", fg="red")
label_tempo.pack(pady=5)

frame_botoes = tk.Frame(frame_jogo, bg="#f0f8ff")
frame_botoes.pack()

botao_A = tk.Button(frame_botoes, text="A", width=10, height=2, bg="#2196F3", fg="white",
          command=lambda: responder("A"))
botao_A.grid(row=0, column=0, padx=10)

botao_B = tk.Button(frame_botoes, text="B", width=10, height=2, bg="#FF9800", fg="white",
          command=lambda: responder("B"))
botao_B.grid(row=0, column=1, padx=10)

botao_C = tk.Button(frame_botoes, text="C", width=10, height=2, bg="#9C27B0", fg="white",
          command=lambda: responder("C"))
botao_C.grid(row=0, column=2, padx=10)

feedback = tk.Label(frame_jogo, text="", font=("Arial", 12), bg="#f0f8ff", fg="green")
feedback.pack(pady=10)

# --------- Tela Final ---------
frame_final = tk.Frame(root, bg="#f0f8ff")

mensagem_final = tk.Label(frame_final, text="", font=("Arial", 14), bg="#f0f8ff")
mensagem_final.pack(pady=20)

tk.Button(frame_final, text="Jogar Novamente", font=("Arial", 12), bg="#2196F3", fg="white", command=jogar_novamente).pack(pady=5)
tk.Button(frame_final, text="Sair", font=("Arial", 12), bg="#f44336", fg="white", command=sair).pack()

# --------- Iniciar loop principal ---------
root.mainloop()

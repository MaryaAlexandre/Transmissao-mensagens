import socket
import tkinter as tk
from tkinter import messagebox

# ------------------- CONFIGS -------------------
TCP_PORT = 5050
UDP_PORT = 5051
TEMPO_RESPOSTA = 15
TOTAL_PERGUNTAS = 5


# ------------------ VARIÁVEIS GLOBAIS ------------------
jogador_nome = ""
pergunta_num = 1
pontuacao = 0
tcp_socket = None
udp_socket = None
timer_id = None
tempo_restante = TEMPO_RESPOSTA


# ------------------ FUNÇÕES ------------------
def obter_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except:
        ip = "255.255.255.0"
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
        host_servidor = entrada_ip.get().strip()
        tcp_socket.connect((host_servidor, TCP_PORT))

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("", UDP_PORT))

        frame_inicio.pack_forget()
        frame_final.pack_forget()
        frame_jogo.pack()
        feedback.config(text="")
        carregar_pergunta()

    except Exception as e:
        messagebox.showerror("Erro de conexão", f"Erro ao conectar com o servidor: {e}")


def carregar_pergunta():
    global pergunta_num, tempo_restante, timer_id

    if pergunta_num > TOTAL_PERGUNTAS:
        encerrar_jogo()
        return

    if timer_id:
        root.after_cancel(timer_id)

    try:
        tcp_socket.send("PEDIR_ENUNCIADO".encode())
        enunciado_raw = tcp_socket.recv(2048).decode()

        tempo_restante = TEMPO_RESPOSTA
        label_tempo.config(text=f"Tempo restante: {tempo_restante} segundos")
        saudacao.config(text=f"{jogador_nome}, aqui vai sua pergunta {pergunta_num}:")
        enunciado.config(text=enunciado_raw)
        feedback.config(text="")
        botao_A.config(state="normal")
        botao_B.config(state="normal")
        botao_C.config(state="normal")
        iniciar_contador()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar pergunta: {e}")
        root.quit()


def iniciar_contador():
    global timer_id
    timer_id = root.after(1000, atualizar_tempo)


def atualizar_tempo():
    global tempo_restante, timer_id

    if tempo_restante <= 1:
        label_tempo.config(text="Tempo restante: 0 segundos")
        enviar_resposta("-")
        return

    tempo_restante -= 1
    label_tempo.config(text=f"Tempo restante: {tempo_restante} segundos")
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
    enviar_resposta(opcao)


def enviar_resposta(opcao):
    global timer_id, pontuacao

    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

    desativar_botoes()

    try:
        tcp_socket.send(opcao.encode())
        resultado, _ = udp_socket.recvfrom(1024)
        resultado_texto = resultado.decode()

        if "Correta" in resultado_texto:
            pontuacao += 1
            feedback.config(text=resultado_texto, fg="green")
        else:
            feedback.config(text=resultado_texto, fg="red")

        root.after(1500, proxima_pergunta)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao enviar resposta: {e}")
        root.quit()


def encerrar_jogo():
    frame_jogo.pack_forget()

    if pontuacao == TOTAL_PERGUNTAS:
        mensagem_final.config(
            text=f"Parabéns, {jogador_nome}!!! você acertou todas!!!\nPortanto, você ganhou e não vai levar! É isso."
        )

    else:
        mensagem_final.config(
            text=f"Parabéns, {jogador_nome}!\nVocê acertou {pontuacao} de {TOTAL_PERGUNTAS} perguntas!"
        )

    frame_final.pack()


def jogar_novamente():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
    entrada_nome.delete(0, tk.END)
    frame_final.pack_forget()
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
tk.Label(
    frame_inicio,
    text="Bem-vindo ao Jogo de Perguntas!",
    font=("Arial", 16, "bold"),
    bg="#f0f8ff",
).pack(pady=10)
tk.Label(frame_inicio, text="Digite seu nome para começar:", bg="#f0f8ff").pack()

entrada_nome = tk.Entry(frame_inicio, font=("Arial", 12))
entrada_nome.pack(pady=5)

tk.Label(frame_inicio, text="Digite o IP do servidor:", bg="#f0f8ff").pack()
entrada_ip = tk.Entry(frame_inicio, font=("Arial", 12))
entrada_ip.pack(pady=5)

tk.Button(
    frame_inicio,
    text="Começar Jogo",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12),
    command=iniciar_jogo,
).pack(pady=10)

frame_inicio.pack()

# --------- Tela do Jogo ---------
frame_jogo = tk.Frame(root, bg="#f0f8ff")

saudacao = tk.Label(frame_jogo, text="", font=("Arial", 14, "bold"), bg="#f0f8ff")
saudacao.pack(pady=10)

enunciado = tk.Label(
    frame_jogo,
    text="",
    font=("Arial", 12),
    bg="#f0f8ff",
    wraplength=500,
    justify="left",
)
enunciado.pack(pady=10)

label_tempo = tk.Label(
    frame_jogo,
    text=f"Tempo restante: {TEMPO_RESPOSTA} segundos",
    font=("Arial", 12),
    bg="#f0f8ff",
    fg="red",
)
label_tempo.pack(pady=5)

frame_botoes = tk.Frame(frame_jogo, bg="#f0f8ff")
frame_botoes.pack()

botao_A = tk.Button(
    frame_botoes,
    text="A",
    width=10,
    height=2,
    bg="#2196F3",
    fg="white",
    command=lambda: responder("A"),
)
botao_A.grid(row=0, column=0, padx=10)

botao_B = tk.Button(
    frame_botoes,
    text="B",
    width=10,
    height=2,
    bg="#FF9800",
    fg="white",
    command=lambda: responder("B"),
)
botao_B.grid(row=0, column=1, padx=10)

botao_C = tk.Button(
    frame_botoes,
    text="C",
    width=10,
    height=2,
    bg="#9C27B0",
    fg="white",
    command=lambda: responder("C"),
)
botao_C.grid(row=0, column=2, padx=10)

feedback = tk.Label(frame_jogo, text="", font=("Arial", 12), bg="#f0f8ff", fg="green")
feedback.pack(pady=10)

# --------- Tela Final ---------
frame_final = tk.Frame(root, bg="#f0f8ff")

mensagem_final = tk.Label(frame_final, text="", font=("Arial", 14), bg="#f0f8ff")
mensagem_final.pack(pady=20)

tk.Button(
    frame_final,
    text="Jogar Novamente",
    font=("Arial", 12),
    bg="#2196F3",
    fg="white",
    command=jogar_novamente,
).pack(pady=5)
tk.Button(
    frame_final, text="Sair", font=("Arial", 12), bg="#f44336", fg="white", command=sair
).pack()

# --------- Iniciar loop principal ---------
root.mainloop()

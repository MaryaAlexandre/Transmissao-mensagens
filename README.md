# 🧠 Jogo de Perguntas – Comunicação TCP/UDP com Python

Bem-vindo ao repositório do projeto **Jogo de Perguntas**, desenvolvido como parte prática da disciplina de **Sistemas Distribuídos**.  
Aqui, exploramos a comunicação entre **cliente e servidor** usando **dois protocolos** de transporte diferentes: **TCP** e **UDP**.  

> 🎯 Objetivo: Demonstrar de forma simples e interativa a troca de mensagens entre cliente e servidor usando Python.

---

## 🚀 Como funciona o projeto?

- O **cliente** se conecta ao servidor via **TCP** (conexão confiável).
- O **servidor** envia perguntas no terminal e aguarda as respostas do cliente.
- O cliente envia a resposta pela conexão TCP.
- O **servidor**, ao verificar se a resposta está correta, envia o feedback de volta **via UDP**.
- Essa troca acontece 3 vezes, simulando um mini jogo interativo 🕹️.

---

## 💡 Tecnologias e conceitos aplicados

| Tecnologia | Explicação |
|------------|------------|
| **Python** | Linguagem principal usada para programar o cliente e o servidor |
| **Sockets** | Biblioteca que permite criar conexões em rede com protocolos TCP e UDP |
| **TCP (SOCK_STREAM)** | Utilizado para envio das respostas do cliente — confiável e com conexão |
| **UDP (SOCK_DGRAM)** | Usado para envio rápido da correção de cada resposta — sem necessidade de conexão |

---
## 🎮 Executando o projeto

> Requisitos:
> - Python 3.x instalado
> - Terminal ou Codespaces
---
## Clone o repositório

bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
- CD Jogo;
- Digite no terminal "Python servidor_jogo.py";
- Em outro terminal digite "Python cliente_jogo.py";
Prontinho agora é so jogar :)
---
## 📽️ Apresentação do Projeto

👉 [**Ver apresentação no Canva**](https://www.canva.com/design/DAGn0N0RMXA/fer563X8W1gl4_BNq_4c_g/view?utm_content=DAGn0N0RMXA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h35a44d03b2)


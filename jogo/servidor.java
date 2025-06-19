import java.io.*;
import java.net.*;
import java.util.*;

public class servidor {

    private static final int TCP_PORT = 5050;
    private static final int UDP_PORT = 5051;

    private static Map<Integer, Pergunta> perguntas = new HashMap<>();

    public static void main(String[] args) {
        preencherPerguntas();

        try (ServerSocket serverSocket = new ServerSocket(TCP_PORT)) {
            System.out.println("Servidor aguardando conexões TCP na porta " + TCP_PORT);

            while (true) {
                Socket tcpSocket = serverSocket.accept();
                System.out.println("Cliente conectado: " + tcpSocket.getInetAddress());

                new Thread(() -> tratarCliente(tcpSocket)).start();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void tratarCliente(Socket tcpSocket) {
        try (
            BufferedReader in = new BufferedReader(new InputStreamReader(tcpSocket.getInputStream()));
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(tcpSocket.getOutputStream()));
        ) {
            DatagramSocket udpSocket = new DatagramSocket();

            InetAddress clienteIP = tcpSocket.getInetAddress();

            for (int num : new TreeSet<>(perguntas.keySet())) {
                while (true) {
                    String data = in.readLine();
                    if (data == null) break;
                    data = data.trim();

                    if (data.equals("PEDIR_ENUNCIADO")) {
                        Pergunta p = perguntas.get(num);
                        StringBuilder msg = new StringBuilder();
                        msg.append(p.enunciado).append("\n");
                        for (String opcao : p.opcoes) {
                            msg.append(opcao).append("\n");
                        }

                        System.out.println("Enviando pergunta " + num + ": " + p.enunciado);
                        out.write(msg.toString());
                        out.flush();

                    } else if (Arrays.asList("A", "B", "C", "-").contains(data)) {
                        Pergunta p = perguntas.get(num);
                        String resultado;

                        System.out.println("Resposta recebida: " + data);

                        if (data.equals(p.correta)) {
                            resultado = "Pergunta " + num + ": Correta ✅";
                        } else if (data.equals("-")) {
                            resultado = "Pergunta " + num + ": Tempo esgotado ❌ (Sem resposta)";
                        } else {
                            resultado = "Pergunta " + num + ": Incorreta ❌ (Certa: " + p.correta + ")";
                        }

                        byte[] buffer = resultado.getBytes();
                        DatagramPacket packet = new DatagramPacket(
                            buffer, buffer.length, clienteIP, UDP_PORT
                        );
                        udpSocket.send(packet);

                        break;
                    } else {
                        System.out.println("Comando desconhecido recebido: " + data);
                    }
                }
            }

            System.out.println("Jogo finalizado para " + clienteIP);
            tcpSocket.close();
            udpSocket.close();

        } catch (IOException e) {
            System.out.println("Erro com cliente: " + e.getMessage());
        }
    }

    private static void preencherPerguntas() {
        perguntas.put(1, new Pergunta(
                "Qual a capital do Brasil?",
                "B",
                new String[]{"A) São Paulo", "B) Brasília", "C) Rio de Janeiro"}));

        perguntas.put(2, new Pergunta(
                "Quanto é 5 + 3?",
                "C",
                new String[]{"A) 6", "B) 9", "C) 8"}));

        perguntas.put(3, new Pergunta(
                "Qual disciplina incorpora esse projeto?",
                "A",
                new String[]{"A) Sistemas Distribuidos", "B) Programação", "C) Banco de dados"}));

        perguntas.put(4, new Pergunta(
                "Quem pintou a Mona Lisa?",
                "B",
                new String[]{"A) Pablo Vittar", "B) Leonardo da Vinci", "C) Michelangelo"}));

        perguntas.put(5, new Pergunta(
                "Qual o melhor jogo?\nFortnite, LoL ou Roblox?",
                "B",
                new String[]{"A) Fortnite", "B) League of Legends", "C) Roblox"}));
    }

    static class Pergunta {
        String enunciado;
        String correta;
        String[] opcoes;

        Pergunta(String enunciado, String correta, String[] opcoes) {
            this.enunciado = enunciado;
            this.correta = correta;
            this.opcoes = opcoes;
        }
    }
}


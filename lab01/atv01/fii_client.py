import socket

# Configurações de Conexão
# Se o servidor estiver em outra máquina, troque '127.0.0.1' pelo IP dela.
SERVER_IP = '127.0.0.1' 
SERVER_PORT = 8080

def iniciar_cliente():
    print("=== Cliente de Teste FII ===")
    print("Exemplos de comandos: PRECO;HGLG11 | PROVENTO;KNRI11 | STATUS;MXRF11")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            # 1. Entrada do usuário
            mensagem = input("Comando > ")
            
            if mensagem.lower() == 'sair':
                break

            # 2. Criação do Socket TCP
            # Criamos o socket DENTRO do loop porque o servidor da Atividade 1
            # fecha a conexão logo após enviar a resposta (modelo iterativo simples).
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # 3. Conexão com o servidor
            cliente.connect((SERVER_IP, SERVER_PORT)) # [cite: 32]

            # 4. Envio da mensagem
            # Importante: encode('utf-8') conforme solicitado nas dicas gerais
            cliente.sendall(mensagem.encode('utf-8')) # 

            # 5. Recebimento da resposta
            data = cliente.recv(1024)
            resposta = data.decode('utf-8') # 

            print(f"Resposta do Servidor: {resposta}\n")

        except ConnectionRefusedError:
            print("ERRO: Não foi possível conectar. O servidor está rodando?")
        except Exception as e:
            print(f"ERRO: {e}")
        finally:
            # Garante que o socket seja fechado a cada requisição
            cliente.close()

if __name__ == "__main__":
    iniciar_cliente()
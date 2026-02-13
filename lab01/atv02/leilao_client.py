import socket
import threading
import sys

# Configuração
HOST = '127.0.0.1'
PORT = 8080

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                print("\n[DESCONECTADO] Servidor fechou a conexão.")
                # Encerra o programa se o servidor cair
                sys.exit(0)
            
            # Imprime a mensagem do servidor e restaura o prompt de input
            print(f"\n{msg.decode('utf-8')}")
            print("Seu lance: ", end='', flush=True)
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor.")
        return

    print(f"Conectado ao Leilão! Envie valores para dar lances.")
    
    # Inicia a thread que escuta as mensagens do servidor
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True # Thread morre se o programa principal fechar
    thread.start()

    # Loop principal para enviar lances
    print("Seu lance: ", end='', flush=True)
    while True:
        try:
            # Lê do teclado (bloqueante)
            msg = input()
            client.sendall(msg.encode('utf-8'))
        except KeyboardInterrupt:
            print("\nSaindo...")
            client.close()
            break

if __name__ == "__main__":
    start_client()
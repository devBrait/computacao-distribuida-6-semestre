import socket
import threading

# Configurações do Servidor
HOST = '0.0.0.0'
PORT = 8080

# Estado Compartilhado (Global)
clients = []        # Lista de clientes conectados
highest_bid = 0.0   # Maior lance atual (inicia em 0)

# Controle de Concorrência
bid_lock = threading.Lock()

def broadcast(message, sender_conn):
    for client in clients:
        try:
            client.sendall(message.encode('utf-8'))
        except:
            # Se falhar ao enviar, assume que o cliente desconectou e remove
            clients.remove(client)

def handle_client(conn, addr):
    global highest_bid
    
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    
    # Adiciona o novo cliente à lista de broadcast
    with bid_lock:
        clients.append(conn)

    try:
        conn.sendall(f"BEM-VINDO. Lance atual: {highest_bid:.2f}\n".encode('utf-8'))

        while True:
            # Recebe o lance
            data = conn.recv(1024)
            if not data:
                break

            try:
                msg = data.decode('utf-8').strip()
                bid_value = float(msg)

                # Adquire o bloqueio para ler e escrever na variável global com segurança
                with bid_lock:
                    if bid_value > highest_bid:
                        highest_bid = bid_value
                        print(f"Novo lance aceito: {bid_value} de {addr}")
                        
                        # Notifica TODOS
                        msg_broadcast = f"NOVO LANCE: {highest_bid:.2f} por {addr}"
                        broadcast(msg_broadcast, conn)
                    else:
                        # Lance baixo ou igual: responde apenas ao remetente
                        conn.sendall("LANCE RECUSADO: Valor baixo\n".encode('utf-8'))

            except ValueError:
                conn.sendall("ERRO: Envie apenas numeros (ex: 500.50)\n".encode('utf-8'))

    except Exception as e:
        print(f"[ERRO] {addr}: {e}")
    finally:
        # Limpeza ao desconectar
        print(f"[DESCONECTADO] {addr} saiu.")
        with bid_lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"--- Servidor de Leilão Iniciado em {HOST}:{PORT} ---")

    while True:
        # Aceita conexão principal
        conn, addr = server.accept()
        
        # Cria uma nova Thread para este cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ATIVOS] {threading.active_count() - 1} clientes conectados.")

if __name__ == "__main__":
    start_server()
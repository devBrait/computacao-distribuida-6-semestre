import socket
import threading
import datetime

HOST = '0.0.0.0'
PORT = 12346
storage = 10
lock = threading.Lock()
clientes_ativos = []

def broadcast(mensagem):
    for client_conn in clientes_ativos[:]:
        try:
            client_conn.sendall(mensagem.encode())
        except:
            clientes_ativos.remove(client_conn)

def handle_client(conn, addr):
    print(f"[{datetime.datetime.now()}] Conectado por {addr}")
    clientes_ativos.append(conn)
    
    try:
        while True:
            data = conn.recv(1024).decode().strip().upper()
            if not data:
                break
            
            log_msg = f"[{datetime.datetime.now()}] Cliente {addr} enviou: {data}"
            print(log_msg)

            if data == "CONSULTAR":
                resposta = f"storage atual: {storage}"
                conn.sendall(resposta.encode())

            elif data == "COMPRAR":
                with lock:
                    if storage > 0:
                        storage -= 1
                        storage_atual = storage
                        resposta = f"Compra realizada. storage restante: {storage_atual}"
                        conn.sendall(resposta.encode())
                        
                        if storage_atual == 0:
                            broadcast("\nAVISO: O storage acabou de esgotar!\n")
                    else:
                        conn.sendall("ERRO: Produto esgotado".encode())
            else:
                conn.sendall("Comando desconhecido".encode())
                
    except ConnectionResetError:
        print(f"Cliente {addr} desconectou abruptamente.")
    finally:
        clientes_ativos.remove(conn)
        conn.close()
        print(f"Conexão encerrada com {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor aguardando conexões na porta {PORT}...")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()
import socket
import threading
from datetime import datetime

# Definição das configs do servidor
HOST = '0.0.0.0'
PORT = 12346  

# Dicionário que simula o estoque, como se estivesse em um db
stock = { "estoque": 10 }

# Lock do threading para evitar condições de corrida
lock = threading.Lock()
# Lista que armazena os clientes ativos
current_customers = []

# Função para tratar todas as requests
def handle_client(conn, addr):

    # Exibe conexão e adiciona cliente
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Conectado por {addr[0]}:{addr[1]}") 
    current_customers.append(conn)
    
    try:
        while True:
            # Recebe a requisição do cliente
            request = conn.recv(1024).decode('utf-8').strip().upper()
            if not request:
                break
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Cliente {addr} enviou: {request}")
            
            if request == "CONSULTAR":
                answer = f"Estoque atual: {stock['estoque']}"
                conn.sendall(answer.encode('utf-8')) # Envia a resposta calculada de volta ao cliente com o estoque atual

            elif request == "COMPRAR":
                #lock garante que apenas este cliente modifique o estoque
                with lock:
                    # Verifica e altera direto no dicionário
                    if stock["estoque"] > 0:
                        stock["estoque"] -= 1
                        current_stock = stock["estoque"] 
                        
                        answer = f"Compra realizada!!! Estoque restante: {current_stock}"
                        conn.sendall(answer.encode('utf-8')) # Envia o sucesso da compra para este cliente
                        
                        # Avisa todos os clientes que o estoque acabou
                        if current_stock == 0:
                            warning = "ESTOQUE ESGOTADO!!!"
                            for client in current_customers.copy():
                                try:
                                    client.sendall(warning.encode('utf-8'))
                                except:
                                    current_customers.remove(client) # Remove clientes que se desconectaram indevidamente
                    else:
                        # Tratamento quando o estoque já estivesse zerado antes do cliente entrar na região crítica
                        conn.sendall("ERRO: Produto esgotado".encode('utf-8'))
            else:
                conn.sendall("Ocorreu algo inesperado".encode('utf-8'))
                
    except Exception as e:
        print(f"Cliente {addr} foi desconectado ou apresentou erro: {e}")
    finally:
        # Finaliza a conexão
        if conn in current_customers:
            current_customers.remove(conn)
        conn.close()
        print(f"Conexão finalizada com {addr}")

# Função para inicialização do servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    # Inicia o servidor
    server.listen()
    print(f"Aguardando conexões na porta {PORT}...")
    
    # Fica ouvindo e aguardando conexão de todos os clientes
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
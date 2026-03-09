import socket
import threading
import time
import random

# Definição das configs do servidor
SERVER_IP = '127.0.0.1' 
SERVER_PORT = 12346    
# Define a quantidade de usuário/clientes
NUM_THREADS = 15

# Simulação do usuário fazendo a compra
def user_simulation(user_id):
    try:
        
        # Estabelece a conexão com o servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT)) 
            s.settimeout(12.0)
            
            # Numéro aleatório de tentativas por usuário
            attempts = random.randint(10, 20)
            
            for i in range(attempts):
                # Primeiro envia requisição para consultar o estoque
                s.sendall("CONSULTAR".encode())
                print(f"Usuário {user_id}: {s.recv(1024).decode()}") 
                
                time.sleep(random.uniform(1, 3)) # TimeSpleep para simular o pensamento por usuário
                
                # Envia a requisição de compra
                s.sendall("COMPRAR".encode())
                answer_request = s.recv(1024).decode()
                print(f"Usuário {user_id}: {answer_request}")
                
                # Aguarda por notificações de broadcast do servidor 
                print(f"Usuário {user_id} aguardando mensagens de erro...")
                s.settimeout(random.uniform(5, 10))
                
                try:
                    # Verifica se recebeu mensagem de erro
                    warning_message = s.recv(1024).decode()
                    if warning_message:
                        print(f"*** NOTIFICAÇÃO PARA {user_id}: {warning_message} ***")
                        
                except socket.timeout:
                    pass

                s.settimeout(12.0)
                    
    except Exception as e:
        print(f"Erro no Usuário {user_id}: {e}")

if __name__ == "__main__":
    threads = []
    
    # Inicializa todas as threads
    for i in range(NUM_THREADS):
        t = threading.Thread(target=user_simulation, args=(i,))
        threads.append(t)
        t.start()
        
    # Espera todas as threads finalizarem para encerrar o sistema
    for t in threads:
        t.join()
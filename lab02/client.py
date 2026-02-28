import socket
import threading
import time
import random

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12346
NUM_THREADS = 15

def simular_usuario(id_usuario):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.settimeout(12.0)
            
            repeticoes = random.randint(1, 3)
            for i in range(repeticoes):
                s.sendall("CONSULTAR".encode())
                print(f"Usuário {id_usuario}: {s.recv(1024).decode()}")
                
                time.sleep(random.uniform(1, 3))
                
                s.sendall("COMPRAR".encode())
                resposta_compra = s.recv(1024).decode()
                print(f"Usuário {id_usuario}: {resposta_compra}")
                
                print(f"Usuário {id_usuario} aguardando avisos...")
                try:
                    aviso = s.recv(1024).decode()
                    if aviso:
                        print(f"*** NOTIFICAÇÃO PARA {id_usuario}: {aviso} ***")
                except socket.timeout:
                    pass
                    
    except Exception as e:
        print(f"Erro no Usuário {id_usuario}: {e}")

if __name__ == "__main__":
    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=simular_usuario, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
import socket

# Configuração de conexão local
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080

def run_client():
    print("--- Cliente de Teste FII ---")
    print("Formato: COMANDO;TICKER")
    print("Exemplos: PRECO;MXRF11 | PROVENTO;KNRI11 | STATUS;HGLG11")
    print("Digite 'exit' para sair.\n")

    while True:
        user_input = input("Digite o comando: ")
        
        if user_input.lower() == 'exit':
            break

        # Cria um novo socket para cada requisição
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # Tenta conectar ao servidor
                client_socket.connect((SERVER_IP, SERVER_PORT))
                
                # Envia a mensagem codificada em UTF-8
                client_socket.sendall(user_input.encode('utf-8'))
                
                # Aguarda e recebe a resposta do servidor
                response = client_socket.recv(1024)
                print(f"Resposta do Servidor: {response.decode('utf-8')}\n")
                
        except ConnectionRefusedError:
            print("ERRO: Não foi possível conectar. Verifique se o servidor está rodando.\n")
        except Exception as e:
            print(f"ERRO: {e}\n")

if __name__ == "__main__":
    run_client()
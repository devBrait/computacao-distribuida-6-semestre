import socket

# Configurações do Servidor
HOST = '0.0.0.0' 
PORT = 8080    

# Base de Dados em Memória
FII_DATABASE = {
    "HGLG11": {"price": "160.00", "yield": "1.10"},
    "KNRI11": {"price": "155.50", "yield": "0.80"},
    "MXRF11": {"price": "10.50",  "yield": "0.12"}
}

def handle_request(raw_message):
    try:
        # Limpa espaços e separa a string pelo delimitador ';'
        parts = raw_message.strip().split(';')
        
        # Validação básica do formato
        if len(parts) != 2:
            return "ERRO: Comando invalido"
        
        # Normaliza para letras maiúsculas
        command = parts[0].upper().strip()
        ticker = parts[1].upper().strip()

        # Verifica se o Ticker existe na base de dados
        if ticker not in FII_DATABASE:
            return "ERRO: FII nao encontrado"

        data = FII_DATABASE[ticker]

        # Lógica dos Comandos (Protocolo definido no PDF)
        if command == "PRECO":
            return data["price"]
        
        elif command == "PROVENTO":
            return data["yield"]
        
        elif command == "STATUS":
            # Retorna string formatada com todos os dados
            return f"{ticker}; {data['price']}; {data['yield']}"
        
        else:
            return "ERRO: Comando invalido"

    except Exception as e:
        print(f"Erro no processamento: {e}")
        return "ERRO: Comando invalido"

def start_server():
    # Criação do Socket TCP (IPv4, Stream)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Permite o reuso da porta imediatamente após fechar o servidor
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Vincula o socket ao IP e Porta (Bind)
            server_socket.bind((HOST, PORT))
            # Coloca em modo de escuta (Listen)
            server_socket.listen()
            print(f"Servidor rodando em {HOST}:{PORT}")
            print("Aguardando conexões...")

            while True:
                # Aceita uma nova conexão (Bloqueante)
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Conectado por: {addr}")
                    
                    # Recebe os dados (buffer de 1024 bytes)
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    # Decodifica a mensagem (bytes -> string)
                    message = data.decode('utf-8')
                    print(f"Recebido: {message}")
                    
                    # Processa a lógica de negócio
                    response = handle_request(message)
                    
                    # Envia a resposta codificada (string -> bytes)
                    conn.sendall(response.encode('utf-8'))
                    
        except KeyboardInterrupt:
            print("\nServidor encerrado manualmente.")
        except Exception as e:
            print(f"Erro fatal: {e}")

if __name__ == "__main__":
    start_server()
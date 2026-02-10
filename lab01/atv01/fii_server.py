import socket

HOST = '0.0.0.0'
PORT = 8080    

dados_fii = {
    "HGLG11": {"preco": "160.00", "provento": "1.10"},
    "KNRI11": {"preco": "155.50", "provento": "0.80"},
    "MXRF11": {"preco": "10.50", "provento": "0.12"}
}

def iniciar_servidor():
    # 1. Criação do Socket TCP
    # AF_INET = IPv4, SOCK_STREAM = TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor.bind((HOST, PORT))
        servidor.listen(5)
        print(f"Servidor de FIIs rodando em {HOST}:{PORT}")
        print("Aguardando conexões...")

        while True:
            conn, addr = servidor.accept()
            print(f"Conectado por: {addr}")

            try:
                dados = conn.recv(1024).decode('utf-8').strip()
                
                if not dados:
                    conn.close()
                    continue

                print(f"Recebido: {dados}")
                
                partes = dados.split(';')
                
                resposta = ""

                if len(partes) != 2:
                    resposta = "ERRO: Comando invalido"
                else:
                    comando = partes[0].upper()
                    ticker = partes[1].upper()

                    if ticker not in dados_fii:
                        resposta = "ERRO: FII nao encontrado"
                    else:
                        info = dados_fii[ticker]
                        
                        if comando == "PRECO":
                            resposta = info["preco"]
                        elif comando == "PROVENTO":
                            resposta = info["provento"]
                        elif comando == "STATUS": 
                            resposta = f"{ticker}: R{info['preco']} Div: R{info['provento']}"
                        else:
                            resposta = "ERRO: Comando invalido"

                conn.sendall(resposta.encode('utf-8'))

            except Exception as e:
                print(f"Erro no processamento: {e}")
            finally:
                conn.close()

    except KeyboardInterrupt:
        print("\nDesligando servidor...")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()
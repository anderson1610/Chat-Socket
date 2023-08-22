import socket
import threading

# Configurações do servidor
HOST = '172.16.254.169'  # Endereço IP do servidor
PORT = 12345     # Porta para ouvir conexões

# Dicionário para armazenar os clientes conectados
clientes = {}

# Função para lidar com as mensagens de um cliente
def handle_client(client_socket, client_address):
    while True:
        mensagem = client_socket.recv(1024).decode()
        if mensagem == "sair":
            break
        broadcast(mensagem, client_address)
    
    client_socket.close()
    del clientes[client_address]
    broadcast(f"Cliente {client_address} saiu do chat", None)

# Função para enviar mensagens para todos os clientes
def broadcast(mensagem, origem):
    for client_socket in clientes:
        if client_socket != origem:
            try:
                clientes[client_socket].send(mensagem.encode())
            except:
                pass

# Inicializa o servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Servidor iniciado e ouvindo em", HOST, ":", PORT)

# Aceita conexões e cria uma thread para cada cliente
while True:
    client_socket, client_address = server_socket.accept()
    print("Conexão recebida de", client_address)
    clientes[client_address] = client_socket
    
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

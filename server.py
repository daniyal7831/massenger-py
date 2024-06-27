import socket
import threading

def start_server():
    HOST = '0.0.0.0'
    PORT = 12345

    clients = []

    def handle_client(client_socket, address):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"{address} says: {message}")
                    broadcast_message(f"{address} says: {message}", client_socket)
                else:
                    remove_client(client_socket)
                    break
            except:
                continue

    def broadcast_message(message, client_socket):
        for client in clients:
            if client != client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    remove_client(client)

    def remove_client(client_socket):
        if client_socket in clients:
            clients.remove(client_socket)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        print(f"Connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
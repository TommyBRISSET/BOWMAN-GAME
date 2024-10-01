import socket
import threading


class Server:
    """Classe représentant un serveur pour le jeu"""
    def __init__(self, ip='0.0.0.0', port=12345):
        self.ip = ip
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.is_running = False
        self.client_connected = False

    def start_server(self):
        """Démarre le serveur"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)
        self.is_running = True
        threading.Thread(target=self.accept_client).start()

    def accept_client(self):
        """Accepte un client"""
        self.client_socket, self.client_address = self.server_socket.accept()
        self.client_connected = True

    def stop_server(self):
        """Arrête le serveur"""
        self.is_running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()

    def send_message(self, message):
        """Envoyer un message au client"""
        if self.client_socket:
            self.client_socket.sendall(message.encode())

    def receive_message(self):
        """Recevoir un message du client"""
        if self.client_socket:
            return self.client_socket.recv(1024).decode()
        return None

import socket


class Client:
    """Classe représentant un client pour le jeu"""
    def __init__(self, server_ip='127.0.0.1', server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.is_connected = False
        self.server_not_found = False  # Préviens les tentatives de connexion multiples si le serveur n'est pas trouvé

    def connect_to_server(self):
        """Se connecter au serveur"""
        if self.server_not_found:
            return  # Ne pas essayer de se connecter si le serveur n'est pas trouvé
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.is_connected = True
            self.server_not_found = False
        except ConnectionRefusedError:
            self.server_not_found = True

    def disconnect(self):
        """Déconnecter le client du serveur"""
        self.is_connected = False
        if self.client_socket:
            self.client_socket.close()

    def send_message(self, message):
        """Envoyer un message au serveur"""
        if self.client_socket:
            self.client_socket.sendall(message.encode())

    def receive_message(self):
        """Recevoir un message du serveur"""
        if self.client_socket:
            return self.client_socket.recv(1024).decode()
        return None

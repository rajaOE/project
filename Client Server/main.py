import threading
from scripts.Client import Client
from scripts.Server import Server  # Assumendo che tu abbia anche separato Server

class Main:
    def __init__(self):
        self.server = Server()
        self.client = Client()

    def start(self):
        server_thread = threading.Thread(target=self.server.start, daemon=True)
        server_thread.start()
        self.client.start()

if __name__ == "__main__":
    Main().start()
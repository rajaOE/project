import socket
import time
import random
from scripts.Quiz import quiz

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('127.0.0.1', 8888)
        self.server_socket.bind(self.server_address)

    def start(self):
        print("Server: In attesa della connessione del client...")
        try:
            while True:
                data, client_address = self.server_socket.recvfrom(4096)
                message = data.decode('utf-8').strip()
                if message == "START":
                    print(f"Server: Client connesso da {client_address}")
                    self.server_socket.sendto("Benvenuto al quiz!".encode('utf-8'), client_address)
                    self.inizia_quiz(client_address)
        except Exception as e:
            print(f"Server: Errore fatale - {e}")
        finally:
            self.server_socket.close()

    def inizia_quiz(self, client_address):
        random.shuffle(quiz)
        for question, correct_answer in quiz:
            print(f"Server: Invio domanda - {question}")
            self.server_socket.sendto(question.encode('utf-8'), client_address)
            try:
                self.server_socket.settimeout(20)
                data, _ = self.server_socket.recvfrom(4096)
                answer = data.decode('utf-8').strip()
                print(f"Server: Risposta ricevuta - {answer}")
                if answer.lower() == correct_answer.lower():
                    feedback = "Risposta corretta!"
                else:
                    feedback = f"Sbagliato! La risposta corretta era: {correct_answer}"
                self.server_socket.sendto(feedback.encode('utf-8'), client_address)
            except socket.timeout:
                print("Server: Nessuna risposta ricevuta (timeout)")
                self.server_socket.sendto("Tempo scaduto! Nessuna risposta data.".encode('utf-8'), client_address)
            time.sleep(2)
        self.server_socket.sendto("Quiz finito! Grazie per aver partecipato.".encode('utf-8'), client_address)
        print("Server: Quiz terminato.")
        
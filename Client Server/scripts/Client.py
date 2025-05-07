import socket
import threading
import tkinter as tk

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('127.0.0.1', 8888)

        self.root = tk.Tk()
        self.root.title("🧠 Quiz Interattivo")
        self.root.geometry("500x300")
        self.root.configure(bg="#1e1e1e")
        self.root.eval('tk::PlaceWindow . center')

        self.domanda_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="#ffffff", wraplength=450)
        self.domanda_label.pack(pady=10)

        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 12), fg="#00ff88", bg="#1e1e1e")
        self.feedback_label.pack(pady=5)

        self.entry = tk.Entry(self.root, font=("Arial", 12), bg="#2e2e2e", fg="#ffffff", insertbackground="white")
        self.entry.pack(pady=10)

        self.button = tk.Button(
            self.root,
            text="Invia risposta",
            font=("Arial", 12),
            bg="#007acc",
            fg="white",
            activebackground="#005f99",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand",
            command=self.invia_risposta
        )
        self.button.pack(pady=10)
        
        self.quit_button = tk.Button(
            self.root,
            text="Termina Quiz",
            font=("Arial", 12),
            bg="#cc0000",
            fg="white",
            activebackground="#990000",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            command=self.termina_quiz
        )
        self.quit_button.pack(pady=5)

        self.risposta = ""
        threading.Thread(target=self.aggiorna_label, daemon=True).start()

    def start(self):
        self.client_socket.sendto("START".encode('utf-8'), self.server_address)
        self.root.mainloop()

    def aggiorna_label(self):
        while True:
            try:
                data, _ = self.client_socket.recvfrom(4096)
                message = data.decode('utf-8')

                if "Quiz finito" in message:
                    self.feedback_label.config(text=message, fg="#00ff88")
                    self.button.config(state="disabled")
                    self.entry.config(state="disabled")

                elif "Risposta corretta!" in message:
                    self.feedback_label.config(text=message, fg="#00ff88")
                    self.entry.config(state="normal")
                    self.button.config(state="normal")

                elif "Sbagliato!" in message or "Tempo scaduto" in message:
                    self.feedback_label.config(text=message, fg="#ff4c4c")
                    self.entry.config(state="normal")
                    self.button.config(state="normal")

                else:
                    self.domanda_label.config(text=message)
                    self.feedback_label.config(text="")
                    self.entry.config(state="normal")
                    self.button.config(state="normal")

            except Exception as e:
                print(f"Client: Errore durante la connessione - {e}")

    def invia_risposta(self):
        self.risposta = self.entry.get()
        self.client_socket.sendto(self.risposta.encode('utf-8'), self.server_address)
        self.entry.delete(0, tk.END)
        
    def termina_quiz(self):
        self.client_socket.sendto("QUIT".encode('utf-8'), self.server_address)
        self.root.destroy()  
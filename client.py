import tkinter as tk
import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_list = tk.Listbox(self.message_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.message_list.yview)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)

        self.entry_label = tk.Label(self.entry_frame, text="Enter message:")
        self.entry_label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.entry_frame, width=40)
        self.entry.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

        threading.Thread(target=self.receive_messages).start()

    def connect_to_server(self):
        try:
            self.client.connect((SERVER_HOST, SERVER_PORT))
        except Exception as e:
            print(f"Error while connecting to server: {e}")
            self.root.quit()

    def send_message(self):
        message = self.entry.get()
        if message:
            try:
                self.client.send(message.encode('utf-8'))
                self.message_list.insert(tk.END, f"You: {message}")
                self.entry.delete(0, tk.END)
            except Exception as e:
                print(f"Error while sending message: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    self.message_list.insert(tk.END, message)
            except Exception as e:
                print(f"Error while receiving message: {e}")
                self.client.close()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()
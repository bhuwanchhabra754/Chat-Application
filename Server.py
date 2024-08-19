import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Server Configuration
HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5

# Global Variables
clients = []  # List to keep track of connected clients

def send_messages_to_all(from_username, message):
    for client, _ in clients:
        try:
            client.send(f"{from_username}: {message}".encode())
        except:
            # Handle client disconnection
            clients.remove((client, _))

def client_handler(client, address):
    username = client.recv(1024).decode()
    clients.append((client, username))
    server_log.insert(tk.END, f"Client {address} connected as {username}\n")
    server_log.yview(tk.END)

    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                server_log.insert(tk.END, f"{username}: {message}\n")
                server_log.yview(tk.END)
                send_messages_to_all(username, message)
            else:
                break
        except:
            break

    client.close()
    clients.remove((client, username))
    server_log.insert(tk.END, f"Client {address} disconnected\n")
    server_log.yview(tk.END)

def start_server():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen(LISTENER_LIMIT)
        server_log.insert(tk.END, f"Server started on {HOST}:{PORT}\n")
        server_log.yview(tk.END)
        accept_connections()
    except Exception as e:
        server_log.insert(tk.END, f"Unable to bind to {HOST}:{PORT} - {e}\n")
        server_log.yview(tk.END)

def accept_connections():
    while True:
        client, address = server.accept()
        threading.Thread(target=client_handler, args=(client, address)).start()

def send_message():
    message = message_entry.get()
    if message:
        send_messages_to_all("Server", message)
        server_log.insert(tk.END, f"Server: {message}\n")
        server_log.yview(tk.END)
        message_entry.delete(0, tk.END)

def stop_server():
    server.close()
    server_log.insert(tk.END, "Server stopped\n")
    server_log.yview(tk.END)

# Create the main window
root = tk.Tk()
root.title("Server GUI")

# Create and place widgets
start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.grid(row=0, column=0, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop Server", command=stop_server)
stop_button.grid(row=0, column=1, padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

send_button = tk.Button(root, text="Send Message", command=send_message)
send_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

server_log = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
server_log.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()

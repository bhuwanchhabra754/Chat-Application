import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Client Configuration
HOST = '127.0.0.1'
PORT = 1234

def connect_to_server():
    global client
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        chat_log.insert(tk.END, "Successfully connected to server\n")
        chat_log.yview(tk.END)
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        chat_log.insert(tk.END, f"Unable to connect to server: {e}\n")
        chat_log.yview(tk.END)

def send_message():
    message = message_entry.get()
    if message:
        try:
            client.send(message.encode())
            chat_log.insert(tk.END, f"You: {message}\n")
            chat_log.yview(tk.END)
            message_entry.delete(0, tk.END)
        except:
            chat_log.insert(tk.END, "Failed to send message\n")
            chat_log.yview(tk.END)

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                chat_log.insert(tk.END, f"Server: {message}\n")
                chat_log.yview(tk.END)
        except:
            chat_log.insert(tk.END, "Connection to server lost\n")
            chat_log.yview(tk.END)
            break

def close_connection():
    try:
        client.close()
        chat_log.insert(tk.END, "Disconnected from server\n")
        chat_log.yview(tk.END)
    except:
        chat_log.insert(tk.END, "Error closing connection\n")
        chat_log.yview(tk.END)

# Create the main window
root = tk.Tk()
root.title("Client GUI")

# Create and place widgets
connect_button = tk.Button(root, text="Connect to Server", command=connect_to_server)
connect_button.grid(row=0, column=0, padx=10, pady=10)

disconnect_button = tk.Button(root, text="Disconnect", command=close_connection)
disconnect_button.grid(row=0, column=1, padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

chat_log = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
chat_log.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()

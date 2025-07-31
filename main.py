import socket
import threading
import json5
import os
import time
from cryptography.fernet import Fernet

def generate_encryption_key():
    key = Fernet.generate_key()
    with open('secret.key', 'xb') as f:
        f.write(key)
    os.chmod('secret.key', 0o600)

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(token, key):
    fernet = Fernet(key)
    return fernet.decrypt(token).decode()

def handle_client(connection, client, key):
    try:
        while True:
            data = connection.recv(4064)
            if not data:
                break
            decrypted_data = decrypt_message(data, key)
            print(decrypted_data)

            if decrypted_data.strip() == ':q':
                break
    finally:
        connection.close()

def server(IP, PORT, key):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, PORT)
    tcp_socket.bind(server_address)
    tcp_socket.listen()
    
    while True:
        connection, client = tcp_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, client, key))
        client_thread.daemon = True
        client_thread.start()

def client(IP, PORT, data):
    tcp_socket = socket.create_connection((IP, PORT))
    try:
        tcp_socket.sendall(data)
    finally:
        tcp_socket.close()

def get_data():
    with open('config.json', 'r') as file:
        config = json5.load(file)
    username = config['username']
    reciever_ip = config['reciever']['IP']
    reciever_port = config['reciever']['PORT']
    return {
        'user': username,
        'reciever': {
            'IP': reciever_ip,
            'PORT': reciever_port
        }
    }

if __name__ == "__main__":
    if not os.path.exists('secret.key'):
        print("Generating key...")
        generate_encryption_key()

    with open('secret.key', 'rb') as secret:
        key = secret.read()

    reciever_name = input('Enter name of receiver: ')
    with open(f'contacts/{reciever_name}.json', 'r') as file:
        reciever = json5.load(file)

    data = get_data()

    server_thread = threading.Thread(
        target=server,
        args=(data['reciever']['IP'], data['reciever']['PORT'], reciever['KEY'])
    )
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)

    while True:
        user_input = input()
        message = f"<{data['user']}>{user_input}"
        encrypted_message = encrypt_message(message, key)

        client_thread = threading.Thread(
            target=client,
            args=(reciever['IP'], reciever['PORT'], encrypted_message)
        )
        client_thread.start()
        client_thread.join()

        if user_input.strip() == ":q":
            break

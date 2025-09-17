import socket
import ssl
import threading
import json5
import os
import time

from cryptography.fernet import Fernet

def generate_encryption_key():
    key = Fernet.generate_key()
    ans = input('Do you know your key? (y/N): ')

    y = 'y'

    if ans != y.upper():
        print(f'Your key is: {key.decode()}')
        print(f'Add this: export CHAT_SECRET_KEY="{key.decode()}" to your shell config and restart your terminal.')
    else:
        print('Make sure: export CHAT_SECRET_KEY="*your_key*" is in your shell config')

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(token, key):
    fernet = Fernet(key)
    return fernet.decrypt(token).decode()

def handle_client(connection, client, key, context):
    while True:
        with context.wrap_socket(conn, server_side=True) as tls_connection:
            data = tsl_connection.recv(4064).decode()

def server(IP, PORT, key):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="../config/cert.pem", keyfile="../config/key.pem")

    while True:
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (IP, PORT)
            tcp_socket.bind(server_address)
            tcp_socket.listen()
        except:
            print("Error when trying to build connection with subject, perhaps theire not online or don't exist")
            ans = input('Try again? (Y/n) ')
            y = 'y'
            if ans != y.upper():
                break
    
    while True:
        try:
            connection, client = tcp_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(context, connection, client, key))
            client_thread.daemon = True
            client_thread.start()
        except:
            print('Something went wrong')
            ans = input('Try again? (Y/n) ')
            y = 'y'
            if ans != y.upper():
                break

def client(IP, PORT, data):
    context = ssl.create_default_context()
    context.load_verify_location("../config/cert.pem")
    with socket.create_connection((IP, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=IP) as tls_sock:
            tls_sock.sendall(data)

def get_data():
    with open('../config/config.json', 'r') as file:
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

def main(): 
    generate_encryption_key()

    key = os.environ.get("CHAT_SECRET_KEY")

    reciever_name = input('Enter name of receiver: ')
    with open(f'../contacts/{reciever_name}.json', 'r') as file:
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

if __name__ == "__main__":
    main()

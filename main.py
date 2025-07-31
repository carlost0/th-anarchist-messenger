import socket
import threading
import json
import time

def handle_client(connection, client):
    try:
        while True:
            data = connection.recv(4064)
            if not data:
                break
            formatted_data = data.decode()
            print(formatted_data)

            if formatted_data.strip() == ':q':
                break
    finally:
        #print(f"Connection with {client} closed.")
        connection.close()

def server(IP, PORT):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, PORT)
    tcp_socket.bind(server_address)
    tcp_socket.listen()

    #print(f"Server listening on {IP}:{PORT}")
    
    while True:
        #print("Waiting for connection...")
        connection, client = tcp_socket.accept()
        # Handle each client in a new thread
        client_thread = threading.Thread(target=handle_client, args=(connection, client))
        client_thread.daemon = True
        client_thread.start()


def client(IP, PORT, message):
    # Create a connection to the server application on port 81
    tcp_socket = socket.create_connection((IP, PORT))
 
    try:
        data = str.encode(message)
        tcp_socket.sendall(data)
 
    finally:
        if message == ':q':
            print("quitting")
            tcp_socket.close()

def get_data():
    with open('config.json', 'r') as file:
        config = json.load(file)
 
    username = config['username']

    sender_ip = config['sender']['IP']
    sender_port = config['sender']['PORT']

    reciever_ip = config['reciever']['IP']
    reciever_port = config['reciever']['PORT']

    data = {
            'user': username,

            'sender': {
                'IP': sender_ip,
                'PORT': sender_port
            },

            'reciever': {
                'IP': reciever_ip,
                'PORT': reciever_port
            },
    }

    return data

if __name__ == "__main__":
    
    data = get_data()

    server_thread = threading.Thread(target=server, args=(data['reciever']['IP'], data['reciever']['PORT']))
    server_thread.start()

    time.sleep(1)
    #client = threading.Thread(target=client, args=(data['sender']['IP'], data['sender']['PORT'], data['message']))
    while True:
        client_thread = threading.Thread(target=client, args=(data['sender']['IP'], data['sender']['PORT'], f'<{data['user']}>{input()}'))
        client_thread.start()
        client_thread.join()

    server:thread.join()

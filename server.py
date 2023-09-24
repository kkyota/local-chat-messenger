import socket
import os
from faker import Faker

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = '/tmp/socket_file'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

sock.bind(server_address)

sock.listen(1)

fake = Faker()

def generate_fake_response():
    return fake.sentence().replace('\n', ' ')  # Remove newlines from the response

while True:
    connection, client_address = sock.accept()
    try:
        print('Connection from', client_address)

        while True:
            data = b''
            while b'\n' not in data:
                chunk = connection.recv(16)
                if not chunk:
                    break
                data += chunk
            data_str = data.decode('utf-8').strip()
            print('Received ' + data_str)

            if data_str:
                response = generate_fake_response()
                try:
                    connection.sendall(response.encode() + b'\n')  # Add a newline after the response
                except BrokenPipeError:
                    print('Client connection closed')
                    break

            else:
                print('No data from', client_address)
                break

    except ConnectionResetError:
        print('Client connection closed')
        connection.close()
        break

    finally:
        print("Closing current connection")
        connection.close()

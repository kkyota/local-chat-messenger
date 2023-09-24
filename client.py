import socket
import sys
from faker import Faker

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = '/tmp/socket_file'

print('Connecting to {}'.format(server_address))

try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

fake = Faker()

def send_and_receive_message(message):
    sock.sendall((message + '\n').encode())  # Add a newline after the message

    while True:  # Loop until data is received from the server
        try:
            data = sock.recv(32).decode()
            print('Server response: ' + data.strip())
            break
        except socket.timeout:
            print('Socket timeout, ending listening for server messages')
            break

message = fake.sentence().replace('\n', ' ')  # Remove newlines from the message
send_and_receive_message(message)

message = fake.sentence().replace('\n', ' ')  # Remove newlines from the message
send_and_receive_message(message)

# Add more messages if needed

print('Closing socket')
sock.close()

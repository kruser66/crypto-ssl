import socket
import ssl

server_cert = 'server.crt'
port = 65432

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    with context.wrap_socket(sock, server_hostname='127.0.0.1') as ssock:
        ssock.connect(('127.0.0.1', port))
        try:
            ssock.sendall(b"Hello, server!")
            response = ssock.recv(1024).decode()
            print(response)
        finally:
            ssock.close()

import socket
import ssl
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

server_cert = 'server.crt'
port = 65432

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_hostname='127.0.0.1') as ssock:
            ssock.connect(('127.0.0.1', port))
            try:
                while True:
                    ssock.sendall(b'Hello, server!')
                    response = ssock.recv(1024).decode()
                    logging.info(response)
                    time.sleep(10)
            finally:
                ssock.close()

def main():
    while True:
        try:
            connect_to_server()
        except (socket.error, ssl.SSLError) as e:
            logging.error('Server is not available: {}. Retrying in 10 seconds...'.format(e))
            time.sleep(10)

if __name__ == '__main__':
    main()

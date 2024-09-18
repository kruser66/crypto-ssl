import argparse
import logging
import os
import ssl
import socket
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

server_cert = 'server.crt'
port = int(os.getenv('PORT', 65432))

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

def connect_to_server(message, interval):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_hostname='127.0.0.1') as ssock:
            ssock.connect(('127.0.0.1', port))
            try:
                while True:
                    ssock.sendall(message.encode())
                    response = ssock.recv(1024).decode()
                    logging.info(response)
                    time.sleep(interval)
            finally:
                ssock.close()

def main():
    parser = argparse.ArgumentParser(description='Client to send messages to the server.')
    parser.add_argument('-m', '--message', type=str, default='Hello, server!', help='Message to send to the server (default: "Hello, server!")')
    parser.add_argument('-i', '--interval', type=int, default=10, help='Interval in seconds between sending messages (default: 10)')
    args = parser.parse_args()

    while True:
        try:
            connect_to_server(args.message, args.interval)
        except (socket.error, ssl.SSLError) as e:
            logging.error('Server is not available: {}. Retrying in 10 seconds...'.format(e))
            time.sleep(10)

if __name__ == '__main__':
    main()

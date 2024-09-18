import socket
import ssl
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

server_key = 'server.key'
server_cert = 'server.crt'
port = 65432

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.options |= ssl.OP_SINGLE_ECDH_USE
# context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Отключаем только TLS 1.0 и 1.1

def handle_client(ssock):
    try:
        while True:
            message = ssock.recv(1024).decode()
            if not message:
                logging.info("Client disconnected")
                break
            logging.info('Received: {}'.format(message))
            capitalized_message = message.upper()
            ssock.send(capitalized_message.encode())
            logging.info('Sending answer...{}'.format(capitalized_message))
    except ssl.SSLError as e:
        logging.error("SSL error: {}".format(e))
    except Exception as e:
        logging.error("Error: {}".format(e))
    finally:
        ssock.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('', port))
    sock.listen(1)
    logging.info('Listen port: {}'.format(port))
    while True:
        try:
            client_sock, addr = sock.accept()
            logging.info("Connection from {}".format(addr))
            with context.wrap_socket(client_sock, server_side=True) as ssock:
                handle_client(ssock)
        except Exception as e:
            logging.error("Error during accept: {}".format(e))

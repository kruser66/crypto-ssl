import socket
import ssl

server_key = 'server.key'
server_cert = 'server.crt'
port = 65432

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Отключаем только TLS 1.0 и 1.1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('', port))
    sock.listen(1)
    print('Listen port: {}'.format(port))
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        print(addr)
        try:
            message = conn.recv(1024).decode()
            capitalizedMessage = message.upper()
            conn.send('Answer: {}'.format(capitalizedMessage.encode()))
        finally:
            conn.close()

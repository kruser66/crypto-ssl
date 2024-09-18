import asyncio
import logging
import os
import ssl

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

server_key = 'server.key'
server_cert = 'server.crt'
port = int(os.getenv('PORT', 65432))

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.options |= ssl.OP_SINGLE_ECDH_USE
# context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Отключаем только TLS 1.0 и 1.1

def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    logging.info('Connection from {}'.format(addr))
    try:
        while True:
            data = yield from reader.read(1024)
            if not data:
                logging.info('Client {} disconnected'.format(addr))
                break
            message = data.decode()
            logging.info('Received message from: {}'.format(addr))
            capitalized_message = message.upper()
            writer.write(capitalized_message.encode())
            logging.info('Answer: {} to {}'.format(capitalized_message, port))
            yield from writer.drain()
    except Exception as e:
        logging.error('Error: {}'.format(e))
    finally:
        writer.close()

def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_client, '127.0.0.1', port, ssl=context, loop=loop)
    server = loop.run_until_complete(coro)

    logging.info('Listen port: {}'.format(port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main()
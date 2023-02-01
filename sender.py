import asyncio
import argparse
import json
import sys
import logging

from environs import Env


HOST = 'minechat.dvmn.org'
PORT = 5050


def arg_parser(host, port):
    parser = argparse.ArgumentParser(prog='Script to send messages into minechat')

    parser.add_argument('user_hash', type=str, help='Your user hash')
    parser.add_argument('message', type=str, help='Message to send')
    parser.add_argument('-ho', '--host', type=str, help='Host of minechat', default=host)
    parser.add_argument('-p', '--port', type=int, help='Port of minechat', default=port)

    return parser.parse_args()


async def send_message(writer, message):
    message = message.encode(encoding="utf-8") + b'\n\n'
    writer.write(message)
    await writer.drain()
    logging.debug(f'message {message} has been sent')


async def get_messenger_connection(host, port, message, user_hash):
    reader, writer = await asyncio.open_connection(
        host, port)

    data = await reader.readline()
    logging.debug(data.decode())

    await send_message(writer, user_hash)

    data = await reader.readline()
    if json.loads(data) is None:
        logging.debug('Invalid token. Check it out or register again.')
        writer.close()
        return 
    logging.debug(data.decode())

    await send_message(writer, message)

    writer.close()


if __name__ == '__main__':
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.DEBUG)

    args = arg_parser(env('HOST', HOST), env('PORT', PORT))
    asyncio.run(get_messenger_connection(args.host, args.port, args.message, args.user_hash))

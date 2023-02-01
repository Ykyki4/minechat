import asyncio
import argparse
import logging

from environs import Env

from helpers import authorize, register


HOST = 'minechat.dvmn.org'
PORT = 5050


def arg_parser(host, port, nickname, user_hash):
    parser = argparse.ArgumentParser(prog='Script to send messages into minechat')

    parser.add_argument('message', type=str, help='Message to send')
    parser.add_argument('-n', '--nickname', type=str, help='Nickname you want to use', default=nickname)
    parser.add_argument('-ha', '--hash', type=str, help='Your user hash', default=user_hash)
    parser.add_argument('-ho', '--host', type=str, help='Host of minechat', default=host)
    parser.add_argument('-p', '--port', type=int, help='Port of minechat', default=port)

    return parser.parse_args()


async def get_messenger_connection(args):
    reader, writer = await asyncio.open_connection(
        args.host, args.port)

    if args.hash is not None:
        print('authorize')
        await authorize(reader, writer, args.hash, args.message)

    if args.nickname is not None:
        print('register')
        user_hash = await register(reader, writer, args.nickname)
        reader, writer = await asyncio.open_connection(
            args.host, args.port)
        await authorize(reader, writer, user_hash, args.message)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.DEBUG)

    args = arg_parser(env('HOST', HOST), env('PORT', PORT), env('NICKNAME', None), env('USER_HASH', None))
    asyncio.run(get_messenger_connection(args))

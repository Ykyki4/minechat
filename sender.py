import asyncio
import argparse
import logging

from environs import Env

from helpers import authorize, register,


HOST = 'minechat.dvmn.org'
PORT = 5050


def arg_parser(host, port):
    parser = argparse.ArgumentParser(prog='Script to send messages into minechat')

    parser.add_argument('message', type=str, help='Message to send')
    parser.add_argument('-u', '--username', type=str, help='Username you want to use')
    parser.add_argument('-ha', '--hash', type=str, help='Your user hash')
    parser.add_argument('-ho', '--host', type=str, help='Host of minechat', default=host)
    parser.add_argument('-p', '--port', type=int, help='Port of minechat', default=port)

    return parser.parse_args()


async def get_messenger_connection(args):
    reader, writer = await asyncio.open_connection(
        args.host, args.port)

    if args.hash:
        await authorize(reader, writer, args.hash, args.message)

    if args.username:
        user_hash = await register(reader, writer, args.username)
        reader, writer = await asyncio.open_connection(
            args.host, args.port)
        await authorize(reader, writer, user_hash, args.message)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.DEBUG)

    args = arg_parser(env('HOST', HOST), env('PORT', PORT))
    asyncio.run(get_messenger_connection(args))

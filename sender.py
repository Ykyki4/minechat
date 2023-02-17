import asyncio
import argparse
import logging

from environs import Env

from helpers import authorize, register, send_message, sanitize_message


HOST = 'minechat.dvmn.org'
PORT = 5050


def arg_parser(host, port, nickname, user_hash):
    parser = argparse.ArgumentParser(prog='Script to send messages into minechat')

    parser.add_argument('message', type=str, help='Message to send')
    parser.add_argument('-n', '--nickname', type=str, help='Nickname you want to use', default=nickname)
    parser.add_argument('-uh', '--user_hash', type=str, help='Your user hash', default=user_hash)
    parser.add_argument('-ho', '--host', type=str, help='Host of minechat', default=host)
    parser.add_argument('-p', '--port', type=int, help='Port of minechat', default=port)

    return parser.parse_args()


async def get_messenger_connection(args):
    reader, writer = await asyncio.open_connection(args.host, args.port)

    if args.user_hash:
        try:
            authorize_response = await authorize(reader, writer, args.user_hash)
            if authorize_response is None:
                logging.error('Invalid token. Check it out or register again.')
                return

            # Именно для отправки сообщения в чат требуется добавить два '\n', в остальных случаях всё нормально с одним.
            await send_message(writer, sanitize_message(args.message) + '\n')
        finally:
            writer.close()
    elif args.nickname:
        user_hash = await register(reader, writer, args.nickname)
        writer.close()

        reader, writer = await asyncio.open_connection(args.host, args.port)
        await authorize(reader, writer, user_hash)
        # Именно для отправки сообщения в чат требуется добавить два '\n', в остальных случаях всё нормально с одним.
        await send_message(writer, sanitize_message(args.message) + '\n')
        writer.close()
    else:
        logging.error('You need to pass only your hash or only your preferred nickname')


if __name__ == '__main__':
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.DEBUG)

    args = arg_parser(env('HOST', HOST), env('PORT', PORT), env('NICKNAME', None), env('USER_HASH', None))
    asyncio.run(get_messenger_connection(args))

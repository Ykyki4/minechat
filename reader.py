import asyncio
import datetime
import argparse
import logging

import aiofiles
from environs import Env


HOST = 'minechat.dvmn.org'
PORT = 5000
HISTORY_PATH = 'minechat.history'


def arg_parser(host, port, history_path):
    parser = argparse.ArgumentParser(prog='Script to read minechat')

    parser.add_argument('-ho', '--host', type=str, help='Host of minechat', default=host)
    parser.add_argument('-p', '--port', type=int, help='Port of minechat', default=port)
    parser.add_argument('-hp', '--history_path',
                        type=str,
                        help='Path to file where store minechat history',
                        default=history_path)

    return parser.parse_args()


async def read_messenger(reader, history_path):
    async with aiofiles.open(history_path, mode='a', encoding='utf-8') as f:
        while True:
            data = await reader.read(100)
            if not data:
                break
            try:
                current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

                message = f'[{current_datetime}] {data.decode().strip()}'

                await f.write(message + '\n')

                logging.debug(message)
            except UnicodeDecodeError:
                continue


async def get_messenger_connection(host, port, history_path):
    reader, writer = await asyncio.open_connection(host, port)

    message = f'[{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}] Установлено соединение'

    async with aiofiles.open(history_path, mode='w', encoding='utf-8') as f:
        await f.write(message+'\n')

    logging.debug(message)

    try:
        await read_messenger(reader, history_path)
    finally:
        logging.debug('Close the connection')
        writer.close()


if __name__ == '__main__':
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.DEBUG)

    args = arg_parser(env('HOST', HOST), env('PORT', PORT), env('HISTORY_PATH', HISTORY_PATH))
    asyncio.run(get_messenger_connection(args.host, args.port, args.history_path))

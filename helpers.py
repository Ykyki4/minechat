import logging
import json


def sanitize_message(messages):
    return messages.strip().replace('\r', '').replace('\n', '')


async def send_message(writer, message):
    message = message.encode(encoding='utf-8')+b'\n'
    writer.write(message)
    await writer.drain()
    logging.debug(f'message {message} has been sent')


async def register(reader, writer, nickname):
    received_line = await reader.readline()
    logging.debug(received_line.decode())

    await send_message(writer, '')

    received_line = await reader.readline()
    logging.debug(received_line.decode())

    await send_message(writer, sanitize_message(nickname))

    received_line = await reader.readline()
    response = json.loads(received_line.decode())
    user_hash = response.get('account_hash')
    nickname = response.get('nickname')
    user_received_line = f'Name: {nickname}, hash: {user_hash}'
    logging.debug(f'Registred. '+user_received_line)

    with open(f'{nickname}.txt', 'w', encoding='utf-8') as f:
        f.write(user_received_line)

    return user_hash


async def authorize(reader, writer, user_hash):
    received_line = await reader.readline()
    logging.debug(received_line.decode())

    await send_message(writer, sanitize_message(user_hash))

    received_line = await reader.readline()
    response = json.loads(received_line.decode())

    if response is None:
        logging.error('Invalid token. Check it out or register again.')
        writer.close()
        return

    logging.debug(f'Authorized. Name: {response.get("nickname")}, hash: {response.get("account_hash")}')

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
    data = await reader.readline()
    logging.debug(data.decode())

    await send_message(writer, '')

    data = await reader.readline()
    logging.debug(data.decode())

    await send_message(writer, sanitize_message(nickname))

    data = await reader.readline()
    response = json.loads(data.decode())
    user_hash = response.get('account_hash')
    nickname = response.get('nickname')
    user_data = f'Name: {nickname}, hash: {user_hash}'
    logging.debug(f'Registred. '+user_data)

    with open(f'{nickname}.txt', 'w', encoding='utf-8') as f:
        f.write(user_data)

    writer.close()

    return user_hash


async def authorize(reader, writer, user_hash, message):
    data = await reader.readline()
    logging.debug(data.decode())

    await send_message(writer, sanitize_message(user_hash))

    data = await reader.readline()
    if json.loads(data) is None:
        logging.error('Invalid token. Check it out or register again.')
        writer.close()
        return
    response = json.loads(data.decode())
    logging.debug(f'Authorized. Name: {response.get("nickname")}, hash: {response.get("account_hash")}')

    # Именно для отправки сообщения в чат требуется добавить два '\n', в остальных случаях всё нормально с одним.
    await send_message(writer, sanitize_message(message)+'\n')

    writer.close()

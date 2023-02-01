import asyncio
import sys
import datetime
import aiofiles

async def get_messenger_connection():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)

    message = f'[{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}] Установлено соединение'

    async with aiofiles.open('minechat.history', mode='w', encoding='utf-8') as f:
    	await f.write(message+'\n')

    print(message, file=sys.stdout)

    while True:
    	data = await reader.read(100)
    	if not data:
    		break
    	try:
    		current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    		message = f'[{current_datetime}] {data.decode().strip()}'

    		async with aiofiles.open('minechat.history', mode='a', encoding='utf-8') as f:
    			await f.write(message+'\n')

    		print(message, file=sys.stdout)
    	except UnicodeDecodeError:
    		continue

    print('Close the connection', file=sys.stdout)
    writer.close()

asyncio.run(get_messenger_connection())
# Gulambi - UserBot
# Copyright (C) 2022-3022
#
# This file is a part of <https://github.com/imDivu/Gulambi/>
# Please read the GNU General Public License
# <https://github.com/imDivu/Gulambi/blob/main/LICENSE/>.

import os
import logging
from typing import List
from asyncio.exceptions import TimeoutError as Timeout

from telethon import events
from telethon.sync import TelegramClient 
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import YouBlockedUserError

# Environments
CHATS: List[int] = [int(chat) for chat in os.environ.get('CHATS', '').split()]
API_ID: int = int(os.environ.get('API_ID', 123456))
API_HASH: str = os.environ.get('API_HASH', None)
SESSION: str = os.environ.get('SESSION', None)

# Logging
logging.basicConfig(
        format='%(message)s',
        level=logging.INFO,
        datefmt='%m/%d/%Y, %H:%M:%S',
        handlers=[logging.FileHandler('gulambi.log'), logging.StreamHandler()],
)
LOGS = logging.getLogger('[Gulambi]')
LOGS.info(
"""
                    -----------------------------------
                            Starting Deployment
                    -----------------------------------
"""
)


# Made By Divu (@AssKetchum)
# ===========================================
# Copyright (©) 2022-3022


with TelegramClient(StringSession(SESSION), API_ID, API_HASH) as client:


    @client.on(events.NewMessage(from_users=[572621020], chats=CHATS))
    async def guessing(event):
        if "hint:" in event.raw_text.lower():
            try:
                await event.forward_to('GulambiRobot')
                async with event.client.conversation('GulambiRobot') as conv:
                    response = await conv.wait_event(events.NewMessage(from_users=['GulambiRobot'], chats=['GulambiRobot']), timeout=10)
                results = response.text.replace('"', '').strip('][').split(', ')
                for result in results:
                     await event.respond(result)
            except YouBlockedUserError:
                return LOGS.info('You Blocked @GulambiRobot - Kindly /start @GulambiRobot.')
            except Timeout:
                return


    @client.on(events.NewMessage(from_users=[572621020], chats=CHATS))
    async def sendguess(event):
        if 'nobody guessed correctly.' in event.raw_text.lower() or (
           'guessed correctly.' in event.raw_text.lower() and '💵' in event.raw_text):
            await event.respond('/guess')
            try:
                response = await conv.wait_event(events.NewMessage(from_users=['GulambiRobot'], chats=CHATS, photo=True), timeout=15)
            except Timeout:
                await sendguess(event)


    LOGS.info('Gulambi has been deployed!....\n....')
    LOGS.info('Made With ❤\n....')
    LOGS.info('© @AssKetchum - (@GulambiRobot)')
    client.run_until_disconnected()

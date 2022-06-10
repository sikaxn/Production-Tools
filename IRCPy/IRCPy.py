#!/usr/bin/env python

import asyncio
import logging

import irctk


class Bot:
    async def connect(self, hostname, port=6667, secure=False):
        client = irctk.Client()
        client.delegate = self
        await client.connect(hostname, port, secure)

    def irc_registered(self, client):
        client.send('MODE', client.nick, '+B')
        client.send('JOIN', '#xmas')

    def irc_private_message(self, client, nick, message):
        if message == 'ping':
            client.send('PRIVMSG', nick, 'pong')

    def irc_channel_message(self, client, nick, channel, message):
        if message == 'ping':
            client.send('PRIVMSG', channel, f'{nick}: pong')
        elif message == 'quit':
            client.quit()


def mainTask():
    bot.connect('127.0.0.1')
    bot.irc_private_message(client,"#xmas", 'Hi')



if __name__ == '__main__':
    # Enable debug logging
    logging.basicConfig(level='DEBUG')

    bot = Bot()

    loop = asyncio.get_event_loop(mainTask())
    loop.create_task()
    loop.run_forever()
	
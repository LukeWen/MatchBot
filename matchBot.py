# -*- coding: utf-8 -*-
import json
from khl import TextMsg, Bot, Cert

# load config from config/botConfig.json, replace `path` points to your own config file
# config template: `./config/botConfig.json.example`
with open('./config/botConfig.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
print(config)
# init Cert and Bot
cert = Cert(client_id = config['client_id'], client_secret = config['client_secret'], token = config['token'])
bot = Bot(cmd_prefix=['.', '。'], cert=cert)


@bot.command(name='hello')
async def roll(msg: TextMsg):
    await msg.reply('world!')


bot.run()
# now invite the bot to ur server,
# and type '.hello'(in any channel) to check ur san today!
# (remember to grant read & send permissions to the bot first)
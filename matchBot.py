# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone, timedelta
from khl import TextMsg, Bot, Cert

# load config from config/botConfig.json, replace `path` points to your own config file
# config template: `./config/botConfig.json.example`
with open('./config/botConfig.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

with open('./jsonTemplate/menu.json', 'r', encoding='utf-8') as menu:
    menuJson = json.load(menu)

# init Cert and Bot
cert = Cert(client_id = config['client_id'], client_secret = config['client_secret'], token = config['token'])
bot = Bot(cmd_prefix=['.', '。'], cert=cert)
matchBoard = dict()
utc = timezone.utc
beijing = timezone(timedelta(hours=8))

@bot.command(name='菜单')
async def roll(msg: TextMsg):
    await msg.ctx.send_card_temp(menuJson)

@bot.command(name='组队')
async def roll(msg: TextMsg, t_info: str, t_time: str = 300):
    int_time = 0
    try:
        int_time = int(t_time)
    except ValueError as e:
        await msg.reply_temp('时间必须是数字')
    else:
        if int_time > 1800:
            int_time = 1800
        if int_time < 10:
            await msg.reply_temp('时间过短请重新申请')
        else:
            ddl = datetime.utcnow().replace(tzinfo=utc) + timedelta(seconds = int(t_time))
            matchInfo = (t_info, ddl)
            matchBoard[msg.author_id] = matchInfo
            print(msg.author_id)
            print(t_info)
            print(ddl.strftime("%Y-%m-%d %H:%M:%S"))
            await msg.reply_temp('(met)' + msg.author_id + '(met)发布成功\n信息：'+ t_info +' 截止时间：' + ddl.astimezone(beijing).strftime("%Y-%m-%d %H:%M:%S") )


@bot.command(name='取消组队')
async def roll(msg: TextMsg):
    matchBoard.pop(msg.author_id)
    await msg.reply_temp('取消组队成功')

@bot.command(name='所有组队')
async def roll(msg: TextMsg):
    nowtime = datetime.utcnow().replace(tzinfo=utc)
    global matchBoard
    matchBoard = filter_dict(matchBoard, lambda k,v: nowtime < v[1])
    if (len (matchBoard) < 1):
        await msg.reply_temp('还没有人组队哦')
    else:
        replyJson = '''[
            {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
                {
                "type": "section",
                "text": {
                    "type": "kmarkdown",
                    "content": "**组队信息**"
                }
            },
            {
            "type": "section",
            "text": {
                "type": "paragraph",
                "rows": ''' + str(len (matchBoard)) + ''',
                "fields": ['''
        for key, values in matchBoard.items():
            replyJson = replyJson + '''{
                "type": "kmarkdown",
                "content": "发布者：(met)'''+ str(key) +'''(met)\\n信息：''' + values[0] + '''\\t截止时间：''' + values[1].astimezone(beijing).strftime("%m-%d %H:%M:%S") + '''"
              },'''
        replyJson = replyJson[:-1]
        replyJson = replyJson + ']}}]}]'
        await msg.ctx.send_card_temp(replyJson)

def filter_dict(d, f):
    ''' Filters dictionary d by function f. '''
    newDict = dict()

    # Iterate over all (k,v) pairs in names
    for key, value in d.items():
        # Is condition satisfied?
        if f(key, value):
            newDict[key] = value

    return newDict

bot.run()
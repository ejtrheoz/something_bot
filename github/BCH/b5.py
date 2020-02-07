from telethon import TelegramClient, events, sync
import os
import time
import urllib.request
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import sys
from telethon.sync import TelegramClient
from telethon import functions, types

api_id = "1014479"
api_hash = "3b52708bdb4a7690d6f7f2f8f2503ee5"

client = TelegramClient('5', api_id, api_hash)

client.start()


username = "5"
wallet = "qpts650wkchyymzs80sxry29hu07c3l73ggumvezmm"
l = []
chan = []
bot_l = []
n = 1

def channel_visit(chan):
    time.sleep(3)
    client.send_message('BCH_clickbot', '/join')
    time.sleep(1)
    msgs = client.get_messages('BCH_clickbot')
    name = msgs[0].reply_markup.rows[0].buttons[0].url
    name = name.replace("https://t.me/", '')
    chan.append(name)

    if (len(chan) > 1) and (chan[-1] == chan[-2]):
        resp = client(GetBotCallbackAnswerRequest(
            'BCH Click Bot',
            msgs[0].id,
            data=msgs[0].reply_markup.rows[1].buttons[1].data
        ))
        print("повторяется ссылка")

    result = client(functions.channels.JoinChannelRequest(
            channel=name
        ))

    button_data = msgs[0].reply_markup.rows[0].buttons[1].data
    message_id = msgs[0].id

    resp = client(GetBotCallbackAnswerRequest(
                    'BCH Click Bot',
                    message_id,
                    data=button_data
                ))
    if len(chan) >= 2:
        del chan[0]

def bot_send(username, bot_l):
    time.sleep(3)
    client.send_message('BCH_clickbot', '/bots')
    time.sleep(1)
    msgs = client.get_messages('BCH_clickbot')
    url = msgs[0].reply_markup.rows[0].buttons[0].url
    url = url.replace("https://t.me/", "")
    name = ""
    for x in url:
        if x == '?':
            break
        name+= x

    bot_l.append(name)
    print(bot_l)
    if (len(bot_l) > 1) and (bot_l[-1] == bot_l[-2]):
        result = client(functions.messages.DeleteHistoryRequest(
            peer=name,
            max_id=0,
            just_clear=True,
            revoke=True
        ))
        print("повторяется ссылка")

    if (len(bot_l) > 1) and (bot_l[-1] == bot_l[-3]):
        button_data = msgs[0].reply_markup.rows[1].buttons[1].data
        message_id = msgs[0].id

        resp = client(GetBotCallbackAnswerRequest(
                        'BCH Click Bot',
                        message_id,
                        data=button_data
                    ))

    
    try:
        result = client(functions.messages.StartBotRequest(
            bot=name,
            peer=username,
            start_param="asasas"
        ))
    except:
        result = client(functions.messages.DeleteHistoryRequest(
            peer=name,
            max_id=0,
            just_clear=True,
            revoke=True
        ))

    time.sleep(2)
    msgs = client.get_messages(name)

    result = client(
        functions.messages.ForwardMessagesRequest(
            from_peer=name,
            id=[msgs[0].id],
            to_peer="BCH_clickbot",
            with_my_score=True
            ))
    if len(bot_l) >= 3:
        del bot_l[0]

while True:
    if n % 10 == 0:
        client.send_message('BCH_clickbot', '/withdraw')
        time.sleep(1)
        msgs = client.get_messages('BCH_clickbot')
            
        if "To withdraw, enter your" in msgs[0].message:
            client.send_message('BCH_clickbot', wallet)
            time.sleep(1)
            client.send_message('BCH_clickbot', '0.0001')
            time.sleep(1)
            client.send_message('BCH_clickbot', 'Confirm')
    j = 0    
            

    msgs = client.get_messages('BCH_clickbot')
    while True:
        j+=1
        if j == 20:
            h = 0
            print("другой заработок")
            while h <= 25:
                    try:
                        bot_send(username, bot_l)
                    except:
                        pass
                    h+=1
                    print(h)
                    try:
                        channel_visit(chan)
                    except:
                        pass
                    
                    h+=1
                    print(h)
            sys.exit(1)
        url_exist = True
        try:
            client.send_message('BCH_clickbot', '/visit')
            time.sleep(2)
            msgs = client.get_messages('BCH_clickbot')
            time.sleep(2)
            url = msgs[0].reply_markup.rows[0].buttons[0].url
        except:
            url_exist = False

        if msgs[0].reply_markup != None and url_exist == True:
            url = msgs[0].reply_markup.rows[0].buttons[0].url
            break

    print(url)
    l.append(url)
    
    button_data = msgs[0].reply_markup.rows[1].buttons[1].data
    message_id = msgs[0].id

    if (len(l) > 1) and (l[-1] == l[-2]):
        resp = client(GetBotCallbackAnswerRequest(
            'BCH Click Bot',
            message_id,
            data=button_data
        ))
        print("повторяется ссылка")
        continue
    
    to_check = True
    try:
        check = urllib.request.urlopen(url).read()
    except:
        to_check = False
    print("проверяю капча или нет")
    if to_check:
        check = urllib.request.urlopen(url).read()
        if "recaptcha" in str(check):
            resp = client(GetBotCallbackAnswerRequest(
                'BCH Click Bot',
                message_id,
                data=button_data
            ))
            print("капча")
            continue

    os.system("curl " + url)
    time.sleep(2)

    msgs = client.get_messages('BCH_clickbot')
    requirement = msgs[0].message
    if requirement == "Please stay on the site for at least 10 seconds...":
        os.system("curl " + url)
        print("закурлил ссылку")
        print("оставаться не нужно")
        time.sleep(14)

    if ('You must stay on the site for' in requirement):
        resp = client(GetBotCallbackAnswerRequest(
                'BCH Click Bot',
                message_id,
                data=button_data
            ))
    
    if (len(l) >= 2):
        del l[0]
    n+=1

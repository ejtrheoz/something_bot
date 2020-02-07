from telethon import TelegramClient, events, sync
import os
import time
import urllib.request
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import sys
from telethon.sync import TelegramClient
from telethon import functions, types

api_id = "1024716"
api_hash = "e997e320da04f4fa2c82c9f40d670b48"

client = TelegramClient('4', api_id, api_hash)

client.start()


username = "4"
wallet = "ltc1qwr5pmth9hzmf3s363mnnwzaaz5u84n9srkc3ju"
l = []
chan = []
bot_l = []
n = 1

def channel_visit(chan):
    time.sleep(3)
    client.send_message('Litecoin_click_bot', '/join')
    time.sleep(1)
    msgs = client.get_messages('Litecoin_click_bot')
    name = msgs[0].reply_markup.rows[0].buttons[0].url
    name = name.replace("https://t.me/", '')
    chan.append(name)

    if (len(chan) > 1) and (chan[-1] == chan[-2]):
        resp = client(GetBotCallbackAnswerRequest(
            'LTC Click Bot',
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
                    'LTC Click Bot',
                    message_id,
                    data=button_data
                ))
    if len(chan) >= 2:
        del chan[0]

def bot_send(username, bot_l):
    time.sleep(3)
    client.send_message('Litecoin_click_bot', '/bots')
    time.sleep(1)
    msgs = client.get_messages('Litecoin_click_bot')
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
                        'LTC Click Bot',
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
            to_peer="Litecoin_click_bot",
            with_my_score=True
            ))
    if len(bot_l) >= 3:
        del bot_l[0]

while True:
    if n % 10 == 0:
        client.send_message('Litecoin_click_bot', '/withdraw')
        time.sleep(1)
        msgs = client.get_messages('Litecoin_click_bot')
            
        if "To withdraw, enter your" in msgs[0].message:
            client.send_message('Litecoin_click_bot', wallet)
            time.sleep(1)
            client.send_message('Litecoin_click_bot', '0.0004')
            time.sleep(1)
            client.send_message('Litecoin_click_bot', 'Confirm')
    j = 0    
            

    msgs = client.get_messages('Litecoin_click_bot')
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
            client.send_message('Litecoin_click_bot', '/visit')
            time.sleep(2)
            msgs = client.get_messages('Litecoin_click_bot')
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
            'LTC Click Bot',
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
                'LTC Click Bot',
                message_id,
                data=button_data
            ))
            print("капча")
            continue

    os.system("curl " + url)
    time.sleep(2)

    msgs = client.get_messages('Litecoin_click_bot')
    requirement = msgs[0].message
    if requirement == "Please stay on the site for at least 10 seconds...":
        os.system("curl " + url)
        print("закурлил ссылку")
        print("оставаться не нужно")
        time.sleep(14)

    if ('You must stay on the site for' in requirement):
        resp = client(GetBotCallbackAnswerRequest(
                'LTC Click Bot',
                message_id,
                data=button_data
            ))
    
    if (len(l) >= 2):
        del l[0]
    n+=1

import requests  
import datetime
from config import BOT_TOKEN
from db import BotDB


class BotHandler:


    def __init__(self):
        self.db = BotDB()
        self.token = BOT_TOKEN
        self.api_url = 'https://api.telegram.org/bot5649451560:AAGib_eO3tvCAuqHoNLq5hpya8__69-ZMs4/'
        self.last_update = 0 


    def get_updates(self, timeout=30):
        method = 'getUpdates'
        params = {'offset' : self.last_update + 1,'timeout': timeout}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        if len(result_json) > 0:
            self.last_update = result_json[-1]['update_id']
            for i in result_json:
                message = i['message']
                #print(message)
                id = str(message['from']['id'])
                user_id = self.db.get_user_id(id)[0]
                telegramUserId = self.db.get_user_id(id)[1]
                if message['text'] == '/start':    
                    self.start(id)
                if message['text'].startswith('/write') and not message['text'].startswith('/write_tag'):
                    text = message['text'][7:]
                    create_message, message_id = self.db.create_message(user_id, text)
                    self.send_message(telegramUserId, f'заметка {message_id} сохранена')
                if message['text'] == '/read_last':
                    answer = self.db.read_last(user_id)
                    self.send_message(telegramUserId, answer)
                if message['text'].startswith('/read') and message['text'] != '/read_all' and message['text'][:9] != '/read_tag':
                    message_id = message['text'][6:]
                    message_id_exist, user_id_db = self.db.message_id_exist(message_id, user_id)
                    if message_id_exist == False:
                        if user_id_db == user_id:
                            self.send_message(telegramUserId, f'заметка {message_id} не найдена')
                        else:
                            self.send_message(telegramUserId, f'заметка {message_id} принадлежит другому пользователю')
                    else:
                        answer = self.db.read_id(message_id, user_id)
                        self.send_message(telegramUserId, answer)
                if message == '/read_all':
                    answer = self.db.read_all(user_id)
                    res = ''
                    for i in answer:
                        for j in i:
                            res += j+'\n'
                    self.send_message(telegramUserId, res)
                if message['text'][:9] == '/read_tag':
                    tag = message['text'][10:]
                    answer = self.db.read_tag(user_id,tag)
                    res = ''
                    for i in answer:
                        for j in i:
                            res += j+'\n'
                    self.send_message(telegramUserId, res)
                if message['text'].startswith('/write_tag'):
                    write_tag = message['text'].split(' #')[1:]
                    if len(write_tag) < 2:
                        continue
                    tag = '#' + write_tag[0]
                    descript = '#' + write_tag[1]
                    tag_id = self.db.get_tag_id(tag)[0]
                    if self.db.tag_exist(tag) == True:
                        self.db.write_tag_change(tag_id, descript)
                    else:
                        self.db.write_tag_new(tag, descript)
                if message['text'].startswith('/tag') and message['text'] != '/tag_all':
                    tags = message['text'].split(' #')[1:]
                    if len(tags) < 2:
                        continue
                    answer = ''
                    for t in tags:
                        t = '#' + t
                        tag_id = self.db.get_tag_id(t)[0]
                        res = self.db.tag(self.db.get_tag_id(t)[0])[0]
                        if res == '':
                            answer += t + ' ' + 'нет описания' + '\n'
                        else:
                            answer +=  res + '\n'
                    self.send_message(telegramUserId, answer)
                if message['text'] == '/tag_all' and message['text'] != '/tag':
                    answer = ''
                    res = self.db.tag_all()
                    print(answer)
                    for r in res:
                        if r[2] != '':
                            answer += r[2] + '\n'
                        else:
                            answer += r[1] + ' нет описания' + '\n'
                    self.send_message(telegramUserId, answer)

                    

                    




            


    def start(self,id):
        if self.db.user_exists(id) == False:
            self.db.create_user(id)
        else:
            self.id = self.db.get_user_id(id)

    def send_message(self,id, text):
        params = {'chat_id':id,'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

greet_bot = BotHandler()  


def main():  
    new_offset = None

    while True:
        greet_bot.get_updates(new_offset)


if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()


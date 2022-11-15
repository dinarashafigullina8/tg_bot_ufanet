import requests  
import datetime
from config import BOT_TOKEN
from db import BotDB
import logging



logging.basicConfig(level=logging.INFO, filename="py_log.log")
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
                res = ''
                res += 'id: '+ str(message['from']['id']) + ', ' + 'mesage: ' + message['text'] + ', ' + 'date: ' + str(datetime.datetime.fromtimestamp(message['date']))
                logging.info(res)
                id = str(message['from']['id'])
                user_id = self.db.get_user_id(id)[0]
                telegramUserId = self.db.get_user_id(id)[1]
                if message['text'] == '/start':    
                    self.start(id)
                if message['text'].startswith('/write '):
                    self.write(message,user_id,telegramUserId)
                if message['text'] == '/read_last':
                    self.read_last(user_id, telegramUserId)
                if message['text'].startswith('/read '):
                    self.read(message, user_id,telegramUserId)
                if message['text'] == '/read_all':
                    self.read_all(user_id, telegramUserId)
                if message['text'][:9] == '/read_tag':
                    self.read_tag(message, user_id, telegramUserId)
                if message['text'].startswith('/write_tag'):
                    self.write_tag(message)
                if message['text'].startswith('/tag '):
                    self.tag(message, telegramUserId)
                if message['text'] == '/tag_all':
                    self.tag_all(telegramUserId)

    def start(self,id):
        if self.db.user_exists(id) == False:
            self.db.create_user(id)
        else:
            self.id = self.db.get_user_id(id)

    def write(self,message,id, telegramId):
        text = message['text'][7:]
        create_message, message_id = self.db.create_message(id, text)
        print(create_message)
        self.send_message(telegramId, f'заметка {message_id} сохранена')
        print(self.send_message(telegramId, f'заметка {message_id} сохранена'))
        if '#' in text:
            text = text.split(' ')
            for t in text:
                if t.startswith('#'):
                    if self.db.tag_exist(t) == False:
                        res,tag_id = self.db.write_tag_new(t, '')
                        self.db.message_tag(message_id, tag_id)


    def read_last(self,id,telegramId):
        answer = self.db.read_last(id)
        self.send_message(telegramId, answer)

    def read(self, message, id, telegramId):
        message_id = message['text'][6:]
        message_id_exist, user_id_db = self.db.message_id_exist(message_id, id)
        if message_id_exist == False:
            messageText =f'заметка {message_id} не найдена'
            if user_id_db == id:
                messageText = f'заметка {message_id} принадлежит другому пользователю'
            self.send_message(telegramId, messageText)
        else:
            answer = self.db.read_id(message_id, id)
            self.send_message(telegramId, answer)

    def read_all(self, id, telegramId):
        answer = self.db.read_all(id)
        res = ''
        for i in answer:
            for j in i:
                res += j+'\n'
        self.send_message(telegramId, res)

    def read_tag(self, message, id, telegramId):
        text = message['text'][10:]
        tag = self.db.get_tag_id(text)[0]
        print(tag)
        answer = self.db.read_tag(tag,id)
        print(answer)
        res = ''
        for i in answer:
            for j in i:
                res += j+'\n'
        self.send_message(telegramId, res)

    def write_tag(self,message):
        write_tag = message['text'].split(' #')[1:]
        if len(write_tag) < 2:
            return False
        tag = '#' + write_tag[0]
        descript = '#' + write_tag[1]
        tag_id = self.db.get_tag_id(tag)[0]
        if self.db.tag_exist(tag) == True:
            self.db.write_tag_change(tag_id, descript)
        else:
            self.db.write_tag_new(tag, descript)
    
    def tag(self,message, telegramId):
        tags = message['text'].split(' #')[1:]
        if len(tags) < 2:
            return False
        answer = ''
        for t in tags:
            t = '#' + t
            tag_id = self.db.get_tag_id(t)[0]
            res = self.db.tag(tag_id)[0]
            if res == '':
                answer += t + ' ' + 'нет описания' + '\n'
            else:
                answer +=  res + '\n'
            self.send_message(telegramId, answer)
    
    def tag_all(self,telegramId):
        answer = ''
        res = self.db.tag_all()
        for r in res:
            if r[2] != '':
                answer += r[2] + '\n'
            else:
                answer += r[1] + ' нет описания' + '\n'
        self.send_message(telegramId, answer)


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


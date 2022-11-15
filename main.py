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
        self.api_url ='https://api.telegram.org/bot' + f'{self.token}' + '/'
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
                message_text = message['text'].partition(' ')
                print(message_text)
                command = message_text[0]
                text = message_text[2]
                id = str(message['from']['id'])
                loggegMessage = ''
                logDate = str(datetime.datetime.fromtimestamp(message['date']))
                loggegMessage += 'id: '+ id + ', ' + 'mesage: ' + message['text'] + ', ' + 'date: ' + logDate
                logging.info(loggegMessage)
                user_id = self.db.get_user_id(id)[0]
                telegramUserId = self.db.get_user_id(id)[1]
                if command == '/start':    
                    self.start(id)
                if command == '/write':
                    self.write(user_id,telegramUserId, text)
                if command == '/read_last':
                    self.read_last(user_id, telegramUserId)
                if command == '/read ':
                    self.read(text, user_id,telegramUserId)
                if command == '/read_all':
                    self.read_all(user_id, telegramUserId)
                if command == '/read_tag':
                    self.read_tag(text, user_id, telegramUserId)
                if command == '/write_tag':
                    self.write_tag(message)
                if command == '/tag ':
                    self.tag(message, telegramUserId)
                if command == '/tag_all':
                    self.tag_all(telegramUserId)

    def start(self,id):
        if self.db.user_exists(id) == False:
            self.db.create_user(id)

    def write(self,id, telegramId, text):
        # text = message['text'][7:]
        create_message, message_id = self.db.create_message(id, text)
        self.send_message(telegramId, f'заметка {message_id} сохранена')
        if '#' in text:
            text = text.split(' ')
            for t in text and self.db.tag_exist(t) == False:
                if t.startswith('#'):
                    res,tag_id = self.db.write_tag_new(t, '')
                    self.db.message_tag(message_id, tag_id)


    def read_last(self,id,telegramId):
        answer = self.db.read_last(id)
        self.send_message(telegramId, answer)

    def read(self, message_id, id, telegramId):
        message_id_exist, user_id_db = self.db.message_id_exist(text, id)
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

    def read_tag(self, text, id, telegramId):
        tag = self.db.get_tag_id(text)[0]
        answer = self.db.read_tag(tag,id)
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
        for tag in tags:
            tag = '#' + tag
            tag_id = self.db.get_tag_id(tag)[0]
            res = self.db.tag(tag_id)[0]
            if res == '':
                answer += tag + ' ' + 'нет описания' + '\n'
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
        return requests.post(self.api_url + method, params)

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


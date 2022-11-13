import requests  
import datetime
from config import BOT_TOKEN
from db import BotDB


class BotHandler:


    def __init__(self):
        self.db = BotDB()
        self.token = BOT_TOKEN
        self.api_url = 'https://api.telegram.org/bot5649451560:AAGib_eO3tvCAuqHoNLq5hpya8__69-ZMs4/'


    def get_updates(self, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        self.update_id = result_json['update_id']
        print(self.update_id)
        for i in result_json:
            message = i['message']
            id = str(message['from']['id'])
            # if message['text'] == '/start':    
            #     self.start(id)
            # if message['text'].startswith('/write'):
            #     text = message['text']
            #     self.db.create_message(self.db.get_user_id(id), text[7:])
            #     self.send_message('заметка {self.id} сохранена')
                


    def start(self,id):
        if self.db.user_exists(id) == False:
            self.db.create_user(id)
        else:
            self.id = self.db.get_user_id(id)

    def send_message(self, text):
        params = {'text': text}
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


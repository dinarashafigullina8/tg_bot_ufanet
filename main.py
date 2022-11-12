import requests
from time import sleep

url = 'https://api.telegram.org/bot5649451560:AAGib_eO3tvCAuqHoNLq5hpya8__69-ZMs4'

def get_updates_json(request):
    params = {'timeout': 100, 'offset': None}
    responce = requests.get(request + '/getupdates', data=params )
    return responce.json()

def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def main():  
    update_id = last_update(get_updates_json(url))['update_id']
    # while True:
    #     if update_id == last_update(get_updates_json(url))['update_id']:
    #        send_mess(get_chat_id(last_update(get_updates_json(url))), 'test')
    #        update_id += 1
    sleep(1)       

if __name__ == '__main__':  
    main()


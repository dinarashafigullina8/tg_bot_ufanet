from tg_bot import BotHandler

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


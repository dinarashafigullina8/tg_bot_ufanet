import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')


config = {
'user': 'root',
'password': '12345',
'host': '127.0.0.1',
'port': '3306',
'database': 'telegram_bot',
'raise_on_warnings': True,}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

class BotDB:
    def __init__(self):
        print('OK')

    def user_exists(self, telegramUserId):
        """Проверяем, есть ли юзер в базе"""
        result = cursor.execute("SELECT 'telegramUserId' FROM telegram_bot.user WHERE 'telegramUserId' = %s", (telegramUserId,))
        return bool(len(cursor.fetchall()))

    def get_user_id(self, telegramUserId):
        """Достаем юзера в базе по его user_id"""
        cursor.execute("SELECT * FROM telegram_bot.user WHERE telegramUserId = %s", (telegramUserId,))
        return cursor.fetchone()

    def create_user(self, telegramUserId):
        """Добавляем юзера в базу"""
        cursor.execute("INSERT INTO telegram_bot.user (telegramUserId) VALUES (%s)", (telegramUserId,))
        return cnx.commit()

    def create_message(self, user_id, text):
        """Создаем запись сообщения"""
        cursor.execute("INSERT INTO telegram_bot.message (user_id,text) VALUES (%s, %s)",(user_id, text))
        last_id = cursor.lastrowid
        return cnx.commit(), last_id 

    def message_tag(self, message_id, tag_id):
        """Создаем связь сообщения и тэга"""
        cursor.execute("INSERT INTO telegram_bot.message_tag (message_id, tag_id) VALUES (%s, %s)", (message_id, tag_id))
        return cnx.commit()

    def read_last(self, user_id):
        """Выводим последнее сообщение"""
        cursor.execute("SELECT text FROM telegram_bot.message WHERE user_id = %s ORDER BY createdAT DESC LIMIT 1", (user_id,))
        return cursor.fetchone()

    def read_id(self, message_id, user_id):
        """Выводим поле сообщение с указанным id"""
        cursor.execute("SELECT text FROM telegram_bot.message WHERE message_id = %s AND user_id = %s", (message_id, user_id))
        return cursor.fetchone()
    
    def message_id_exist(self, message_id, user_id):
        """Проверяем есть ли сообщение в базе"""
        cursor.execute("SELECT message_id FROM telegram_bot.message WHERE message_id = %s AND user_id = %s", (message_id, user_id))
        return bool(len(cursor.fetchall())), user_id

    def read_all(self, user_id):
        """Выводим все сообщения пользователя"""
        cursor.execute("SELECT text FROM telegram_bot.message WHERE user_id = %s ORDER BY createdAT", (user_id,))
        return cursor.fetchall()

    def read_tag(self,tag_id,user_id):
        """Выводим все сообщения с тэгом"""
        cursor.execute("SELECT text FROM telegram_bot.message left JOIN telegram_bot.message_tag ON telegram_bot.message.message_id = telegram_bot.message_tag.message_id WHERE tag_id = %s AND user_id = %s ORDER BY createdAT", (tag_id, user_id))
        return cursor.fetchall()
        
    def tag_exist(self, name):
        """Проверяем есть ли тэг в базе"""
        cursor.execute("SELECT name FROM telegram_bot.tag WHERE name = %s", (name,))
        return bool(len(cursor.fetchall()))
    
    def write_tag_new(self, name, descript):
        """Записываем новый тэг"""
        cursor.execute("INSERT INTO telegram_bot.tag (name, descript) VALUES (%s, %s)", (name, descript))
        last_id = cursor.lastrowid
        return cnx.commit(), last_id
    
    def get_tag_id(self, name):
        """Поиск id тэга"""
        cursor.execute("SELECT tag_id FROM telegram_bot.tag WHERE name = %s", (name,))
        return cursor.fetchone()

    def write_tag_change(self, tag_id, descript):
        """Изменяем старый тэг"""
        cursor.execute("SET SQL_SAFE_UPDATES = 0")
        cnx.commit()
        cursor.execute("UPDATE telegram_bot.tag SET descript = %s WHERE tag_id = %s", (descript, tag_id))
        return cnx.commit()

    def tag(self, tag_id):
        """Выводим описание тэгов"""
        cursor.execute("SELECT descript FROM telegram_bot.tag WHERE tag_id = %s", (tag_id,))
        return cursor.fetchone()

    def tag_all(self):
        """Выводим все тэги"""
        cursor.execute("SELECT * FROM telegram_bot.tag")
        return cursor.fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
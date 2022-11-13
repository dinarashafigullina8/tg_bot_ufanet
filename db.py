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

# with cnx.cursor() as cursor:   
#     cursor = cursor
# except Error as e:
# print('OK',e)

class BotDB:
    def __init__(self):
        print('OK')
    
        

    def user_exists(self, telegramUserId):
        """Проверяем, есть ли юзер в базе"""
        result = cursor.execute("SELECT 'telegramUserId' FROM telegram_bot.user WHERE 'telegramUserId' = %s", (telegramUserId,))
        return bool(len(cursor.fetchall()))

    def get_user_id(self, telegramUserId):
        """Достаем юзера в базе по его user_id"""
        cursor.execute("SELECT 'telegramUserId' FROM telegram_bot.user WHERE 'telegramUserId' = %s", (telegramUserId,))
        return cursor.fetchone()

    def create_user(self, telegramUserId):
        """Добавляем юзера в базу"""
        cursor.execute("INSERT INTO telegram_bot.user (telegramUserId) VALUES (%s)", (telegramUserId,))
        return cnx.commit()

    def create_message(self, user_id, text):
        """Создаем запись сообщения"""
        cursor.execute("INSERT INTO telegram_bot.message (user_id,text) VALUES (%s, %s)",(user_id, text))
        return cnx.commit()
    
    def read_last(self, text):
        """Выводим последнее сообщение"""
        result = self.cursor.execute("SELECT LAST_VALUE ('text') OVER (ORDER BY 'createdAT') FROM 'message' ", (text,))
        return result.fetchone()[0]

    def read_id(self, message_id):
        """Выводим поле сообщение с указанным id"""
        result = self.cursor.execute("SELECT 'text' FROM 'messsage' WHERE 'message_id' = ?", (message_id))
        return result.fetchone()[0]
    
    def read_all(self,text):
        """Выводим все сообщения пользователя"""
        result = self.cursor.execute("SELECT 'text' FROM 'messsage' ORDER BY 'createdAT'", (text,))
        return result.fetchone()[0]

    def read_tag(self,text):
        """Выводим все сообщения с тэгом"""
        result = self.cursor.execute("SELECT 'text' FROM 'message' INNER JOIN 'message_tag' WHERE 'message.message_id' = 'message_tag.message_id'INNER JOIN 'tag' WHERE 'message_tag.tag_id' = 'tag.tag_id' and 'tag' = ?", (text,))
        return result.fetchone()[0]
        
    def write_tag_new(self, name, descript):
        """Записываем новый тэг"""
        self.cursor.execute("INSERT INTO 'tag' ('name', 'desript') VALUES (?, ?)", (name, descript))
        return self.conn.commit()
    
    def write_tag_change(self, name, descript):
        """Изменяем старый тэг"""
        self.cursor.execute("UPDATE 'tag' SET 'descript' = ? WHERE 'name' = ?", (name, descript))
        return self.conn.commit()

    def tag(self, descript):
        """Выводим описание тэгов"""
        result = self.cursor.execute("SELECT 'descript' FROM 'tag' WHERE 'name' = ?", (descript,))
        return result.fetchone()[0]

    def tag_all(self, name, descript):
        """Выводим все тэги"""
        result = self.cursor.execute("SELECT 'name','descript' FROM 'tag'", (name,descript))
        return result.fetchone()[0]

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error


class BotDB:

    def __init__(self):
        try:
            with connect(
                host="localhost",
                user=input("Имя пользователя: "),
                password=getpass("Пароль: "),
                database="telegram_bot",
            ) as self.conn:
                print(self.conn)
        except Error as e:
            print(e)
        self.cursor = self.conn.cursor()

    def user_exists(self, telegramUserId):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT 'telegramUserId' FROM 'user' WHERE 'telegramUserId' = ?", (telegramUserId,))
        return bool(len(result.fetchall()))

    def get_user_id(self, telegramUserId):
        """Достаем юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT 'telegramUserId' FROM 'user' WHERE 'telegramUserId' = ?", (telegramUserId,))
        return result.fetchone()[0]

    def add_user(self, telegramUserId):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO 'user' ('telegramUserId') VALUES (?)", (telegramUserId,))
        return self.conn.commit()

    def add_message(self, user_id, operation, value):
        """Создаем запись сообщения"""
        self.cursor.execute("INSERT INTO 'message' ('createdAt', 'text') VALUES (?, ?, ?)",
            (self.get_user_id(user_id),
            operation == "+",
            value))
        return self.conn.commit()
    
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
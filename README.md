# tg_bot_ufanet
The repository contains a telegram bot application created without the use of auxiliary libraries (telebot etc.).
## To use the application, you need to install:
- python == 2.7
- pip-20.3.4
- mysql-connector-python==8.0.11
- config.py - bot token file
- .env - file with username and password for MySQL
## Install MySQL:
```
$ sudo apt-install mysql 

$ mysql -u root -p

```
Run the following to setup root password.

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';

FLUSH PRIVILEGES;
```
#### _NOTE: Make sure the telegram_bot database is created on your development machine!_
```
CREATE DATABASE telegram_bot;
```

## Import data from MySQL:
We go to MySQLWorkbench, create a connection, enter the password from the MySQL. Next, find the button Server in the menu, select Data Import. 


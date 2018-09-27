from peewee import *
from datetime import datetime

db = MySQLDatabase(host="localhost", user="root", password="", database="crudapplication")


class User(Model):
    client_name = CharField()
    email = CharField()
    password = CharField()

    class Meta:
        database = db
        db_table = 'users'

# User.create_table()
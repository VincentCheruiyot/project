from peewee import *
from datetime import datetime

db = MySQLDatabase(host="localhost", user="root", password="", database="crudapplication")


class Client(Model):
    # `id`, `client_name`, `registration_date`, `parent_name`, `postal_address`,
    # `personal_address`, `date_of_birth`, `gender`, `email`, `phone`, `client_package`, `lessons`
    client_name = CharField()
    registration_date = DateField()
    parent_name = CharField()
    postal_address = CharField()
    personal_address = CharField()
    date_of_birth = DateField()
    gender = CharField()
    email = CharField()
    phone = CharField()
    client_package = CharField()
    lessons = IntegerField()

    class Meta:
        database = db
        db_table = 'clients'


class Lesson(Model):
    client_id = IntegerField()
    lesson_date = DateField(default=datetime.now().date())

    class Meta:
        database = db
        db_table = 'lessons'


# Lesson.create_table()

class User(Model):
    names = CharField()
    email = CharField()
    password = CharField()

    class Meta:
        database = db
        db_table = 'users'

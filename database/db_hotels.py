from peewee import *

db = SqliteDatabase('hotels.db')

class Person(Model):
    telegram_id = IntegerField()
    name = CharField()

    class Meta:
        database = db


class DateTime(Model):
    name_id = ForeignKeyField(Person)
    when = DateTimeField()
    command = CharField()

    class Meta:
        database = db


class Hotels(Model):
    name_hotel = CharField()
    # name_hotel_who = ForeignKeyField(Person)
    name_hotel_when = ForeignKeyField(DateTime)

    class Meta:
        database = db

with db:
    Person.create_table()
    DateTime.create_table()
    Hotels.create_table()

from peewee import *


db = SqliteDatabase('users.db')

class BaseModel(Model):
    user_id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class User(BaseModel):
    command = CharField()

    class Meta:
        db_table = 'user'


class Output(BaseModel):
    output = CharField()

    class Meta:
        db_table = 'output'

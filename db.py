from peewee import *

database = SqliteDatabase('predictions.db')


class Prediction(Model):
    text = TextField()
    date_modified = DateField()

    class Meta:
        database = database

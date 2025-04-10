from peewee import Model, CharField, FloatField, DateField

from app.extensions import db


class BaseModel(Model):
    class Meta:
        database = db


class CurrencyRate(BaseModel):
    """Модель таблицы с кэшированными курсами валют."""
    date = DateField()
    code = CharField()
    rate = FloatField()

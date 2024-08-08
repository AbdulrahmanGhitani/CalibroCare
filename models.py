from peewee import *

database = SqliteDatabase('calibration.db')


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Device(BaseModel):
    brand = TextField(null=True)
    dept = TextField()
    name = TextField()
    recommendation = IntegerField(default=2, null=True)  # INTEGER (1)
    serial = TextField(primary_key=True)

    class Meta:
        table_name = 'device'


class Reading(BaseModel):
    device_serial = ForeignKeyField(column_name='device_serial', field='serial', model=Device)
    ref_value = FloatField()
    unit = TextField(null=True)
    value = FloatField()
    year = IntegerField()  # INTEGER (4)

    class Meta:
        table_name = 'reading'
        primary_key = False

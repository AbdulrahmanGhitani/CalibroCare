from peewee import *

database = SqliteDatabase('calibration.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Device(BaseModel):
    brand = TextField()
    category = TextField()
    dept_id = TextField()
    serial = TextField(primary_key=True)

    class Meta:
        table_name = 'device'

class Reading(BaseModel):
    device_serial = ForeignKeyField(column_name='device_serial', field='serial', model=Device)
    ref_value = FloatField()
    value = FloatField()
    year = UnknownField()  # INTEGER (4)

    class Meta:
        table_name = 'reading'
        primary_key = False


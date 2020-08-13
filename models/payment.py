import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.image import Image
from playhouse.hybrid import hybrid_property

class Payment(BaseModel):
    amount = pw.DecimalField()
    image = pw.ForeignKeyField(Image, backref="payments")
    sender = pw.ForeignKeyField(User, backref="payments")
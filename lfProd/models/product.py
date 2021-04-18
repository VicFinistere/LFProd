from lfProd.models import Base
from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Integer

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value
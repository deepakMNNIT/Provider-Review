from py_files.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship

class Provider(Base):
    __tablename__ = 'provider'
    provider_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)


class Provider_Review(Base):
    __tablename__ = 'provider_review'
    id = Column(Integer, primary_key=True)
    p_id = Column(Integer, ForeignKey('provider.provider_id'))
    review = Column(String)
    result = Column(String)
    provider = relationship(
        Provider,
        backref=backref('provider',
                        uselist=True,
                        cascade='delete,all'))

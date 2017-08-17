from sqlalchemy import Column, String, Integer, TIMESTAMP

from shrim._sqlalchemy_base import Base


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=200))
    last_name = Column(String(length=200))
    room = Column(Integer)
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)

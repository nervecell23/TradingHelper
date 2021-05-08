from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, Date

Base = declarative_base()


class Candle(Base):
    __tablename__ = "candles"
    id = Column(Integer, primary_key=True)
    open = (Column(Float),)
    high = (Column(Float),)
    low = (Column(Float),)
    close = (Column(Float),)
    starting_time = Column(Date)

    def __str__(self) -> str:
        return f"date: {self.starting_time}\nopen: {self.open}\nhigh: {self.high}\nlow: {self.low}\nclose: {self.close}"

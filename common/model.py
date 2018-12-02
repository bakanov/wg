# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Engine(Base):
    __tablename__ = 'engines'

    engine = Column(Text, primary_key=True)
    power = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)


class Hull(Base):
    __tablename__ = 'hulls'

    hull = Column(Text, primary_key=True)
    armor = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)


class Weapon(Base):
    __tablename__ = 'weapons'

    weapon = Column(Text, primary_key=True)
    reload_speed = Column(Integer, nullable=False)
    rotational_speed = Column(Integer, nullable=False)
    diameter = Column(Integer, nullable=False)
    power_volley = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)


class Ship(Base):
    __tablename__ = 'ships'

    ship = Column(Text, primary_key=True)
    weapon = Column(ForeignKey('weapons.weapon'), nullable=False)
    hull = Column(ForeignKey('hulls.hull'), nullable=False)
    engine = Column(ForeignKey('engines.engine'), nullable=False)

    engine1 = relationship('Engine')
    hull1 = relationship('Hull')
    weapon1 = relationship('Weapon')

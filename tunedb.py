import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Musician(Base):
    __tablename__ = 'musician'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    instruments = relationship('Instrument', 
                               secondary='musician_instrument_link')
    tunes = relationship('Tune',
                         secondary='musician_tune_link')


class Instrument(Base):
    __tablename__ = 'instrument'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class TimeSignature(Base):
    __tablename__ = 'timesignature'
    id = Column(Integer, primary_key=True)
    lower = Column(Integer)
    upper = Column(Integer)


class KeySignature(Base):
    __tablename__ = 'keysignature'
    id = Column(Integer, primary_key=True)
    name = Column(String(12), nullable=False)


class Tune(Base):
    __tablename__ = 'tune'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    timesignature = Column(Integer, 
                           ForeignKey('timesignature.id'), primary_key=True)
    keysignatures = relationship(KeySignature, 
                                 secondary='tune_keysignature_link')


class TuneKeySignatureLink(Base):
    __tablename__ = 'tune_keysignature_link'
    tune_id = Column(Integer, ForeignKey('tune.id'), primary_key=True)
    keysignature_id = Column(Integer, 
                             ForeignKey('keysignature.id'), primary_key=True)


class MusicianTuneLink(Base):
    __tablename__ = 'musician_tune_link'
    musician_id = Column(Integer, ForeignKey('musician.id'), primary_key=True)
    tune_id = Column(Integer, ForeignKey('tune.id'), primary_key=True)


class MusicianInstrumentLink(Base):
    __tablename__ = 'musician_instrument_link'
    musician_id = Column(Integer, ForeignKey('musician.id'), primary_key=True)
    instrument_id = Column(Integer, 
                           ForeignKey('instrument.id'), primary_key=True)


class MusicianTuneInstrumentLink(Base):
    __tablename__ = 'musician_tune_instrument_link'
    musician_id = Column(Integer, ForeignKey('musician.id'), primary_key=True)
    tune_id = Column(Integer, ForeignKey('tune.id'), primary_key=True)
    instrument_id = Column(Integer, 
                           ForeignKey('instrument.id'), primary_key=True)

fp = 'tunedb.sqlite'

from sqlalchemy import create_engine
engine = create_engine('sqlite:///' + fp)
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

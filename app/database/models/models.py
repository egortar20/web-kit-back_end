from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, UniqueConstraint, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class DSCIWeekData(Base):
    __tablename__ = "dsci_clean"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    releaseID = Column(Integer, nullable=False)
    mapDate = Column(VARCHAR(10), nullable=False)
    stateAbbr = Column(VARCHAR(5), nullable=False)
    none = Column(REAL, nullable=False)
    d0 = Column(REAL, nullable=False)
    d1 = Column(REAL, nullable=False)
    d2 = Column(REAL, nullable=False)
    d3 = Column(REAL, nullable=False)
    d4 = Column(REAL, nullable=False)

class DSCIAll(Base):
     __tablename__ = 'dsci_all'

     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
     date = Column(VARCHAR(10), nullable=False)
     value = Column(REAL, nullable=False)

class DSCISrw(Base):
     __tablename__ = 'dsci_srw'

     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
     date = Column(VARCHAR(10), nullable=False)
     value = Column(REAL, nullable=False)

class DSCISp(Base):
     __tablename__ = 'dsci_sp'

     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
     date = Column(VARCHAR(10), nullable=False)
     value = Column(REAL, nullable=False)

class DSCIWnr(Base):
     __tablename__ = 'dsci_wnr'

     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
     date = Column(VARCHAR(10), nullable=False)
     value = Column(REAL, nullable=False)
    
class allProduction(Base):
    __tablename__ = 'all_prod'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    stateAbbr = Column(VARCHAR(2), nullable=False)
    year = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)

class srwProduction(Base):
    __tablename__ = 'srw_prod'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    stateAbbr = Column(VARCHAR(2), nullable=False)
    year = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)

class srwProductionPct(Base):
    __tablename__ = 'srw_prod_pct'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    stateAbbr = Column(VARCHAR(2), nullable=False)
    year = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    
class spProduction(Base):
    __tablename__ = 'sp_prod'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    stateAbbr = Column(VARCHAR(2), nullable=False)
    year = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)

class wnrProduction(Base):
    __tablename__ = 'wnr_prod'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    stateAbbr = Column(VARCHAR(2), nullable=False)
    year = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
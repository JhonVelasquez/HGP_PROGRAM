from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from sqlalchemy import create_engine, select, Column, Integer, String, Date, ForeignKey, PrimaryKeyConstraint, Float, SmallInteger
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import func, extract
from sqlalchemy import or_, and_
from sqlalchemy import join
import re
from datetime import datetime,date,timedelta
from PyQt6 import QtCore, QtGui, QtWidgets
import inspect
from db_model import *

sqlite_engine = create_engine("sqlite:///.\\db\\hgp.db")

mysql_engine = create_engine("mysql+pymysql://root:R0ck0!@localhost:3306/hgp")


sqlite_session_maker = sessionmaker(bind=sqlite_engine)
sqlite_session = sqlite_session_maker()

mysql_session_maker = sessionmaker(bind=mysql_engine)
mysql_session = mysql_session_maker()


Base.metadata.create_all(mysql_engine)

for table in [Habitacion_caracteristica, Habitacion_cama, Habitacion_estado, Empleado, Cliente, Habitacion, Habitaciones_registro, Arquiler]:
    records = sqlite_session.query(table).all()
    for record in records:
        mysql_session.merge(record)

mysql_session.commit()

sqlite_session.close()
mysql_session.close()
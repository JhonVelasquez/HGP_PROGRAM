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
from sqlalchemy.sql import text

from datetime import datetime,date,timedelta
from PyQt6 import QtCore, QtGui, QtWidgets
import inspect
from db_model import *
from db import *

def migrar_db(url_from, url_to):
    try:
        r_f, mssg_f = validate_ping_db(url_from)
        r_t, mssg_t = validate_create_db(url_to)

        if(r_f == True and r_t == True):
            from_engine = create_engine(url_from)
            to_engine = create_engine(url_to)

            from_session = sessionmaker(bind=from_engine)()
            to_session = sessionmaker(bind=to_engine)()

            Base.metadata.create_all(to_engine)

            for table in [Habitacion_caracteristica, Habitacion_cama, Habitacion_estado, Empleado, Cliente, Habitacion, Habitaciones_registro, Arquiler]:
                records = from_session.query(table).all()
                for record in records:
                    to_session.merge(record)

            to_session.commit()

            from_session.close()
            to_session.close()                                          

        return mssg_f, mssg_t
    except BaseException as e:
        return "Error", (f"Error occurred: {e}")


""" 
url_from = "sqlite:///.\\db\\hgp_dev.db"
url_to = "mysql+pymysql://root:R0ck0!@localhost:3306/hgp_devx21"
migrar_db(url_from, url_to)
"""



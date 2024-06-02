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

import os
import re
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import urlparse, urlunparse
from sqlalchemy import text
import hashlib

class DataBase():
    url_db = None
    engine = None
    session = None
    #inspection = None
    
    def __init__(self, url):
        self.url_db = url
        self.engine = create_engine(self.url_db)
        #self.inspection = inspect(engine)

    def open_session(self):
        self.session = (sessionmaker(bind=self.engine))()

    def close_session(self):
        self.session.close_all()
        self.session = None     

    def get_dic_table_empleado(self,id_emp = None, username = None, order_by= None, n_last = None):
        try:
                
            self.open_session()
            result_query = self.session.query(Empleado)

            if(id_emp != None):
                result_query = result_query.filter( id_emp == Empleado.id)

            if(username != None):
                result_query = result_query.filter( username == Empleado.username)

            if(order_by is not None):
                result_query = result_query.order_by(order_by)
            else:
                result_query = result_query.order_by(Empleado.id.asc())

            if(n_last != None):
                result_fetch = result_query.limit(n_last).all()
            else:
                result_fetch = result_query.all()

            self.close_session()

            d={}
            for r in result_fetch:
                d[r.id]=r

            return d
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}

    def get_dic_table_habitacion(self, id_hab = None, asc_id_hab = True, asc_piso = True, asc_precioReferencia = False):
        count_filter=0
        try:
                
            self.open_session()
            result_query = self.session.query(Habitacion)
            
            if(id_hab != None):
                result_query = result_query.filter( id_hab == Habitacion.id)

            if(asc_piso == True):
                result_query = result_query.order_by(Habitacion.piso.asc())
                count_filter=count_filter+1
            elif(asc_piso == False):
                result_query = result_query.order_by(Habitacion.piso.desc())
                count_filter=count_filter+1
            
            if(asc_id_hab == True and count_filter < 2 ):
                result_query = result_query.order_by(Habitacion.id.asc())
                count_filter=count_filter+1
            elif(asc_id_hab == False and count_filter < 2 ):
                result_query = result_query.order_by(Habitacion.id.desc())
                count_filter=count_filter+1

            if(asc_precioReferencia == True and count_filter < 2 ):
                result_query = result_query.order_by(Habitacion.precioReferencia.asc())
            elif(asc_precioReferencia == False and count_filter < 2 ):
                result_query = result_query.order_by(Habitacion.precioReferencia.desc())
            
            result_fetch = result_query.all()
            self.close_session()

            d_hab = {}
            now =datetime.now()
            for hab in result_fetch:
                order_by = Habitaciones_registro.fechaHoraInicio.desc()
                inverted = True
                hab.last_registers =        self.get_dic_table_registro(inicio_min= None, inicio_max= now, empty_inicio= False, fin_min= None, fin_max= now, empty_fin= False, id_hab= hab.id, n_last= 3, order_by = order_by, inverted= inverted)
                hab.now_def_registers =     self.get_dic_table_registro(inicio_min= None, inicio_max= now, empty_inicio= False, fin_min= now, fin_max= None, empty_fin= False, id_hab= hab.id, n_last= 3, order_by = order_by, inverted= inverted)
                hab.now_undef_registers =   self.get_dic_table_registro(inicio_min= None, inicio_max= now, empty_inicio= False, fin_min= None, fin_max= None, empty_fin= True, id_hab= hab.id, n_last= 3, order_by = order_by, inverted= inverted)
                hab.fut_registers =         self.get_dic_table_registro(inicio_min= now, inicio_max= None, empty_inicio= False, fin_min= None, fin_max= None, empty_fin= None, id_hab= hab.id, n_last= 3, order_by = order_by, inverted= inverted)
                d_hab[hab.id]=hab
            
                if ((hab.id_permanent_state == 0) or ((hab.id_permanent_state == 1) and (len(hab.now_def_registers)==0) and (len(hab.now_undef_registers)==0))):#  0 state value is "Indisponible", 1 is "Disponible"
                    hr = Habitaciones_registro()
                    hr.id = None
                    hr.id_hab_est = hab.id_permanent_state
                    hab.now_def_registers[-1] = hr

            return d_hab
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}

    def get_dic_table_arquiler(self, id_arq= None, id_hab= None, document= None, name= None, surname= None, id_hab_reg= None, id_hab_est= None, fecha_checking:datetime= None, order_by= None, n_last = None, page_size = None, page_current = None):
        try:
                
            self.open_session()
            result_query = self.session.query(Arquiler, Cliente, Habitaciones_registro, Habitacion_estado)

            if(id_arq != None):
                result_query = result_query.filter( id_arq == Arquiler.id)

            if(id_hab != None):
                result_query = result_query.filter( id_hab == Arquiler.id_hab)

            if(document != None):
                result_query = result_query.filter( document == Cliente.nDocumento)

            if(name != None):
                result_query = result_query.filter( name == Cliente.nombre)

            if(surname != None):
                result_query = result_query.filter( surname == Cliente.apellido)

            if(id_hab_reg != None):
                result_query = result_query.filter( id_hab_reg == Arquiler.id_hab_reg)

            if(id_hab_est != None):
                result_query = result_query.filter( id_hab_est == Habitaciones_registro.id_hab_est)

            if(fecha_checking != None):
                dt_t_min = datetime(year=fecha_checking.year, month=fecha_checking.month, day=fecha_checking.day, hour=0, minute=0, second=0, microsecond=0)
                dt_t_max = dt_t_min + timedelta(days=1)

                result_query = result_query.filter( and_(dt_t_min <= Arquiler.fechaHoraChecking, dt_t_max > Arquiler.fechaHoraChecking))


            if(order_by is not None):
                result_query = result_query.order_by(order_by)
            else:
                result_query = result_query.order_by(Arquiler.lastUpdate.desc())

            result_query = result_query.outerjoin(Cliente, Arquiler.id_cli == Cliente.id)
            result_query = result_query.outerjoin(Habitaciones_registro, Arquiler.id_hab_reg == Habitaciones_registro.id)
            result_query = result_query.outerjoin(Habitacion_estado, Habitaciones_registro.id_hab_est == Habitacion_estado.id)

            result_query = result_query.order_by(Arquiler.lastUpdate.desc())

            if(page_current != None and page_size != None):
                result_query = result_query.offset(page_size*(page_current-1))
                result_fetch = result_query.limit(page_size).all()
            else:
                if(n_last != None):
                    result_fetch = result_query.limit(n_last).all()
                else:
                    result_fetch = result_query.all()

            self.close_session()
                
            d={}
            for r in result_fetch:
                arq_v = r[0]
                cli_v = r[1]
                hab_reg_v = r[2]
                hab_est_v = r[3]
                if(hab_reg_v != None): hab_reg_v.hab_estado = hab_est_v
                arq_v.cli = cli_v
                arq_v.hab_reg = hab_reg_v

                d[arq_v.id]=arq_v
            return d
             
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}


    def get_dic_table_cliente(self,id_cli = None, nDocumento = None, nombre = None, apellido = None, celular = None, n_last = None, order_by = None, page_size = None, page_current = None):
        try:
                
            self.open_session()
            result_query = self.session.query(Cliente)

            if(id_cli != None):
                result_query = result_query.filter( id_cli == Cliente.id)

            if(nDocumento != None):
                result_query = result_query.filter( nDocumento == Cliente.nDocumento)


            if(nombre != None):
                result_query = result_query.filter( nombre == Cliente.nombre)

            if(apellido != None):
                result_query = result_query.filter( apellido == Cliente.apellido)

            if(celular != None):
                result_query = result_query.filter( celular == Cliente.celular)

    
            if(order_by is not None):
                result_query = result_query.order_by(order_by)
            else:
                result_query = result_query.order_by(Cliente.lastUpdate.desc())

            if(page_current != None and page_size != None):
                result_query = result_query.offset(page_size*(page_current-1))
                result_fetch = result_query.limit(page_size).all()
            else:
                if(n_last != None):
                    result_fetch = result_query.limit(n_last).all()
                else:
                    result_fetch = result_query.all()

            self.close_session()

            d={}
            for r in result_fetch:
                d[r.id]=r

            return d
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}
           
    def get_dic_table_registro(self,id_hab_reg = None, id_hab_est = None, id_hab = None, n_last = None, dateInicio:datetime = None, page_size = None, page_current = None, inicio_min:datetime = None, inicio_max:datetime = None, empty_inicio:bool = None, fin_min:datetime = None, fin_max:datetime = None, empty_fin:bool = None, order_by = None, inverted = False):
        try:
            self.open_session()
            result_query = self.session.query(Habitaciones_registro)

            if(id_hab_reg != None):
                result_query = result_query.filter( id_hab_reg == Habitaciones_registro.id)

            if(id_hab != None):
                result_query = result_query.filter( id_hab == Habitaciones_registro.id_hab)

            if(id_hab_est != None):
                result_query = result_query.filter( id_hab_est == Habitaciones_registro.id_hab_est)

            if(dateInicio != None):
                dt_t_min = datetime(year=dateInicio.year, month=dateInicio.month, day=dateInicio.day, hour=0, minute=0, second=0, microsecond=0)
                dt_t_max = dt_t_min + timedelta(days=1)

                result_query = result_query.filter( and_(dt_t_min <= Habitaciones_registro.fechaHoraInicio, dt_t_max > Habitaciones_registro.fechaHoraInicio))

            if(inicio_min != None):
                result_query = result_query.filter(Habitaciones_registro.fechaHoraInicio >=  inicio_min)
            if(inicio_max != None):
                result_query = result_query.filter(Habitaciones_registro.fechaHoraInicio <=  inicio_max)
            if(fin_min != None):
                result_query = result_query.filter(Habitaciones_registro.fechaHoraFin >=  fin_min)
            if(fin_max != None):
                result_query = result_query.filter(Habitaciones_registro.fechaHoraFin <=  fin_max)
            if(empty_inicio != None):
                if(empty_inicio == True):
                    result_query = result_query.filter(Habitaciones_registro.fechaHoraInicio ==  None)
                else:
                    result_query = result_query.filter(Habitaciones_registro.fechaHoraInicio !=  None)

            if(empty_fin != None):
                if(empty_fin == True):
                    result_query = result_query.filter(Habitaciones_registro.fechaHoraFin ==  None)
                else:
                    result_query = result_query.filter(Habitaciones_registro.fechaHoraFin !=  None)
  
            
            if(order_by is not None):
                result_query = result_query.order_by(order_by)
            else:
                result_query = result_query.order_by(Habitaciones_registro.lastUpdate.desc())

            if(page_current != None and page_size != None):
                result_query = result_query.offset(page_size*(page_current-1))
                result_fetch = result_query.limit(page_size).all()
            else:
                if(n_last != None):
                    result_fetch = result_query.limit(n_last).all()
                else:
                    result_fetch = result_query.all()

            self.close_session()

            res = result_fetch
            if(inverted): res.reverse()

            d={}
            for r in res:
                d[r.id]=r

            return d
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}
    def get_dic_table_from_class(self,clss):
        try:
                
            self.open_session()
            result_query = self.session.query(clss)
            result_fetch = result_query.all()
            self.close_session()

            d={}
            for r in result_fetch:
                d[r.id]=r
            return d
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}
            
    def get_emp_from_username(self, username: str):
        var = self.get_dic_table_empleado(username= username)
        hr = list(var.values())
        if (len(hr)==0):
            return None
        else:
            return hr[0]


    def get_hab_reg_from_id(self,id):
        var = self.get_dic_table_registro(id_hab_reg=id)
        hr = list(var.values())
        if (len(hr)==0):
            return None
        else:
            return hr[0]
            
    def get_hab_from_id(self,id):
        var = self.get_dic_table_habitacion(id_hab=id)
        hr = list(var.values())
        if (len(hr)==0):
            return None
        else:
            return hr[0]
  
    def get_client_by_doc(self, doc):
        d_cl = self.get_dic_table_cliente(id_cli = None, nDocumento = doc, nombre = None, apellido = None,n_last = 1)
        
        if (len(d_cl)==0):
            return None
        else:
            return list(d_cl.values())[0]
        
    def get_client_by_id(self, cli_id):
        d_cl = self.get_dic_table_cliente(id_cli = cli_id, nDocumento = None, nombre = None, apellido = None,n_last = 1)
        
        if (len(d_cl)==0):
            return None
        else:
            return list(d_cl.values())[0]

    def get_arq_by_id(self, id):
        d_arq = self.get_dic_table_arquiler(id_arq= id, n_last = 1)
        
        if (len(d_arq)==0):
            return None
        else:
            return list(d_arq.values())[0]
        
    def create_object_class(self, class_var):
        try:
            b = class_var
            self.open_session()
            self.session.add(b)
            #self.session.flush()
            self.session.commit()
            self.session.refresh(b)
            self.close_session()
            return b

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        
    def create_Client(self, c: Cliente):
        return self.create_object_class(c)

    def create_Arquiler(self, a: Arquiler):
        return self.create_object_class(a)

    def create_Hab_Reg(self, a: Habitaciones_registro):
        return self.create_object_class(a)

    def update_Client(self, c: Cliente, c_d: Cliente):
        try:
            q_d = {}
            if(c.nDocumento != c_d.nDocumento): q_d["nDocumento"] = c.nDocumento
            if(c.nombre != c_d.nombre): q_d["nombre"] = c.nombre
            if(c.apellido != c_d.apellido): q_d["apellido"] = c.apellido
            if(c.datosAdicionales != c_d.datosAdicionales): q_d["datosAdicionales"] = c.datosAdicionales
            if(c.celular != c_d.celular): q_d["celular"] = c.celular

            if (len(q_d)!=0):
                if(c.lastUpdate != c_d.lastUpdate): q_d["lastUpdate"] = c.lastUpdate
                self.open_session()
                self.session.query(Cliente).filter(c_d.id == Cliente.id).update(q_d)
                self.session.commit()
                self.close_session()
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    
    def update_hab_reg_Arquiler(self, arq: Arquiler):
        try:
            q_d = {}
            q_d["id_hab_reg"] = arq.id_hab_reg
            
            if (len(q_d)!=0):
                q_d["lastUpdate"] = arq.lastUpdate
                self.open_session()
                self.session.query(Arquiler).filter(arq.id == Arquiler.id).update(q_d)
                self.session.commit()
                self.close_session()
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    
    
    def update_Arquiler(self, arq: Arquiler, arq_d: Arquiler):
        try:
            q_d = {}
            if(arq.id_hab != arq_d.id_hab): q_d["id_hab"] = arq.id_hab
            if(arq.id_cli != arq_d.id_cli): q_d["id_cli"] = arq.id_cli
            if(arq.id_emp != arq_d.id_emp): q_d["id_emp"] = arq.id_emp
            #if(arq.id_hab_reg != arq_d.id_hab_reg): q_d["id_hab_reg"] = arq.id_hab_reg
            if(arq.precioReal != arq_d.precioReal): q_d["precioReal"] = arq.precioReal
            if(arq.deuda != arq_d.deuda): q_d["deuda"] = arq.deuda
            if(arq.fechaHoraChecking != arq_d.fechaHoraChecking): q_d["fechaHoraChecking"] = arq.fechaHoraChecking
            if(arq.fechaHoraCheckout != arq_d.fechaHoraCheckout): q_d["fechaHoraCheckout"] = arq.fechaHoraCheckout

            if (len(q_d)!=0):
                if(arq.lastUpdate != arq_d.lastUpdate): q_d["lastUpdate"] = arq.lastUpdate
                self.open_session()
                self.session.query(Arquiler).filter(arq_d.id == Arquiler.id).update(q_d)
                self.session.commit()
                self.close_session()
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    
    def update_Hab_Reg(self, hab_reg: Habitaciones_registro, hab_reg_d: Habitaciones_registro):
        try:
            q_d = {}
            if(hab_reg.id_hab != hab_reg_d.id_hab): q_d["id_hab"] = hab_reg.id_hab
            if(hab_reg.id_hab_est != hab_reg_d.id_hab_est): q_d["id_hab_est"] = hab_reg.id_hab_est
            if(hab_reg.fechaHoraInicio != hab_reg_d.fechaHoraInicio): q_d["fechaHoraInicio"] = hab_reg.fechaHoraInicio
            if(hab_reg.fechaHoraFin != hab_reg_d.fechaHoraFin): q_d["fechaHoraFin"] = hab_reg.fechaHoraFin
            
            if (len(q_d)!=0):
                if(hab_reg.lastUpdate != hab_reg_d.lastUpdate): q_d["lastUpdate"] = hab_reg.lastUpdate
                self.open_session()
                self.session.query(Habitaciones_registro).filter(hab_reg_d.id == Habitaciones_registro.id).update(q_d)
                self.session.commit()
                self.close_session()
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

    def delete_object(self, class_var, object):
        try:
            self.open_session()
            self.session.query(class_var).filter(object.id == class_var.id).delete()
            self.session.commit()
            self.close_session()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

    def delete_Client(self, c_d: Cliente):
        self.delete_object( Cliente, c_d)

    def delete_Arquiler(self, a_d: Arquiler):
        self.delete_object( Arquiler, a_d)
    
    def delete_Hab_Reg(self, hr_d: Habitaciones_registro):
        self.delete_object( Habitaciones_registro, hr_d)

    def printList(self,list):
        for e in list.values():
            print(e)
        
    def get_test():
      
        return 0
    



def validate_connection_string(connection_string):
    sqlite_pattern = re.compile(r'sqlite:///(.+.db)')
    mysql_pattern = re.compile(r'mysql\+pymysql://[^:]+:[^@]+@[^:]+:\d+/[^/]+')

    if sqlite_pattern.match(connection_string):
        return 'sqlite'
    elif mysql_pattern.match(connection_string):
        return 'mysql'
    else:
        return None

def get_absolute_path(connection_string):
    parsed_url = urlparse(connection_string)
    db_path = parsed_url.path

    # Handle both forward and backward slashes
    if db_path.startswith('/') or db_path.startswith('\\'):
        db_path = db_path[1:]

    # Normalize and get the absolute path
    db_file = os.path.abspath(os.path.normpath(db_path))
    return db_file

def verify_path_existance(connection_string):
    db_file = get_absolute_path(connection_string)
    e = os.path.exists(db_file)
    return e, ("Path exists: "+str(e))

def validate_db_url(connection_string):
    db_type = validate_connection_string(connection_string)
    if db_type == 'sqlite':
        e,m = verify_path_existance(connection_string)
        if (e == True):
            try:
                return True, "Success validating db URL SQLITE", 'sqlite'
            except SQLAlchemyError as e:
                #print(f"Error occurred: {e}")
                return False, (f"Error occurred: {e}"), None
        else:
            #print(f"The SQLite database file {connection_string} does not exist.")
            return False, (f"The SQLite database file {connection_string} does not exist."), None
    elif db_type == 'mysql':
        # MySQL database
        try:
            return True, "Success validating db URL MYSQL", 'mysql'
        except SQLAlchemyError as e:
            #print(f"Error occurred: {e}")
            return False, (f"Error occurred: {e}"), None
    else:
        return False, ("Invalid or unsupported connection string format"), None

def ping_database(connection_string):
    engine = create_engine(connection_string)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.fetchone():
                #print("Successfully connected to the database")
                return True, ("Successfully connected to the database")
            else:
                #print("Failed to connect to the database")
                return False, ("Failed to connect to the database")
    except SQLAlchemyError as e:
        #print(f"Error occurred: {e}")
        return False, (f"Error occurred: {e}")

def validate_ping_db(connection_string):
    validate, mval, type_db = validate_db_url(connection_string)
    if(validate):
        return ping_database(connection_string)
    else:
        return False, mval
    
def validate_create_db(url_str: str):
    result = False
    type_db = validate_connection_string(url_str)
    #isValid, mssg, type_db = validate_db_url(url_str)
    if(type_db == 'mysql'):
        try:
            url = urlparse(url_str)
            db_name = url.path.lstrip('/')
            url_without_db = urlunparse(url._replace(path=''))
            engine_no_db = create_engine(url_without_db)
            
            therePing, mssgPing  = ping_database(url_without_db)
            if(therePing == True):
                with engine_no_db.connect() as conn:
                    conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {db_name}"))

            therePing, mssgPing  = ping_database(url_str)
            return therePing, mssgPing
        except SQLAlchemyError as e:
            return False, (f"Error occurred: {e}")
    elif(type_db == 'sqlite'):
        return True, "Ruta válida"
    else:
        return False, "Ruta inválida"

def read_db_file():
    content = ""
    file_path = 'db_address.txt'
    try:
        with open( file_path,'r') as data:  
            content = str(data.read()) 
    except FileNotFoundError:
        with open(file_path, 'w') as file:
            file.write("")
            content = ""
    return content

def write_db_file(content: str):
    file_path = 'db_address.txt'
    with open( file_path,'w') as data:  
        data.write(content)   

def getHashFromText(text: str):
    e_8 = text.encode('utf-8')
    h_8 = hashlib.sha3_512()
    h_8.update(e_8)
    hexdigest = (h_8.hexdigest())
    return hexdigest
    
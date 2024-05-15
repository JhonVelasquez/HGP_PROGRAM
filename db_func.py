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

Base = declarative_base()

class Habitacion_caracteristica(Base):
    __tablename__ = 'Habitacion_caracteristica'
    id = Column(Integer, primary_key=True)
    value = Column(String(50))
    def __str__(self):
        return 'id:{0} - value: {1}'.format(self.id,self.value)

class Habitacion_cama(Base):
    __tablename__ = 'Habitacion_cama'
    id = Column(Integer, primary_key=True)
    value = Column(String(50))
    def __str__(self):
        return 'id:{0} - value: {1}'.format(self.id,self.value)

class Habitacion_estado(Base):
    __tablename__ = 'Habitacion_estado'
    id = Column(Integer, primary_key=True)
    value = Column(String(50))
    is_in_arquiler = Column(String(10))
    background = Column(String(20))

    def __str__(self):
        return 'id:{0} - value: {1} - value: {2}'.format(self.id, self.value, self.is_in_arquiler)

class Habitacion(Base):
    __tablename__ = 'Habitacion'
    id = Column(String(20), primary_key=True)
    #id_hab_est = Column(Integer, ForeignKey('Habitacion.id_hab_est'))
    nombre = Column(String(50))
    descripcion = Column(String(50))
    precioReferencia = Column(Float)
    piso = Column(Integer)
    camas = Column(String(50))
    caracteristicas = Column(String(50))
    last_registers = {}
    def __str__(self):
        #return 'id:{0} - id_hab_est:{1} - nombre: {2} - descripcion: {3} - precioReferencia: {4} - piso: {5}- camas: {6}- caracteristicas: {7}'.format(self.id, str(self.id_hab_est),self.nombre,self.descripcion,self.precioReferencia,self.piso,self.camas,self.caracteristicas)
        return 'id:{0} - nombre: {1} - descripcion: {2} - precioReferencia: {3} - piso: {4}- camas: {5}- caracteristicas: {6}'.format(self.id,self.nombre,self.descripcion,self.precioReferencia,self.piso,self.camas,self.caracteristicas)
    
    
    """    
    def getEstadoString(self, d_Hab_est):
    est = ""
    last_hab_reg = self.getLastHabReg()
    if(last_hab_reg!=None):
        est = d_Hab_est[last_hab_reg.id_hab_est]
    return est
    """
    
    def getCamasList(self, d_Hab_cam):
        array_cammas = [int(num) for num in re.findall(r'\d+', self.camas)]
        array_cammas_str = []
        for n, a in enumerate(array_cammas):
           array_cammas_str.append(d_Hab_cam[a].value)
        return array_cammas_str

    def getCamasString(self, d_Hab_cam):
        array_cammas_str = self.getCamasList(d_Hab_cam)     
        txt = ""
        for n, a in enumerate(array_cammas_str):
            txt = txt + a
            if (n != (len(array_cammas_str)-1)):
                txt = txt + ", "
        return txt
    
    def getCaracteristicasList(self, d_Habitacion_car):
        array_car = [int(num) for num in re.findall(r'\d+', self.caracteristicas)]
        array_car_str = []
        for n, a in enumerate(array_car):
           array_car_str.append(d_Habitacion_car[a].value)
        return array_car_str

    def getCaracteristicasString(self, d_Habitacion_car):
        array_car = self.getCaracteristicasList(d_Habitacion_car)     
        txt = ""
        for n, a in enumerate(array_car):
            txt = txt + a
            if (n != (len(array_car)-1)):
                txt = txt + ", "
        return txt    
    
    def getCaracteristicasList(self):
        array_cammas = [int(num) for num in re.findall(r'\d+', self.caracteristicas)]
        return array_cammas

    def getCaracteristicasString(self, d_Habitacion_car):
        array_car = self.getCaracteristicasList()
        txt = ""
        for n, a in enumerate(array_car):
            txt = txt + d_Habitacion_car[a].value
            if (n != (len(array_car)-1)):
                txt = txt + ", "
        return txt

    def getTableElementByPos(self, pos, d_Hab_est, d_Hab_cam, d_Hab_car):
       match pos:
           case 0:
               return (self.id)
           case 1:
               return (self.piso)
           case 2:
               return self.nombre
           case 3:
               return self.getCamasString(d_Hab_cam)
           case 4:
               return self.descripcion
           case 5:
               return (self.precioReferencia)
           case 6:
               return self.getCaracteristicasString(d_Hab_car)
           case 7:
               b = list(self.last_registers.values())
               l_b = len(b)
               if l_b > 1:
                return b[0:l_b-1]
               else:
                return []
           case 8:
               b = list(self.last_registers.values())
               l_b = len(b)
               if l_b != 0:
                return [b[l_b-1]]
               else:
                return []
           case _:
               return "--"
    def getLastHabReg(self):
            b = list(self.last_registers.values())
            l_b = len(b)
            if l_b != 0:
                return b[l_b-1]
            else:
                return  None

                   
table_hab_column_names = { 0 : "ID", 1 : "Piso", 2 : "Nombre", 3 : "Camas", 4 : "Descripcion", 5 : "Precio Base", 6 : "Caracteristicas", 7 : "Estado anterior", 8 : "Estado actual"}

""" 
class Habitacion_caracteristica_join(Base):
    __tablename__ = 'Habitacion_caracteristica_join'
    id = Column(Integer, primary_key=True)
    id_hab = Column(String(20),ForeignKey('Habitacion.id'))
    id_hab_car = Column(Integer, ForeignKey('Habitacion_caracteristica.id'))
    def __str__(self):
        return 'id:{0} - id_hab:{1} - id_hab_car: {2}'.format(self.id,self.id_hab,self.id_hab_car)


class Habitacion_cama_join(Base):
    __tablename__ = 'Habitacion_cama_join'
    id = Column(Integer, primary_key=True)
    id_hab = Column(String(20),ForeignKey('Habitacion.id'))
    id_hab_cam = Column(Integer, ForeignKey('Habitacion_cama.id'))
    def __str__(self):
        return 'id:{0} - id_hab:{1} - id_hab_cam: {2}'.format(self.id,self.id_hab,self.id_hab_cam)
 """

class Habitaciones_registro(Base):
    __tablename__ = 'Habitaciones_registro'
    id = Column(Integer, primary_key=True)
    id_hab = Column(String(20),ForeignKey('Habitacion.id'))
    id_hab_est = Column(Integer, ForeignKey('Habitacion_estado.id'))
    fechaHoraInicio = Column(DateTime)
    fechaHoraFin = Column(DateTime)
    lastUpdate = Column(DateTime)
    hab_estado = None
    def __str__(self):
        return 'id:{0} - id_hab: {1} - id_hab_est: {2} - fechaHoraInicio: {3} - fechaHoraFin: {4} - lastUpdate: {5} '.format(self.id,self.id_hab,self.id_hab_est,self.fechaHoraInicio,self.fechaHoraFin,self.lastUpdate)
    
    def getEstadoString(self, d_Hab_est):
            return d_Hab_est[self.id_hab_est].value
    
    def getTableElementByPos(self, pos, d_Hab_est):
       match pos:
           case 0:
               return (self.id)
           case 1:
                if(self.fechaHoraInicio != None):
                    return str(self.fechaHoraInicio.replace(microsecond=0))
                else:
                    return None
           case 2:
                if(self.fechaHoraFin != None):
                    return str(self.fechaHoraFin.replace(microsecond=0))
                else:
                    return None
           case 3:
               return (self.id_hab)
           case 4:
               return self.getEstadoString(d_Hab_est)
           case 5:
                if(self.lastUpdate != None):
                    return str(self.lastUpdate.replace(microsecond=0))
                else:
                    return None
           case _:
               return "--"
                   
table_hab_reg_column_names = { 0 : "ID", 1 : "F/h Inicio", 2 : "F/h Fin", 3 : "Habitacion", 4 : "Estado", 5 : "Ultima modificación"}
table_hab_reg_column_variable = { 0 : Habitaciones_registro.id, 1 : Habitaciones_registro.fechaHoraInicio, 2 : Habitaciones_registro.fechaHoraFin, 3 : Habitaciones_registro.id_hab, 4 : Habitaciones_registro.id_hab_est, 5 : Habitaciones_registro.lastUpdate}


class Empleado(Base):
    __tablename__ = 'Empleado'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(20))
    apellido = Column(String(20))
    contrasena = Column(String(20))
    def __str__(self):
        return 'id:{0} - nombre: {1} - apellido: {2} - contrasena: {3}'.format(self.id,self.nombre,self.apellido,self.contrasena)

class Cliente(Base):
    __tablename__ = 'Cliente'
    id = Column(Integer, primary_key=True)
    nDocumento = Column(String(20))
    nombre = Column(String(20))
    apellido = Column(String(20))
    datosAdicionales = Column(String(50))
    celular = Column(String(15))
    lastUpdate = Column(DateTime)
    def __str__(self):
        return 'id:{0} - nDocumento: {1} - nombre: {2} - apellido: {3} - datosAdicionales: {4} - celular: {5} - fechaHoraChecking: {6}'.format(self.id,self.nDocumento,self.nombre,self.apellido,self.datosAdicionales,self.celular,self.lastUpdate)

    def getTableElementByPos(self, pos):
       match pos:
           case 0:
               return (self.id)
           case 1:
               return (self.nDocumento)
           case 2:
               return self.nombre
           case 3:
               return self.apellido
           case 4:
               return self.datosAdicionales
           case 5:
               return self.celular
           case 6:
                if(self.lastUpdate != None):
                    return str(self.lastUpdate.replace(microsecond=0))
                else:
                    return None
           case _:
               return "--"
                   
table_cli_column_names = { 0 : "ID", 1 : "nDocumento", 2 : "Nombre", 3 : "Apellido", 4 : "Datos adicionales", 5 : "Celular", 6 : "Ultima modificación"}

class Arquiler(Base):
    __tablename__ = 'Arquiler'
    id = Column(Integer, primary_key=True)
    id_hab = Column(String(20),ForeignKey('Habitacion.id'))
    id_cli = Column(Integer, ForeignKey('Cliente.id'))
    id_emp = Column(Integer, ForeignKey('Empleado.id'))
    id_hab_reg = Column(Integer, ForeignKey('Habitaciones_registro.id'))
    precioReal = Column(Float)
    deuda = Column(Float)
    fechaHoraChecking = Column(DateTime)
    fechaHoraCheckout = Column(DateTime)
    lastUpdate = Column(DateTime)
    cli = Cliente()
    hab_reg = Habitaciones_registro()
    def __str__(self):
        return 'id:{0} - id_hab: {1} - id_cli: {2} - id_emp: {3} - id_hab_reg: {4} - precioReal: {5} - deuda: {6} - fechaHoraChecking: {7} - fechaHoraCheckout: {8} - lastUpdate: {9} - cliente: {10} - hab_est: {11} '.format(self.id,self.id_hab,self.id_cli,self.id_hab_est,self.id_emp,self.precioReal,self.deuda,self.fechaHoraChecking,self.fechaHoraCheckout,self.lastUpdate, self.cli, self.hab_est)

    def getEmpleadoString(self, d_Empleado):
        return d_Empleado[self.id_emp].nombre

    def getTableElementByPos(self, pos, d_Empleado):
       match pos:
           case 0:
               return (self.id)
           case 1:
               return (self.id_hab)
           case 2:
               if(self.cli != None):
                    return self.cli.nDocumento + ", " + self.cli.nombre + " " + self.cli.apellido
               else:
                    return "-"
           case 3:
               return self.getEmpleadoString(d_Empleado)
           case 4:
               if(self.hab_reg != None and self.hab_reg.hab_estado != None ):
                return str(self.hab_reg.id) + ", " + str(self.hab_reg.hab_estado.value)
               else:
                return "-"
           case 5:
                if(self.fechaHoraChecking != None):
                    return str(self.fechaHoraChecking.replace(microsecond=0))
                else:
                    return None
           case 6:
                if(self.fechaHoraCheckout != None):
                    return str(self.fechaHoraCheckout.replace(microsecond=0))
                else:
                    return None
           case 7:
               return (self.precioReal)
           case 8:
               return (self.deuda)
           case 9:
                if(self.lastUpdate != None):
                    return str(self.lastUpdate.replace(microsecond=0))
                else:
                    return None
           case _:
               return "--"
                   
table_arq_column_names = { 0 : "ID", 1 : "Habitacion", 2 : "Cliente", 3 : "Empleado", 4 : "Hab_estado", 5 : "F/h checking", 6 : "F/h checkout", 7 : "Precio", 8 : "Deuda", 9 : "Ultima modificación"}


class DataBase():
    url_db = None
    engine = None
    session = None
    #inspection = None
    
    def init_db(self):
        self.url_db = "sqlite:///.\\db\\hgp_dev.db"
        self.engine = create_engine(self.url_db)
        #self.inspection = inspect(engine)

    def open_session(self):
        self.session = (sessionmaker(bind=self.engine))()

    def close_session(self):
        self.session.close_all()
        self.session = None     

    def get_dic_table_habitacion(self,asc_id_hab, asc_piso, asc_precioReferencia):
        count_filter=0
        try:
                
            self.open_session()
            result_query = self.session.query(Habitacion)
            
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
            for hab in result_fetch:
                hab.last_registers = self.get_dic_table_registro(id_hab = hab.id, n_last = 5, maximum_date_inicio = datetime.now(), order_by = Habitaciones_registro.fechaHoraInicio.desc(), inverted= True)
                d_hab[hab.id]=hab
            return d_hab
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}

    def get_dic_table_arquiler(self,id_arq = None, id_hab = None, n_last = None, dateChecking = None, page_size = None, page_current = None):
        try:
                
            self.open_session()
            result_query = self.session.query(Arquiler, Cliente, Habitaciones_registro, Habitacion_estado)

            if(id_arq != None):
                result_query = result_query.filter( id_arq == Arquiler.id)

            if(id_hab != None):
                result_query = result_query.filter( id_hab == Arquiler.id_hab)

            if(dateChecking != None):
                result_query = result_query.filter( dateChecking == Arquiler.fechaHoraChecking)

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
        
    def get_dic_table_arquiler_test(self,id_arq = None, id_hab = None, n_last = None, dateChecking = None, page_size = None, page_current = None):
        try:
                
            self.open_session()
            result_query = self.session.query(Arquiler, Cliente)

            if(id_arq != None):
                result_query = result_query.filter( id_arq == Arquiler.id)

            if(id_hab != None):
                result_query = result_query.filter( id_hab == Arquiler.id_hab)

            if(dateChecking != None):
                result_query = result_query.filter( dateChecking == Arquiler.fechaHoraChecking)

            result_query = result_query.filter( Arquiler.id_cli == Cliente.id)

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
            i=1
            for r in result_fetch:
                r[0].cli = r[1]
                print(i)
                i=i+1
                print(r[0])
                print("-")
             
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return {}

    def get_dic_table_cliente(self,id = None, nDocumento = None, nombre = None, apellido = None,n_last = None, page_size = None, page_current = None):
        try:
                
            self.open_session()
            result_query = self.session.query(Cliente)

            if(id != None):
                result_query = result_query.filter( id == Cliente.id)

            if(nDocumento != None):
                result_query = result_query.filter( nDocumento == Cliente.nDocumento)


            if(nombre != None):
                result_query = result_query.filter( nombre == Cliente.nombre)

            if(apellido != None):
                result_query = result_query.filter( apellido == Cliente.apellido)

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
        
    def get_dic_table_registro(self,id_hab_reg = None, id_hab_est = None, id_hab = None, n_last = None, dateInicio:datetime = None, page_size = None, page_current = None, maximum_date_inicio:datetime = None, order_by = None, inverted = False):
        try:
            print("Getting hab_Reg from db" + str(datetime.now()))
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

            if(maximum_date_inicio != None):
                result_query = result_query.filter(Habitaciones_registro.fechaHoraInicio < maximum_date_inicio)
  
            
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
            
    def get_hab_reg_from_id(self,id):
        try:

            self.open_session()
            hr = self.session.query(Habitaciones_registro).filter(Habitaciones_registro.id == id).all()
            self.close_session()

            if (len(hr)==0):
                return None
            else:
                return hr[0]
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return None
            
    def get_hab_from_id(self,id):
        try:

            self.open_session()
            hab_list = self.session.query(Habitacion).filter(Habitacion.id == id).all()
            self.close_session()
            

            if (len(hab_list)==0):
                return None
            else:
                hab = hab_list[0]
                hab.last_registers = self.get_dic_table_registro(id_hab = hab.id, n_last = 5, maximum_date_inicio = datetime.now(), order_by = Habitaciones_registro.fechaHoraInicio.desc(), inverted= True)
                return hab
            
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return None
  
    def get_client_by_doc(self, doc):
        d_cl = self.get_dic_table_cliente(id = None, nDocumento = doc, nombre = None, apellido = None,n_last = 1)
        
        if (len(d_cl)==0):
            return None
        else:
            return list(d_cl.values())[0]
        
    def get_client_by_id(self, cli_id):
        d_cl = self.get_dic_table_cliente(id = cli_id, nDocumento = None, nombre = None, apellido = None,n_last = 1)
        
        if (len(d_cl)==0):
            return None
        else:
            return list(d_cl.values())[0]

    def get_arq_by_id(self, id):
        d_arq = self.get_dic_table_arquiler(id_arq= id, n_last = 1, dateChecking = None)
        
        if (len(d_arq)==0):
            return None
        else:
            return list(d_arq.values())[0]
        
    def create_Client(self, c: Cliente):
        try:

            self.open_session()
            self.session.add(c)
            self.session.commit()
            self.close_session()

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

    def create_Arquiler(self, a: Arquiler):
        try:
            b = a
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

    def create_Hab_Reg(self, a: Habitaciones_registro):
        try:
            b = a
            self.open_session()
            self.session.add(b)
            self.session.commit()
            #self.session.flush()
            self.session.refresh(b)
            self.close_session()
            return b

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

    def delete_Client(self, c_d: Cliente):
        try:
            self.open_session()
            self.session.query(Cliente).filter(c_d.id == Cliente.id).delete()
            self.session.commit()
            self.close_session()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    
    def update_Client(self, c: Cliente, c_d: Cliente):
        try:
            q_d = {}
            if(c.nDocumento != c_d.nDocumento): q_d["nDocumento"] = c.nDocumento
            if(c.nombre != c_d.nombre): q_d["nombre"] = c.nombre
            if(c.apellido != c_d.apellido): q_d["apellido"] = c.apellido
            if(c.datosAdicionales != c_d.datosAdicionales): q_d["datosAdicionales"] = c.datosAdicionales
            if(c.celular != c_d.celular): q_d["celular"] = c.celular
            if(c.lastUpdate != c_d.lastUpdate): q_d["lastUpdate"] = c.lastUpdate

            if (len(q_d)!=0):
                self.open_session()
                self.session.query(Cliente).filter(c_d.id == Cliente.id).update(q_d)
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
            if(arq.id_hab_reg != arq_d.id_hab_reg): q_d["id_hab_reg"] = arq.id_hab_reg
            if(arq.precioReal != arq_d.precioReal): q_d["precioReal"] = arq.precioReal
            if(arq.deuda != arq_d.deuda): q_d["deuda"] = arq.deuda
            if(arq.fechaHoraChecking != arq_d.fechaHoraChecking): q_d["fechaHoraChecking"] = arq.fechaHoraChecking
            if(arq.fechaHoraCheckout != arq_d.fechaHoraCheckout): q_d["fechaHoraCheckout"] = arq.fechaHoraCheckout
            if(arq.lastUpdate != arq_d.lastUpdate): q_d["lastUpdate"] = arq.lastUpdate

            if (len(q_d)!=0):
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
            if(hab_reg.lastUpdate != hab_reg_d.lastUpdate): q_d["lastUpdate"] = hab_reg.lastUpdate

            if (len(q_d)!=0):
                self.open_session()
                self.session.query(Habitaciones_registro).filter(hab_reg_d.id == Habitaciones_registro.id).update(q_d)
                self.session.commit()
                self.close_session()
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


    def delete_Arquiler(self, a_d: Arquiler):
        try:
            self.open_session()
            self.session.query(Arquiler).filter(a_d.id == Arquiler.id).delete()
            self.session.commit()
            self.close_session()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    
    def delete_Hab_Reg(self, hr_d: Habitaciones_registro):
        try:
            self.open_session()
            self.session.query(Habitaciones_registro).filter(hr_d.id == Habitaciones_registro.id).delete()
            self.session.commit()
            self.close_session()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    

    def printList(self,list):
        for e in list.values():
            print(e)

    """    
        def get_Arquiler_table(self,filter_hab, filter_piso, filter_hab_est, ascChecking):
        
        self.open_session()
        result_query = self.session.query(Arquiler, Habitacion, Cliente, Empleado, Habitacion_estado)\
        #    .join(Habitacion, Habitacion.id == Arquiler.id_hab)\
        #    .join(Cliente, Cliente.id == Arquiler.id_cli)\
        #    .join(Empleado, Empleado.id == Arquiler.id_emp)\
        #    .join(Habitacion_estado, Habitacion_estado.id == Habitacion.id_hab_est)\

        result_query = result_query.filter( Habitacion.id == Arquiler.id_hab)
        result_query = result_query.filter( Cliente.id == Arquiler.id_cli)
        result_query = result_query.filter( Empleado.id == Arquiler.id_emp)
        result_query = result_query.filter( Habitacion_estado.id == Habitacion.id_hab_est)
        
        if(filter_hab):
            result_query = result_query.filter(Habitacion.id == filter_hab)
        if(filter_piso):
            result_query = result_query.filter(Habitacion.piso == filter_piso)
        if(filter_hab_est):
            result_query = result_query.filter(Habitacion.id_hab_est == filter_hab_est)

        if(ascChecking): result_query = result_query.order_by(Arquiler.fechaHoraChecking.asc())
        else: result_query = result_query.order_by(Arquiler.fechaHoraChecking.desc())

        
        result_fetch = result_query.all()
        self.close_session()

        arq = Arquiler()
        hab = Habitacion()
        cli = Cliente()
        emp = Empleado()
        hab_est = Habitacion_estado()
        hab_reg = Habitaciones_registro()
        n=1

        for r in result_fetch:
            n=n+1

            arq = r[0]
            hab = r[1]
            cli = r[2]
            emp = r[3]
            hab_est = r[4]

    def find(arr , id):
        for x in arr:
            if x.id_hab == id:
                return x
    """

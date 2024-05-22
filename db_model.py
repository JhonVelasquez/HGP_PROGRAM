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

                   
table_hab_column_names = { 
    0 : "ID", 
    1 : "Piso", 
    2 : "Nombre", 
    3 : "Camas", 
    4 : "Descripcion", 
    5 : "Precio Base", 
    6 : "Caracteristicas", 
    7 : "Estado anterior", 
    8 : "Estado actual"
    }

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
                   
table_hab_reg_column_names = { 
    0 : "ID", 
    1 : "F/h Inicio", 
    2 : "F/h Fin", 
    3 : "Habitacion", 
    4 : "Estado", 
    5 : "Ultimo cambio"
    }

hab_reg_cmb_order_by_name = table_hab_reg_column_names

hab_reg_cmb_order_by_feature = { 
    0 : Habitaciones_registro.id, 
    1 : Habitaciones_registro.fechaHoraInicio, 
    2 : Habitaciones_registro.fechaHoraFin, 
    3 : Habitaciones_registro.id_hab, 
    4 : Habitaciones_registro.id_hab_est, 
    5 : Habitaciones_registro.lastUpdate
    }

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
                   
table_cli_column_names = { 
    0 : "ID", 
    1 : "nDocumento", 
    2 : "Nombre", 
    3 : "Apellido", 
    4 : "Datos adicionales", 
    5 : "Celular", 
    6 : "Ultimo cambio"
    }
cli_cmb_order_by_name = table_cli_column_names
cli_cmb_order_by_feature = { 
    0 : Cliente.id, 
    1 : Cliente.nDocumento, 
    2 : Cliente.nombre, 
    3 : Cliente.apellido, 
    4 : Cliente.datosAdicionales, 
    5 : Cliente.celular, 
    6 : Cliente.lastUpdate
    }

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
               if(self.hab_reg != None):
                return str(self.hab_reg.id)
               else:
                return "-"
           case 5:
               if(self.hab_reg != None and self.hab_reg.hab_estado != None ):
                return str(self.hab_reg.hab_estado.value)
               else:
                return "-"
           case 6:
                if(self.fechaHoraChecking != None):
                    return str(self.fechaHoraChecking.replace(microsecond=0))
                else:
                    return None
           case 7:
                if(self.fechaHoraCheckout != None):
                    return str(self.fechaHoraCheckout.replace(microsecond=0))
                else:
                    return None
           case 8:
               return (self.precioReal)
           case 9:
               return (self.deuda)
           case 10:
                if(self.lastUpdate != None):
                    return str(self.lastUpdate.replace(microsecond=0))
                else:
                    return None
           case _:
               return "--"
                   
table_arq_column_names = { 
    0 : "ID",
    1 : "Habitacion",
    2 : "Cliente",
    3 : "Empleado",
    4 : "Hab_reg",
    5 : "Estado",
    6 : "F/h checking",
    7 : "F/h checkout",
    8 : "Precio",
    9 : "Deuda",
    10 : "Ultimo cambio"
    }
arq_cmb_order_by_name = {
    0 : "Arquiler ID", 
    1 : "Habitacion ID", 
    2 : "Cli-ID", 
    3 : "Cli-nombre", 
    4 : "Cli-apellido", 
    5 : "Empleado", 
    6 : "Hab_reg", 
    7 : "Estado", 
    8 : "F/h checking",
    9 : "F/h checkout", 
    10 : "Precio", 
    11 : "Deuda", 
    12 : "Ultimo cambio"
    }
arq_cmb_order_by_feature = { 
    0 : Arquiler.id, 
    1 : Arquiler.id_hab, 
    2 : Cliente.nDocumento, 
    3 : Cliente.nombre, 
    4 : Cliente.apellido, 
    5 : Arquiler.id_emp, 
    6 : Habitaciones_registro.id, 
    7 : Habitacion_estado.value, 
    8 : Arquiler.fechaHoraChecking, 
    9 : Arquiler.fechaHoraCheckout, 
    10 : Arquiler.precioReal, 
    11 : Arquiler.deuda, 
    12 : Arquiler.lastUpdate
    }

from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from sqlalchemy import create_engine, select, Column, Integer, String, Date, ForeignKey, PrimaryKeyConstraint, Float, SmallInteger
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import func, extract
from sqlalchemy import or_, and_
from sqlalchemy import join

from db_model import *
from db import *
from migrate_db import *

from gui_hgp import *
from datetime import datetime
from theme_css import dark_theme
import webbrowser
#import qdarktheme

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import *
from db_model import *



class Controller():
    mainWindow = None
    dbWindow = None

    habWindow = None
    arqWindow = None
    cliWindow = None
    habRegWindow = None
    
    newCliWindow = None
    newArqWindow = None
    newHabRegWindow = None

    testWindow = None

    currentEmpleadoID = None
    db_hgp = None

    #Almost fixed
    d_Empleado = {}
    d_Hab_cam = {}
    d_Hab_car = {}
    d_Hab_est = {}

    #Related to tables and possibly changing constantly
    d_Habitaciones = {}
    d_Clientes = {}
    d_Arquileres = {}
    d_Hab_Reg = {}
    d_var={}

    failback_path = "sqlite:///"
    def __init__(self, failback_path):
        self.failback_path = failback_path

    def init_db(self):
        path = read_db_file()
        val, e_m = validate_ping_db(path)

        if(val == False):
            CustomDialog("Error","La conexión a la Base de Datos (DB): \""+str(path)+ "\" falló. "+ "Usando el de respaldo:\""+str(self.failback_path)+ "\". ").exec()
            path = self.failback_path

        self.db_hgp = DataBase(path)
        self.load_default_values()

    def setNewDB(self, path: str):
        self.db_hgp = DataBase(path)
        self.load_default_values()
        self.mainWindow.update_all_opened_windows()

    def load_default_values(self):
        self.d_Empleado=self.db_hgp.get_dic_table_from_class(Empleado).copy()
        self.d_Hab_cam=self.db_hgp.get_dic_table_from_class(Habitacion_cama).copy()
        self.d_Hab_car=self.db_hgp.get_dic_table_from_class(Habitacion_caracteristica).copy()
        self.d_Hab_est=self.db_hgp.get_dic_table_from_class(Habitacion_estado).copy()

    def get_values_hab(self):
        self.d_Habitaciones = {}
        self.d_Habitaciones = self. db_hgp.get_dic_table_habitacion(asc_piso=True, asc_id_hab=True, asc_precioReferencia=False)
        
    def get_values_arq(self,id_arq= None, id_hab= None, document= None, name= None, surname= None, id_hab_reg= None, id_hab_est= None, fecha_checking= None, order_by= None):
        new = self. db_hgp.get_dic_table_arquiler(id_arq= id_arq, id_hab= id_hab, document= document, name= name, surname= surname, id_hab_reg= id_hab_reg, id_hab_est= id_hab_est, fecha_checking= fecha_checking, order_by= order_by, n_last = None, page_size= self.arqWindow.getSizePage(), page_current= self.arqWindow.getCurrentPage())
        
        return new

    def get_values_client(self, id_cli= None, nDocumento = None, nombre = None, apellido = None, celular = None, order_by = None):
        new = self. db_hgp.get_dic_table_cliente(id_cli= id_cli, nDocumento = nDocumento, nombre = nombre, apellido = apellido, celular= celular, order_by= order_by,n_last = None, page_size= self.cliWindow.getSizePage(), page_current= self.cliWindow.getCurrentPage())
        return new

    def get_values_hab_reg(self, id_hab_reg = None, id_hab = None, id_hab_est = None, dateInicio= None, order_by=None):
        new = self. db_hgp.get_dic_table_registro(id_hab_reg= id_hab_reg, id_hab= id_hab, id_hab_est= id_hab_est, n_last= None, dateInicio= dateInicio, order_by=order_by, page_size= self.habRegWindow.getSizePage(), page_current= self.habRegWindow.getCurrentPage())
        return new
           
    def init_visual_main(self):
        app = QtWidgets.QApplication(sys.argv) 
        #app.setStyleSheet(dark_theme)       
        self.mainWindow = MainWindowMoid(self)
        self.dbWindow = DatabaseWindow()
        
        #qdarktheme.setup_theme()
        # Customize accent color.
        # qdarktheme.setup_theme(custom_colors={"primary": "#D0BCFF"})
        self.mainWindow.mdiAreaMain.cascadeSubWindows()
        #self.mainWindow.mdiAreaMain.tileSubWindows()

        self.currentEmpleadoID = 5

        self.init_db()
        self.dbW_init()   

        self.habW_init()   
        self.cliW_init()
        self.habRegW_init()
        self.newCliW_init()
        self.arqW_init()
        self.newArqW_init()
        self.newHabRegW_init()

        self.mainWindow.btnHab.clicked.connect(self.callback_mainW_openHabW)
        self.mainWindow.btnHabReg.clicked.connect(self.callback_habW_openHabRegW)
        self.mainWindow.btnArq.clicked.connect(self.callback_mainW_openArqW)
        self.mainWindow.btnClient.clicked.connect(self.callback_mainW_openClientW)
        self.mainWindow.btnSunat.clicked.connect(self.callback_mainW_sunat)
        self.mainWindow.btnDB.clicked.connect(self.callback_mainW_db)

        self.mainWindow.btnAddArquiler.clicked.connect(self.callback_arqW_openNewArqW)
        self.mainWindow.btnAddClient.clicked.connect(self.callback_cliW_openNewCliW)
        self.mainWindow.btnAddRegistro.clicked.connect(self.callback_habRegW_openNewHabRegW)

        self.mainWindow.btnTest.clicked.connect(self.callback_test)
        self.mainWindow.btnTest.setVisible(False)

        self.mainWindow.show_visual()
        self.mainWindow.showMaximized()
        self.mainWindow.addAction("Cerrar todo", self.call_close_all_sub_windows)
        

        sys.exit(app.exec())

    def dbW_init(self):
        self.dbWindow = DatabaseWindow()
        self.dbWindow.btnPingDB.clicked.connect(self.callback_dbW_ping)
        self.dbWindow.btnSavePath.clicked.connect(self.callback_dbW_save)
        self.dbWindow.btnLoadPath.clicked.connect(self.callback_dbW_load)
        self.dbWindow.btnMigrate.clicked.connect(self.callback_dbW_migrate)

    def habW_init(self):
        self.habWindow = HabWindow(table_column_names= table_hab_column_names)
        self.habWindow.btnUpdate.clicked.connect(self.callback_habW_update)
        self.habWindow.addAction("Actualizar", self.callback_habW_update)
        self.habWindow.addAction("Cerrar todo", self.call_close_all_sub_windows)

    def arqW_init(self, data_front = None, data_back = None):
        self.arqWindow = ArqWindow(data_front= data_front, data_back= data_back, d_Hab_est= self.d_Hab_est, table_column_names= table_arq_column_names, cmb_order_by_name= arq_cmb_order_by_name)
        self.arqWindow.btnUpdate.clicked.connect(self.callback_arqW_update)
        self.arqWindow.btnNewEdit.clicked.connect(self.callback_arqW_openNewArqW)

        self.arqWindow.btnPrev.clicked.connect(self.callback_arqW_prev)
        self.arqWindow.btnNext.clicked.connect(self.callback_arqW_next)

        self.arqWindow.addAction("Actualizar", self.callback_arqW_update)
        self.arqWindow.addAction("Cerrar todo", self.call_close_all_sub_windows)

        self.arqWindow.btnUpdateTimeChecking.clicked.connect(self.callback_habRegW_update_time_checking)     
        self.arqWindow.btnClearTimeChecking.clicked.connect(self.callback_habRegW_clear_time_checking)

    def cliW_init(self, data_front = None, data_back = None):
        self.cliWindow = ClientWindow(data_front= data_front, data_back= data_back, table_column_names= table_cli_column_names, cmb_order_by_name= cli_cmb_order_by_name)
        self.cliWindow.btnUpdate.clicked.connect(self.callback_cliW_update)
        self.cliWindow.btnNewEdit.clicked.connect(self.callback_cliW_openNewCliW)

        self.cliWindow.btnPrev.clicked.connect(self.callback_cliW_prev)
        self.cliWindow.btnNext.clicked.connect(self.callback_cliW_next)
        self.cliWindow.addAction("Actualizar", self.callback_cliW_update)
        self.cliWindow.addAction("Cerrar todo", self.call_close_all_sub_windows)

    def habRegW_init(self, data_front = None, data_back = None):
        self.habRegWindow = HabRegWindow(data_front= data_front, data_back= data_back, d_Hab_est= self.d_Hab_est, table_column_names= table_hab_reg_column_names, cmb_order_by_name= hab_reg_cmb_order_by_name)
        self.habRegWindow.btnUpdate.clicked.connect(self.callback_habRegW_update)        
        self.habRegWindow.btnNewEdit.clicked.connect(self.callback_habRegW_openNewHabRegW)

        self.habRegWindow.btnPrev.clicked.connect(self.callback_habRegW_prev)
        self.habRegWindow.btnNext.clicked.connect(self.callback_habRegW_next)

        self.habRegWindow.btnUpdateTimeStart.clicked.connect(self.callback_habRegW_update_time_start)     
        self.habRegWindow.btnClearTimeStart.clicked.connect(self.callback_habRegW_clear_time_start)
        self.habRegWindow.addAction("Actualizar", self.callback_habRegW_update)
        self.habRegWindow.addAction("Cerrar todo", self.call_close_all_sub_windows)

    def newCliW_init(self):
        self.newCliWindow = NewClientWindow()
        self.newCliWindow.btnSearchClient.clicked.connect(self.callback_newCliW_search)
        self.newCliWindow.btnUpdateClient.clicked.connect(self.callback_newCliW_update)
        self.newCliWindow.btnCreateClient.clicked.connect(self.callback_newCliW_create)
        self.newCliWindow.btnDeleteClient.clicked.connect(self.callback_newCliW_delete)
        self.newCliWindow.btnCancelClient.clicked.connect(self.callback_newCliW_cancel)
        self.newCliWindow.addAction("Cerrar todo", self.call_close_all_sub_windows)

    def newArqW_init(self):
        self.newArqWindow = NewArqWindow(d_Hab_est=self.d_Hab_est)
        self.newArqWindow.btnSearchClient.clicked.connect(self.callback_newArqW_cli_search)
        self.newArqWindow.btnUpdateClient.clicked.connect(self.callback_newArqW_cli_update)
        self.newArqWindow.btnCreateClient.clicked.connect(self.callback_newArqW_cli_create)

        self.newArqWindow.btnSearchHab.clicked.connect(self.callback_newArqW_hab_search)
        
        self.newArqWindow.btnSearchArq.clicked.connect(self.callback_newArqW_arq_search)
        self.newArqWindow.btnUpdateArq.clicked.connect(self.callback_newArqW_arq_update)
        self.newArqWindow.btnPrepareCreateArq.clicked.connect(self.callback_newArqW_arq_create_prepare)
        self.newArqWindow.btnPrepareCreateArq.setVisible(False)
        self.newArqWindow.btnCreateArq.clicked.connect(self.callback_newArqW_arq_create)
        self.newArqWindow.btnCancelArq.clicked.connect(self.callback_newArqW_arq_cancel)
        self.newArqWindow.btnDeleteArq.clicked.connect(self.callback_newArqW_arq_delete)

        self.newArqWindow.btnUpdateTimeChecking.clicked.connect(self.callback_newArqW_update_time_checking)
        self.newArqWindow.btnUpdateTimeCheckout.clicked.connect(self.callback_newArqW_update_time_checkout)
        self.newArqWindow.btnClearTimeChecking.clicked.connect(self.callback_newArqW_clear_time_checking)
        self.newArqWindow.btnClearTimeCheckout.clicked.connect(self.callback_newArqW_clear_time_checkout)
        self.newArqWindow.addAction("Cerrar todo", self.call_close_all_sub_windows)

    def newHabRegW_init(self):
        self.newHabRegWindow = NewHabRegWindow(self.d_Hab_est)

        self.newHabRegWindow.btnSearchHab.clicked.connect(self.callback_newHabRegW_hab_search)
        
        self.newHabRegWindow.btnSearchHabReg.clicked.connect(self.callback_newHabRegW_search)
        self.newHabRegWindow.btnUpdateHabReg.clicked.connect(self.callback_newHabRegW_update)
        self.newHabRegWindow.btnCreateHabReg.clicked.connect(self.callback_newHabRegW_create)
        self.newHabRegWindow.btnCancelHabReg.clicked.connect(self.callback_newHabRegW_cancel)
        self.newHabRegWindow.btnDeleteHabReg.clicked.connect(self.callback_newHabRegW_delete)

        self.newHabRegWindow.btnUpdateTimeHabRegStart.clicked.connect(self.callback_newHabRegW_update_time_start)
        self.newHabRegWindow.btnUpdateTimeHabRegEnd.clicked.connect(self.callback_newHabRegW_update_time_end)
        self.newHabRegWindow.btnClearTimeHabRegStart.clicked.connect(self.callback_newHabRegW_clear_time_start)
        self.newHabRegWindow.btnClearTimeHabRegEnd.clicked.connect(self.callback_newHabRegW_clear_time_end)
        self.newHabRegWindow.addAction("Cerrar todo", self.call_close_all_sub_windows)

    #CALLBACKS - MAIN WINDOW 

    def call_close_all_sub_windows(self):
        self.mainWindow.mdiAreaMain.closeAllSubWindows()

    def callback_mainW_openHabW(self):
        self.habW_show_update(foc= True)
    
    def callback_mainW_openArqW(self):
        self.arqW_show_update(foc= True)
    
    def callback_mainW_openClientW(self):
        self.cliW_show_update(foc= True, reset_back= True)

    def callback_mainW_sunat(self):
        webbrowser.open('https://e-menu.sunat.gob.pe/cl-ti-itmenu/MenuInternet.htm?pestana=*&agrupacion=*')
    
    def callback_mainW_db(self):
        self.dbWindow.show_visual()

    #CALLBACKS - DATABASE WINDOW
    
    def load_path_from_file():
        path = read_db_file()
        val, e_m, type_db = validate_db_url(path)

    def callback_dbW_load(self): 
        path = read_db_file()
        val, e_m, type_db = validate_db_url(path)
        self.dbWindow.setInf(e_m)

        if(val == True):
            self.dbWindow.setPath(path)
        else:
            self.dbWindow.addToInf("Wrong path")
            self.dbWindow.addToInf(path)
            default = self.failback_path
            self.dbWindow.setPath(default)
            #write_db_file(default)

    def callback_dbW_migrate(self):
        source = self.dbWindow.getPathSource()
        destination = self.dbWindow.getPathDestination()
        mssg_f, mssg_t = migrar_db(source, destination)
        self.dbWindow.addToInf(mssg_f)
        self.dbWindow.addToInf(mssg_t)
        
    def callback_dbW_ping(self):
        
        """         
        path = self.dbWindow.getPathInUse()
        val, e_m = verify_path_existance(path)
        self.dbWindow.setInf(str(datetime.now()) + ": "  + e_m)
        val, e_m = validate_db_url(path)
        i = self.dbWindow.getInf()
        self.dbWindow.setInf(i+"\n"+ str(datetime.now()) + ": "  +  e_m) 
        """

        path = self.dbWindow.getPathInUse()
        val, e_m = validate_ping_db(path)
        self.dbWindow.setInf(e_m)

    def callback_dbW_save(self):
        path = self.dbWindow.getPathInUse()
        
        val, e_m = validate_ping_db(path)
        self.dbWindow.setInf(e_m)

        if(val == True):
            write_db_file(path)
            self.setNewDB(path)

    
    #CALLBACKS - HABITACION WINDOW
    def callback_habW_update(self):
        self.habW_show_update(foc = True)

    def callback_habW_openHabRegW(self):
        self.habRegW_show_update(foc= True, reset_back= True)
    
    #CALLBACKS - ARQUILER WINDOW
    def callback_arqW_update(self):
        self.arqWindow.pushFrontDataToBack()
        self.arqW_show_update(foc=True,set_page= 1)

    def callback_arqW_openNewArqW(self):
        self.newArqW_show_update(foc= True)
        if(self.arqWindow.isCreated == True):
            id_sel = self.arqWindow.get_arq_id_selected()
            if(id_sel != None): self.f_newArq_search_fill(id_arq= id_sel)

    def callback_arqW_prev(self):
        if(self.arqWindow.getCurrentPage() >= 2):
            self.arqWindow.prevPage()
            self.arqW_show_update(foc=False)
    
    def callback_arqW_next(self):
        if(self.d_Arquileres != None):
            if(len(self.d_Arquileres) != 0):
                self.arqWindow.nextPage()
                self.arqW_show_update(foc=False)
    
    def callback_habRegW_update_time_checking(self):
        self.arqWindow.set_time_checking_now()

    def callback_habRegW_clear_time_checking(self):
        self.arqWindow.clear_time_checking_now()

    #CALLBACKS - CLIENTE WINDOW
    def callback_cliW_update(self):
        self.cliWindow.pushFrontDataToBack()
        self.cliW_show_update(foc=True,set_page=1)

    def callback_cliW_openNewCliW(self):
        self.newCliW_show_update(foc= True)
        if(self.cliWindow.isCreated == True):
            id_sel = self.cliWindow.get_cli_id_selected()
            if(id_sel != None): self.f_client_fill_widget_by_id(id= id_sel, widg= self.newCliWindow)

    def callback_cliW_prev(self):
        if(self.cliWindow.getCurrentPage() >= 2):
            self.cliWindow.prevPage()
            self.cliW_show_update(foc=False)
    
    def callback_cliW_next(self):
        if(self.d_Clientes != None):
            if(len(self.d_Clientes) != 0):
                self.cliWindow.nextPage()
                self.cliW_show_update(foc=False)
    
    #CALLBACKS - HABITACION REGISTRO WINDOW
    def callback_habRegW_update(self):
        self.habRegWindow.pushFrontDataToBack()
        self.habRegW_show_update(foc=True, set_page= 1)

    def callback_habRegW_openNewHabRegW(self):
        self.newHabRegW_show_update(foc= True)
        if(self.habRegWindow.isCreated == True):
            id_sel = self.habRegWindow.get_hab_reg_id_selected()
            if(id_sel != None): self.f_newHabReg_search_fill(hab_reg_id= id_sel, window= None)

    def callback_habRegW_prev(self):
        if(self.habRegWindow.getCurrentPage() >= 2):
            self.habRegWindow.prevPage()
            self.habRegW_show_update(foc=False)
    
    def callback_habRegW_next(self):
        if(self.d_Hab_Reg != None):
            if(len(self.d_Hab_Reg) != 0):
                self.habRegWindow.nextPage()
                self.habRegW_show_update(foc=False)

    def callback_habRegW_update_time_start(self):
        self.habRegWindow.set_time_start_now()

    def callback_habRegW_clear_time_start(self):
        self.habRegWindow.clear_time_start_now()
    
    #CALLBACKS - NEW CLIENT WINDOW
    def callback_newCliW_search(self):
        self.f_client_search_from_widget(self.newCliWindow)

    def callback_newCliW_update(self):
        self.f_client_update_from_widget(self.newCliWindow, show_end_cliW= True)

    def callback_newCliW_create(self):
        self.f_client_create_from_widget(self.newCliWindow, show_end_cliW= True)

    def callback_newCliW_delete(self):
        self.f_client_delete_from_widget(self.newCliWindow, show_end_cliW= False)
 
    def callback_newCliW_cancel(self):
        self.newCliWindow.close()
        self.mainWindow.mdiAreaMain.removeSubWindow(self.newCliWindow.subWindowRef)
    
    #CALLBACKS - NEW ARQUILER WINDOW
    def callback_newArqW_cli_search(self):
        self.f_client_search_from_widget(self.newArqWindow)

    def callback_newArqW_cli_update(self):
        self.f_client_update_from_widget(self.newArqWindow, show_end_cliW= False)

    def callback_newArqW_cli_create(self):
        self.f_client_create_from_widget(self.newArqWindow, show_end_cliW= True)

    def callback_newArqW_hab_search(self):
        id_hab =  self.newArqWindow.getID_hab()
        self.newArqW_f_fill_hab_from_id(id_hab)

    def callback_newArqW_arq_search(self):
        arq_form, cli_doc = self.newArqWindow.getArqFromForm(self.d_Hab_est, self.currentEmpleadoID, "search")
        if(arq_form != None):
            id_arq_form = arq_form.id
            self.f_newArq_search_fill(id_arq_form)
        else:
            return 0

    def callback_newArqW_arq_update(self):
        show_end_habRegW = False
        show_end_arqW = True
        show_end_habW = True

        err = 0
        arq_form = None
        arq_form, cli_doc = self.newArqWindow.getArqFromForm(self.d_Hab_est, self.currentEmpleadoID, "update")
        if(arq_form != None):
            id_arq_form = arq_form.id
            
            #verifying Arquiler
            arq_db = self. db_hgp.get_arq_by_id(id_arq_form)
            if (arq_db!=None):
                try:
                    #verifying client doc and id
                    cl = self. db_hgp.get_client_by_doc(cli_doc)
                    if (cl!=None):           
                        arq_form.id_cli = cl.id
                        self.newArqWindow.setInf_cli("Valido")
                    else:
                        CustomDialog("Error","No hay cliente con documento " + cli_doc).exec()
                        self.newArqWindow.setInf_cli("B:Error")
                        err=err+1

                    #verifying habitacion id
                    hab = self. db_hgp.get_hab_from_id(arq_form.id_hab)
                    if (hab!=None):
                        self.newArqWindow.setInf_hab("Valido")
                    else:
                        CustomDialog("Error","No hay habitacion con id " + arq_form.id_hab).exec()
                        self.newArqWindow.setInf_hab("B:Error")
                        err=err+1

                    #If there is not Hab_reg, then create one.
                    if(arq_db.id_hab_reg == None):
                        #create hab_reg
                        #update visual
                        new_hab_reg = None
                        new_hab_reg = self.f_habReg_create(hab_reg_form= arq_form.hab_reg, window= None, show_end_habRegW= show_end_habRegW, show_end_habW= False)
                        if(new_hab_reg!=None):
                            if(new_hab_reg.id!=None):
                                arq_form.id_hab_reg = new_hab_reg.id
                                self. db_hgp.update_hab_reg_Arquiler(arq_form)
                                self.newArqWindow.fillData_arq_habReg(new_hab_reg, d_Hab_est=self.d_Hab_est)
                    else:
                        self.f_habReg_update(hab_reg_form= arq_form.hab_reg, window= None, show_end_habRegW= show_end_habRegW, show_end_habW = False)

                    #If there is Hab_reg, then verify and update

                    if(err == 0):
                        arq_form.lastUpdate = datetime.now()
                        self. db_hgp.update_Arquiler(arq_form,arq_db)
                        self.f_newArq_search_fill(arq_form.id)
                        self.newArqWindow.setInf_arq("U:Listo")
                        if(show_end_arqW or (show_end_arqW == False and self.arqWindow.isCreated == True)): self.arqW_show_update(foc= False, id_select= arq_form.id)
                        if(show_end_habW or (show_end_habW == False and self.habWindow.isCreated == True)):self.habW_show_update(foc= False, id_select= arq_form.id_hab)

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newArqWindow.setInf_arq("N:Intente de nuevo")
            else:
                CustomDialog("Error","No hay arquiler con id " + str(id_arq_form)).exec()

    def callback_newArqW_arq_create_prepare(self):
        self.newArqWindow.prepare_create()

    def callback_newArqW_arq_create(self):
        show_end_habRegW = False
        show_end_arqW = False
        show_end_habW = True

        err = 0
        arq_form, cli_doc = self.newArqWindow.getArqFromForm(self.d_Hab_est, self.currentEmpleadoID, "create")
        if(arq_form != None):
            id_arq_form = arq_form.id
            
            if (id_arq_form==None):
                try:
                    #verifying client doc and id
                    cl = self. db_hgp.get_client_by_doc(cli_doc)
                    if (cl!=None):           
                        arq_form.id_cli = cl.id
                        self.newArqWindow.setInf_cli("Valido")
                    else:
                        CustomDialog("Error","No hay cliente con documento " + cli_doc).exec()
                        self.newArqWindow.setInf_cli("B:Error")
                        err=err+1

                    #verifying habitacion id
                    hab = self. db_hgp.get_hab_from_id(arq_form.id_hab)
                    if (hab!=None):
                        self.newArqWindow.setInf_hab("Valido")
                    else:
                        CustomDialog("Error","No hay habitacion con id " + arq_form.id_hab).exec()
                        self.newArqWindow.setInf_hab("B:Error")
                        err=err+1

                    if(err == 0):

                        new_hab_reg = None
                        arq_form.hab_reg.id = None
                        new_hab_reg = self.f_habReg_create(hab_reg_form= arq_form.hab_reg, window= None, show_end_habRegW= show_end_habRegW, show_end_habW= False)
                        if(new_hab_reg!=None):
                            if(new_hab_reg.id!=None):
                                arq_form.id_hab_reg = new_hab_reg.id
                                self.newArqWindow.fillData_arq_habReg(new_hab_reg, d_Hab_est=self.d_Hab_est)
                                
                        arq_form.lastUpdate = datetime.now()
                        created_arq = self. db_hgp.create_Arquiler(arq_form)
                        self.newArqWindow.lineEditArqID.setText(str(created_arq.id))
                        self.newArqW_f_fill_hab_from_id(arq_form.id_hab)
                        self.newArqWindow.setInf_arq("C:Listo")
                        if(show_end_arqW or (show_end_arqW == False and self.arqWindow.isCreated == True)): self.arqW_show_update(foc= False, id_select= created_arq.id)
                        if(show_end_habW or (show_end_habW == False and self.habWindow.isCreated == True)): self.habW_show_update(foc= False, id_select= created_arq.id_hab)

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se creó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newArqWindow.setInf_arq("N:Intente de nuevo")
            else:
                CustomDialog("Error","Ya hay arquiler con id " + str(id_arq_form)).exec()
        
    def callback_newArqW_arq_cancel(self):
        self.newArqWindow.close()
        self.mainWindow.mdiAreaMain.removeSubWindow(self.newArqWindow.subWindowRef)

    def callback_newArqW_arq_delete(self):
        show_end_habRegW = False
        show_end_arqW = False
        show_end_habW = True

        arq_form, cli_doc = self.newArqWindow.getArqFromForm(self.d_Hab_est, self.currentEmpleadoID, "delete")
        if(arq_form != None):
            id_arq_form = arq_form.id
            arq_db = self. db_hgp.get_arq_by_id(id_arq_form)
            if (arq_db!=None):
                try:
                        self. db_hgp.delete_Arquiler(arq_db)
                        self.newArqWindow.setInf_arq("C:Listo")
                        if(show_end_arqW or (show_end_arqW == False and self.arqWindow.isCreated == True)): self.arqW_show_update(foc= False)
                        if(arq_db.hab_reg != None and arq_db.hab_reg.id != None):
                            self. db_hgp.delete_Hab_Reg(arq_db.hab_reg)
                            self.newArqW_f_fill_hab_from_id(arq_form.id_hab)
                            self.callback_newArqW_arq_create_prepare()
                            if(show_end_habRegW or (show_end_habRegW == False and self.habRegWindow.isCreated == True)): self.habRegW_show_update(foc= False, reset_back=True)
                            if(show_end_habW or (show_end_habW == False and self.habWindow.isCreated == True)): self.habW_show_update(foc= False)

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se eliminó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newArqWindow.setInf_arq("N:Intente de nuevo")
            else:
                CustomDialog("Error","No hay arquiler con id " + str(id_arq_form)).exec()

    def callback_newArqW_update_time_checking(self):
        self.newArqWindow.set_time_checking_now()

    def callback_newArqW_update_time_checkout(self):
        self.newArqWindow.set_time_checkout_now()

    def callback_newArqW_clear_time_checking(self):
        self.newArqWindow.clear_time_checking_now()

    def callback_newArqW_clear_time_checkout(self):
        self.newArqWindow.clear_time_checkout_now()
    
    # <<CALLBACKS - NEW HABITACION REGISTRO WINDOW
    def callback_newHabRegW_hab_search(self):
        id_hab =  self.newHabRegWindow.getID_hab()
        self.newHabRegW_f_fill_hab_from_id(id_hab)
        
    def callback_newHabRegW_search(self):
        hab_reg_form = self.newHabRegWindow.getHabRegFromForm(self.d_Hab_est, "search")
        if(hab_reg_form != None):
            self.f_newHabReg_search_fill(hab_reg_id= hab_reg_form.id, window = self.newHabRegWindow)
        
    def callback_newHabRegW_update(self):
        hab_reg_form = self.newHabRegWindow.getHabRegFromForm(self.d_Hab_est, "update")
        self.f_habReg_update(hab_reg_form = hab_reg_form, window = self.newHabRegWindow, show_end_habRegW= True, show_end_habW= True)
        if(hab_reg_form != None):
            self.newHabRegW_f_fill_hab_from_id(hab_reg_form.id_hab)

    def callback_newHabRegW_create(self):
        hab_reg_form = self.newHabRegWindow.getHabRegFromForm(self.d_Hab_est, "create")
        self.f_habReg_create(hab_reg_form = hab_reg_form, window = self.newHabRegWindow, show_end_habRegW= True, show_end_habW= True)
        if(hab_reg_form != None):
            self.newHabRegW_f_fill_hab_from_id(hab_reg_form.id_hab)
        
    def callback_newHabRegW_cancel(self):
        self.newHabRegWindow.close()
        self.mainWindow.mdiAreaMain.removeSubWindow(self.newHabRegWindow.subWindowRef)

    def callback_newHabRegW_delete(self):
        show_end_habRegW = False
        show_end_habW = True

        hab_reg_form = self.newHabRegWindow.getHabRegFromForm(self.d_Hab_est, "delete")
        if(hab_reg_form != None):
            id_hab_reg_form = hab_reg_form.id
            #verifying reg
            hab_reg_db = self. db_hgp.get_hab_reg_from_id(id_hab_reg_form)
            if (hab_reg_db!=None):
                try:
                    self. db_hgp.delete_Hab_Reg(hab_reg_form)
                    self.newHabRegWindow.setInf_hab_reg("C:Listo")
                    self.newHabRegW_f_fill_hab_from_id(hab_reg_form.id_hab)
                    if(show_end_habRegW or (show_end_habRegW == False and self.habRegWindow.isCreated == True)): self.habRegW_show_update(foc= False, reset_back=True)
                    if(show_end_habW or (show_end_habW == False and self.habWindow.isCreated == True)): self.habW_show_update(foc= False)
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se eliminó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newHabRegWindow.setInf_hab_reg("N:Intente de nuevo")
            else:
                CustomDialog("Error","No hay registro con id " + str(id_hab_reg_form)).exec()

    def callback_newHabRegW_update_time_start(self):
        self.newHabRegWindow.set_time_start_now()

    def callback_newHabRegW_update_time_end(self):
        self.newHabRegWindow.set_time_end_now()

    def callback_newHabRegW_clear_time_start(self):
        self.newHabRegWindow.clear_time_start_now()

    def callback_newHabRegW_clear_time_end(self):
        self.newHabRegWindow.clear_time_end_now()

    ###################
    ### FUNCTIONS - GENERAL
    
    def create_visual_sub_window(self, wid, pos_x = None, pos_y = None):
        wid.subWindowRef = self.mainWindow.mdiAreaMain.addSubWindow(wid)
        if((pos_x != None) and (pos_y != None)): wid.subWindowRef.move(pos_x, pos_y)
        wid.isCreated = True
        wid.show_visual(False)
   
    ### FUNCTIONS - MAIN WINDOW
    
    
    
    ### FUNCTIONS - HABITACION WINDOW

    def habW_setup(self, pos_x = None, pos_y= None, data_back= None, data_front= None):
        self.habW_init()
        self.habW_update_values_table()
        self.create_visual_sub_window(self.habWindow,pos_x, pos_y)

    def habW_show_update(self, foc, id_select = None):

        curr_act=None
        if((foc == False)):
            curr_act = self.mainWindow.mdiAreaMain.activeSubWindow()

        if(self.habWindow.isCreated == False):
            self.habW_setup()
        else:
            pos_x = self.habWindow.subWindowRef.pos().x()
            pos_y = self.habWindow.subWindowRef.pos().y()
            data_front = self.habWindow.getWindowDataFront()
            data_back = self.habWindow.getWindowDataBack()

            self.mainWindow.mdiAreaMain.removeSubWindow(self.habWindow.subWindowRef)
            self.habW_setup(pos_x = pos_x, pos_y = pos_y, data_front = data_front, data_back = data_back)

        if(foc == True):
            self.habWindow.subWindowRef.setFocus()
        elif((curr_act != None)):
            self.mainWindow.mdiAreaMain.setActiveSubWindow(curr_act)

        if(id_select != None): self.habWindow.select_row_by_id(id_select)
    
    def habW_update_values_table(self):
        self.get_values_hab()
        self.habWindow.updateTableView(self.d_Habitaciones, self.d_Hab_est, self.d_Hab_cam, self.d_Hab_car)

    ### FUNCTIONS - ARQUILER WINDOW

    def arqW_setup(self, pos_x = None, pos_y= None, data_back= None, data_front= None):
        self.arqW_init(data_front=data_front, data_back=data_back)
        self.arqW_update_values_table()
        self.create_visual_sub_window(self.arqWindow,pos_x, pos_y)

    def arqW_show_update(self, foc, set_page = None, reset_back = None, id_select = None):
        curr_act=None
        if((foc == False)):
            curr_act = self.mainWindow.mdiAreaMain.activeSubWindow()
    
        if(self.arqWindow.isCreated == False):
            self.arqW_setup()
        else:
            pos_x = self.arqWindow.subWindowRef.pos().x()
            pos_y = self.arqWindow.subWindowRef.pos().y()
            data_front = self.arqWindow.getWindowDataFront()
            data_back = self.arqWindow.getWindowDataBack()
            if(set_page != None): data_back.set_pageCurrent(page=1)
            if(reset_back == True): data_back.reset()

            self.mainWindow.mdiAreaMain.removeSubWindow(self.arqWindow.subWindowRef)
            self.arqW_setup(pos_x = pos_x, pos_y = pos_y, data_front = data_front, data_back = data_back)

        if(foc == True):
            self.arqWindow.subWindowRef.setFocus()
        elif((curr_act != None)):
            self.mainWindow.mdiAreaMain.setActiveSubWindow(curr_act)

        if(id_select != None): self.arqWindow.select_row_by_id(id_select)

    def arqW_update_values_table(self):
        wd = self.arqWindow.getWindowDataBack()
        
        id_arq = None
        id_hab = None
        document = None
        name = None
        surname = None
        id_hab_reg = None
        id_hab_est = None
        fecha_checking = None
        order_by = None

        if(wd.id_arq != None and wd.id_arq.isnumeric()): id_arq = int(wd.id_arq)
        if(wd.id_hab != None): id_hab = wd.id_hab  
        if(wd.document != None): document = wd.document  
        if(wd.name != None): name = wd.name  
        if(wd.surname != None): surname = wd.surname  
        if(wd.id_hab_reg != None and wd.id_hab_reg.isnumeric()): id_hab_reg = int(wd.id_hab_reg)
        if(wd.id_hab_est != None and wd.id_hab_est.isnumeric()): id_hab_est = int(wd.id_hab_est)
        
        if(wd.hab_est != None): 
            hab_est_value = wd.hab_est
            for k in self.d_Hab_est.keys():
                if(self.d_Hab_est[k].value == hab_est_value):
                    id_hab_est = self.d_Hab_est[k].id
        
        if(wd.fecha_checking != None): fecha_checking = wd.fecha_checking.toPyDateTime()
        if(wd.order_type != None and wd.order_feature != None):
            order_feature = wd.order_feature
            order_type = wd.order_type
            order_by = None
            var = None
            for k in arq_cmb_order_by_name.keys():
                if(arq_cmb_order_by_name[k] == order_feature):
                    var = arq_cmb_order_by_feature[k]
                    if(order_type == "asce"):
                        order_by = var.asc()
                    elif(order_type == "desc" ):
                        order_by = var.desc()   

        new = self.get_values_arq(id_arq= id_arq, id_hab= id_hab, document= document, name= name, surname= surname, id_hab_reg= id_hab_reg, id_hab_est= id_hab_est, fecha_checking= fecha_checking, order_by= order_by)
        if(len(new) == 0 and self.arqWindow.getCurrentPage() > 1):
            self.arqWindow.prevPage()
            self.d_Arquileres = self.get_values_arq(id_arq= id_arq, id_hab= id_hab, document= document, name= name, surname= surname, id_hab_reg= id_hab_reg, id_hab_est= id_hab_est, fecha_checking= fecha_checking, order_by= order_by)
        else:
            self.d_Arquileres = new

        self.arqWindow.updateTableView(self.d_Arquileres, self.d_Empleado)
    
    ### FUNCTIONS - CLIENT WINDOW

    def cliW_setup(self, pos_x  = None, pos_y = None, data_back = None, data_front = None):
        self.cliW_init(data_front=data_front, data_back=data_back)
        self.cliW_update_values_table()
        self.create_visual_sub_window(self.cliWindow,pos_x, pos_y)

    def cliW_show_update(self, foc, set_page = None, reset_back = None, id_select = None):
        
        curr_act=None
        if((foc == False)):
            curr_act = self.mainWindow.mdiAreaMain.activeSubWindow()

        if(self.cliWindow.isCreated == False):
            self.cliW_setup()
        else:
            pos_x = self.cliWindow.subWindowRef.pos().x()
            pos_y = self.cliWindow.subWindowRef.pos().y()
            data_front = self.cliWindow.getWindowDataFront()
            data_back = self.cliWindow.getWindowDataBack()
            if(set_page != None): data_back.set_pageCurrent(page=1)
            if(reset_back == True): data_back.reset()

            self.mainWindow.mdiAreaMain.removeSubWindow(self.cliWindow.subWindowRef)
            self.cliW_setup(pos_x = pos_x, pos_y = pos_y, data_front = data_front, data_back = data_back)

        if(foc == True):
            self.cliWindow.subWindowRef.setFocus()
        elif((curr_act != None)):
            self.mainWindow.mdiAreaMain.setActiveSubWindow(curr_act)

        if(id_select != None): self.cliWindow.select_row_by_id(id_select)

    def cliW_update_values_table(self):
        wd = self.cliWindow.getWindowDataBack()

        id_cli = None
        nDocumento = None
        nombre = None
        apellido = None
        celular = None
        order_by = None

        if(wd.id_cli != None and wd.id_cli.isnumeric()): id_cli = int(wd.id_cli)
        if(wd.document != None): nDocumento = wd.document
        if(wd.name != None): nombre = wd.name
        if(wd.surname != None): apellido = wd.surname     
        if(wd.cellphone != None): celular = wd.cellphone  
        if(wd.order_type != None and wd.order_feature != None):
            order_feature = wd.order_feature
            order_type = wd.order_type
            order_by = None
            var = None
            for k in cli_cmb_order_by_name.keys():
                if(cli_cmb_order_by_name[k] == order_feature):
                    var = cli_cmb_order_by_feature[k]
                    if(order_type == "asce"):
                        order_by = var.asc()
                    elif(order_type == "desc" ):
                        order_by = var.desc()    

        new = self.get_values_client( id_cli= id_cli, nDocumento = nDocumento, nombre = nombre, apellido = apellido, celular= celular, order_by= order_by)
        if(len(new) == 0 and self.cliWindow.getCurrentPage() > 1):
            self.cliWindow.prevPage()
            self.d_Clientes =  self.get_values_client( id_cli= id_cli, nDocumento = nDocumento, nombre = nombre, apellido = apellido, celular= celular, order_by= order_by)
        else:
            self.d_Clientes = new

        self.cliWindow.updateTableView(self.d_Clientes)


    # General - client
    def f_client_create_from_widget(self, widg, show_end_cliW= True):
        client =  widg.getClientFromForm_cli()
        if (client != None):
            cl_db = self. db_hgp.get_client_by_doc(client.nDocumento)
            if(cl_db == None):
                try:
                    client.lastUpdate = datetime.now()
                    created_cli = self. db_hgp.create_Client(client)
                    widg.setInf_cli("N:Listo")
                    if(show_end_cliW or (show_end_cliW == False and self.cliWindow.isCreated == True)): self.cliW_show_update(foc= False, reset_back= True, id_select= created_cli.id)
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se creó o intente de nuevo.\n\n"+str(err)).exec()
                    widg.setInf_cli("N:Intente de nuevo")
            else:
                CustomDialog("Error","El cliente con documento " + str(client.nDocumento) +" ya existe.\n\n").exec()
                widg.setInf_cli("N:Intente de nuevo")

    def f_client_delete_from_widget(self, widg, show_end_cliW= False):
        client =  widg.getClientFromForm_cli()
        if (client != None):
            cl_db = self. db_hgp.get_client_by_doc(client.nDocumento)
            if(cl_db == None):
                CustomDialog("Error","El cliente con documento " + str(client.nDocumento) +" no existe.\n\n").exec()
                widg.setInf_cli("N:Intente de nuevo")
            else:
                try:
                    self. db_hgp.delete_Client(cl_db)
                    widg.setInf_cli("N:Eliminado")
                    if(show_end_cliW or (show_end_cliW == False and self.cliWindow.isCreated == True)): self.cliW_show_update(foc= False, reset_back= True)
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    widg.setInf_cli("N:Intente de nuevo")

    def f_client_update_from_widget(self, widg, show_end_cliW= False):
        client =  widg.getClientFromForm_cli()
        if (client != None):
            cl_db = self. db_hgp.get_client_by_doc(client.nDocumento)
            if(cl_db == None):
                CustomDialog("Error","El cliente con documento " + str(client.nDocumento) +" no existe.\n\n").exec()
                widg.setInf_cli("N:Intente de nuevo")
            else:
                try:
                    client.lastUpdate = datetime.now()
                    self. db_hgp.update_Client(client,cl_db)
                    widg.setInf_cli("N:Listo")
                    if(show_end_cliW or (show_end_cliW == False and self.cliWindow.isCreated == True)): self.cliW_show_update(foc= False, reset_back= True, id_select= cl_db.id)
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    widg.setInf_cli("N:Intente de nuevo")

    def f_client_fill_widget_by_doc(self, widg, doc):
        if(doc != None):
            cl = self. db_hgp.get_client_by_doc(doc)
            if (cl!=None):
                widg.fillData_cli(cl)
                widg.setInf_cli("B:Listo")
            else:
                CustomDialog("Error","No hay cliente con documento " + doc).exec()
                #widg.clearLineData_cli()
                widg.setInf_cli("B:Error")
        else:
            CustomDialog("Error","No hay cliente registrado" + doc).exec()
            widg.setInf_cli("B:Error")
            #widg.clearLineData_cli()

    def f_client_fill_widget_by_id(self, widg, id):
        if(id != None):
            cl = self. db_hgp.get_client_by_id(id)
            if (cl!=None):
                widg.fillData_cli(cl)
                widg.setInf_cli("B:Listo")
            else:
                CustomDialog("Error","No hay cliente con id " + id).exec()
                #widg.clearLineData_cli()
                widg.setInf_cli("B:Error")
        else:
            CustomDialog("Error","No hay cliente registrado con id " + id).exec()
            widg.setInf_cli("B:Error")
            #widg.clearLineData_cli()
    
    def f_client_search_from_widget(self, widg):
        doc =  widg.getDocumentFromForm_cli()
        self.f_client_fill_widget_by_doc(widg, doc)

    # General Arquiler
    def f_newArq_search_fill(self, id_arq ):
        arq_db = self. db_hgp.get_arq_by_id(id_arq)
        if (arq_db!=None):
            self.newArqWindow.fillData_arq(arq_db)

            self.newArqW_f_fill_hab_from_id(arq_db.id_hab)

            doc = None
            cli = self. db_hgp.get_client_by_id(arq_db.id_cli)
            if (cli == None): doc = None
            else: doc = cli.nDocumento
            self.f_client_fill_widget_by_doc(self.newArqWindow, doc)
        else:
            CustomDialog("Error","No hay arquiler con id " + str(id_arq)).exec()

    ### FUNCTIONS - HABITACION REGISTRO WINDOW
    def habRegW_setup(self, pos_x  = None, pos_y = None, data_front = None, data_back = None):
        self.habRegW_init(data_front=data_front, data_back=data_back)
        self.habRegW_update_values_table()
        self.create_visual_sub_window(self.habRegWindow,pos_x, pos_y)
    
    def habRegW_show_update(self, foc, set_page = None, reset_back = None, id_select = None):
        
        curr_act=None
        if((foc == False)):
            curr_act = self.mainWindow.mdiAreaMain.activeSubWindow()
        
        if(self.habRegWindow.isCreated == False):
            self.habRegW_setup()
        else:
            pos_x = self.habRegWindow.subWindowRef.pos().x()
            pos_y = self.habRegWindow.subWindowRef.pos().y()
            data_front = self.habRegWindow.getWindowDataFront()
            data_back = self.habRegWindow.getWindowDataBack()
            if(set_page != None): data_back.set_pageCurrent(page=set_page)
            if(reset_back == True): data_back.reset()

            self.mainWindow.mdiAreaMain.removeSubWindow(self.habRegWindow.subWindowRef)
            self.habRegW_setup(pos_x = pos_x, pos_y = pos_y, data_front = data_front, data_back = data_back)

        if(foc == True):
            self.habRegWindow.subWindowRef.setFocus()
        elif((curr_act != None)):
            self.mainWindow.mdiAreaMain.setActiveSubWindow(curr_act)

        if(id_select != None): self.habRegWindow.select_row_by_id(id_select)

    def habRegW_update_values_table(self):
        wd = self.habRegWindow.getWindowDataBack()

        id_hab_reg = None
        fecha_inicio = None
        id_hab = None
        id_hab_est = None
        order_by = None

        if(wd.id_hab_reg != None and wd.id_hab_reg.isnumeric()): id_hab_reg = int(wd.id_hab_reg)

        if(wd.fecha_inicio != None): fecha_inicio = wd.fecha_inicio.toPyDateTime()

        if(wd.id_hab != None): id_hab = wd.id_hab

        if(wd.hab_est != None): 
            hab_est_value = wd.hab_est
            for k in self.d_Hab_est.keys():
                if(self.d_Hab_est[k].value == hab_est_value):
                    id_hab_est = self.d_Hab_est[k].id

        if(wd.order_type != None and wd.order_feature != None):
            order_feature = wd.order_feature
            order_type = wd.order_type
            order_by = None
            var = None
            for k in hab_reg_cmb_order_by_name.keys():
                if(hab_reg_cmb_order_by_name[k] == order_feature):
                    var = hab_reg_cmb_order_by_feature[k]
                    if(order_type == "asce"):
                        order_by = var.asc()
                    elif(order_type == "desc" ):
                        order_by = var.desc()

        new = self.get_values_hab_reg(id_hab_reg= id_hab_reg, dateInicio = fecha_inicio, id_hab= id_hab, id_hab_est = id_hab_est, order_by= order_by)

        if(len(new) == 0 and self.habRegWindow.getCurrentPage() > 1):
            self.habRegWindow.prevPage()
            self.d_Hab_Reg = self.get_values_hab_reg(id_hab_reg= id_hab_reg, dateInicio = fecha_inicio, id_hab= id_hab, id_hab_est = id_hab_est, order_by= order_by)
        else:
            self.d_Hab_Reg = new

        self.habRegWindow.updateTableView(self.d_Hab_Reg, self.d_Hab_est)

    
    ### FUNCTIONS - NEW CLIENT WINDOW

    def newCliW_show_update(self, foc):
        
        if(self.newCliWindow.isCreated == False):
            self.newCliW_init()
            self.create_visual_sub_window(self.newCliWindow)
        else:
            if(foc == True):
                self.newCliWindow.subWindowRef.setFocus()  

    ### FUNCTIONS - NEW ARQUILER WINDOW

    def newArqW_show_update(self, foc):
        
        if(self.newArqWindow.isCreated == False):
            self.newArqW_init()
            self.create_visual_sub_window(self.newArqWindow)
        else:
            if(foc == True):
                self.newArqWindow.subWindowRef.setFocus()
    
    def newArqW_f_fill_hab_from_id(self, id_hab):
        if(id_hab != None):
            hab = self. db_hgp.get_hab_from_id(id_hab)
            if (hab!=None):
                self.newArqWindow.fillData_hab(hab, self.d_Hab_cam, self.d_Hab_est)
                self.newArqWindow.setInf_hab("Valido")
            else:
                CustomDialog("Error","No hay habitacion con id " + id_hab).exec()
                self.newArqWindow.setInf_hab("Error")
        else:
            return 0
    
    ### FUNCTIONS - NEW HABITACION REGISTRO WINDOW

    def newHabRegW_show_update(self, foc):
        
        if(self.newHabRegWindow.isCreated == False):
            self.newHabRegW_init()
            self.create_visual_sub_window(self.newHabRegWindow)
        else:
            if(foc == True):
                self.newHabRegWindow.subWindowRef.setFocus()

    def newHabRegW_f_fill_hab_from_id(self, id_hab):
        if(id_hab != None):
            hab = self. db_hgp.get_hab_from_id(id_hab)
            if (hab!=None):
                self.newHabRegWindow.fillData_hab(hab, self.d_Hab_est)
                self.newHabRegWindow.setInf_hab("Valido")
            else:
                CustomDialog("Error","No hay habitacion con id " + id_hab).exec()
                self.newHabRegWindow.setInf_hab("Error")
        else:
            return 0  

    # General - habitacion registro

    def f_newHabReg_search_fill(self, hab_reg_id, window):  
            id_hab_reg_form = hab_reg_id
            hab_reg_db = self. db_hgp.get_hab_reg_from_id(id_hab_reg_form)
            if (hab_reg_db!=None):
                self.newHabRegWindow.fillData_hab_reg(hab_reg_db, self.d_Hab_est)
                self.newHabRegW_f_fill_hab_from_id(hab_reg_db.id_hab)
            else:
                CustomDialog("Error","No hay registro con id " + str(id_hab_reg_form)).exec()
                if(window != None): window.setInf_hab_reg("N:Intente de nuevo")

    def f_habReg_update(self, hab_reg_form, window, show_end_habRegW= True, show_end_habW = True):
        err = 0
        if(hab_reg_form != None):
            id_hab_reg_form = hab_reg_form.id
            
            #verifying reg
            hab_reg_db = self. db_hgp.get_hab_reg_from_id(id_hab_reg_form)
            if (hab_reg_db!=None):
                try:
                    #verifying habitacion id
                    hab = self. db_hgp.get_hab_from_id(hab_reg_form.id_hab)
                    if (hab!=None):
                        if(window != None): window.setInf_hab("Valido")
                    else:
                        CustomDialog("Error","No hay habitacion con id " + hab_reg_form.id_hab).exec()
                        if(window != None): window.setInf_hab("B:Error")
                        err=err+1

                    if(err == 0):
                        hab_reg_form.lastUpdate = datetime.now()
                        self. db_hgp.update_Hab_Reg(hab_reg_form,hab_reg_db)
                        if(window != None): window.setInf_hab_reg("U:Listo")
                        if(show_end_habRegW or (show_end_habRegW == False and self.habRegWindow.isCreated == True)): self.habRegW_show_update(foc= False, reset_back=True, id_select= hab_reg_form.id)
                        if(show_end_habW or (show_end_habW == False and self.habWindow.isCreated == True)): self.habW_show_update(foc= False, id_select= hab_reg_form.id_hab)

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    if(window != None): window.setInf_hab_reg("N:Intente de nuevo")
            else:
                CustomDialog("Error","No hay arquiler con id " + str(id_hab_reg_form)).exec()

    def f_habReg_create(self, hab_reg_form, window, show_end_habRegW = True, show_end_habW = True):
        err = 0
        new_hab_reg = None
        if(hab_reg_form != None):
            id_hab_reg_form = hab_reg_form.id
            
            if (id_hab_reg_form==None):
                try:
                    #verifying habitacion id
                    hab = self. db_hgp.get_hab_from_id(hab_reg_form.id_hab)
                    if (hab!=None):
                        if(window != None): window.setInf_hab("Valido")
                    else:
                        CustomDialog("Error","No hay habitacion con id " + hab_reg_form.id_hab).exec()
                        if(window != None): window.setInf_hab("B:Error")
                        err=err+1

                    if(err == 0):
                        hab_reg_form.lastUpdate = datetime.now()
                        new_hab_reg = self. db_hgp.create_Hab_Reg(hab_reg_form)
                        if(window != None): 
                            window.lineEditHabRegID.setText(str(new_hab_reg.id))
                            window.setInf_hab_reg("C:Listo")
                            
                        if(show_end_habRegW or (show_end_habRegW == False and self.habRegWindow.isCreated == True)): self.habRegW_show_update(foc= False, reset_back=True, id_select= new_hab_reg.id)
                        if(show_end_habW or (show_end_habW == False and self.habWindow.isCreated == True)): self.habW_show_update(foc= False, id_select= new_hab_reg.id_hab)

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se creó o intente de nuevo.\n\n"+str(err)).exec()
                    if(window != None): window.setInf_hab_reg("N:Intente de nuevo")
            else:
                CustomDialog("Error","Ya hay registro con id " + str(id_hab_reg_form)).exec()
        return new_hab_reg
    

    def test_db_dunctions(self):
        #d_var = self. db_hgp.get_dic_table_arquiler(id_hab="31", n_last=5, dateChecking=None)
        #d_var = self. db_hgp.get_dic_table_arquiler()
        #d_var = self. db_hgp.get_dic_table_registro(id_hab="B", n_last=5, dateChecking=None)
        #d_var = self. db_hgp.get_dic_table_registro(id_hab="31")
        #d_var = self. db_hgp.get_dic_table_cliente()
        #self. db_hgp.printList(d_var)
        #print(d_Habitaciones["B"])
        return 0
    
    def callback_test(self):
        new = self. db_hgp.get_test()






























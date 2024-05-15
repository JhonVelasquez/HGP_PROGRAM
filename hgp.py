from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from sqlalchemy import create_engine, select, Column, Integer, String, Date, ForeignKey, PrimaryKeyConstraint, Float, SmallInteger
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import func, extract
from sqlalchemy import or_, and_
from sqlalchemy import join

from db_func import *
from gui_hgp import *
from datetime import datetime
from theme_css import dark_theme
import webbrowser
#import qdarktheme

db_hgp = DataBase()
db_hgp.init_db()

class Controller():
    mainWindow = None

    habWindow = None
    arqWindow = None
    cliWindow = None
    habRegWindow = None
    
    newCliWindow = None
    newArqWindow = None
    newHabRegWindow = None

    testWindow = None

    currentEmpleadoID = None

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

    def load_default_values(self):
        self.d_Empleado=db_hgp.get_dic_table_from_class(Empleado).copy()
        self.d_Hab_cam=db_hgp.get_dic_table_from_class(Habitacion_cama).copy()
        self.d_Hab_car=db_hgp.get_dic_table_from_class(Habitacion_caracteristica).copy()
        self.d_Hab_est=db_hgp.get_dic_table_from_class(Habitacion_estado).copy()

    def get_values_hab(self):
        self.d_Habitaciones = {}
        self.d_Habitaciones = db_hgp.get_dic_table_habitacion(asc_piso=True, asc_id_hab=True, asc_precioReferencia=False)
        
    def get_values_arq(self):
        new = db_hgp.get_dic_table_arquiler(id_hab = None, n_last = None, dateChecking = None, page_size= self.arqWindow.getSizePage(), page_current= self.arqWindow.getCurrentPage())
        if(len(new) == 0 and self.arqWindow.getCurrentPage() > 1):
            self.arqWindow.prevPage()
        else:
            self.d_Arquileres = new

    def get_values_client(self):
        new = db_hgp.get_dic_table_cliente(id = None, nDocumento = None, nombre = None, apellido = None, n_last = None, page_size= self.cliWindow.getSizePage(), page_current= self.cliWindow.getCurrentPage())
        if(len(new) == 0 and self.cliWindow.getCurrentPage() > 1):
            self.cliWindow.prevPage()
        else:
            self.d_Clientes = new

    def get_values_hab_reg(self, id_hab_reg = None, id_hab = None, id_hab_est = None, n_last = None, dateInicio= None, order_by=None):
        new = db_hgp.get_dic_table_registro(id_hab_reg= id_hab_reg, id_hab= id_hab, id_hab_est= id_hab_est, n_last= n_last, dateInicio= dateInicio, order_by=order_by, page_size= self.habRegWindow.getSizePage(), page_current= self.habRegWindow.getCurrentPage())
        
        return new
           
    def init_visual_main(self):
        app = QtWidgets.QApplication(sys.argv) 
        #app.setStyleSheet(dark_theme)       
        self.mainWindow = MainWindow()
        
        #qdarktheme.setup_theme()
        # Customize accent color.
        # qdarktheme.setup_theme(custom_colors={"primary": "#D0BCFF"})
        #self.mainWindow.mdiAreaMain.cascadeSubWindows()
        #self.mainWindow.mdiAreaMain.tileSubWindows()

        self.currentEmpleadoID = 5

        self.init_habW()   
        self.init_cliW()
        self.init_habRegW()
        self.init_newCliW()
        self.init_arqW()
        self.init_newArqW()
        self.init_newHabRegW()

    
        
        self.mainWindow.btnHab.clicked.connect(self.show_update_habW)
        self.mainWindow.btnArq.clicked.connect(self.show_update_arqW)
        self.mainWindow.btnClient.clicked.connect(self.show_update_cliW)
        self.mainWindow.btnSunat.clicked.connect(self.callback_sunat)
    
        self.mainWindow.btnTest.clicked.connect(self.callback_test)

        self.mainWindow.show_visual()
        self.mainWindow.showMaximized()

        sys.exit(app.exec())

    def init_habW(self):
        self.habWindow = HabWindow()
        self.habWindow.btnUpdate.clicked.connect(self.update_values_table_habW)
        self.habWindow.btnHabReg.clicked.connect(self.show_update_habRegW)
        self.habWindow.btnHabReg.clicked.connect(self.callback_openHabRegW_habW)

    def init_arqW(self, window_data = None):
        self.arqWindow = ArqWindow(window_data)
        self.arqWindow.btnUpdate.clicked.connect(self.callback_update_arqW)
        self.arqWindow.btnNewEdit.clicked.connect(self.show_update_newArqW)

        self.arqWindow.btnPrev.clicked.connect(self.callback_prev_arqW)
        self.arqWindow.btnNext.clicked.connect(self.callback_next_arqW)


    def init_cliW(self, window_data = None):
        self.cliWindow = ClientWindow(window_data)
        self.cliWindow.btnUpdate.clicked.connect(self.callback_update_cliW)
        self.cliWindow.btnNewEdit.clicked.connect(self.show_update_newCliW)

        self.cliWindow.btnPrev.clicked.connect(self.callback_prev_cliW)
        self.cliWindow.btnNext.clicked.connect(self.callback_next_cliW)

    def init_habRegW(self, data_front = None, data_back = None):
        self.habRegWindow = HabRegWindow(data_front= data_front, data_back= data_back, d_Hab_est= self.d_Hab_est, table_column_names= table_hab_reg_column_names)
        self.habRegWindow.btnUpdate.clicked.connect(self.callback_update_habRegW)
        self.habRegWindow.btnNewEdit.clicked.connect(self.show_update_newHabRegW)

        self.habRegWindow.btnPrev.clicked.connect(self.callback_prev_habRegW)
        self.habRegWindow.btnNext.clicked.connect(self.callback_next_habRegW)

        self.habRegWindow.btnUpdateTimeStart.clicked.connect(self.callback_habRegW_update_time_start)     
        self.habRegWindow.btnClearTimeStart.clicked.connect(self.callback_habRegW_clear_time_start)

    def init_newCliW(self):
        self.newCliWindow = NewClientWindow()
        self.newCliWindow.btnSearchClient.clicked.connect(self.callback_newCliW_search)
        self.newCliWindow.btnUpdateClient.clicked.connect(self.callback_newCliW_update)
        self.newCliWindow.btnCreateClient.clicked.connect(self.callback_newCliW_create)
        self.newCliWindow.btnDeleteClient.clicked.connect(self.callback_newCliW_delete)
        self.newCliWindow.btnCancelClient.clicked.connect(self.callback_newCliW_cancel)

    def init_newArqW(self):
        self.newArqWindow = NewArqWindow(d_Hab_est=self.d_Hab_est)
        self.newArqWindow.btnSearchClient.clicked.connect(self.callback_newArqW_cli_search)
        self.newArqWindow.btnUpdateClient.clicked.connect(self.callback_newArqW_cli_update)
        self.newArqWindow.btnCreateClient.clicked.connect(self.callback_newArqW_cli_create)

        self.newArqWindow.btnSearchHab.clicked.connect(self.callback_newArqW_hab_search)
        
        self.newArqWindow.btnSearchArq.clicked.connect(self.callback_newArqW_arq_search)
        self.newArqWindow.btnUpdateArq.clicked.connect(self.callback_newArqW_arq_update)
        self.newArqWindow.btnPrepareCreateArq.clicked.connect(self.callback_newArqW_arq_create_prepare)
        self.newArqWindow.btnCreateArq.clicked.connect(self.callback_newArqW_arq_create)
        self.newArqWindow.btnCancelArq.clicked.connect(self.callback_newArqW_arq_cancel)
        self.newArqWindow.btnDeleteArq.clicked.connect(self.callback_newArqW_arq_delete)

        self.newArqWindow.btnUpdateTimeChecking.clicked.connect(self.callback_newArqW_update_time_checking)
        self.newArqWindow.btnUpdateTimeCheckout.clicked.connect(self.callback_newArqW_update_time_checkout)
        self.newArqWindow.btnClearTimeChecking.clicked.connect(self.callback_newArqW_clear_time_checking)
        self.newArqWindow.btnClearTimeCheckout.clicked.connect(self.callback_newArqW_clear_time_checkout)

    def init_newHabRegW(self):
        self.newHabRegWindow = NewHabRegWindow(self.d_Hab_est)

        self.newHabRegWindow.btnSearchHab.clicked.connect(self.callback_newHabRegW_hab_search)
        
        self.newHabRegWindow.btnSearchHabReg.clicked.connect(self.callback_newHabRegW_arq_search)
        self.newHabRegWindow.btnUpdateHabReg.clicked.connect(self.callback_newHabRegW_arq_update)
        self.newHabRegWindow.btnCreateHabReg.clicked.connect(self.callback_newHabRegW_arq_create)
        self.newHabRegWindow.btnCancelHabReg.clicked.connect(self.callback_newHabRegW_arq_cancel)
        self.newHabRegWindow.btnDeleteHabReg.clicked.connect(self.callback_newHabRegW_arq_delete)

        self.newHabRegWindow.btnUpdateTimeHabRegStart.clicked.connect(self.callback_newHabRegW_update_time_start)
        self.newHabRegWindow.btnUpdateTimeHabRegEnd.clicked.connect(self.callback_newHabRegW_update_time_end)
        self.newHabRegWindow.btnClearTimeHabRegStart.clicked.connect(self.callback_newHabRegW_clear_time_start)
        self.newHabRegWindow.btnClearTimeHabRegEnd.clicked.connect(self.callback_newHabRegW_clear_time_end)


    def update_all_subwindows(self): 
        for sub in self.mainWindow.mdiAreaMain.subWindowList():
            sub.adjustSize()
            sub.repaint()
            sub.activateWindow()
            sub.setUpdatesEnabled(True)
            sub.update()
            sub.updateGeometry()

    def create_visual_sub_window(self, wid, pos_x = None, pos_y = None):
        wid.subWindowRef = self.mainWindow.mdiAreaMain.addSubWindow(wid)
        if((pos_x != None) and (pos_y != None)): wid.subWindowRef.move(pos_x, pos_y)
        wid.isCreated = True
        wid.show_visual(False)
        

    def show_update_habW(self, foc):
        if(foc == False): foc = "True" #foc is Flase by default when interruption

        if(self.habWindow.isCreated == False):
            self.init_habW()
            self.update_values_table_habW()
            self.create_visual_sub_window(wid = self.habWindow)
        else:
            self.update_values_table_habW()
            if(foc == "True"):
                self.habWindow.subWindowRef.setFocus()
    """     
    def show_update_habRegW(self, foc):
        if(foc == False): foc = "True" #foc is Flase by default when interruption
        
        if(self.habRegWindow.isCreated == False):
            self.init_habRegW()
            self.update_values_table_habRegW()
            self.create_visual_sub_window(wid = self.habRegWindow)
        else:
            self.update_values_table_habRegW() 
            if(foc == "True"):
                self.habRegWindow.subWindowRef.setFocus()
    """

    def setup_habRegW(self, pos_x  = None, pos_y = None, data_front = None, data_back = None):
        self.init_habRegW(data_front, data_back)
        self.update_values_table_habRegW()
        #self.habRegWindow.updatePageLabel(self.habRegWindow.data.page_current)
        self.create_visual_sub_window(self.habRegWindow,pos_x, pos_y)

    def callback_openHabRegW_habW(self):
        self.show_update_habRegW(foc = True, reset_back=True)
        return 0 
    
    def show_update_habRegW(self, foc, set_page = None, reset_back = None):        
        if(self.habRegWindow.isCreated == False):
            self.setup_habRegW()
        else:
            curr_act=None
            if((foc == False)): curr_act = self.mainWindow.mdiAreaMain.activeSubWindow()

            pos_x = self.habRegWindow.subWindowRef.pos().x()
            pos_y = self.habRegWindow.subWindowRef.pos().y()
            data_front = self.habRegWindow.getWindowDataFront()
            data_back = self.habRegWindow.getWindowDataBack()
            if(set_page != None): data_back.set_pageCurrent(page=1)
            if(reset_back == True): data_back.reset()

            self.mainWindow.mdiAreaMain.removeSubWindow(self.habRegWindow.subWindowRef)
            self.setup_habRegW(pos_x, pos_y, data_front, data_back)

            if(foc == True):
                self.habRegWindow.subWindowRef.setFocus()
            elif((curr_act != None)):
                self.mainWindow.mdiAreaMain.setActiveSubWindow(curr_act)

    def setup_arqW(self, pos_x  = None, pos_y = None, window_data = None):
        self.init_arqW(window_data)
        self.update_values_table_arqW()
        #self.arqWindow.updatePageLabel(self.arqW_data.page_current)
        self.create_visual_sub_window(self.arqWindow,pos_x, pos_y)

    def show_update_arqW(self, foc):
        if(foc == False): foc = "True" #foc is Flase by default when interruption
        
        if(self.arqWindow.isCreated == False):
            self.setup_arqW()
        else:
            curr_act=None
            if((foc == "False")): curr_act = self.mainWindow.mdiAreaMain.activeSubWindow()

            pos_x = self.arqWindow.subWindowRef.pos().x()
            pos_y = self.arqWindow.subWindowRef.pos().y()
            temp_window_data = self.arqWindow.getWindowData()


            self.mainWindow.mdiAreaMain.removeSubWindow(self.arqWindow.subWindowRef)
            self.setup_arqW(pos_x, pos_y, temp_window_data)

            if(foc == "True"):
                self.arqWindow.subWindowRef.setFocus()
            elif((curr_act != None)):
                self.mainWindow.mdiAreaMain.setActiveSubWindow(curr_act)

    def setup_cliW(self, pos_x  = None, pos_y = None, window_data = None):
        self.init_cliW(window_data)
        self.update_values_table_cliW()
        #self.cliWindow.updatePageLabel(self.cliW_data.page_current)
        self.create_visual_sub_window(self.cliWindow,pos_x, pos_y)

    def show_update_cliW(self, foc):
        if(foc == False): foc = "True" #foc is Flase by default when interruption
        
        if(self.cliWindow.isCreated == False):
            self.setup_cliW()
        else:
            curr_act=None
            if((foc == "False")): curr_act = self.mainWindow.mdiAreaMain.activeSubWindow()

            pos_x = self.cliWindow.subWindowRef.pos().x()
            pos_y = self.cliWindow.subWindowRef.pos().y()
            temp_window_data = self.cliWindow.getWindowData()

            self.mainWindow.mdiAreaMain.removeSubWindow(self.cliWindow.subWindowRef)
            self.setup_cliW(pos_x , pos_y, temp_window_data)

            if(foc == "True"):
                self.cliWindow.subWindowRef.setFocus()
            elif((curr_act != None)):
                self.mainWindow.mdiAreaMain.setActiveSubWindow(curr_act)
 
            
    def show_update_newCliW(self, foc):
        if(foc == False): foc = "True" #foc is Flase by default when interruption
        
        if(self.newCliWindow.isCreated == False):
            self.init_newCliW()
            self.create_visual_sub_window(self.newCliWindow)
        else:
            if(foc == "True"):
                self.newCliWindow.subWindowRef.setFocus()     

    def show_update_newArqW(self, foc):
        if(foc == False): foc = "True" #foc is Flase by default when interruption
        
        if(self.newArqWindow.isCreated == False):
            self.init_newArqW()
            self.create_visual_sub_window(self.newArqWindow)
        else:
            if(foc == "True"):
                self.newArqWindow.subWindowRef.setFocus()

    def show_update_newHabRegW(self, foc):
        if(foc == False): foc = "True" #foc is Flase by default when interruption
        
        if(self.newHabRegWindow.isCreated == False):
            self.init_newHabRegW()
            self.create_visual_sub_window(self.newHabRegWindow)
        else:
            if(foc == "True"):
                self.newHabRegWindow.subWindowRef.setFocus()
        
    def update_values_table_habW(self):
        self.get_values_hab()
        self.habWindow.updateTableView(self.d_Habitaciones, table_hab_column_names, self.d_Hab_est, self.d_Hab_cam, self.d_Hab_car)

    def update_values_table_arqW(self):
        self.get_values_arq()
        self.get_values_client()
        self.arqWindow.updateTableView(self.d_Arquileres, table_arq_column_names, self.d_Empleado, self.d_Clientes)


    def callback_update_arqW(self):
        self.arqWindow.setCurrentPage(1)
        self.show_update_arqW(foc="True")

    def callback_prev_arqW(self):
        if(self.arqWindow.getCurrentPage() >= 2):
            self.arqWindow.prevPage()
            self.show_update_arqW(foc="False")
    
    def callback_next_arqW(self):
        if(self.d_Arquileres != None):
            if(len(self.d_Arquileres) != 0):
                self.arqWindow.nextPage()
                self.show_update_arqW(foc="False")


    def callback_update_cliW(self):
        self.cliWindow.setCurrentPage(1)
        self.show_update_cliW(foc="True")

    def callback_prev_cliW(self):
        if(self.cliWindow.getCurrentPage() >= 2):
            self.cliWindow.prevPage()
            self.show_update_cliW(foc="False")
    
    def callback_next_cliW(self):
        if(self.d_Clientes != None):
            if(len(self.d_Clientes) != 0):
                self.cliWindow.nextPage()
                self.show_update_cliW(foc="False")

    def callback_update_habRegW(self):
        self.habRegWindow.pushFrontDataToBack()
        self.show_update_habRegW(foc=True, set_page= 1)

    def callback_prev_habRegW(self):
        if(self.habRegWindow.getCurrentPage() >= 2):
            self.habRegWindow.prevPage()
            self.show_update_habRegW(foc=False)
    
    def callback_next_habRegW(self):
        if(self.d_Hab_Reg != None):
            if(len(self.d_Hab_Reg) != 0):
                self.habRegWindow.nextPage()
                self.show_update_habRegW(foc=False)

    def callback_habRegW_update_time_start(self):
        self.habRegWindow.set_time_start_now()
        return 0

    def callback_habRegW_clear_time_start(self):
        self.habRegWindow.clear_time_start_now()
        return 0


    def update_values_table_cliW(self):
        self.get_values_client()
        self.cliWindow.updateTableView(self.d_Clientes, table_cli_column_names)

    def update_values_table_habRegW(self):
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
            column_name = wd.order_feature
            order_type = wd.order_type
            order_by = None
            var = None
            for k in table_hab_reg_column_names.keys():
                if(table_hab_reg_column_names[k] == column_name):
                    var = table_hab_reg_column_variable[k]
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
    
    """ 
    def callback_newCliW_create_update(self):
        client =  self.newCliWindow.getClientFromForm_cli()

        if (client != None):
            cl_db = db_hgp.get_client_by_doc(client.nDocumento)
            print(cl_db)
            if(cl_db == None):
                try:
                    db_hgp.create_Client(client)
                    self.newCliWindow.labelInfClient.setText("N:Listo")
                    self.update_values_table_cliW()
                except Exception as err:
                    print(f"Unexpected {err=}, {type(err)=}")
                    CustomDialog("Error","Hubo un problema. Verifique si se creó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newCliWindow.labelInfClient.setText("N:Intente de nuevo")
            else:
                try:
                    db_hgp.update_Client(client,cl_db)
                    self.newCliWindow.labelInfClient.setText("N:Listo")
                    self.update_values_table_cliW()
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newCliWindow.labelInfClient.setText("N:Intente de nuevo")
    """

    def f_create_client_from_widget(self, widg):
        client =  widg.getClientFromForm_cli()

        if (client != None):
            cl_db = db_hgp.get_client_by_doc(client.nDocumento)
            if(cl_db == None):
                try:
                    client.lastUpdate = datetime.now()
                    db_hgp.create_Client(client)
                    widg.setInf_cli("N:Listo")
                    self.show_update_cliW(foc= "False")
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se creó o intente de nuevo.\n\n"+str(err)).exec()
                    widg.setInf_cli("N:Intente de nuevo")
            else:
                CustomDialog("Error","El cliente con documento " + str(client.nDocumento) +" ya existe.\n\n").exec()
                widg.setInf_cli("N:Intente de nuevo")

    def f_delete_client_from_widget(self, widg):
        client =  widg.getClientFromForm_cli()

        if (client != None):
            cl_db = db_hgp.get_client_by_doc(client.nDocumento)
            if(cl_db == None):
                CustomDialog("Error","El cliente con documento " + str(client.nDocumento) +" no existe.\n\n").exec()
                widg.setInf_cli("N:Intente de nuevo")
            else:
                try:
                    db_hgp.delete_Client(cl_db)
                    widg.setInf_cli("N:Eliminado")
                    self.show_update_cliW(foc= "False")
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    widg.setInf_cli("N:Intente de nuevo")

    def f_update_client_from_widget(self, widg):
        client =  widg.getClientFromForm_cli()

        if (client != None):
            cl_db = db_hgp.get_client_by_doc(client.nDocumento)
            if(cl_db == None):
                CustomDialog("Error","El cliente con documento " + str(client.nDocumento) +" no existe.\n\n").exec()
                widg.setInf_cli("N:Intente de nuevo")
            else:
                try:
                    client.lastUpdate = datetime.now()
                    db_hgp.update_Client(client,cl_db)
                    widg.setInf_cli("N:Listo")
                    self.show_update_cliW(foc= "False")
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    widg.setInf_cli("N:Intente de nuevo")

    def f_fill_cli_by_doc_from_widget(self, widg, doc):
        if(doc != None):
            cl = db_hgp.get_client_by_doc(doc)
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

        return 0
    
    def f_search_client_from_widget(self, widg):
        doc =  widg.getDocumentFromForm_cli()
        self.f_fill_cli_by_doc_from_widget(widg, doc)

    def callback_newCliW_search(self):
        self.f_search_client_from_widget(self.newCliWindow)

    def callback_newCliW_update(self):
        self.f_update_client_from_widget(self.newCliWindow)

    def callback_newCliW_create(self):
        self.f_create_client_from_widget(self.newCliWindow)

    def callback_newCliW_delete(self):
        self.f_delete_client_from_widget(self.newCliWindow)
 
    def callback_newCliW_cancel(self):
        self.newCliWindow.close()
        self.mainWindow.mdiAreaMain.removeSubWindow(self.newCliWindow.subWindowRef)

    def callback_newArqW_cli_search(self):
        self.f_search_client_from_widget(self.newArqWindow)

    def callback_newArqW_cli_update(self):
        self.f_update_client_from_widget(self.newArqWindow)

    def callback_newArqW_cli_create(self):
        self.f_create_client_from_widget(self.newArqWindow)

    def arqW_f_fill_hab_from_id(self, id_hab):
        if(id_hab != None):
            hab = db_hgp.get_hab_from_id(id_hab)
            if (hab!=None):
                self.newArqWindow.fillData_hab(hab, self.d_Hab_cam, self.d_Hab_est)
                self.newArqWindow.setInf_hab("Valido")
            else:
                CustomDialog("Error","No hay habitacion con id " + id_hab).exec()
                self.newArqWindow.setInf_hab("Error")
        else:
            return 0

    def callback_newArqW_hab_search(self):
        id_hab =  self.newArqWindow.getID_hab()
        self.arqW_f_fill_hab_from_id(id_hab)
        return 0
        
    def callback_newArqW_arq_search(self):
        arq_form, cli_doc = self.newArqWindow.getArqFromForm(self.d_Hab_est, self.currentEmpleadoID, "search")
        if(arq_form != None):
            id_arq_form = arq_form.id
            arq_db = db_hgp.get_arq_by_id(id_arq_form)
            if (arq_db!=None):
                self.newArqWindow.fillData_arq(arq_db)

                self.arqW_f_fill_hab_from_id(arq_db.id_hab)

                doc = None
                cli = db_hgp.get_client_by_id(arq_db.id_cli)
                if (cli == None): doc = None
                else: doc = cli.nDocumento
                self.f_fill_cli_by_doc_from_widget(self.newArqWindow, doc)
            else:
                CustomDialog("Error","No hay arquiler con id " + str(id_arq_form)).exec()
        else:
            return 0
        
    def callback_newArqW_arq_update(self):
        err = 0
        arq_form = None
        arq_form, cli_doc = self.newArqWindow.getArqFromForm(self.d_Hab_est, self.currentEmpleadoID, "update")
        if(arq_form != None):
            id_arq_form = arq_form.id
            
            #verifying Arquiler
            arq_db = db_hgp.get_arq_by_id(id_arq_form)
            if (arq_db!=None):
                try:
                    #verifying client doc and id
                    cl = db_hgp.get_client_by_doc(cli_doc)
                    if (cl!=None):           
                        arq_form.id_cli = cl.id
                        self.newArqWindow.setInf_cli("Valido")
                    else:
                        CustomDialog("Error","No hay cliente con documento " + cli_doc).exec()
                        self.newArqWindow.setInf_cli("B:Error")
                        err=err+1

                    #verifying habitacion id
                    hab = db_hgp.get_hab_from_id(arq_form.id_hab)
                    if (hab!=None):
                        self.newArqWindow.setInf_hab("Valido")
                    else:
                        CustomDialog("Error","No hay habitacion con id " + arq_form.id_hab).exec()
                        self.newArqWindow.setInf_hab("B:Error")
                        err=err+1

                    #If there is not Hab_reg, then create one.
                    if(arq_form.id_hab_reg == None):
                        #create hab_reg
                        #update visual
                        new_hab_reg = None
                        new_hab_reg = self.f_create_hab_reg(arq_form.hab_reg, None)
                        if(new_hab_reg!=None):
                            if(new_hab_reg.id!=None):
                                arq_form.id_hab_reg = new_hab_reg.id
                                self.newArqWindow.fillData_arq_habReg(new_hab_reg, d_Hab_est=self.d_Hab_est)
                    else:
                        self.f_update_hab_reg(arq_form.hab_reg, None)

                    #If there is Hab_reg, then verify and update

                    if(err == 0):
                        arq_form.lastUpdate = datetime.now()
                        db_hgp.update_Arquiler(arq_form,arq_db)
                        self.newArqWindow.setInf_arq("U:Listo")
                        self.show_update_arqW(foc= "False")

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newArqWindow.setInf_arq("N:Intente de nuevo")
            else:
                CustomDialog("Error","No hay arquiler con id " + str(id_arq_form)).exec()

        return 0
        
    def callback_newArqW_arq_create_prepare(self):
        self.newArqWindow.prepare_create()

    def callback_newArqW_arq_create(self):
        err = 0
        arq_form, cli_doc = self.newArqWindow.getArqFromForm(self.d_Hab_est, self.currentEmpleadoID, "create")
        if(arq_form != None):
            id_arq_form = arq_form.id
            
            if (id_arq_form==None):
                try:
                    #verifying client doc and id
                    cl = db_hgp.get_client_by_doc(cli_doc)
                    if (cl!=None):           
                        arq_form.id_cli = cl.id
                        self.newArqWindow.setInf_cli("Valido")
                    else:
                        CustomDialog("Error","No hay cliente con documento " + cli_doc).exec()
                        self.newArqWindow.setInf_cli("B:Error")
                        err=err+1

                    #verifying habitacion id
                    hab = db_hgp.get_hab_from_id(arq_form.id_hab)
                    if (hab!=None):
                        self.newArqWindow.setInf_hab("Valido")
                    else:
                        CustomDialog("Error","No hay habitacion con id " + arq_form.id_hab).exec()
                        self.newArqWindow.setInf_hab("B:Error")
                        err=err+1

                    if(err == 0):

                        new_hab_reg = None
                        arq_form.hab_reg.id = None
                        new_hab_reg = self.f_create_hab_reg(arq_form.hab_reg, None)
                        if(new_hab_reg!=None):
                            if(new_hab_reg.id!=None):
                                arq_form.id_hab_reg = new_hab_reg.id
                                self.newArqWindow.fillData_arq_habReg(new_hab_reg, d_Hab_est=self.d_Hab_est)
                                
                        arq_form.lastUpdate = datetime.now()
                        b = db_hgp.create_Arquiler(arq_form)
                        self.newArqWindow.lineEditArqID.setText(str(b.id))
                        self.newArqWindow.setInf_arq("C:Listo")
                        self.show_update_arqW(foc= "False")

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se creó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newArqWindow.setInf_arq("N:Intente de nuevo")
            else:
                CustomDialog("Error","Ya hay arquiler con id " + str(id_arq_form)).exec()

        return 0
        
    def callback_newArqW_arq_cancel(self):
        self.newArqWindow.close()
        self.mainWindow.mdiAreaMain.removeSubWindow(self.newArqWindow.subWindowRef)
        return 0

    def callback_newArqW_arq_delete(self):
        arq_form, cli_doc = self.newArqWindow.getArqFromForm(self.d_Hab_est, self.currentEmpleadoID, "delete")
        if(arq_form != None):
            id_arq_form = arq_form.id
            arq_db = db_hgp.get_arq_by_id(id_arq_form)
            if (arq_db!=None):
                try:
                        db_hgp.delete_Arquiler(arq_db)
                        self.newArqWindow.setInf_arq("C:Listo")
                        self.show_update_arqW(foc= "False")
                        if(arq_db.hab_reg != None and arq_db.hab_reg.id != None):
                            db_hgp.delete_Hab_Reg(arq_db.hab_reg)
                            self.show_update_habRegW(foc= False, reset_back=True)

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se eliminó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newArqWindow.setInf_arq("N:Intente de nuevo")
            else:
                CustomDialog("Error","No hay arquiler con id " + str(id_arq_form)).exec()

        return 0
        
        
    def callback_newArqW_update_time_checking(self):
        self.newArqWindow.set_time_checking_now()
        return 0

    def callback_newArqW_update_time_checkout(self):
        self.newArqWindow.set_time_checkout_now()
        return 0

    def callback_newArqW_clear_time_checking(self):
        self.newArqWindow.clear_time_checking_now()
        return 0

    def callback_newArqW_clear_time_checkout(self):
        self.newArqWindow.clear_time_checkout_now()
        return 0
    
    #new hab reg
    def habRegW_f_fill_hab_from_id(self, id_hab):
        if(id_hab != None):
            hab = db_hgp.get_hab_from_id(id_hab)
            if (hab!=None):
                self.newHabRegWindow.fillData_hab(hab, self.d_Hab_est)
                self.newHabRegWindow.setInf_hab("Valido")
            else:
                CustomDialog("Error","No hay habitacion con id " + id_hab).exec()
                self.newHabRegWindow.setInf_hab("Error")
        else:
            return 0
        
    def callback_newHabRegW_hab_search(self):
        id_hab =  self.newHabRegWindow.getID_hab()
        self.habRegW_f_fill_hab_from_id(id_hab)
        return 0
        
    def callback_newHabRegW_arq_search(self):
        hab_reg_form = self.newHabRegWindow.getHabRegFromForm(self.d_Hab_est, "search")
        if(hab_reg_form != None):
            id_hab_reg_form = hab_reg_form.id
            hab_reg_db = db_hgp.get_hab_reg_from_id(id_hab_reg_form)
            if (hab_reg_db!=None):
                self.newHabRegWindow.fillData_hab_reg(hab_reg_db, self.d_Hab_est)
                self.habRegW_f_fill_hab_from_id(hab_reg_db.id_hab)
            else:
                CustomDialog("Error","No hay registro con id " + str(id_hab_reg_form)).exec()
        else:
            return 0
        

    def f_update_hab_reg(self, hab_reg_form, window):
        err = 0
        if(hab_reg_form != None):
            id_hab_reg_form = hab_reg_form.id
            
            #verifying reg
            hab_reg_db = db_hgp.get_hab_reg_from_id(id_hab_reg_form)
            if (hab_reg_db!=None):
                try:
                    #verifying habitacion id
                    hab = db_hgp.get_hab_from_id(hab_reg_form.id_hab)
                    if (hab!=None):
                        if(window != None): window.setInf_hab("Valido")
                    else:
                        CustomDialog("Error","No hay habitacion con id " + hab_reg_form.id_hab).exec()
                        if(window != None): window.setInf_hab("B:Error")
                        err=err+1

                    if(err == 0):
                        hab_reg_form.lastUpdate = datetime.now()
                        db_hgp.update_Hab_Reg(hab_reg_form,hab_reg_db)
                        if(window != None): window.setInf_hab_reg("U:Listo")
                        self.show_update_habRegW(foc= False, reset_back=True)

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se actualizó o intente de nuevo.\n\n"+str(err)).exec()
                    if(window != None): window.setInf_hab_reg("N:Intente de nuevo")
            else:
                CustomDialog("Error","No hay arquiler con id " + str(id_hab_reg_form)).exec()

        
    def callback_newHabRegW_arq_update(self):
        hab_reg_form = self.newHabRegWindow.getHabRegFromForm(self.d_Hab_est, "update")
        self.f_update_hab_reg(hab_reg_form = hab_reg_form, window = self.newHabRegWindow)
        return 0
    
    def f_create_hab_reg(self, hab_reg_form, window):
        err = 0
        new_hab_reg = None
        if(hab_reg_form != None):
            id_hab_reg_form = hab_reg_form.id
            
            if (id_hab_reg_form==None):
                try:
                    #verifying habitacion id
                    hab = db_hgp.get_hab_from_id(hab_reg_form.id_hab)
                    if (hab!=None):
                        if(window != None): window.setInf_hab("Valido")
                    else:
                        CustomDialog("Error","No hay habitacion con id " + hab_reg_form.id_hab).exec()
                        if(window != None): window.setInf_hab("B:Error")
                        err=err+1

                    if(err == 0):
                        hab_reg_form.lastUpdate = datetime.now()
                        new_hab_reg = db_hgp.create_Hab_Reg(hab_reg_form)
                        if(window != None): 
                            window.lineEditHabRegID.setText(str(new_hab_reg.id))
                            window.setInf_hab_reg("C:Listo")
                        self.show_update_habRegW(foc= False, reset_back=True)

                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se creó o intente de nuevo.\n\n"+str(err)).exec()
                    if(window != None): window.setInf_hab_reg("N:Intente de nuevo")
            else:
                CustomDialog("Error","Ya hay registro con id " + str(id_hab_reg_form)).exec()
        return new_hab_reg


    def callback_newHabRegW_arq_create(self):
        hab_reg_form = self.newHabRegWindow.getHabRegFromForm(self.d_Hab_est, "create")
        self.f_create_hab_reg(hab_reg_form = hab_reg_form, window = self.newHabRegWindow)
        return 0
        
    def callback_newHabRegW_arq_cancel(self):
        self.newHabRegWindow.close()
        self.mainWindow.mdiAreaMain.removeSubWindow(self.newHabRegWindow.subWindowRef)
        return 0

    def callback_newHabRegW_arq_delete(self):
        hab_reg_form = self.newHabRegWindow.getHabRegFromForm(self.d_Hab_est, "delete")
        if(hab_reg_form != None):
            id_hab_reg_form = hab_reg_form.id
            #verifying reg
            hab_reg_db = db_hgp.get_hab_reg_from_id(id_hab_reg_form)
            if (hab_reg_db!=None):
                try:
                    db_hgp.delete_Hab_Reg(hab_reg_form)
                    self.newHabRegWindow.setInf_hab_reg("C:Listo")
                    self.show_update_habRegW(foc= False, reset_back=True)
                except Exception as err:
                    CustomDialog("Error","Hubo un problema. Verifique si se eliminó o intente de nuevo.\n\n"+str(err)).exec()
                    self.newHabRegWindow.setInf_hab_reg("N:Intente de nuevo")
            else:
                CustomDialog("Error","No hay registro con id " + str(id_hab_reg_form)).exec()

        return 0
        
        
    def callback_newHabRegW_update_time_start(self):
        self.newHabRegWindow.set_time_start_now()
        return 0

    def callback_newHabRegW_update_time_end(self):
        self.newHabRegWindow.set_time_end_now()
        return 0

    def callback_newHabRegW_clear_time_start(self):
        self.newHabRegWindow.clear_time_start_now()
        return 0

    def callback_newHabRegW_clear_time_end(self):
        self.newHabRegWindow.clear_time_end_now()
        return 0
    
    
    def test_db_dunctions(self):
        #d_var = db_hgp.get_dic_table_arquiler(id_hab="31", n_last=5, dateChecking=None)
        #d_var = db_hgp.get_dic_table_arquiler()
        #d_var = db_hgp.get_dic_table_registro(id_hab="B", n_last=5, dateChecking=None)
        #d_var = db_hgp.get_dic_table_registro(id_hab="31")
        #d_var = db_hgp.get_dic_table_cliente()
        #db_hgp.printList(d_var)
        #print(d_Habitaciones["B"])

        return 0
    
    def callback_sunat(self):
        webbrowser.open('https://e-menu.sunat.gob.pe/cl-ti-itmenu/MenuInternet.htm?pestana=*&agrupacion=*')
    
    def callback_test(self):
        new = db_hgp.get_dic_table_arquiler_test(id_hab = None, n_last = None, dateChecking = None, page_size= None, page_current= None)
        return 0

controllerHGP = Controller()

controllerHGP.get_values_hab()
controllerHGP.load_default_values()
controllerHGP.test_db_dunctions()
controllerHGP.init_visual_main()































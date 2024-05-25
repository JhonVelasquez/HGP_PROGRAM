import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import *
from db_model import *
from PyQt6.QtCore import Qt, QDateTime, QDate
#from main import *
import datetime

global controllerHGP

class Window_data():
    page_current = 1

    id_hab_reg = None
    fecha_inicio = None
    id_hab = None
    id_hab_est = None
    hab_est = None

    id_cli = None
    document = None
    name = None
    surname = None
    cellphone = None

    id_arq = None
    fecha_checking = None

    order_type = None
    order_feature = None
    
    #permanent values
    consumed = False
    page_size = 10
    default_type = None
    default_feature = None
    path_gui = None
    title_window = None
    has_table = None
    has_pages = None
    has_client_section = None
    has_combo_estados = None
    extra_combo_estados = None
    combo_estados_in_arquiler = None
    combo_estados_in_hab_reg = None
    
    has_combos_orderby = None

    def reset(self):
        self.page_current = 1
        self.id_hab_reg = None
        self.fecha_inicio = None
        self.id_hab = None
        self.id_hab_est = None
        self.hab_est = None

        self.id_cli = None
        self.document = None
        self.name = None
        self.surname = None
        self.cellphone = None

        self.id_arq = None
        self.fecha_checking = None

        self.order_type = None
        self.order_feature = None

        return 0   
    def set_pageCurrent(self, page):
        self.page_current = page

class GeneralWindow(QtWidgets.QWidget):
    isCreated = None
    subWindowRef = None
    data_back = None
    newCliFuncs = None
    context_menu = None

    table_column_names = None

    cmb_order_by_name = None

    data_front = None

    def __init__(self, data_back: Window_data = None, data_front: Window_data = None, d_Hab_est:dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(data_back.path_gui, self)
        self.setWindowTitle(data_back.title_window)
        icon = QtGui.QIcon("./src/logoHGP.png")
        self.setWindowIcon(icon)
        self.isCreated = False

        if (data_back == None): self.data_back = Window_data()
        else: self.data_back = data_back
        
        if (data_front == None): self.data_front = Window_data()
        else: self.data_front = data_front

        if(self.data_back.has_client_section ==True): self.newCliFuncs = NewClientFunctions()
        if(self.data_back.has_combo_estados == True): self.loadComboState(d_Hab_est)

        if(self.data_back.has_combos_orderby == True):
            data_back.default_type = "desc"
            data_back.default_feature = "Ultimo cambio"
            self.loadComboOrder()

        #loading graphics
        self.updateUsingWindowData()
        self.context_menu = QMenu(self)
        self.addAction("Limpiar ventana", self.clearWindow)

    def addAction(self, name, action):
        clearWindow = self.context_menu.addAction(name)
        clearWindow.triggered.connect(action)

        
    def clearWindow(self):
        self.data_front.reset()
        self.data_back.reset()
        self.updateUsingWindowData()

    def updateUsingWindowData(self):      
        if(self.data_back.page_current == None): self.data_back.page_current = 1
        self.updateUsingWindowDataBack()
        self.updateUsingWindowDataFront()

    def updateUsingWindowDataBack(self):      
        if(self.data_back.has_pages):
            if(self.data_back.page_current == None): self.data_back.page_current = 1
            self.updatePageLabel(self.data_back.page_current)
    
    def updateUsingWindowDataFront(self):
        if(self.data_back.has_combos_orderby): self.updateCombosOrderBy()
        return 0
    
    def pushFrontDataToBack(self):
        if (self.data_back.has_combos_orderby):    
            self.data_back.order_feature = self.data_front.order_feature
            self.data_back.order_type = self.data_front.order_type
        return 0
    
    def getWindowDataFront(self):  
        if(self.data_back.has_combos_orderby): self.getDataFrontCombosOrder()
        return 0
    
    def getWindowDataBack(self):
        return self.data_back

    def contextMenuEvent(self, event):
        self.context_menu.exec(event.globalPos())

    def closeEvent(self, event):
        # do stuff
        should_it_close = True
        if should_it_close:
            self.isCreated = False
            event.accept() # let the window close
        else:
            event.ignore()

    def show_visual(self, focus = True):
        self.show()
        #self.showNormal()
        #self.setVisible(True)
        if focus: self.setFocus()
        #self.activateWindow()
        #self.raise_()
        #self.blockSignals(False)

    def resetTableView(self):
        self.tableContent.reset()
        self.tableContent.setSortingEnabled(False)

    def setTableViewPost(self):
        self.tableContent.setSortingEnabled(True)

    def get_element_selected_text(self, column = 0):
        r = (self.tableContent.currentRow())
        if(r == -1):
            return None
        else:
            id_sel = self.tableContent.item(r,column).text()
            return id_sel
    
    def select_row_by_id(self, id_ref):
        found_row = None
        n_r = self.tableContent.rowCount()
        id_ref_str = str(id_ref)
        
        for r in range(n_r):
            id_str = self.tableContent.item(r,0).text()
            if(id_str == id_ref_str):
                found_row = r

        if (found_row != None): self.tableContent.selectRow(found_row)
        return 0
    
    #If there is page_current and page_next    
    def getSizePage(self):
        return self.data_back.page_size

    def getCurrentPage(self):
        return self.data_back.page_current
    
    def setCurrentPage(self, page: int):
        self.data_back.page_current = page
        self.updatePageLabel(page)
 
    def nextPage(self):
        self.setCurrentPage(self.getCurrentPage()+1)

    def prevPage(self):
        self.setCurrentPage(self.getCurrentPage()-1)

    def  updatePageLabel(self, page_current):
        self.lblPage.setText(str(page_current))

    #cliente section
    def fillData_cli(self, c: Cliente):
        self.newCliFuncs.fillData(self, c)

    def clearLineData_cli(self):
        self.newCliFuncs.clearLineData(self)

    def getDocumentFromForm_cli(self):
        return self.newCliFuncs.getDocumentFromForm(self)
    
    def getClientFromForm_cli(self):
        return self.newCliFuncs.getClientFromForm(self)
    
    def isDocEmpty_cli(self):
        return self.newCliFuncs.isDocEmpty(self)
    
    def setInf_cli(self, mssg):
        return self.newCliFuncs.setInf(self, mssg) 
    
    #combo box estado
    def loadComboState(self, d_Hab_est):
        self.comboBoxState.clear()
        for hab_est in d_Hab_est.values():
            if(self.data_back.combo_estados_in_arquiler == True):
                if(hab_est.is_in_arquiler == "True"):
                    self.comboBoxState.addItem(hab_est.value)
            elif(self.data_back.combo_estados_in_hab_reg == True):
                if(hab_est.is_in_hab_reg== "True"):
                    self.comboBoxState.addItem(hab_est.value)

        if(self.data_back.extra_combo_estados != None):
            self.comboBoxState.addItem(self.data_back.extra_combo_estados)
            self.comboBoxState.setCurrentText(self.data_back.extra_combo_estados)
    #combo box order by

    def updateCombosOrderBy(self):
        if(self.data_front.order_type == None): self.comboBoxOrderType.setCurrentText(self.data_back.default_type)
        else: self.comboBoxOrderType.setCurrentText(str(self.data_front.order_type))

        if(self.data_front.order_feature == None): self.comboBoxOrderFeature.setCurrentText(self.data_back.default_feature)
        else: self.comboBoxOrderFeature.setCurrentText(str(self.data_front.order_feature))
    
    def getDataFrontCombosOrder(self):
        order_type = self.comboBoxOrderType.currentText()
        if(order_type == ""): order_type = self.data_back.default_type
        self.data_front.order_type = order_type
        
        order_feature = self.comboBoxOrderFeature.currentText()
        if(order_feature == ""): order_feature = self.data_back.default_feature
        self.data_front.order_feature = order_feature

    def loadComboOrder(self):
        self.comboBoxOrderType.clear()
        self.comboBoxOrderType.addItem("asce")
        self.comboBoxOrderType.addItem("desc")
        self.comboBoxOrderType.setCurrentText(self.data_back.default_type)

        self.comboBoxOrderFeature.clear()
        for col in self.cmb_order_by_name.values():
            self.comboBoxOrderFeature.addItem(col)
        self.comboBoxOrderFeature.setCurrentText(self.data_back.default_feature)
           

class MainWindow(GeneralWindow):
    
    def __init__(self, *args, **kwargs):
        data_back = Window_data()
        data_back.path_gui = './ui/main_widget.ui'
        data_back.title_window = "HGP"
        data_back.has_table = True
        data_back.has_pages = False
        super().__init__(data_back=data_back,*args, **kwargs)    
    
class HabWindow(GeneralWindow):

    def __init__(self, table_column_names, *args, **kwargs):
        data_back = Window_data()
        data_back.path_gui = './ui/hab.ui'
        data_back.title_window = "Habitaciones"
        data_back.has_table = True
        data_back.has_pages = False
        self.table_column_names = table_column_names
        super().__init__(data_back=data_back,*args, **kwargs)

    def get_hab_id_selected(self):
        v = self.get_element_selected_text(column=0)
        if(v != None): return v
        else: return None
    
    def updateTableView(self, d_Habitaciones: dict[str, Habitacion], d_Hab_est, d_Hab_cam, d_Hab_car):

        #self.resetTableView()
        n_row = len(d_Habitaciones)
        n_col = len (self.table_column_names.values())

        self.tableContent.setColumnCount(n_col)
        self.tableContent.setRowCount(n_row)
        self.tableContent.setStyleSheet("QTableWidget::item { padding-left:0px; padding-right:0px; padding-top: 5px; padding-bottom: 5px;}")
        self.tableContent.setSortingEnabled(False)

        for i,key in enumerate(d_Habitaciones.keys()):
            header_item = QtWidgets.QTableWidgetItem(str(i+1))
            self.tableContent.setVerticalHeaderItem(i, header_item)

        for j,name in enumerate(self.table_column_names.values()):
            self.tableContent.setHorizontalHeaderItem(j,QtWidgets.QTableWidgetItem(name))

        for i,key in enumerate(d_Habitaciones.keys()):
            for j,col_name in enumerate(self.table_column_names.values()):
                hab_row =  d_Habitaciones[key]
                var =  hab_row.getTableElementByPos(j, d_Hab_est, d_Hab_cam, d_Hab_car) 
                element = None
                if(j == 7 or j == 8 or j == 9 or j == 10): # lists of hab_reg in var
                    element = QtWidgets.QTableWidgetItem()
                    self.tableContent.setItem(i, j, element)
                    #element.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
                    widget = QWidget()
                    layout = QHBoxLayout()
                    btn = QPushButton()
                    spacer = None
                    spacer = QSpacerItem(5, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    
                    """ 
                    elif(j==8):
                        spacer = QSpacerItem(10, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed) """

                    if(j==9):
                        add_hab_state = False
                        if(len(var)==0 and hab_row.state == 1): #state value 1 is "Disponible"
                            add_hab_state = True
                        elif (hab_row.state == 0): #state value 1 is "Inisponible"
                            add_hab_state = True

                        if(add_hab_state == True):
                            hr = Habitaciones_registro()
                            hr.id = -1
                            hr.id_hab_est = hab_row.state
                            var.append(hr)
                                    
                    layout.addItem(spacer)
                    for m,hab_reg in enumerate(var):
                            est = d_Hab_est[hab_reg.id_hab_est]

                            if(hab_reg.id != -1): text = str(hab_reg.id) + ": " + str(est.value)
                            else: text = est.value

                            btn = QLabel()
                            btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
                            style_str = "padding-left: 5px; padding-right: 5px; padding-top: 3px; padding-bottom: 3px; height: 40px; width: 200px;"
                            
                            if(est.background != None and est.background!=""): style_str = style_str + "background-color:"+ est.background +";"
                            #btn.setMinimumSize(btn.sizeHint())
                            btn.setStyleSheet(style_str)
                            
                            btn.setText(text)       
                            layout.addWidget(btn)

                        #if(i==0): s =">> " +str(hab_reg.id) + ": " + str(d_Hab_est[hab_reg.id_hab_est].value)
                        #else: s = s + " > " + str(hab_reg.id) + ": " + str(d_Hab_est[hab_reg.id_hab_est].value)    


                    if(len(var) == 1 and j == 9):
                        spacer = QSpacerItem(5, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    else:
                        spacer = QSpacerItem(5, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
                    
                    layout.addItem(spacer)

                    layout.setContentsMargins(0,0,0,0)
                    layout.setSpacing(3)
                    layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
                    widget.setLayout(layout) 
                    widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

                    self.tableContent.setCellWidget(i, j, widget)
                else:
                    element = QtWidgets.QTableWidgetItem()
                    element.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    element.setData(Qt.ItemDataRole.DisplayRole, var)
                    self.tableContent.setItem(i, j, element)

        self.tableContent.resizeColumnsToContents()
        self.tableContent.resizeRowsToContents()    
        self.setTableViewPost()
        self.tableContent.setSortingEnabled(False)    

class ArqWindow(GeneralWindow):

    def __init__(self, data_front: Window_data, data_back: Window_data, d_Hab_est, table_column_names, cmb_order_by_name: None, *args, **kwargs):
        if(data_back == None): data_back = Window_data()
        data_back.path_gui = './ui/arq.ui'
        data_back.title_window = "Arquileres"
        data_back.has_table = True
        data_back.has_pages = True
        data_back.page_size = 15

        data_back.has_combo_estados = True
        data_back.extra_combo_estados = ""
        data_back.combo_estados_in_arquiler = True

        data_back.has_combos_orderby = True
        self.table_column_names = table_column_names
        self.cmb_order_by_name = cmb_order_by_name
        super().__init__(data_back=data_back,data_front=data_front,d_Hab_est=d_Hab_est,*args, **kwargs)

    def get_arq_id_selected(self):
        v = self.get_element_selected_text(column=0)
        if(v != None): return int(v)
        else: return None

    def set_time_checking_now(self):
        self.dateEditChecking.setDateTime(QDateTime.currentDateTime())

    def clear_time_checking_now(self):
        self.dateEditChecking.setDateTime(self.dateEditChecking.minimumDateTime())

    def updateUsingWindowDataFront(self):
        super().updateUsingWindowDataFront()

        if(self.data_front.id_arq == None): self.lineEditArqID.setText("")
        else: self.lineEditArqID.setText(str(self.data_front.id_arq)) 

        if(self.data_front.id_hab == None): self.lineEditHabID.setText("")
        else: self.lineEditHabID.setText(str(self.data_front.id_hab)) 

        if(self.data_front.document == None): self.lineEditDocumento.setText("")
        else: self.lineEditDocumento.setText(str(self.data_front.document))
        
        if(self.data_front.name == None): self.lineEditNombre.setText("")
        else: self.lineEditNombre.setText(str(self.data_front.name))

        if(self.data_front.surname == None): self.lineEditApellido.setText("")
        else: self.lineEditApellido.setText(str(self.data_front.surname))

        if(self.data_front.id_hab_reg == None): self.lineEditHabRegID.setText("")
        else: self.lineEditHabRegID.setText(str(self.data_front.id_hab_reg))

        if(self.data_front.hab_est == None): self.comboBoxState.setCurrentText("")
        else: self.comboBoxState.setCurrentText(str(self.data_front.hab_est))

        if(self.data_front.fecha_checking == None): self.clear_time_checking_now()
        else: self.dateEditChecking.setDateTime(self.data_front.fecha_checking)

    def getWindowDataFront(self):
        super().getWindowDataFront()

        id_arq = self.lineEditArqID.text()
        if(id_arq == ""): id_arq = None
        self.data_front.id_arq = id_arq

        id_hab = self.lineEditHabID.text()
        if(id_hab == ""): id_hab = None
        self.data_front.id_hab = id_hab

        document = self.lineEditDocumento.text()
        if (document == ""): document = None
        self.data_front.document = document

        name = self.lineEditNombre.text()
        if(name == ""): name = None
        self.data_front.name = name

        surname = self.lineEditApellido.text()
        if (surname == ""): surname = None
        self.data_front.surname = surname
        
        id_hab_reg = self.lineEditHabRegID.text()
        if(id_hab_reg == ""): id_hab_reg = None
        self.data_front.id_hab_reg = id_hab_reg

        fecha_checking = self.dateEditChecking.dateTime()
        if(fecha_checking == self.dateEditChecking.minimumDateTime()): fecha_checking = None
        self.data_front.fecha_checking = fecha_checking
        
        hab_est = self.comboBoxState.currentText()
        if(hab_est == ""): hab_est = None
        self.data_front.hab_est = hab_est


        return self.data_front

    def pushFrontDataToBack(self):
        self.getWindowDataFront() #pullgin dataFront from UI
        self.data_back.id_arq = self.data_front.id_arq
        self.data_back.id_hab = self.data_front.id_hab
        self.data_back.document = self.data_front.document
        self.data_back.name = self.data_front.name
        self.data_back.surname = self.data_front.surname
        self.data_back.id_hab_reg = self.data_front.id_hab_reg
        self.data_back.fecha_checking = self.data_front.fecha_checking
        self.data_back.hab_est = self.data_front.hab_est
        self.data_back.id_hab_est = self.data_front.id_hab_est
        super().pushFrontDataToBack()

    def updateTableView(self, d_Arquiler: dict[str, Arquiler], d_Empleado):
        #self.resetTableView()

        n_row = len(d_Arquiler)
        n_col = len (self.table_column_names.values())

        self.tableContent.setColumnCount(n_col)
        self.tableContent.setRowCount(n_row)
        self.tableContent.setStyleSheet("QTableWidget::item { padding: 10px }")

        for i,key in enumerate(d_Arquiler.keys()):
            header_item = QtWidgets.QTableWidgetItem(str(i+1))
            self.tableContent.setVerticalHeaderItem(i, header_item)

        for j,name in enumerate(self.table_column_names.values()):
            self.tableContent.setHorizontalHeaderItem(j,QtWidgets.QTableWidgetItem(name))

        for i,key in enumerate(d_Arquiler.keys()):
            for j,col_name in enumerate(self.table_column_names.values()):

                client_id = d_Arquiler[key].id_cli
                #cli_info_str =  d_Clientes[client_id].nDocumento + ", " + d_Clientes[client_id].nombre + " " + d_Clientes[client_id].apellido
                #cli_info_str =  d_Arquiler[key].cli.
                cli_info_str = d_Arquiler[key].cli.nDocumento + ", " + d_Arquiler[key].cli.nombre + " " + d_Arquiler[key].cli.apellido
                
                var_raw = d_Arquiler[key].getTableElementByPos(j, d_Empleado)
                if(var_raw==None):
                    var = "-"
                elif("F/h checking" == col_name or "F/h checkout" == col_name or  "Ultimo cambio" == col_name):
                    var = QtCore.QDateTime.fromString(var_raw, "yyyy-MM-dd hh:mm:ss")
                    #print(var_raw)
                else:
                    var = var_raw

                element = QtWidgets.QTableWidgetItem()
                element.setData(Qt.ItemDataRole.DisplayRole, var)

                if("Cliente"!= col_name):
                    element.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                #else:
                #    element.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.tableContent.setItem(i, j, element)
        self.tableContent.resizeColumnsToContents()

        self.setTableViewPost()

class NewArqWindow(GeneralWindow):

    def __init__(self, d_Hab_est, *args, **kwargs):
        data_back = Window_data()
        data_back.path_gui = './ui/new_arq.ui'
        data_back.title_window = "Nuevo arquiler"
        data_back.has_table = False
        data_back.has_pages = False
        data_back.has_client_section = True

        data_back.has_combo_estados = True
        data_back.extra_combo_estados = "(Estado no válido)"

        data_back.combo_estados_in_arquiler = True

        super().__init__(data_back=data_back,d_Hab_est=d_Hab_est,*args, **kwargs)

        self.set_time_checking_now()
        self.set_time_checkout_now()
        self.timeEditChecking.setCalendarPopup(True)
        self.timeEditCheckout.setCalendarPopup(True)

    def fillData_hab(self, h: Habitacion, d_Hab_cam, d_Hab_est):
        self.lineEditHabID.setText(h.id)
        self.label_camas.setText(h.getCamasString(d_Hab_cam))
        self.label_precio.setText(str(h.precioReferencia))

        last_hab_reg = h.getLastHabReg()
        if(last_hab_reg!=None):
            est = d_Hab_est[last_hab_reg.id_hab_est]
            self.label_estado.setText(str(est.value))
        else:
            self.label_estado.setText("")
            
    def clearWindow(self):
        self.lineEditArqID.setText("")
        
        self.lineEditHabID.setText("")
        self.label_camas.setText("")
        self.label_precio.setText("")
        self.label_estado.setText("")

        self.lineEditDocument.setText("")
        self.lineEditName.setText("")
        self.lineEditLastName.setText("")
        self.lineEditCellphone.setText("")
        self.lineEditAdditionalData.setText("")

        self.labelEstadoID.setText("")
        self.comboBoxState.setCurrentText("(Estado no válido)")
        
        self.clear_time_checking_now()
        self.clear_time_checkout_now()
        self.lineEditPrice.setText("")
        self.lineEditDeuda.setText("")

        self.labelInfHab.setText("-")
        self.labelInfClient.setText("-")
        self.labelInfArq.setText("-")

    def getID_hab(self):
        return self.lineEditHabID.text()
    
    def set_time_checking_now(self):
        self.timeEditChecking.setDateTime(QDateTime.currentDateTime())

    def set_time_checkout_now(self):
        self.timeEditCheckout.setDateTime(QDateTime.currentDateTime())
    
    def clear_time_checking_now(self):
        self.timeEditChecking.setDateTime(self.timeEditChecking.minimumDateTime())

    def clear_time_checkout_now(self):
        self.timeEditCheckout.setDateTime(self.timeEditCheckout.minimumDateTime())
    
    def prepare_create(self):
        self.labelEstadoID.setText("")
    
    def getArqFromForm(self, d_Hab_est, id_emp, type_op):
        arq = Arquiler()
        cliDoc = ""
        err = 0
        if(type_op == "create" ):
            a = (self.lineEditArqID.text() == "")
            b = self.isDataInFormValid()
            if(a and b):
                arq.id = None
            else:
                err=err+1
                CustomDialog("Error","Arquiler ID debe estar vacio para crear y los demas no.").exec()
            
        elif(type_op == "update"):
            if((self.lineEditArqID.text() != "") and self.isDataInFormValid()):
                arq.id = int(self.lineEditArqID.text())
            else:
                err=err+1
                CustomDialog("Error","Revise los datos, no debe haber vacios.").exec()
            
        elif(type_op == "search"):
            if(self.lineEditArqID.text() != ""):
                arq.id = int(self.lineEditArqID.text())
            else:
                err=err+1
                CustomDialog("Error","Arquiler ID no debe estar vacio para buscar.").exec()

        elif(type_op == "delete"):
            if(self.lineEditArqID.text() != ""):
                arq.id = int(self.lineEditArqID.text())
            else:
                err=err+1
                CustomDialog("Error","Arquiler ID no debe estar vacio para eliminar.").exec()

        if(err!=0):
            arq = None
            cliDoc = None
        else:
            arq.id_hab = self.lineEditHabID.text()
            arq.id_cli = None
            arq.id_emp = int(id_emp)

            pri_str = self.lineEditPrice.text()
            if(pri_str==""): arq.precioReal = None
            else: arq.precioReal = float(pri_str)

            deu_str = self.lineEditDeuda.text()
            if(deu_str==""): arq.deuda = None
            else: arq.deuda = float(self.lineEditDeuda.text())
            
            if(self.timeEditChecking.dateTime() == self.timeEditChecking.minimumDateTime()): arq.fechaHoraChecking = None
            else: arq.fechaHoraChecking = self.timeEditChecking.dateTime().toPyDateTime()

            if(self.timeEditCheckout.dateTime() == self.timeEditCheckout.minimumDateTime()): arq.fechaHoraCheckout = None
            else: arq.fechaHoraCheckout = self.timeEditCheckout.dateTime().toPyDateTime()
            
            
            if(self.labelEstadoID.text() != ""):
                arq.id_hab_reg = self.labelEstadoID.text()
            else:
                arq.id_hab_reg = None
                
            arq.hab_reg = Habitaciones_registro()

            arq.hab_reg.id = arq.id_hab_reg
            arq.hab_reg.id_hab = arq.id_hab

            est_str = self.comboBoxState.currentText()
            if(est_str==""): arq.hab_reg.id_hab_est = None
            else:
                found = False
                default_last_is_in_arquiler = 0
                for k in d_Hab_est.keys():
                    if(d_Hab_est[k].value == est_str):
                        arq.hab_reg.id_hab_est = d_Hab_est[k].id
                        found = True
                    if(d_Hab_est[k].is_in_arquiler == "True"):
                        default_last_is_in_arquiler = d_Hab_est[k].id


                if(found == False or arq.hab_reg.id_hab_est == None): arq.hab_reg.id_hab_est = default_last_is_in_arquiler

            arq.hab_reg.fechaHoraInicio = arq.fechaHoraChecking
            arq.hab_reg.fechaHoraFin = arq.fechaHoraCheckout

            #if(type_op == "create" or type_op == "update"):
            #    h.lastUpdate = QDateTime.currentDateTime().toPyDateTime()
            #else:
            #    h.lastUpdate = None

            #datetime_object = self.timeEditChecking.dateTime().toPyDateTime().strftime("%m/%d/%Y, %H:%M:%S")
            cliDoc = self.lineEditDocument.text()
           
            #QDateTime.toString("yyyy-MM-dd hh:mm:ss")
            #QDateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        return arq, cliDoc
    
    def fillData_arq(self, arq: Arquiler):

        if(arq.id != None): self.lineEditArqID.setText(str(arq.id))
        else: self.lineEditArqID.setText("")

        if(arq.precioReal != None): self.lineEditPrice.setText(str(arq.precioReal))
        else: self.lineEditPrice.setText("")

        if(arq.deuda != None): self.lineEditDeuda.setText(str(arq.deuda))
        else: self.lineEditDeuda.setText("")

        if(arq.fechaHoraChecking != None):
            self.timeEditChecking.setDateTime(arq.fechaHoraChecking)
        else:
            #d = QDateTime.fromString("0001-01-01 01:01:01", "yyyy-MM-dd hh:mm:ss")
            self.timeEditChecking.setDateTime(self.timeEditChecking.minimumDateTime())

        if(arq.fechaHoraCheckout != None):
            self.timeEditCheckout.setDateTime(arq.fechaHoraCheckout)
        else:
            #d = QDateTime.fromString("0001-01-01 01:01:01", "yyyy-MM-dd hh:mm:ss")
            self.timeEditCheckout.setDateTime(self.timeEditCheckout.minimumDateTime())
        self.fillData_arq_habReg(arq.hab_reg)
        
    def fillData_arq_habReg(self, hab_reg: Habitaciones_registro, d_Hab_est = None):
        if(hab_reg != None and hab_reg.hab_estado == None and d_Hab_est != None):
            found = False
            for k in d_Hab_est.keys():
                if(d_Hab_est[k].id == hab_reg.id_hab_est):
                    hab_reg.hab_estado = d_Hab_est[k]

        if(hab_reg != None and hab_reg.hab_estado != None):
            if(hab_reg.hab_estado.is_in_arquiler == "True"):
                self.labelEstadoID.setText(str(hab_reg.id) )
                self.labelEstadoInf.setText("")
                self.comboBoxState.setCurrentText(str(hab_reg.hab_estado.value))
            else:
                self.labelEstadoID.setText(str(hab_reg.id))
                self.labelEstadoInf.setText( str(hab_reg.hab_estado.value))
                self.comboBoxState.setCurrentText("(Estado no válido)")
        else:
            self.labelEstadoID.setText("")
            self.labelEstadoInf.setText("")
            self.comboBoxState.setCurrentText("(Estado no válido)")

        return 0


    def isDataInFormValid(self):
        return self.isHabIDValid() and self.isCliIDValid() and self.isPriceValid() and self.isDateValid()
    
    def isHabIDValid(self):
        if(self.lineEditHabID.text() == ""):
            return False
        else:
            return True
        
    def isCliIDValid(self):
        if(self.lineEditDocument.text() == ""):
            return False
        else:
            return True
        
    def isPriceValid(self):
        if(self.lineEditPrice.text() == ""):
            return False
        else:
            return True 
        
    def isDateValid(self):
        isvalid1 = True
        isvalid2 = True
        if(self.timeEditChecking.dateTime() == self.timeEditChecking.minimumDateTime()): isvalid1=False
        if(self.timeEditCheckout.dateTime() == self.timeEditCheckout.minimumDateTime()): isvalid2=True
        return isvalid1 and isvalid2 
        
    def setInf_arq(self, mssg):
        return self.labelInfArq.setText(mssg)
    
    def setInf_hab(self, mssg):
        return self.labelInfHab.setText(mssg)
    
class NewHabRegWindow(GeneralWindow):

    def __init__(self, d_Hab_est, *args, **kwargs):
        data_back = Window_data()
        data_back.path_gui = './ui/new_hab_reg.ui'
        data_back.title_window = "Nuevo registro de estado"
        data_back.has_table = False
        data_back.has_pages = False
        data_back.has_client_section = False

        data_back.has_combo_estados = True
        data_back.extra_combo_estados = None
        data_back.combo_estados_in_arquiler = False
        data_back.combo_estados_in_hab_reg = True

        super().__init__(data_back=data_back,d_Hab_est=d_Hab_est,*args, **kwargs)

        self.set_time_start_now()
        self.set_time_end_now()
        self.timeEditHabRegStart.setCalendarPopup(True)
        self.timeEditHabRegEnd.setCalendarPopup(True)
            
    def clearWindow(self):
        self.lineEditHabRegID.setText("")
        
        self.lineEditHabID.setText("")
        self.label_estado.setText("")
        
        self.set_time_start_now()
        self.set_time_end_now()
        self.comboBoxState.setCurrentIndex(0)

    def getID_hab_reg(self):
        return self.lineEditHabRegID.text()

    def getID_hab(self):
        return self.lineEditHabID.text()
    
    def set_time_start_now(self):
        self.timeEditHabRegStart.setDateTime(QDateTime.currentDateTime())

    def set_time_end_now(self):
        self.timeEditHabRegEnd.setDateTime(QDateTime.currentDateTime())
    
    def clear_time_start_now(self):
        self.timeEditHabRegStart.setDateTime(self.timeEditHabRegStart.minimumDateTime())

    def clear_time_end_now(self):
        self.timeEditHabRegEnd.setDateTime(self.timeEditHabRegEnd.minimumDateTime())
 
    def fillData_hab(self, h: Habitacion, d_Hab_est):
        self.lineEditHabID.setText(h.id)
        last_hab_reg = h.getLastHabReg()
        if(last_hab_reg!=None):
            est = d_Hab_est[last_hab_reg.id_hab_est]
            self.label_estado.setText(str(est.value))
        else:
            self.label_estado.setText("")

    def fillData_hab_reg(self, h: Habitaciones_registro, d_Hab_est):

        if(h.id != None): self.lineEditHabRegID.setText(str(h.id))
        else: self.lineEditHabRegID.setText("")

        if(h.id_hab != None): self.lineEditHabID.setText(str(h.id_hab))
        else: self.lineEditHabID.setText("")

        self.label_estado.setText("-")

        if(h.fechaHoraInicio != None):
            self.timeEditHabRegStart.setDateTime(h.fechaHoraInicio)
        else:
            self.timeEditHabRegStart.setDateTime(self.timeEditHabRegStart.minimumDateTime())
        
        if(h.fechaHoraFin != None):
            self.timeEditHabRegEnd.setDateTime(h.fechaHoraFin)
        else:
            self.timeEditHabRegEnd.setDateTime(self.timeEditHabRegEnd.minimumDateTime())

        if(h.id_hab_est != None): self.comboBoxState.setCurrentText(d_Hab_est[h.id_hab_est].value)
        else: self.comboBoxState.setCurrentText("")

        self.labelInfHabReg.setText("-")
        
    def isDataInFormValid(self):
        return self.isHabIDValid() and self.isDateStartValid() and self.isDateEndValid()
    
    def isHabIDValid(self):
        if(self.lineEditHabID.text() == ""):
            return False
        else:
            return True

    def isDateStartValid(self):
        return True  

    def isDateEndValid(self):
        return True  
        
    def setInf_hab_reg(self, mssg):
        return self.labelInfHabReg.setText(mssg)
    
    def setInf_hab(self, mssg):
        return self.labelInfHab.setText(mssg)
    
    def getHabRegFromForm(self, d_Hab_est, type_op):
        hr = Habitaciones_registro()
        err = 0

        if(type_op == "create" ):
            a = (self.lineEditHabRegID.text() == "")
            b = self.isDataInFormValid()
            if(a and b):
                hr.id = None
            else:
                err=err+1
                CustomDialog("Error","Registro de estado ID debe estar vacio para crear y los demas no.").exec()
            
        elif(type_op == "update"):
            if((self.lineEditHabRegID.text() != "") and self.isDataInFormValid()):
                hr.id = int(self.lineEditHabRegID.text())
            else:
                err=err+1
                CustomDialog("Error","Revise los datos.").exec()
            
        elif(type_op == "search"):
            if(self.lineEditHabRegID.text() != ""):
                hr.id = int(self.lineEditHabRegID.text())
            else:
                err=err+1
                CustomDialog("Error","Registro de estado ID no debe estar vacio para buscar.").exec()

        elif(type_op == "delete"):
            if(self.lineEditHabRegID.text() != ""):
                hr.id = int(self.lineEditHabRegID.text())
            else:
                err=err+1
                CustomDialog("Error","Registro de estado ID no debe estar vacio para eliminar.").exec()

        if(err!=0):
            hr = None
        else:
            hr.id_hab = self.lineEditHabID.text()
            
            if(self.timeEditHabRegStart.dateTime() == self.timeEditHabRegStart.minimumDateTime()): hr.fechaHoraInicio = None
            else: hr.fechaHoraInicio = self.timeEditHabRegStart.dateTime().toPyDateTime()

            if(self.timeEditHabRegEnd.dateTime() == self.timeEditHabRegEnd.minimumDateTime()): hr.fechaHoraFin = None
            else: hr.fechaHoraFin = self.timeEditHabRegEnd.dateTime().toPyDateTime()
            
            est_str = self.comboBoxState.currentText()
            if(est_str==""): hr.id_hab_est = None
            else:
                found = False
                for k in d_Hab_est.keys():
                    if(d_Hab_est[k].value == est_str):
                        hr.id_hab_est = d_Hab_est[k].id
                        found = True

                if(found == False): hr.id_hab_est = None
            
        return hr
    
class ClientWindow(GeneralWindow):

    def __init__(self, data_front: Window_data, data_back: Window_data, table_column_names, cmb_order_by_name: None, *args, **kwargs):
        if(data_back == None): data_back = Window_data()
        data_back.path_gui = './ui/client.ui'
        data_back.title_window = "Clientes"
        data_back.has_table = True
        data_back.has_pages = True
        data_back.page_size = 10
        data_back.has_client_section = True

        data_back.has_combo_estados = False
        data_back.extra_combo_estados = "(Estado no válido)"

        data_back.has_combos_orderby = True
        self.table_column_names = table_column_names
        self.cmb_order_by_name = cmb_order_by_name
        super().__init__(data_back=data_back,data_front=data_front,*args, **kwargs)

    def get_cli_id_selected(self):
        v = self.get_element_selected_text(column=0)
        if(v != None): return int(v)
        else: return None

    def get_cli_doc_selected(self):
        v = self.get_element_selected_text(column=1)
        if(v != None): return v
        else: return None

    def updateUsingWindowDataFront(self):
        super().updateUsingWindowDataFront()
        if(self.data_front.id_cli == None): self.lineEditCliID.setText("")
        else: self.lineEditCliID.setText(str(self.data_front.id_cli))

        if(self.data_front.document == None): self.lineEditDocumento.setText("")
        else: self.lineEditDocumento.setText(str(self.data_front.document))
        
        if(self.data_front.name == None): self.lineEditNombre.setText("")
        else: self.lineEditNombre.setText(str(self.data_front.name))

        if(self.data_front.surname == None): self.lineEditApellido.setText("")
        else: self.lineEditApellido.setText(str(self.data_front.surname))
        
        if(self.data_front.cellphone == None): self.lineEditCelular.setText("")
        else: self.lineEditCelular.setText(str(self.data_front.cellphone))   

    def getWindowDataFront(self):
        super().getWindowDataFront()
        id_cli = self.lineEditCliID.text()
        if(id_cli == ""): id_cli = None
        self.data_front.id_cli = id_cli

        document = self.lineEditDocumento.text()
        if (document == ""): document = None
        self.data_front.document = document

        name = self.lineEditNombre.text()
        if(name == ""): name = None
        self.data_front.name = name

        surname = self.lineEditApellido.text()
        if (surname == ""): surname = None
        self.data_front.surname = surname

        cellphone = self.lineEditCelular.text()
        if(cellphone == ""): cellphone = None
        self.data_front.cellphone = cellphone

        return self.data_front

    def pushFrontDataToBack(self):
        self.getWindowDataFront() #pullgin dataFront from UI
        self.data_back.id_cli = self.data_front.id_cli
        self.data_back.document = self.data_front.document
        self.data_back.name = self.data_front.name
        self.data_back.surname = self.data_front.surname
        self.data_back.cellphone = self.data_front.cellphone
        super().pushFrontDataToBack()
    
    def updateTableView(self, d_Clientes: dict[str, Cliente]):

        self.resetTableView()

        n_row = len(d_Clientes)
        n_col = len (self.table_column_names.values())

        self.tableContent.setColumnCount(n_col)
        self.tableContent.setRowCount(n_row)
        self.tableContent.setStyleSheet("QTableWidget::item { padding: 10px }")

        for i,key in enumerate(d_Clientes.keys()):
            header_item = QtWidgets.QTableWidgetItem(str(i+1))
            self.tableContent.setVerticalHeaderItem(i, header_item)

        for j,name in enumerate(self.table_column_names.values()):
            self.tableContent.setHorizontalHeaderItem(j,QtWidgets.QTableWidgetItem(name))

        for i,key in enumerate(d_Clientes.keys()):
            for j,col_name in enumerate(self.table_column_names.values()):

                var_raw = d_Clientes[key].getTableElementByPos(j)
                if(var_raw==None):
                    var = "-"
                elif("Ultimo cambio" == col_name):
                    var = QtCore.QDateTime.fromString(var_raw, "yyyy-MM-dd hh:mm:ss")
                    #print(var_raw)
                else:
                    var = var_raw

                element = QtWidgets.QTableWidgetItem()
                element.setData(Qt.ItemDataRole.DisplayRole, var)
                element.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableContent.setItem(i, j, element)
        self.tableContent.resizeColumnsToContents()

        self.setTableViewPost()

class HabRegWindow(GeneralWindow):

    def __init__(self, data_front: Window_data, data_back: Window_data, d_Hab_est, table_column_names, cmb_order_by_name: None, *args, **kwargs):
        if(data_back==None): data_back = Window_data()
        data_back.path_gui = './ui/hab_reg.ui'
        data_back.title_window = "Registros de habitación"
        data_back.has_table = True
        data_back.has_pages = True
        data_back.page_size = 10
        data_back.has_client_section = False

        data_back.has_combo_estados = True
        data_back.extra_combo_estados = ""
        data_back.combo_estados_in_arquiler = False
        data_back.combo_estados_in_hab_reg = True

        data_back.has_combos_orderby = True
        self.table_column_names = table_column_names
        self.cmb_order_by_name = cmb_order_by_name
        super().__init__(data_back=data_back,d_Hab_est=d_Hab_est,data_front=data_front,*args, **kwargs)

        self.dateEditStart.setCalendarPopup(True)

    def get_hab_reg_id_selected(self):
        v = self.get_element_selected_text(column=0)
        if(v != None): return int(v)
        else: return None

    def updateUsingWindowDataFront(self):
        super().updateUsingWindowDataFront()
        if(self.data_front.id_hab_reg == None): self.lineEditID.setText("")
        else: self.lineEditID.setText(str(self.data_front.id_hab_reg))

        if(self.data_front.fecha_inicio == None): self.clear_time_start_now()
        else: self.dateEditStart.setDateTime(self.data_front.fecha_inicio)

        if(self.data_front.id_hab == None): self.lineEditHabID.setText("")
        else: self.lineEditHabID.setText(str(self.data_front.id_hab))

        if(self.data_front.hab_est == None): self.comboBoxState.setCurrentText("")
        else: self.comboBoxState.setCurrentText(str(self.data_front.hab_est))


    def getWindowDataFront(self):
        super().getWindowDataFront()
        id_hab_reg = self.lineEditID.text()
        if(id_hab_reg == ""): id_hab_reg = None
        self.data_front.id_hab_reg = id_hab_reg

        fecha_inicio = self.dateEditStart.dateTime()
        if(fecha_inicio == self.dateEditStart.minimumDateTime()): fecha_inicio = None
        self.data_front.fecha_inicio = fecha_inicio

        id_hab = self.lineEditHabID.text()
        if (id_hab == ""): id_hab = None
        self.data_front.id_hab = id_hab
        
        hab_est = self.comboBoxState.currentText()
        if(hab_est == ""): hab_est = None
        self.data_front.hab_est = hab_est

        return self.data_front

    def pushFrontDataToBack(self):
        self.getWindowDataFront() #pullgin dataFront from UI
        self.data_back.id_hab = self.data_front.id_hab
        self.data_back.fecha_inicio = self.data_front.fecha_inicio
        self.data_back.id_hab_reg = self.data_front.id_hab_reg
        self.data_back.hab_est = self.data_front.hab_est
        self.data_back.id_hab_est = self.data_front.id_hab_est
        super().pushFrontDataToBack()

    def set_time_start_now(self):
        self.dateEditStart.setDateTime(QDateTime.currentDateTime())

    def clear_time_start_now(self):
        self.dateEditStart.setDateTime(self.dateEditStart.minimumDateTime())
 
    def updateTableView(self, d_Hab_Reg: dict[str, Habitaciones_registro], d_Hab_est):
        #self.resetTableView()

        n_row = len(d_Hab_Reg)
        n_col = len (self.table_column_names.values())

        self.tableContent.setColumnCount(n_col)
        self.tableContent.setRowCount(n_row)
        self.tableContent.setStyleSheet("QTableWidget::item { padding: 10px }")

        for i,key in enumerate(d_Hab_Reg.keys()):
            header_item = QtWidgets.QTableWidgetItem(str(i+1))
            self.tableContent.setVerticalHeaderItem(i, header_item)

        for j,name in enumerate(self.table_column_names.values()):
            self.tableContent.setHorizontalHeaderItem(j,QtWidgets.QTableWidgetItem(name))

        for i,key in enumerate(d_Hab_Reg.keys()):
            for j,col_name in enumerate(self.table_column_names.values()):

                element = None
                var_raw = d_Hab_Reg[key].getTableElementByPos(j, d_Hab_est)
                if(var_raw==None):
                    var = "-"
                elif("F/h Inicio" == col_name or "F/h Fin" == col_name or "Ultimo cambio" == col_name):
                    var = QtCore.QDateTime.fromString(var_raw, "yyyy-MM-dd hh:mm:ss")
                else: 
                    var = var_raw

                element = QtWidgets.QTableWidgetItem()
                element.setData(Qt.ItemDataRole.DisplayRole, var)
                element.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableContent.setItem(i, j, element)
        self.tableContent.resizeColumnsToContents()

        self.setTableViewPost()

class NewClientWindow(GeneralWindow):
    
    def __init__(self, *args, **kwargs):
        data_back = Window_data()
        data_back.path_gui = './ui/new_client.ui'
        data_back.title_window = "Nuevo cliente"
        data_back.has_table = False
        data_back.has_pages = False
        data_back.has_client_section = True

        data_back.has_combo_estados = False
        data_back.extra_combo_estados = None

        super().__init__(data_back=data_back,*args, **kwargs)
            
    def clearWindow(self):
        self.lineEditDocument.setText("")
        
        self.lineEditName.setText("")
        self.lineEditLastName.setText("")
        
        self.lineEditCellphone.setText("")
        self.lineEditAdditionalData.setText("")
        self.labelInfClient.setText("-")
            
class NewClientFunctions():
    def fillData(self, widg, c: Cliente):
        if(c.nDocumento != None): widg.lineEditDocument.setText(c.nDocumento)
        else: widg.lineEditDocument.setText("")

        if(c.nDocumento != None): widg.lineEditName.setText(c.nombre)
        else: widg.lineEditName.setText("")

        if(c.nDocumento != None): widg.lineEditLastName.setText(c.apellido)
        else: widg.lineEditLastName.setText("")
        
        if(c.nDocumento != None): widg.lineEditCellphone.setText(c.celular)
        else: widg.lineEditCellphone.setText("")
        
        if(c.nDocumento != None): widg.lineEditAdditionalData.setText(c.datosAdicionales)
        else: widg.lineEditAdditionalData.setText("")

    def clearLineData(self, widg):
        widg.lineEditName.setText("")
        widg.lineEditLastName.setText("")
        widg.lineEditCellphone.setText("") 
        widg.lineEditAdditionalData.setText("")

    def getDocumentFromForm(self, widg):
        s = None
        if(not widg.isDocEmpty_cli()):
            s = str(widg.lineEditDocument.text())
        else:
            CustomDialog("Error","Documento no pueda estar vacio").exec()
        return s
    
    def getClientFromForm(self, widg):
        c = Cliente()
        if(not widg.isDocEmpty_cli()):
            c.nDocumento = widg.lineEditDocument.text()
            c.nombre = widg.lineEditName.text()
            c.apellido = widg.lineEditLastName.text()
            c.celular = widg.lineEditCellphone.text()
            c.datosAdicionales = widg.lineEditAdditionalData.toPlainText()
        else:
            c = None
            CustomDialog("Error","Documento no pueda estar vacio").exec()
        return c
    
    def isDocEmpty(self, widg):
        if(widg.lineEditDocument.text() == ""):
            return True
        else:
            return False
        
    def setInf(self, widg, mssg):
        widg.labelInfClient.setText(mssg)
           
class CustomDialog(QDialog):
    def __init__(self, t, m):
        super().__init__()

        self.setWindowTitle(t)
        icon = QtGui.QIcon("./src/logoHGP.png")
        self.setWindowIcon(icon)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(m)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    

class TestWindow(QtWidgets.QWidget):
    arq_ui = None
    client_ui = None
    subWindowRef = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle("Test")
        icon = QtGui.QIcon("./src/logoHGP.png")
        self.setWindowIcon(icon)

        self.arq_ui = ArqWindow()
        self.client_ui = ClientWindow()

        layout = QHBoxLayout()
        # Add widgets to the layout
        layout.addWidget(self.arq_ui)
        layout.addWidget(QPushButton("Center"))
        layout.addWidget(self.client_ui)

        self.setLayout(layout)

    def show_visual(self, focus = True):
        self.show()
        #self.showNormal()
        #self.setVisible(True)
        if focus: self.setFocus()
        #self.activateWindow()
        #self.raise_()
        #self.blockSignals(False)


    QTableWidget.style
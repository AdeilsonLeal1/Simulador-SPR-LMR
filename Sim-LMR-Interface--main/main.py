from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox
from Sim_LMR_interface import Ui_Widget
from numpy import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.patches import Polygon, Rectangle, Circle, Arrow

import icons_
import sys
import matplotlib.pyplot as plt
import time
import save_table


COUPLING, INTERROGATION_MODE, SIMULATOR, TYPE_FIBER= 0, 0, '', 0
STEP = 0    # Also make the adjustment in the 'self.reflectance_AIM()' or 'self.reflectance_WIM()' when necessary

class MainWindow(QWidget, Ui_Widget):
    def __init__(self):
        ## Variables
        self.nLayers = 0 # Number of layers
        self.layers = list() # Layer list
        self.d = list () # Thickness of layers 
        self.material = list()  # List with the materials of each layer
        self.material_id = list()  # List with the materials id of each layer
        self.indexRef = list()  # List with refractive index of each layer
        self.index_ref_analyte = list()  # List with analyte refraction indices for graph plotting
        self.critical_point = list()     # threshold angle for Attenuated Total Reflection
        self.Reflectance_ = list()     # List with reflectance values for plotting multiple curves
        self.Resonance_Point = list()  # Resonance angle or resonance wavelength
        self.sensibility = list()  # List with Sensibility values
        self.Rmin = list()   # List of minimum reflectance values
        self.Fwhm = list()   # List with FWHM values
        self.ax_x = list()
        self.simbols = tuple()
        self.init = 0
        self.final = 0

        self.fom = list()   # Lists with the QF 
        self.da = list()   # Lists with the DA 

        ## Window initialization parameters
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowIcon(QtGui.QIcon('icons/LOGO.png'))
        self.setWindowTitle("Simulation")
        self.showMaximized()

        # Startup for graphics display
        self.figure_ = plt.figure(dpi=250)
        self.canvas_ = FigureCanvas(self.figure_)
        self.toolbar_ = NavigationToolbar2QT(self.canvas_, self)
        self.layout_graphs.addWidget(self.canvas_)
        self.verticalLayout_12.addWidget(self.toolbar_)

        ## APP EVENTS
        ########################################################################
        # Initialization of screens
        self.Stacked_windows.setCurrentIndex(0)
        self.stacked_layers.setCurrentIndex(1)
        self.Stacked_config_mode.setCurrentIndex(1)

        self.btn_close.clicked.connect(self.close)    # close window
        self.btn_minimize.clicked.connect(
            self.showMinimized)    # minimize window
        self.exit_btn.clicked.connect(self.close)    # close window
        self.start_btn.clicked.connect(lambda: self.Stacked_windows.setCurrentWidget(
            self.Select_simulator))    # show 'Select Simulator' window
        
        self.open_btn_ext.clicked.connect(self.open_from_extern_file)

        # return to 'home' window
        self.btn_home.clicked.connect(self.go_to_home)
        self.btn_home_2.clicked.connect(self.go_to_home)
        self.btn_home_3.clicked.connect(self.go_to_home)
        self.btn_home_4.clicked.connect(self.go_to_home)
        self.btn_home_5.clicked.connect(self.go_to_home)
        self.btn_home_6.clicked.connect(self.go_to_home)
        self.btn_home_7.clicked.connect(self.go_to_home)
        self.prev_btn_sel.clicked.connect(self.previous_page)

        # return to 'coupling' page
        self.btn_coupling.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))
        self.btn_coupling_2.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))
        self.btn_coupling_3.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))
        self.btn_coupling_4.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))
        self.btn_coupling_5.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))
        self.btn_coupling_6.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))

        # return to 'interrogation mode' page
        self.btn_interrogation.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.interrogation_window))
        self.btn_interrogation_2.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.interrogation_window))
        self.btn_interrogation_3.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.interrogation_window))

        # return to 'setting layers' page
        self.btn_setting_layers.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.layers_window))
        self.btn_setting_layers_2.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.layers_window))
        
        # return to 'Type of Fiber' page
        self.btn_fiber_type_2.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.select_fiber_window))

        # 'Select simulator' page buttons
        self.spr_btn.clicked.connect(self.spr_selected)
        self.lmr_btn.clicked.connect(self.lmr_selected)
        self.lmr_spr_btn.clicked.connect(self.lmr_spr_selected)

        # 'Coupling' page buttons
        self.prism_btn.clicked.connect(self.prism_btn_clicked)
        self.fiber_btn.clicked.connect(self.fiber_btn_clicked)
        self.prev_btn_coup.clicked.connect(self.previous_page)
        self.next_btn_coup.clicked.connect(
            lambda: self.next_page(op=COUPLING, warning=self.warning_2))
        
        # 'Select fiber' page buttons
        self.cladding_remove_btn.clicked.connect(self.fiber_cr_clicked)
        self.prev_btn_fiber_typ.clicked.connect(self.previous_page)
        self.next_btn_fiber_typ.clicked.connect(
            lambda: self.next_page(op=TYPE_FIBER, warning=self.warning_fiber_typ))
        
        # 'Characteristics Fiber' page buttons
        self.prev_btn_char_fib.clicked.connect(self.previous_page)
        self.next_btn_char_fib.clicked.connect(lambda: self.next_page(op=1, warning=self.label_4))

        # 'Interrogation mode' page buttons
        self.aim_btn.clicked.connect(self.aim_btn_clicked)
        self.wim_btn.clicked.connect(self.wim_btn_clicked)
        self.prev_btn_inter.clicked.connect(self.previous_page)
        self.next_btn_inter.clicked.connect(lambda: self.next_page(
            op=INTERROGATION_MODE, warning=self.warning_inter))
        
        # 'Setting layers' page buttons 
        self.prev_btn_config_layers.clicked.connect(self.previous_page)
        self.next_btn_config_layers.clicked.connect(lambda: self.next_page(
            op=INTERROGATION_MODE, warning=self.label_warning))

        ## Method that updates the incidence wavelength in AIM mode
        self.lambda_i_slider.valueChanged.connect(lambda: self.change_spinbox(self.lambda_i, self.lambda_i_slider))   
        self.lambda_i.valueChanged.connect(lambda: self.change_slider(self.lambda_i, self.lambda_i_slider))

        ## 'Characteristics of Fiber' page buttons
        self.custom_btn.toggled.connect(self.enable_gb_coef_sellmeier)

        ## Enable insertion of new layers
        self.btn_new_layer.clicked.connect(self.set_Enable_True)
        self.btn_new_layer.clicked.connect(self.set_Enable_True_2)
        self.btn_new_layer.clicked.connect(lambda: self.set_RefractiveIndex(self.cbox_material.currentIndex(), self.lambda_i.value()*1E-9))   
        self.btn_add_analyte.clicked.connect(self.set_Enable_False)
        self.btn_add_layer.clicked.connect(self.set_Enable_False_2)
        self.cbox_material.currentIndexChanged.connect(lambda: self.set_RefractiveIndex(self.cbox_material.currentIndex(), self.lambda_i.value()*1E-9))
        self.lambda_i_slider.valueChanged.connect(lambda: self.set_RefractiveIndex(self.cbox_material.currentIndex(), self.lambda_i.value()*1E-9))
        self.lambda_i.valueChanged.connect(lambda: self.set_RefractiveIndex(self.cbox_material.currentIndex(), self.lambda_i.value()*1E-9))
    
        self.btn_new_layer_2.clicked.connect(self.set_Enable_True)
        self.btn_new_layer_2.clicked.connect(self.set_Enable_True_2)  
        self.btn_add_analyte_2.clicked.connect(self.set_Enable_False)
        self.btn_add_layer_2.clicked.connect(self.set_Enable_False_2)
        
        ## Add new layers
        self.btn_add_layer.clicked.connect(self.add_layers)
        self.btn_add_analyte.clicked.connect(self.add_analyte)
        self.btn_add_layer_2.clicked.connect(self.add_layers)
        self.btn_add_analyte_2.clicked.connect(self.add_analyte)
    
        # Geometry settings page buttons 
        self.prev_btn_config_mode.clicked.connect(self.previous_page)
        self.btn_edit_layers_3.clicked.connect(lambda: self.Stacked_windows.setCurrentWidget(self.layers_window))
        
        ## Method that updates the angle of incidence value in WIM mode
        self.angle_Slider.valueChanged.connect(lambda: self.change_spinbox(self.angle_incidence, self.angle_Slider))   
        self.angle_incidence.valueChanged.connect(lambda: self.change_slider(self.angle_incidence, self.angle_Slider))

        ## Method that updates the incidence wavelength range in WIM mode
        self.wavelength_range.valueChanged.connect(lambda: self.change_range_spin(self.a1_2, self.a2_2, self.wavelength_range))
        self.a1_2.valueChanged.connect(lambda: self.change_range_slider2(self.a1_2, self.a2_2, self.wavelength_range, self.warning_range))
        self.a2_2.valueChanged.connect(lambda: self.change_range_slider(self.a1_2, self.a2_2, self.wavelength_range, self.warning_range))

        ## Method that updates the incident angle range in AIM mode
        self.angular_range.valueChanged.connect(lambda: self.change_range_spin(self.a1_3, self.a2_3, self.angular_range))
        self.a1_3.valueChanged.connect(lambda: self.change_range_slider2(self.a1_3, self.a2_3, self.angular_range, self.warning_angular))
        self.a2_3.valueChanged.connect(lambda: self.change_range_slider(self.a1_3, self.a2_3, self.angular_range, self.warning_angular))

        ## Methods for displaying charts
        self.btn_run.clicked.connect(self.start_simulation)
        self.select_graphs.currentIndexChanged.connect(self.show_graphs)
        self.TM_polarization.setChecked(True)
    
        ## Remove and edit table
        self.btn_remove_layers.clicked.connect(self.remove_layers)
        self.btn_edit_layers.clicked.connect(self.select_edit_layer)
        
        self.btn_confirm_edit.clicked.connect(self.edit_layer)
        self.btn_confirm_edit.clicked.connect(self.set_Enable_False_2)
        
        self.btn_confirm_edit_3.clicked.connect(self.edit_layer)
        self.btn_confirm_edit_3.clicked.connect(self.set_Enable_False_2)
        
        self.btn_confirm_edit_2.clicked.connect(self.edit_analyte)
        self.btn_confirm_edit_2.clicked.connect(self.set_Enable_False)
        
        self.btn_confirm_edit_4.clicked.connect(self.edit_analyte)
        self.btn_confirm_edit_4.clicked.connect(self.set_Enable_False)

        self.btn_save_table.clicked.connect(self.save_table)
        self.btn_export_data.clicked.connect(self.export_data)

        self.btn_new_simulation.clicked.connect(self.go_to_home)

    # APP FUNCTIONS 

    def go_to_home(self):
        self.Stacked_windows.setCurrentWidget(self.home_window)
        global SIMULATOR
        SIMULATOR = ''
        self.label_title.setText(QtCore.QCoreApplication.translate(
            "Widget", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Simulator</span></p></body></html>", None))
        self.label_footer.setText(QtCore.QCoreApplication.translate(
            "Widget", u"<html><head/><body><p align=\"center\"> </p></body></html>", None))

    def spr_selected(self):
        self.Stacked_windows.setCurrentWidget(self.coupling_window)
        self.fiber_btn.setEnabled(True)
        self.fiber_btn.setStyleSheet("QPushButton{ background-color: rgb(255, 255, 255);\n"
                                     "border-color: rgb(31, 78, 121);\n"
                                     "border-radius: 30px;\n"
                                     "border-style: outset;\n"
                                     "border-width: 7px;\n"
                                     "}\n"
                                     "QPushButton:hover{ border-color: rgb(255, 170, 0);}\n"
                                     "\n"
                                     "QPushButton:checked{ border-color: rgb(0, 170, 0);}")
        global SIMULATOR
        SIMULATOR = 'SPR'
        self.label_title.setText(QtCore.QCoreApplication.translate(
            "Widget", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Sim-SPR</span></p></body></html>", None))
        self.label_footer.setText(QtCore.QCoreApplication.translate(
            "Widget", u"<html><head/><body><p align=\"center\">Sim-SPR v01.0_a</p></body></html>", None))
    
    def lmr_selected(self):
        self.Stacked_windows.setCurrentWidget(self.coupling_window)
        self.fiber_btn.setEnabled(False)
        self.fiber_btn.setStyleSheet("QPushButton{ background-color: rgb(255, 255, 255);\n"
                                     "border-color: #606060;\n"
                                     "border-radius: 30px;\n"
                                     "border-style: outset;\n"
                                     "border-width: 7px;\n"
                                     "}\n"
                                     "QPushButton:hover{ border-color: rgb(255, 170, 0);}\n"
                                     "\n"
                                     "QPushButton:checked{ border-color: rgb(0, 170, 0);}")
        global SIMULATOR
        SIMULATOR = 'LMR'
        self.label_title.setText(QtCore.QCoreApplication.translate(
            "Widget", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Sim-LMR</span></p></body></html>", None))
        self.label_footer.setText(QtCore.QCoreApplication.translate(
            "Widget", u"<html><head/><body><p align=\"center\">Sim-LMR v01.0_a</p></body></html>", None))

    def lmr_spr_selected(self):
        
        global SIMULATOR
        SIMULATOR = 'LMR+SPR'
        self.label_title.setText(QtCore.QCoreApplication.translate(
            "Widget", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Sim-LMR+SPR</span></p></body></html>", None))
        self.label_footer.setText(QtCore.QCoreApplication.translate(
            "Widget", u"<html><head/><body><p align=\"center\">Sim-LMR+SPR v01.0_a</p></body></html>", None))

    def prism_btn_clicked(self):
        self.warning_2.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\">- Coupling through Prism selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\">Next to continue...</span></pre></body></html>"))
        global COUPLING
        COUPLING = 1
        
    def fiber_btn_clicked(self):
        self.warning_2.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#37eb00;\">- Coupling through Optical Fiber selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\">Next to continue...</span></pre></body></html>"))
        global COUPLING
        COUPLING = 2

    def fiber_cr_clicked(self):
        self.warning_fiber_typ.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#37eb00;\">- Fiber with removed cladding was selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\">Next to continue...</span></pre></body></html>"))
        global TYPE_FIBER
        TYPE_FIBER = 1

    def enable_gb_coef_sellmeier(self):
        if self.custom_btn.isChecked():
            self.coef_sellmeier_gb.setToolTip("Fill in the coefficients")
            self.coef_sellmeier_gb.setStyleSheet(u"/*{font: 14pt \"Ubuntu\";\n"
                                                "color: rgb(255, 255, 255);\n"
                                                "	background-color: rgba(255, 255, 255,20);\n"
                                                "}*/\n"
                                                "\n"
                                                "QGroupBox  {\n"
                                                "	background-color: rgba(255, 255, 255,70);\n"
                                                "	font: 14pt \"Ubuntu\";\n"
                                                "    border: 2px solid;\n"
                                                "    border-color: #FF17365D;\n"
                                                "    margin-top: 25px;\n"
                                                "    border-bottom-left-radius: 20px;\n"
                                                "	border-bottom-right-radius: 20px;\n"
                                                "}\n"
                                                "\n"
                                                "QGroupBox::title  {\n"
                                                "    subcontrol-origin: margin;\n"
                                                "    subcontrol-position: top center;\n"
                                                "    padding: 5px 8000px 5px 8000px;\n"
                                                "    background-color: #FF17365D;\n"
                                                "    color: rgb(255, 255, 255);\n"
                                                "}\n"
                                            "QLineEdit{\n"
                                                "padding: 1px 18px 1px 3px;\n"
                                                "color: rgb(10, 25, 90);\n"
                                                "font: 700 12pt \"Ubuntu\";\n"
                                                " border: 2px solid;\n"
                                                "border-color: #FF17365D;\n"
                                                "background-color: rgba(255, 255, 255,210);\n"
                                                "border-radius:8px;\n"
                                            "}"
                                                "QToolTip { "
                                                "background-color: black; "
                                                "color: white; "
                                                "border: black solid 1px"
                                                "}")
            
            self.coef_sellmeier_gb.setEnabled(True)

            self.btn_add_coef.setStyleSheet(u"QPushButton{\n"
                                            "	font: 400 11pt \"Ubuntu\";\n"
                                            "	color: rgb(255, 255,255);\n"
                                            "	background-color: rgb(0, 130, 180);\n"
                                            "	border-color: rgb(0, 100, 130);\n"
                                            "	border-width: 2px;\n"
                                            "	border-radius:8px;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "	background-color: rgb(00, 140, 70);\n"
                                            "	border-color: rgb(0, 120, 40);\n"
                                            "	width: 40;\n"
                                            "	height: 35;\n"
                                            "}")
        else:
            self.coef_sellmeier_gb.setToolTip("Click in 'Custom' radio button to enable")
            self.coef_sellmeier_gb.setStyleSheet(u"/*{font: 14pt \"Ubuntu\";\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "	background-color: rgba(255, 255, 255,20);\n"
                                            "}*/\n"
                                            "\n"
                                            "QGroupBox  {\n"
                                            "	background-color: rgba(255, 255, 255,70);\n"
                                            "	font: 14pt \"Ubuntu\";\n"
                                            "    border: 2px solid;\n"
                                            "    border-color: #606060;\n"
                                            "    margin-top: 25px;\n"
                                            "    border-bottom-left-radius: 20px;\n"
                                            "	border-bottom-right-radius: 20px;\n"
                                            "}\n"
                                            "\n"
                                            "QGroupBox::title  {\n"
                                            "    subcontrol-origin: margin;\n"
                                            "    subcontrol-position: top center;\n"
                                            "    padding: 5px 8000px 5px 8000px;\n"
                                            "    background-color: #606060;\n"
                                            "    color: rgb(255, 255, 255);\n"
                                            "}\n"
                                            "\n"
                                            "QLineEdit{\n"
                                            "padding: 1px 18px 1px 3px;\n"
                                            "color: rgb(10, 25, 90);\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            " border: 2px solid;\n"
                                            "border-color: #606060;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:8px;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton{\n"
                                            "	font: 400 11pt \"Ubuntu\";\n"
                                            "	color: rgb(255, 255,255);\n"
                                            "	background-color: #606060;\n"
                                            "	border-color: rgb(0, 100, 130);\n"
                                            "	border-width: 2px;\n"
                                            "	borde"
                                                                    "r-radius:8px;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "	background-color: rgb(00, 140, 70);\n"
                                            "	border-color: rgb(0, 120, 40);\n"
                                            "	width: 40;\n"
                                            "	height: 35;\n}"
                                            "QToolTip { "
                                            "background-color: black; "
                                            "color: white; "
                                            "border: black solid 1px"
                                            "}")
        
            self.coef_sellmeier_gb.setEnabled(False)

    def next_page(self, op, warning):
        match self.Stacked_windows.currentWidget():
            case self.coupling_window:
                if op == 0:
                    warning.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#B21222;\">- *! Select a valid option !* - </span></pre></body></html>"))
                elif op == 1:   # Coupling througth prism
                    self.Stacked_windows.setCurrentWidget(self.interrogation_window)
                else:           # Coupling througth optical fiber
                    self.Stacked_windows.setCurrentWidget(self.select_fiber_window)
            
            case self.interrogation_window:
                self.warning.setHidden(True)  
                self.figure_.clear()
                self.canvas_.draw()  
                if op == 0:
                    warning.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#B21222;\">- *! Select a valid option !* - </span></pre></body></html>"))
                elif op == 1:   # AIM mode
                    self.Stacked_windows.setCurrentWidget(self.layers_window) 
                    self.stacked_layers.setCurrentWidget(self.page_layers_aim)
                    self.Stacked_config_mode.setCurrentWidget(self.page_AIM_config)
                    self.btn_config_range.setText("Configure AIM mode")
                    self.textBrowser_2.setText("You have already selected PRISM coupling and ANGULAR INTERROGATION MODE."
                                    "\n\nTo continue your simulation:\n"
                                    "\n\t* Enter the operating wavelength in your simulation, in the 'Incident wavelength' field;"
                                    "\n\t* Add at least 3 layers to build your sensor structure;"
                                    "\n\t* In the 'Layers' field, add optical substrate layers, thin films and adhesion layers;"
                                    "\n\t* Don't forget to add the analyte analysis range, in the 'Analyte refractive " "index range' field."
                                    "\n\nIn the table below you can see the added layers.")
                    self.textBrowser.setText("Select the analysis angular range in the 'Angular range' field;"
                                            "\nClick the 'Run' button to start the calculations;"
                                            "\nYou can choose which chart to view in the combobox below the chart area;")
                else:           # WIM mode
                    self.Stacked_windows.setCurrentWidget(self.layers_window) 
                    self.stacked_layers.setCurrentWidget(self.page_layers_wim)
                    self.Stacked_config_mode.setCurrentWidget(self.page_WIM_config)
                    self.btn_config_range.setText("Configure WIM mode")
                    self.textBrowser_2.setText("You have already selected PRISM coupling and WAVELENGTH INTERROGATION MODE."
                                    "\n\nTo continue your simulation:\n"
                                    "\n\t* Add at least 3 layers to build your sensor structure;"
                                    "\n\t* In the 'Layers' field, add optical substrate layers, thin films and adhesion layers;"
                                    "\n\t* Don't forget to add the analyte analysis range, in the 'Analyte refractive " "index range' field."
                                    "\n\nIn the table below you can see the added layers.")
                    self.textBrowser.setText("Select the wavelength range of the analysis in the 'Spectral range' field   and add the incidence angle in the 'Incidence angle' field;"
                                            "\nClick the 'Run' button to start the calculations;"
                                            "\nYou can choose which chart to view in the combobox below the chart area.")
            
            case self.layers_window:
                if self.nLayers < 3:
                    self.warning.setHidden(False)
                    self.warning.setText(QtCore.QCoreApplication.translate("Widget", f"<html><head/><body><p align=\"center\"><a name=\"tw-target-text\"/><span style=\" font-size:14pt; font-weight:400; color:#d41010;\"># Insert more than 3 layers #</span><p align=\"center\"><span style=\" font-size:14pt; font-weight:400; color:#d41010;\"># {self.nLayers} layer(s) added # </span></body></html>", None))
                else:
                    self.Stacked_windows.setCurrentWidget(self.interval_setting)
            
            case self.select_fiber_window:
                if op == 0:
                    warning.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#B21222;\">- *! Select a valid option !* - </span></pre></body></html>"))
                else:           
                    self.Stacked_windows.setCurrentWidget(self.characteristics_fiber)
            case self.characteristics_fiber:
                ## Falta colocar os casos de exceção que causam erro
                self.Stacked_windows.setCurrentWidget(self.layers_window)
                

    def previous_page(self):
        match self.Stacked_windows.currentWidget():
            case self.Select_simulator:
                self.Stacked_windows.setCurrentWidget(self.home_window)

            case self.coupling_window:
                self.Stacked_windows.setCurrentWidget(self.Select_simulator)

            case self.interrogation_window:
                self.Stacked_windows.setCurrentWidget(self.coupling_window)   
                
            case self.layers_window:
                if COUPLING == 1:
                    self.Stacked_windows.setCurrentWidget(self.interrogation_window)
                else:
                    self.Stacked_windows.setCurrentWidget(self.characteristics_fiber)
            
            case self.select_fiber_window:
                self.Stacked_windows.setCurrentWidget(self.coupling_window)
            
            case self.interval_setting:
                self.Stacked_windows.setCurrentWidget(self.layers_window)
            
            case self.characteristics_fiber:
                self.Stacked_windows.setCurrentWidget(self.select_fiber_window)

    def aim_btn_clicked(self):
        global INTERROGATION_MODE
        self.warning_inter.setText(QtCore.QCoreApplication.translate(
            "Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#37eb00;\">- Angular interrogation mode selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\">Next to continue...</span></pre></body></html>"))
        INTERROGATION_MODE = 1

    def wim_btn_clicked(self):
        global INTERROGATION_MODE
        self.warning_inter.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#37eb00;\">- Wavelength interrogation mode selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\">Next to continue...</span></pre></body></html>"))
        INTERROGATION_MODE = 2

    def set_Enable_True(self):
        # This enable the btn_add_layer button (AIM mode)
        self.btn_add_layer.setEnabled(True)
        self.btn_add_layer.setToolTip("Add layer")
        self.btn_add_layer.setStyleSheet(u"QPushButton{\n"
                                           "	font: 400 11pt \"Ubuntu\";\n"
                                           "	color: rgb(255, 255,255);\n"
                                           "	background-color: rgb(0, 130, 180);\n"
                                           "	border-color: rgb(0, 100, 130);\n"
                                           "	border-width: 2px;\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	background-color: rgb(00, 140, 70);\n"
                                           "	border-color: rgb(0, 120, 40);\n"
                                           "	width: 40;\n"
                                           "	height: 35;\n"
                                           "}")
        
        # This enable the cbox_material field (AIM mode)
        self.cbox_material.setEnabled(True)
        self.cbox_material.setStyleSheet(u"QComboBox::drop-down {\n"
                                         "    width: 25;\n"
                                         "    border-left-width: 1px;\n"
                                         "    border-left-color: darkgray;\n"
                                         "    border-left-style: solid; /* just a single line */\n"
                                         "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                         "    border-bottom-right-radius: 3px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox\n"
                                         "{\n"
                                         " padding: 1px 18px 1px 3px;\n"
                                         "color: rgb(10, 25, 90);\n"
                                         "font: 700 12pt \"Ubuntu\";\n"
                                         "border: 2px solid;\n"
                                         "border-color: #FF17365D;\n"
                                         "background-color: rgba(255, 255, 255,210);\n"
                                         "border-radius:10px;\n"
                                         "}\n"
                                         "QComboBox::down-arrow { /* shift the arrow when popup is open */\n"
                                         "    top: 1px;\n"
                                         "	image: url(:/icons/icons/arrow-down.png);\n"
                                         "    left: 1px;\n"
                                         "}")
        self.thickness.setEnabled(True)
        self.thickness.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
        
        self.real_part_index.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
        self.imaginary_part_index.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")

        self.description.setEnabled(True)
        self.description.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
        self.description_3.setEnabled(True)

        # This enable the btn_add_layer_2 button (WIM mode)
        self.btn_add_layer_2.setEnabled(True)
        self.btn_add_layer_2.setToolTip("Add layer")
        self.btn_add_layer_2.setStyleSheet(u"QPushButton{\n"
                                           "	font: 400 11pt \"Ubuntu\";\n"
                                           "	color: rgb(255, 255,255);\n"
                                           "	background-color: rgb(0, 130, 180);\n"
                                           "	border-color: rgb(0, 100, 130);\n"
                                           "	border-width: 2px;\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	background-color: rgb(00, 140, 70);\n"
                                           "	border-color: rgb(0, 120, 40);\n"
                                           "	width: 40;\n"
                                           "	height: 35;\n"
                                           "}")
        
        # This enable the cbox_material_2 field (WIM mode)
        self.cbox_material_2.setEnabled(True)
        self.cbox_material_2.setStyleSheet(u"QComboBox::drop-down {\n"
                                         "    width: 25;\n"
                                         "    border-left-width: 1px;\n"
                                         "    border-left-color: darkgray;\n"
                                         "    border-left-style: solid; /* just a single line */\n"
                                         "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                         "    border-bottom-right-radius: 3px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox\n"
                                         "{\n"
                                         " padding: 1px 18px 1px 3px;\n"
                                         "color: rgb(10, 25, 90);\n"
                                         "font: 700 12pt \"Ubuntu\";\n"
                                         "border: 2px solid;\n"
                                         "border-color: #FF17365D;\n"
                                         "background-color: rgba(255, 255, 255,210);\n"
                                         "border-radius:10px;\n"
                                         "}\n"
                                         "QComboBox::down-arrow { /* shift the arrow when popup is open */\n"
                                         "    top: 1px;\n"
                                         "	image: url(:/icons/icons/arrow-down.png);\n"
                                         "    left: 1px;\n"
                                         "}")
        self.thickness_2.setEnabled(True)
        self.thickness_2.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
       
        self.description_2.setEnabled(True)
        self.description_2.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
        
        self.warning.setHidden(True)
        
    def set_Enable_True_2(self):
        # This enable the gb_analyte field (AIM mode)
        self.gb_analyte.setEnabled(True)
        self.gb_analyte.setToolTip("Analyte refractive index range")

        self.description_3.setEnabled(True)
        self.description_3.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
        
        self.thickness_4.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
        self.thickness_3.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
        
        self.description_4.setEnabled(True)
        self.description_4.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
              
        # This changes the button style btn_add_layer
        self.Analyte_refractive_index.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: rgb(10, 25, 90);\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #FF17365D;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.n_sample_analyte.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: rgb(10, 25, 90);\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #FF17365D;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.step_analyte.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: rgb(10, 25, 90);\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #FF17365D;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        
        # This enable the btn_add_analyte button
        self.btn_add_analyte.setToolTip("Add analyte")
        self.btn_add_analyte.setStyleSheet(u"QPushButton{\n"
                                           "	font: 400 11pt \"Ubuntu\";\n"
                                           "	color: rgb(255, 255,255);\n"
                                           "	background-color: rgb(0, 130, 180);\n"
                                           "	border-color: rgb(0, 100, 130);\n"
                                           "	border-width: 2px;\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	background-color: rgb(00, 140, 70);\n"
                                           "	border-color: rgb(0, 120, 40);\n"
                                           "	width: 40;\n"
                                           "	height: 35;\n"
                                           "}")

         # This enable the gb_analyte_2 field  
        self.gb_analyte_2.setEnabled(True)
        self.gb_analyte_2.setToolTip("Analyte refractive index range")# This enable the btn_add_layer_2 button 

        # This changes the button style btn_add_layer
        self.n_sample_analyte_wim.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: rgb(10, 25, 90);\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #FF17365D;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.step_analyte_wim.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: rgb(10, 25, 90);\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #FF17365D;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.Analyte_refractive_index_wim.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: rgb(10, 25, 90);\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #FF17365D;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        
        # This enable the btn_add_analyte_2 button
        self.btn_add_analyte_2.setToolTip("Add analyte")
        self.btn_add_analyte_2.setStyleSheet(u"QPushButton{\n"
                                           "	font: 400 11pt \"Ubuntu\";\n"
                                           "	color: rgb(255, 255,255);\n"
                                           "	background-color: rgb(0, 130, 180);\n"
                                           "	border-color: rgb(0, 100, 130);\n"
                                           "	border-width: 2px;\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	background-color: rgb(00, 140, 70);\n"
                                           "	border-color: rgb(0, 120, 40);\n"
                                           "	width: 40;\n"
                                           "	height: 35;\n"
                                           "}")

        self.warning.setHidden(True)

    def set_Enable_False(self):
        # This turns off the analyte related areas
        # This turns off the gb_analyte field (AIM mode)
        self.gb_analyte.setEnabled(False)
        self.gb_analyte.setToolTip("Click in 'New layer' to enable")
        self.Analyte_refractive_index.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: #606060;\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #606060;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.n_sample_analyte.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: #606060;\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #606060;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.step_analyte.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: #606060;\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #606060;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.btn_add_analyte.setToolTip("Click in 'New layer' to enable")
        self.btn_add_analyte.setStyleSheet(u"QPushButton{\n"
                                           "	font: 400 11pt \"Ubuntu\";\n"
                                           "	color: rgb(255, 255,255);\n"
                                           "	background-color: #606060;\n"
                                           "	border-color: rgb(0, 100, 130);\n"
                                           "	border-width: 2px;\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	background-color: rgb(00, 140, 70);\n"
                                           "	border-color: rgb(0, 120, 40);\n"
                                           "	width: 40;\n"
                                           "	height: 35;\n"
                                           "}")
        self.description_3.setEnabled(False)
        self.description_3.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
        self.thickness_4.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")

        # This turns off the gb_analyt_2 field (WIM mode)
        self.gb_analyte_2.setEnabled(False)
        self.gb_analyte_2.setToolTip("Click in 'New layer' to enable")
        self.n_sample_analyte_wim.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: #606060;\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #606060;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.step_analyte_wim.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: #606060;\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #606060;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.Analyte_refractive_index_wim.setStyleSheet(u"\n"
                                            "QDoubleSpinBox\n"
                                            "{\n"
                                            "color: #606060;\n"
                                            "font: 700 12pt \"Ubuntu\";\n"
                                            "border: 2px solid;\n"
                                            "border-color: #606060;\n"
                                            "background-color: rgba(255, 255, 255,210);\n"
                                            "border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QDoubleSpinBox::up-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-up.png);\n"
                                            "	width: 25;\n"
                                            "}\n"
                                            "QDoubleSpinBox::down-button\n"
                                            "{\n"
                                            "    border-left-width: 1px;\n"
                                            "    border-left-color: darkgray;\n"
                                            "    border-left-style: solid; /* just a single line */\n"
                                            "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                            "    border-bottom-right-radius: 3px;\n"
                                            "	image: url(:/icons/icons/arrow-down.png);\n"
                                            "	width: 25;\n"
                                            "}")
        self.btn_add_analyte_2.setToolTip("Click in 'New layer' to enable")
        self.btn_add_analyte_2.setStyleSheet(u"QPushButton{\n"
                                           "	font: 400 11pt \"Ubuntu\";\n"
                                           "	color: rgb(255, 255,255);\n"
                                           "	background-color: #606060;\n"
                                           "	border-color: rgb(0, 100, 130);\n"
                                           "	border-width: 2px;\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	background-color: rgb(00, 140, 70);\n"
                                           "	border-color: rgb(0, 120, 40);\n"
                                           "	width: 40;\n"
                                           "	height: 35;\n"
                                           "}")
        self.description_4.setEnabled(False)
        self.description_4.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")    
        self.thickness_3.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")

        self.btn_confirm_edit_2.setStyleSheet(u"QPushButton{\n"
                                           "	font: 400 11pt \"Ubuntu\";\n"
                                           "	color: rgb(255, 255,255);\n"
                                           "	background-color: #606060;\n"
                                           "	border-color: rgb(0, 100, 130);\n"
                                           "	border-width: 2px;\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	background-color: rgb(00, 140, 70);\n"
                                           "	border-color: rgb(0, 120, 40);\n"
                                           "	width: 40;\n"
                                           "	height: 35;\n"
                                           "}")

        self.btn_confirm_edit_4.setStyleSheet(u"QPushButton{\n"
                                           "	font: 400 11pt \"Ubuntu\";\n"
                                           "	color: rgb(255, 255,255);\n"
                                           "	background-color: #606060;\n"
                                           "	border-color: rgb(0, 100, 130);\n"
                                           "	border-width: 2px;\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	background-color: rgb(00, 140, 70);\n"
                                           "	border-color: rgb(0, 120, 40);\n"
                                           "	width: 40;\n"
                                           "	height: 35;\n"
                                           "}")

    def set_Enable_False_2(self):
        # This unenable the cbox_material field 
        self.cbox_material.setEnabled(False)
        self.cbox_material.setStyleSheet(u"QComboBox::drop-down {\n"
                                         "    width: 25;\n"
                                         "    border-left-width: 1px;\n"
                                         "    border-left-color: darkgray;\n"
                                         "    border-left-style: solid; /* just a single line */\n"
                                         "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                         "    border-bottom-right-radius: 3px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox\n"
                                         "{\n"
                                         " padding: 1px 18px 1px 3px;\n"
                                         "color: #606060;\n"
                                         "font: 700 12pt \"Ubuntu\";\n"
                                         "border: 2px solid;\n"
                                         "border-color: #606060;\n"
                                         "background-color: rgba(255, 255, 255,210);\n"
                                         "border-radius:10px;\n"
                                         "}\n"
                                         "QComboBox::down-arrow { /* shift the arrow when popup is open */\n"
                                         "    top: 1px;\n"
                                         "	image: url(:/icons/icons/arrow-down.png);\n"
                                         "    left: 1px;\n"
                                         "}")
        self.thickness.setEnabled(False)
        self.thickness.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
        self.real_part_index.setEnabled(False)
        self.real_part_index.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
        self.imaginary_part_index.setEnabled(False)
        self.imaginary_part_index.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
        self.description.setEnabled(False)
        self.description.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")

        # This unenable the btn_add_layer button
        self.btn_add_layer.setEnabled(False)
        self.btn_add_layer.setStyleSheet(u"QPushButton{\n"
                                         "	font: 400 11pt \"Ubuntu\";\n"
                                         "	color: rgb(255, 255,255);\n"
                                         "	background-color: #606060;\n"
                                         "	border-color: rgb(0, 100, 130);\n"
                                         "	border-width: 2px;\n"
                                         "	border-radius:10px;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover{\n"
                                         "	background-color: rgb(00, 140, 70);\n"
                                         "	border-color: rgb(0, 120, 40);\n"
                                         "	width: 40;\n"
                                         "	height: 35;\n"
                                         "}")
        self.btn_add_layer.setToolTip("Click in 'New layer' to enable")
        
        self.btn_confirm_edit.setEnabled(False)
        self.btn_confirm_edit.setStyleSheet(u"QPushButton{\n"
                                         "	font: 400 11pt \"Ubuntu\";\n"
                                         "	color: rgb(255, 255,255);\n"
                                         "	background-color: #606060;\n"
                                         "	border-color: rgb(0, 100, 130);\n"
                                         "	border-width: 2px;\n"
                                         "	border-radius:10px;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover{\n"
                                         "	background-color: rgb(00, 140, 70);\n"
                                         "	border-color: rgb(0, 120, 40);\n"
                                         "	width: 40;\n"
                                         "	height: 35;\n"
                                         "}")

        self.btn_confirm_edit_3.setEnabled(False)
        self.btn_confirm_edit_3.setStyleSheet(u"QPushButton{\n"
                                         "	font: 400 11pt \"Ubuntu\";\n"
                                         "	color: rgb(255, 255,255);\n"
                                         "	background-color: #606060;\n"
                                         "	border-color: rgb(0, 100, 130);\n"
                                         "	border-width: 2px;\n"
                                         "	border-radius:10px;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover{\n"
                                         "	background-color: rgb(00, 140, 70);\n"
                                         "	border-color: rgb(0, 120, 40);\n"
                                         "	width: 40;\n"
                                         "	height: 35;\n"
                                         "}")

        # This unenable the cbox_material_2 field
        self.cbox_material_2.setEnabled(False)
        self.cbox_material_2.setStyleSheet(u"QComboBox::drop-down {\n"
                                         "    width: 25;\n"
                                         "    border-left-width: 1px;\n"
                                         "    border-left-color: darkgray;\n"
                                         "    border-left-style: solid; /* just a single line */\n"
                                         "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                         "    border-bottom-right-radius: 3px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox\n"
                                         "{\n"
                                         " padding: 1px 18px 1px 3px;\n"
                                         "color: #606060;\n"
                                         "font: 700 12pt \"Ubuntu\";\n"
                                         "border: 2px solid;\n"
                                         "border-color: #606060;\n"
                                         "background-color: rgba(255, 255, 255,210);\n"
                                         "border-radius:10px;\n"
                                         "}\n"
                                         "QComboBox::down-arrow { /* shift the arrow when popup is open */\n"
                                         "    top: 1px;\n"
                                         "	image: url(:/icons/icons/arrow-down.png);\n"
                                         "    left: 1px;\n"
                                         "}")
        self.thickness_2.setEnabled(False)
        self.thickness_2.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
        self.description_2.setEnabled(False)
        self.description_2.setStyleSheet(u"color: #606060;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #606060;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")

         # This unenable the btn_add_layer_2 button
        self.btn_add_layer_2.setEnabled(False)
        self.btn_add_layer_2.setStyleSheet(u"QPushButton{\n"
                                         "	font: 400 11pt \"Ubuntu\";\n"
                                         "	color: rgb(255, 255,255);\n"
                                         "	background-color: #606060;\n"
                                         "	border-color: rgb(0, 100, 130);\n"
                                         "	border-width: 2px;\n"
                                         "	border-radius:10px;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover{\n"
                                         "	background-color: rgb(00, 140, 70);\n"
                                         "	border-color: rgb(0, 120, 40);\n"
                                         "	width: 40;\n"
                                         "	height: 35;\n"
                                         "}")
        self.btn_add_layer_2.setToolTip("Click in 'New layer' to enable")

        self.btn_new_layer.setEnabled(True)
        self.btn_new_layer.setStyleSheet(u"QPushButton{\n"
                                         "		font: 400 11pt \"Ubuntu\";\n"
                                         "	color: rgb(255, 255,255);\n"
                                         "	background-color: rgb(0, 70, 120);\n"
                                         "	border-radius:6px;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover{\n"
                                         "	background: rgb(0, 0, 255);\n"
                                         "	width: 40;\n"
                                         "	height: 35;\n"
                                         "}")

    def set_RefractiveIndex(self, material, lambda_i):
        
        if material == 23:
            self.real_part_index.setEnabled(True)
            self.real_part_index.setText("")
            self.imaginary_part_index.setEnabled(True)
            self.imaginary_part_index.setText("")
        else:
            wi = lambda_i 
            B1, B2, B3, C1, C2, C3, X, n, k_index = 0, 0, 0, 0, 0, 0, [], [], []  # Initialization of variables
            Lambda_i = wi * 1e6  # Incidence Wavelength in micrometers
            j = complex(0,1)

            # Materials that compose the prisms, modeled by the Sellmeier equation according to the RefractiveIndex.info
            # https://refractiveindex.info/
            if 0 <= material < 8:
                if material == 0:  # BK7
                    B1, B2, B3, C1, C2, C3 = 1.03961212, 2.31792344E-1, 1.01046945, 6.00069867E-3, 2.00179144E-2, 103.560653

                elif material == 1:  # Silica
                    B1, B2, B3, C1, C2, C3 = 0.6961663, 0.4079426, 0.8974794, 4.6791E-3, 1.35121E-2, 97.934003

                elif material == 2:  # N-F2
                    B1, B2, B3, C1, C2, C3 = 1.39757037, 1.59201403E-1, 1.2686543, 9.95906143E-3, 5.46931752E-2, 119.2483460

                elif material == 3:  # Synthetic Sapphire(Al2O3)
                    B1, B2, B3, C1, C2, C3 = 1.4313493, 0.65054713, 5.3414021, 0.00527993, 0.0142383, 325.01783

                elif material == 4:  # SF10
                    B1, B2, B3, C1, C2, C3 = 1.62153902, 0.256287842, 1.64447552, 0.0122241457, 0.0595736775, 147.468793

                elif material == 5:  # FK51A
                    B1, B2, B3, C1, C2, C3 = 0.971247817, 0.216901417, 0.904651666, 0.00472301995, 0.0153575612, 168.68133

                elif material == 6:  # N-SF14
                    B1, B2, B3, C1, C2, C3 = 1.69022361, 0.288870052, 1.704518700, 0.01305121130, 0.0613691880, 149.5176890

                elif material == 7:  # Acrylic SUVT
                    B1, B2, B3, C1, C2, C3 = 0.59411, 0.59423, 0, 0.010837, 0.0099968, 0

                # Sellmeier equation
                n = sqrt(1 + ((B1 * Lambda_i ** 2) / (Lambda_i ** 2 - C1)) + ((B2 * Lambda_i ** 2) / (Lambda_i ** 2 - C2))
                         + ((B3 * Lambda_i ** 2) / (Lambda_i ** 2 - C3)))

            # Glycerol e PVA according to the RefractiveIndex.info: https://refractiveindex.info/
            elif 8 <= material < 10:
                if material == 8:  # PVA
                    B1, B2, B3, C1, C2, C3 = 1.460, 0.00665, 0, 0, 0, 0
                elif material == 9:  # Glycerin/glycerol
                    B1, B2, B3, C1, C2, C3 = 1.45797, 0.00598, -0.00036, 0, 0, 0

                # Equation that models the refractive index as a function of wavelength
                n = B1 + (B2 / Lambda_i ** 2) + (B3 / Lambda_i ** 4)

            # Quartz according to the RefractiveIndex.info: https://refractiveindex.info/
            elif material == 10:    # Quartz
                B1, B2, B3, C1, C2, C3 = 2.356764950, -1.139969240E-2, 1.087416560E-2, 3.320669140E-5, 1.086093460E-5, 0
                n = sqrt(B1 + (B2 * Lambda_i ** 2) + (B3 / Lambda_i ** 2) + (C1 / Lambda_i ** 4) + (C2 / Lambda_i ** 6))

            # Metals
            elif 11 <= material <= 16:
                """
                X - Wavelength in micrometers,
                n - Real part of the refractive index e k_index - Imaginary part of the refractive index
                according to Johnson and Christy, 1972
                """
                if material == 11:  # Gold
                    X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313, 0.2371,
                        0.2426, 0.2490, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107, 0.3204, 0.3315,
                        0.3425, 0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714, 0.4959, 0.5209, 0.5486,
                        0.5821, 0.6168, 0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088, 1.216, 1.393, 1.61, 1.937, 3.5]

                    n = [1.28, 1.32, 1.34, 1.33, 1.33, 1.30, 1.30, 1.30, 1.30, 1.31, 1.30, 1.32, 1.32,
                        1.33, 1.33, 1.35, 1.38, 1.43, 1.47, 1.49, 1.53, 1.53, 1.54,
                        1.48, 1.48, 1.50, 1.48, 1.46, 1.47, 1.46, 1.45, 1.38, 1.31, 1.04,
                        0.62, 0.43, 0.29, 0.21, 0.14, 0.13, 0.14, 0.16, 0.17, 0.22, 0.27, 0.35, 0.43, 0.56, 0.92, 1.8]

                    k_index = [1.188, 1.203, 1.226, 1.251, 1.277, 1.304, 1.35, 1.387, 1.427, 1.46, 1.497, 1.536, 1.577,
                            1.631,
                            1.688, 1.749, 1.803, 1.847, 1.869, 1.878, 1.889, 1.893, 1.898, 1.883, 1.871, 1.866, 1.895,
                            1.933,
                            1.952, 1.958, 1.948, 1.914, 1.849, 1.833, 2.081, 2.455, 2.863, 3.272, 3.697, 4.103, 4.542,
                            5.083,
                            5.663, 6.35, 7.15, 8.145, 9.519, 11.21, 13.78, 25]
                
                elif material == 12:  # Silver
                    X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313,
                        0.2371, 0.2426, 0.249, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107,
                        0.3204, 0.3315, 0.3425, 0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714,
                        0.4959, 0.5209, 0.5486, 0.5821, 0.6168, 0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088,
                        1.216, 1.393, 1.61, 1.937, 5]

                    n = [1.07, 1.1, 1.12, 1.14, 1.15, 1.18, 1.2, 1.22, 1.25, 1.26, 1.28, 1.28, 1.3, 1.31, 1.33, 1.35,
                        1.38, 1.41, 1.41, 1.39, 1.34, 1.13, 0.81, 0.17, 0.14, 0.1, 0.07, 0.05, 0.05, 0.05, 0.04, 0.04,
                        0.05, 0.05, 0.05, 0.06, 0.05, 0.06, 0.05, 0.04, 0.03, 0.04, 0.04, 0.04, 0.04, 0.09, 0.13, 0.15,
                        0.24, 2]

                    k_index = [1.212, 1.232, 1.255, 1.277, 1.296, 1.312, 1.325, 1.336, 1.342, 1.344, 1.357, 1.367, 1.378,
                            1.389, 1.393, 1.387, 1.372, 1.331, 1.264, 1.161, 0.964, 0.616, 0.392, 0.829, 1.142, 1.419,
                            1.657, 1.864, 2.07, 2.275, 2.462, 2.657, 2.869, 3.093, 3.324, 3.586, 3.858, 4.152, 4.483,
                            4.838,
                            5.242, 5.727, 6.312, 6.992, 7.795, 8.828, 10.1, 11.85, 14.08, 35]

                elif material == 13:  # Copper
                    X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313, 0.2371,
                        0.2426, 0.249, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107, 0.3204, 0.3315,
                        0.3425,
                        0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714, 0.4959, 0.5209, 0.5486, 0.5821,
                        0.6168,
                        0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088, 1.216, 1.393, 1.61, 1.937, 5]

                    n = [0.94, 0.95, 0.97, 0.98, 0.99, 1.01, 1.04, 1.08, 1.13, 1.18, 1.23, 1.28, 1.34, 1.37, 1.41, 1.41,
                        1.45,
                        1.46, 1.45, 1.42, 1.4, 1.38, 1.38, 1.34, 1.36, 1.37, 1.36, 1.33, 1.32, 1.28, 1.25, 1.24, 1.25,
                        1.22, 1.18,
                        1.02, 0.7, 0.3, 0.22, 0.21, 0.24, 0.26, 0.3, 0.32, 0.36, 0.48, 0.6, 0.76, 1.09, 2.5]

                    k_index = [1.337, 1.388, 1.44, 1.493, 1.55, 1.599, 1.651, 1.699, 1.737, 1.768, 1.792, 1.802, 1.799,
                            1.783, 1.741, 1.691,
                            1.668, 1.646, 1.633, 1.633, 1.679, 1.729, 1.783, 1.821, 1.864, 1.916, 1.975, 2.045, 2.116,
                            2.207, 2.305, 2.397,
                            2.483, 2.564, 2.608, 2.577, 2.704, 3.205, 3.747, 4.205, 4.665, 5.18, 5.768, 6.421, 7.217,
                            8.245, 9.439, 11.12, 13.43, 35]
                
                elif material == 14:    # P3HT:PC61BM
                    # Refractive index of the P3HT:PC61BM according to the RefractiveIndex.info:
                    # https://refractiveindex.info/

                    X = [0.24718, 0.24878, 0.25038, 0.25198, 0.25358, 0.25518, 0.25678, 0.25838, 0.25998, 0.26158, 0.26318, 0.26478, 0.26638, 0.26798, 
                         0.26958, 0.27118, 0.27278, 0.27438, 0.27598, 0.27758, 0.27918, 0.28078, 0.28238, 0.28398, 0.28558, 0.28718, 0.28878, 0.29038, 
                         0.29198, 0.29358, 0.29518, 0.29678, 0.29838, 0.29998, 0.30158, 0.30318, 0.30478, 0.30638, 0.30798, 0.30958, 0.31118, 0.31278, 
                         0.31438, 0.31598, 0.31758, 0.31918, 0.32078, 0.32238, 0.32398, 0.32558, 0.32718, 0.32878, 0.33038, 0.33198, 0.33358, 0.33518, 
                         0.33678, 0.33838, 0.33998, 0.34158, 0.34318, 0.34477, 0.34637, 0.34797, 0.34957, 0.35117, 0.35277, 0.35437, 0.35597, 0.35757, 
                         0.35917, 0.36077, 0.36237, 0.36396, 0.36556, 0.36716, 0.36876, 0.37036, 0.37196, 0.37356, 0.37516, 0.37675, 0.37835, 0.37995, 
                         0.38155, 0.38315, 0.38475, 0.38635, 0.38794, 0.38954, 0.39114, 0.39274, 0.39434, 0.39593, 0.39753, 0.39913, 0.40073, 0.40233, 
                         0.40392, 0.40552, 0.40712, 0.40872, 0.41032, 0.41191, 0.41351, 0.41511, 0.41671, 0.4183, 0.4199, 0.4215, 0.42309, 0.42469, 
                         0.42629, 0.42789, 0.42948, 0.43108, 0.43268, 0.43427, 0.43587, 0.43747, 0.43906, 0.44066, 0.44226, 0.44385, 0.44545, 0.44705, 
                         0.44864, 0.45024, 0.45183, 0.45343, 0.45503, 0.45662, 0.45822, 0.45981, 0.46141, 0.46301, 0.4646, 0.4662, 0.46779, 0.46939, 
                         0.47098, 0.47258, 0.47417, 0.47577, 0.47736, 0.47896, 0.48055, 0.48215, 0.48374, 0.48534, 0.48693, 0.48853, 0.49012, 0.49172, 
                         0.49331, 0.4949, 0.4965, 0.49809, 0.49969, 0.50128, 0.50287, 0.50447, 0.50606, 0.50765, 0.50925, 0.51084, 0.51243, 0.51403, 0.51562, 0.51721, 0.51881, 0.5204, 0.52199, 0.52358, 0.52518, 0.52677, 0.52836, 0.52995, 0.53155, 0.53314, 0.53473, 0.53632, 
                         0.53791, 0.53951, 0.5411, 0.54269, 0.54428, 0.54587, 0.54746, 0.54905, 0.55065, 0.55224, 0.55383, 0.55542, 0.55701, 0.5586,
                         0.56019, 0.56178, 0.56337, 0.56496, 0.56655, 0.56814, 0.56973, 0.57132, 0.57291, 0.5745, 0.57609, 0.57768, 0.57927, 0.58086,
                         0.58245, 0.58403, 0.58562, 0.58721, 0.5888, 0.59039, 0.59198, 0.59357, 0.59515, 0.59674, 0.59833, 0.59992, 0.60151, 0.60309,
                         0.60468, 0.60627, 0.60786, 0.60944, 0.61103, 0.61262, 0.6142, 0.61579, 0.61738, 0.61896, 0.62055, 0.62213, 0.62372, 0.62531, 
                         0.62689, 0.62848, 0.63006, 0.63165, 0.63323, 0.63482, 0.6364, 0.63799, 0.63957, 0.64116, 0.64274, 0.64433, 0.64591, 0.6475, 
                         0.64908, 0.65066, 0.65225, 0.65383, 0.65541, 0.657, 0.65858, 0.66016, 0.66175, 0.66333, 0.66491, 0.66649, 0.66808, 0.66966, 
                         0.67124, 0.67282, 0.67441, 0.67599, 0.67757, 0.67915, 0.68073, 0.68231, 0.68389, 0.68547, 0.68706, 0.68864, 0.69022, 0.6918, 
                         0.69338, 0.69496, 0.69654, 0.69812, 0.6997, 0.70127, 0.70285, 0.70443, 0.70601, 0.70759, 0.70917, 0.71075, 0.71233, 0.7139,
                         0.71548, 0.71706, 0.71864, 0.72022, 0.72179, 0.72337, 0.72495, 0.72652, 0.7281, 0.72968, 0.73125, 0.73283, 0.73441, 0.73598, 
                         0.73756, 0.73913, 0.74071, 0.74229, 0.74386, 0.74544, 0.74701, 0.74859, 0.75016, 0.75173, 0.75331, 0.75488, 0.75646, 0.75803, 
                         0.7596, 0.76118, 0.76275, 0.76432, 0.7659, 0.76747, 0.76904, 0.77061, 0.77219, 0.77376, 0.77533, 0.7769, 0.77847, 0.78004, 
                         0.78162, 0.78319, 0.78476, 0.78633, 0.7879, 0.78947, 0.79104, 0.79261, 0.79418, 0.79575, 0.79732, 0.79889, 0.80046, 0.80202, 
                         0.80359, 0.80516, 0.80673, 0.8083, 0.80987, 0.81143, 0.813, 0.81457, 0.81614, 0.8177, 0.81927, 0.82084, 0.8224, 0.82397, 0.82554, 
                         0.8271, 0.82867, 0.83023, 0.8318, 0.83336, 0.83493, 0.83649, 0.83806, 0.83962, 0.84119, 0.84275, 0.84431, 0.84588, 0.84744, 
                         0.849, 0.85057, 0.85213, 0.85369, 0.85525, 0.85682, 0.85838, 0.85994, 0.8615, 0.86306, 0.86462, 0.86618, 0.86775, 0.86931, 
                         0.87087, 0.87243, 0.87399, 0.87555, 0.87711, 0.87866, 0.88022, 0.88178, 0.88334, 0.8849, 0.88646, 0.88802, 0.88957, 0.89113, 
                         0.89269, 0.89425, 0.8958, 0.89736, 0.89892, 0.90047, 0.90203, 0.90359, 0.90514, 0.9067, 0.90825, 0.90981, 0.91136, 0.91292, 
                         0.91447, 0.91602, 0.91758, 0.91913, 0.92069, 0.92224, 0.92379, 0.92535, 0.9269, 0.92845, 0.93, 0.93155, 0.93311, 0.93466, 
                         0.93621, 0.93776, 0.93931, 0.94086, 0.94241, 0.94396, 0.94551, 0.94706, 0.94861, 0.95016, 0.95171, 0.95326, 0.95481, 0.95635, 
                         0.9579, 0.95945, 0.961, 0.96255, 0.96409, 0.96564, 0.96719, 0.96873, 0.97028, 0.97182, 0.97337, 0.97492, 0.97646, 0.97801, 
                         0.97955, 0.98109, 0.98264, 0.98418, 0.98573, 0.98727, 0.98881, 0.99036, 0.9919, 0.99344, 0.99498, 0.99653, 0.99807, 0.99961, 
                         1.01227, 1.01567, 1.01908, 1.02248, 1.02588, 1.02929, 1.03269, 1.03609, 1.0395, 1.0429, 1.0463, 1.0497, 1.05311, 1.05651, 
                         1.05991, 1.06331, 1.06671, 1.07011, 1.07352, 1.07692, 1.08032, 1.08372, 1.08712, 1.09052, 1.09392, 1.09733, 1.10073, 1.10413, 
                         1.10753, 1.11093, 1.11433, 1.11773, 1.12113, 1.12453, 1.12794, 1.13134, 1.13474, 1.13814, 1.14154, 1.14494, 1.14834, 1.15175, 
                         1.15515, 1.15855, 1.16195, 1.16535, 1.16876, 1.17216, 1.17556, 1.17896, 1.18237, 1.18577, 1.18917, 1.19258, 1.19598, 1.19938, 
                         1.20279, 1.20619, 1.2096, 1.213, 1.21641, 1.21981, 1.22322, 1.22662, 1.23003, 1.23343, 1.23684, 1.24025, 1.24365, 1.24706, 
                         1.25047, 1.25388, 1.25729, 1.26069, 1.2641, 1.26751, 1.27092, 1.27433, 1.27774, 1.28115, 1.28456, 1.28798, 1.29139, 1.2948, 
                         1.29821, 1.30163, 1.30504, 1.30845, 1.31187, 1.31528, 1.3187, 1.32212, 1.32553, 1.32895, 1.33237, 1.33578, 1.3392, 1.34262, 
                         1.34604, 1.34946, 1.35288, 1.3563, 1.35972, 1.36315, 1.36657, 1.36999, 1.37342, 1.37684, 1.38027, 1.38369, 1.38712, 1.39055, 
                         1.39397, 1.3974, 1.40083, 1.40426, 1.40769, 1.41112, 1.41455, 1.41798, 1.42142, 1.42485, 1.42829, 1.43172, 1.43516, 1.43859, 
                         1.44203, 1.44547, 1.44891, 1.45235, 1.45579, 1.45923, 1.46267, 1.46611, 1.46956, 1.473, 1.47644, 1.47989, 1.48334, 1.48678, 
                         1.49023, 1.49368, 1.49713, 1.50058, 1.50404, 1.50749, 1.51094, 1.5144, 1.51785, 1.52131, 1.52476, 1.52822, 1.53168, 1.53514, 
                         1.5386, 1.54206, 1.54553, 1.54899, 1.55246, 1.55592, 1.55939, 1.56286, 1.56633, 1.5698, 1.57327, 1.57674, 1.58021, 1.58369, 
                         1.58716, 1.59064, 1.59411, 1.59759, 1.60107, 1.60455, 1.60803, 1.61152, 1.615, 1.61849, 1.62197, 1.62546, 1.62895, 1.63244, 
                         1.63593, 1.63942, 1.64291, 1.64641, 1.6499, 1.6534, 1.6569, 1.66039, 1.66389, 1.6674, 1.6709, 1.6744, 1.67791, 1.68141, 1.68492]

                    n = [1.551411, 1.551346, 1.551329, 1.551312, 1.551256, 1.551131, 1.550912, 1.550584, 1.550138, 1.549573, 1.548891, 1.5481, 1.547212, 
                         1.546241, 1.545203, 1.544114, 1.542992, 1.541851, 1.540706, 1.539571, 1.538455, 1.537368, 1.536314, 1.535297, 1.534316, 1.53337, 
                         1.532454, 1.53156, 1.530679, 1.5298, 1.528911, 1.527998, 1.527045, 1.526037, 1.524959, 1.523794, 1.522527, 1.521142, 1.519627, 1.51797, 1.51616, 1.514189, 1.512052, 1.509747, 1.507273, 1.504636, 1.501841, 1.498899, 1.495823, 1.492629, 1.489335, 1.485959, 1.482523, 1.479046, 1.475548, 1.472045, 1.468553, 1.46508, 1.461633, 1.458209, 1.454802, 1.451396, 1.447969, 1.444493, 1.440937, 1.437268, 1.433454, 1.429473, 1.425313, 1.420975, 1.416479, 1.411861, 1.407168, 1.402452, 1.39776, 1.393125, 1.388555, 1.384025, 1.379477, 1.37482, 1.369943, 1.364722, 1.359035, 1.35278, 1.345886, 1.33832, 1.330099, 1.321285, 1.311982, 1.302337, 1.292524, 1.282735, 1.273173, 1.264037, 1.255516, 1.247777, 1.240961, 1.235176, 1.230497, 1.226963, 1.224578, 1.223316, 1.223124, 1.223924, 1.225623, 1.228117, 1.231294, 1.235041, 1.23925, 1.243819, 1.248656, 1.253683, 1.258837, 1.264069, 1.269349, 1.274663, 1.280013, 1.285415, 1.2909, 1.296509, 1.302293, 1.308307, 1.31461, 1.32126, 1.328312, 1.335814, 1.343804, 1.35231, 1.361348, 1.370919, 1.381009, 1.391595, 1.402638, 1.414092, 1.425903, 1.438009, 1.450349, 1.462861, 1.475487, 1.488174, 1.500879, 1.513568, 1.526219, 1.538825, 1.551391, 1.563937, 1.576491, 1.589097, 1.601804, 1.614668, 1.627746, 1.641094, 1.654765, 1.6688, 1.68323, 1.698071, 1.713322, 1.728962, 1.744954, 1.761241, 1.777754, 1.794405, 1.811101, 1.82774, 1.844222, 1.86045, 1.876335, 1.891802, 1.906795, 1.921278, 1.935241, 1.948699, 1.961689, 1.974275, 1.986542, 1.998588, 2.010523, 2.022459, 2.034502, 2.046748, 2.059268, 2.07211, 2.085288, 2.098778, 2.11252, 2.126417, 2.140337, 2.154119, 2.167574, 2.180499, 2.19268, 2.2039, 2.213949, 2.222631, 2.229772, 2.235227, 2.238891, 2.240701, 2.240645, 2.238765, 2.235163, 2.23, 2.223498, 2.215933, 2.207631, 2.198952, 2.190276, 2.181984, 2.174436, 2.167948, 2.162769, 2.159064, 2.156905, 2.156263, 2.157012, 2.158945, 2.161786, 2.165214, 2.168888, 2.172466, 2.175627, 2.17809, 2.179619, 2.180037, 2.179227, 2.177129, 2.173741, 2.169109, 2.16332, 2.156494, 2.148776, 2.140322, 2.131296, 2.121861, 2.11217, 2.102364, 2.092568, 2.08289, 2.073416, 2.064215, 2.055337, 2.046817, 2.038675, 2.030917, 2.023544, 2.016545, 2.009906, 2.003608, 1.997632, 1.991956, 1.986558, 1.981416, 1.976512, 1.971826, 1.967341, 1.963041, 1.958911, 1.954939, 1.951113, 1.947422, 1.943857, 1.94041, 1.937073, 1.933839, 1.930702, 1.927657, 1.924698, 1.921822, 1.919023, 1.916298, 1.913643, 1.911056, 1.908532, 1.90607, 1.903666, 1.901319, 1.899025, 1.896783, 1.894591, 1.892447, 1.890349, 1.888295, 1.886283, 1.884313, 1.882383, 1.880492, 1.878637, 1.876819, 1.875035, 1.873286, 1.871568, 1.869883, 1.868228, 1.866603, 1.865007, 1.863438, 1.861898, 1.860383, 1.858895, 1.857431, 1.855992, 1.854576, 1.853184, 1.851814, 1.850466, 1.849139, 1.847833, 1.846548, 1.845282, 1.844035, 1.842808, 1.841598, 1.840407, 1.839233, 1.838076, 1.836936, 1.835812, 1.834705, 1.833612, 1.832536, 1.831474, 1.830426, 1.829393, 1.828374, 1.827369, 1.826377, 1.825398, 1.824432, 1.823479, 1.822538, 1.821609, 1.820692, 1.819786, 1.818892, 1.818009, 1.817137, 1.816276, 1.815426, 1.814586, 1.813755, 1.812935, 1.812125, 1.811324, 1.810533, 1.809751, 1.808978, 1.808214, 1.807459, 1.806712, 1.805974, 1.805244, 1.804523, 1.803809, 1.803103, 1.802405, 1.801715, 1.801032, 1.800357, 1.799689, 1.799028, 1.798374, 1.797727, 1.797087, 1.796454, 1.795827, 1.795207, 1.794593, 1.793985, 1.793384, 1.792789, 1.792199, 1.791616, 1.791039, 1.790467, 1.789901, 1.78934, 1.788785, 1.788236, 1.787692, 1.787153, 1.786619, 1.78609, 1.785566, 1.785048, 1.784534, 1.784025, 1.783521, 1.783021, 1.782526, 1.782036, 1.78155, 1.781069, 1.780592, 1.78012, 1.779651, 1.779187, 1.778727, 1.778271, 1.777819, 1.777371, 1.776927, 1.776487, 1.776051, 1.775619, 1.77519, 1.774765, 1.774344, 1.773926, 1.773512, 1.773101, 1.772694, 1.77229, 1.77189, 1.771493, 1.771099, 1.770709, 1.770322, 1.769938, 1.769557, 1.769179, 1.768804, 1.768433, 1.768064, 1.767698, 1.767336, 1.766976, 1.766619, 1.766264, 1.765913, 1.765564, 1.765218, 1.764875, 1.764535, 1.764197, 1.763862, 1.763529, 1.763199, 1.762871, 1.762546, 1.762223, 1.761903, 1.761586, 1.76127, 1.760957, 1.760646, 1.760338, 1.760032, 1.759728, 1.759427, 1.759127, 1.75883, 1.758535, 1.758242, 1.757952, 1.757663, 1.757377, 1.757092, 1.75681, 1.756529, 1.756251, 1.755975, 1.7557, 1.755427, 1.755157, 1.754888, 1.754621, 1.754356, 1.754093, 1.753832, 1.753572, 1.753315, 1.753059, 1.752805, 1.752552, 1.752301, 1.752052, 1.751805, 1.749834, 1.749322, 1.748817, 1.748319, 1.747828, 1.747344, 1.746867, 1.746396, 1.745932, 1.745473, 1.745021, 1.744576, 1.744136, 1.743702, 1.743273, 1.742851, 1.742434, 1.742022, 1.741615, 1.741214, 1.740818, 1.740427, 1.740041, 1.73966, 1.739283, 1.738912, 1.738544, 1.738182, 1.737824, 1.73747, 1.73712, 1.736775, 1.736434, 1.736097, 1.735764, 1.735435, 1.73511, 1.734789, 1.734471, 1.734157, 1.733847, 1.73354, 1.733237, 1.732937, 1.732641, 1.732348, 1.732059, 1.731772, 1.731489, 1.731209, 1.730932, 1.730659, 1.730388, 1.73012, 1.729855, 1.729593, 1.729334, 1.729078, 1.728824, 1.728573, 1.728325, 1.728079, 1.727836, 1.727596, 1.727358, 1.727123, 1.72689, 1.726659, 1.726431, 1.726205, 1.725982, 1.725761, 1.725542, 1.725325, 1.72511, 1.724898, 1.724688, 1.72448, 1.724274, 1.72407, 1.723868, 1.723668, 1.72347, 1.723274, 1.723079, 1.722887, 1.722697, 1.722508, 1.722322, 1.722137, 1.721953, 1.721772, 1.721592, 1.721414, 1.721238, 1.721063, 1.720891, 1.720719, 1.720549, 1.720381, 1.720215, 1.72005, 1.719886, 1.719724, 1.719564, 1.719404, 1.719247, 1.719091, 1.718936, 1.718783, 1.718631, 1.71848, 1.718331, 1.718183, 1.718036, 1.717891, 1.717747, 1.717605, 1.717463, 1.717323, 1.717184, 1.717046, 1.71691, 1.716774, 1.71664, 1.716507, 1.716375, 1.716245, 1.716115, 1.715987, 1.715859, 1.715733, 1.715608, 1.715484, 1.715361, 1.715239, 1.715118, 1.714998, 1.714879, 1.714761, 1.714644, 1.714528, 1.714413, 1.714299, 1.714186, 1.714074, 1.713963, 1.713853, 1.713743, 1.713635, 1.713527, 1.713421, 1.713315, 1.71321, 1.713106, 1.713003, 1.7129, 1.712799, 1.712698, 1.712598, 1.712499, 1.712401, 1.712303, 1.712206, 1.71211, 1.712015, 1.711921, 1.711827, 1.711734, 1.711642, 1.71155, 1.71146, 1.71137, 1.71128, 1.711192, 1.711104, 1.711017, 1.71093, 1.710845, 1.710759, 1.710675, 1.710591, 1.710508, 1.710425, 1.710343, 1.710262, 1.710182, 1.710102, 1.710022, 1.709944, 1.709865, 1.709788, 1.709711, 1.709635, 1.709559, 1.709484, 1.709409]

                    k_index = [0.096191, 0.09871, 0.100881, 0.10273, 0.104288, 0.105589, 0.10667, 0.107568, 0.108318, 0.108955, 0.10951, 0.11001, 
                               0.110478,     0.110933, 0.11139, 0.111858, 0.112342, 0.112846, 0.113366, 0.113899, 0.114437, 0.114971, 0.115491, 0.115985, 0.116442, 0.116849, 0.117196, 0.117472, 0.117667, 0.117775, 0.117788, 0.117702, 0.117517, 0.11723, 0.116846, 0.116369, 0.115806, 0.115166, 0.114463, 0.113709, 0.11292, 0.112115, 0.111313, 0.110532, 0.109793, 0.109117, 0.108522, 0.108026, 0.107646, 0.107395, 0.107283, 0.107316, 0.107497, 0.107824, 0.10829, 0.108885, 0.109594, 0.110399, 0.111279, 0.112211, 0.113173, 0.114145, 0.115111, 0.11606, 0.116992, 0.117917, 0.118856, 0.11984, 0.12091, 0.12211, 0.123482, 0.125058, 0.126854, 0.128864, 0.131058, 0.133384, 0.135773, 0.13815, 0.140449, 0.142622, 0.144656, 0.146577, 0.148455, 0.1504, 0.15256, 0.155103, 0.158208, 0.162055, 0.166803, 0.172588, 0.17951, 0.187627, 0.196954, 0.207464, 0.219088, 0.231724, 0.245237, 0.259475, 0.27427, 0.289448, 0.304838, 0.320281, 0.335628, 0.350754, 0.365554, 0.379946, 0.393875, 0.407309, 0.420237, 0.432671, 0.444639, 0.456183, 0.467357, 0.478224, 0.488849, 0.499302, 0.509647, 0.519945, 0.530249, 0.540603, 0.551035, 0.561563, 0.572189, 0.582902, 0.593675, 0.604471, 0.615239, 0.625924, 0.636462, 0.646787, 0.656835, 0.666545, 0.675862, 0.68474, 0.693144, 0.70105, 0.708448, 0.715342, 0.721745, 0.727686, 0.7332, 0.738332, 0.743131, 0.747651, 0.751943, 0.756054, 0.760027, 0.763893, 0.767673, 0.771372, 0.774982, 0.778479, 0.781822, 0.784957, 0.787819, 0.790333, 0.792417, 0.793992, 0.794976, 0.795298, 0.794898, 0.793729, 0.791763, 0.788992, 0.78543, 0.78111, 0.776087, 0.770434, 0.76424, 0.757601, 0.750622, 0.743406, 0.736048, 0.728633, 0.721226, 0.713865, 0.706565, 0.699306, 0.692039, 0.684683, 0.677132, 0.669255, 0.660908, 0.65194, 0.642201, 0.63155, 0.619865, 0.607049, 0.59304, 0.57781, 0.561373, 0.543785, 0.525144, 0.505593, 0.48531, 0.464513, 0.443449, 0.422392, 0.401634, 0.381471, 0.3622, 0.344105, 0.327437, 0.31241, 0.299177, 0.287826, 0.278362, 0.270705, 0.264689, 0.260063, 0.256509, 0.253654, 0.251101, 0.248447, 0.245319, 0.24139, 0.236401, 0.230173, 0.222615, 0.213718, 0.203553, 0.192254, 0.180011, 0.167049, 0.153615, 0.139963, 0.126341, 0.112979, 0.100082, 0.087824, 0.076341, 0.065736, 0.056074, 0.047385, 0.03967, 0.032906, 0.027047, 0.022031, 0.017785, 0.014233, 0.011293, 0.008886, 0.006935, 0.00537, 0.004127, 0.003149, 0.002386, 0.001797, 0.001346, 0.001002, 0.000744, 0.00055, 0.000405, 0.000299, 0.00022, 0.000163, 0.000121, 9.1e-05, 6.8e-05, 5.2e-05, 4e-05, 3.2e-05, 2.5e-05, 2.1e-05, 1.7e-05, 1.5e-05, 1.2e-05, 1.1e-05, 9e-06, 8e-06, 8e-06, 7e-06, 6e-06, 6e-06, 5e-06, 5e-06, 4e-06, 4e-06, 4e-06, 4e-06, 3e-06, 3e-06, 3e-06, 3e-06, 3e-06, 3e-06, 2e-06, 2e-06, 2e-06, 2e-06, 2e-06, 2e-06, 2e-06, 2e-06, 2e-06, 2e-06, 2e-06, 2e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 1e-06, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                
                elif material == 15:    # PEDOT:PSS 
                    X = [0.3019, 0.3062, 0.3113, 0.3189, 0.3274, 0.3367, 0.3461, 0.3563, 0.3665, 0.3775, 0.3868, 0.4021, 0.4149, 0.4276, 0.4395, 0.4522, 0.4641, 0.476, 0.4896, 0.5066, 0.5261, 0.5465, 0.5652, 0.5856, 0.6085, 0.6399, 0.6586, 0.679, 0.7011, 0.724, 0.7461, 0.7741, 0.8038, 0.8276, 0.8522, 0.8786, 0.9032, 0.9278, 0.949, 0.9703, 0.9915, 1.0102, 1.0229, 1.0374, 1.0544, 1.0671, 1.0798, 1.0968, 1.0433, 1.0577, 1.0705, 1.0849, 1.0977, 2.0] 
                    
                    n = [1.5806, 1.5773, 1.5746, 1.5711, 1.5675, 1.5636, 1.5602, 1.5563, 1.5533, 1.5499, 1.5475, 1.5433, 1.5403, 1.5373, 1.5349, 1.5323, 1.53, 1.5276, 1.5253, 1.5223, 1.5191, 1.5161, 1.5129, 1.5101, 1.5067, 1.5022, 1.4994, 1.4964, 1.4934, 1.4902, 1.4872, 1.4836, 1.4797, 1.4767, 1.4742, 1.4714, 1.469, 1.4671, 1.4665, 1.4659, 1.4661, 1.4663, 1.4672, 1.468, 1.4695, 1.4713, 1.4728, 1.476, 1.4785, 1.481, 1.4835, 1.4868, 1.4894, 1.6] 
                    
                    k_index =[0.00043, 0.00044, 0.00066, 0.00089, 0.00111, 0.00133, 0.00156, 0.00178, 0.00222, 0.00266, 0.00331, 0.00397, 0.00463, 0.00551, 0.0066, 0.00769, 0.00856, 0.00987, 0.01117, 0.01248, 0.014, 0.01552, 0.01725, 0.01921, 0.02137, 0.02311, 0.02484, 0.02766, 0.02961, 0.03112, 0.03329, 0.03567, 0.03783, 0.04043, 0.04389, 0.048, 0.05125, 0.05449, 0.05817, 0.06206, 0.06617, 0.07028, 0.07352, 0.07763, 0.08174, 0.08563, 0.09039, 0.09493, 0.10033, 0.10552, 0.10984, 0.11481, 0.11935, 0.24]

                elif material == 16: # 2D HOIP
                    X = [0.370914, 0.372495, 0.374077, 0.375658, 0.37724, 0.378823, 0.380405, 0.381988, 0.383571, 0.385153, 0.386736, 0.388319, 0.389902, 
                         0.391485, 0.393069, 0.394653, 0.396237, 0.39782, 0.399404, 0.400989, 0.402574, 0.404157, 0.405742, 0.407327, 0.408911, 0.410496,
                         0.412082, 0.413667, 0.415252, 0.416838, 0.418423, 0.420009, 0.421595, 0.42318, 0.424766, 0.426353, 0.427939, 0.429525, 0.431111, 
                         0.432699, 0.434284, 0.435872, 0.437459, 0.439045, 0.440632, 0.44222, 0.443807, 0.445395, 0.446983, 0.44857, 0.450158, 0.451745, 
                         0.453334, 0.454923, 0.456511, 0.458098, 0.459688, 0.461276, 0.462864, 0.464452, 0.466041, 0.46763, 0.469219, 0.470809, 0.472398, 
                         0.473987, 0.475576, 0.477165, 0.478755, 0.480345, 0.481934, 0.483524, 0.485113, 0.486703, 0.488294, 0.489884, 0.491474, 0.493063, 
                         0.494655, 0.496244, 0.497837, 0.499427, 0.501017, 0.502607, 0.504198, 0.50579, 0.507379, 0.508971, 0.510561, 0.512154, 0.513743, 
                         0.515336, 0.516926, 0.518517, 0.520109, 0.5217, 0.523292, 0.524883, 0.526474, 0.528066, 0.529659, 0.53125, 0.532844, 0.534435, 
                         0.536027, 0.53762, 0.539212, 0.540804, 0.542396, 0.543988, 0.54558, 0.547172, 0.548765, 0.550356, 0.551949, 0.553543, 0.555134,
                         0.556727, 0.558319, 0.559912, 0.561505, 0.563099, 0.564691, 0.566283, 0.567875, 0.569469, 0.571061, 0.572654, 0.574248, 0.57584, 
                         0.577433, 0.579027, 0.580619, 0.582214, 0.583807, 0.5854, 0.586994, 0.588585, 0.590179, 0.59177, 0.593365, 0.594959, 0.596551, 
                         0.598146, 0.599737, 0.601331, 0.602925, 0.604518, 0.606111, 0.607706, 0.609298, 0.610892, 0.612485, 0.614078, 0.615673, 0.617267, 
                         0.61886, 0.620451, 0.622045, 0.623638, 0.625232, 0.626825, 0.62842, 0.630014, 0.631606, 0.633199, 0.634794, 0.636388, 0.637979, 
                         0.639572, 0.641166, 0.642758, 0.644355, 0.645946, 0.647539, 0.649132, 0.650726, 0.652318, 0.653915, 0.655505, 0.6571, 0.658692, 
                         0.660288, 0.661877, 0.663471, 0.665066, 0.666657, 0.668252, 0.669844, 0.671437, 0.67303, 0.674623, 0.676216, 0.677809, 0.679403, 
                         0.680996, 0.68259, 0.684179, 0.685772, 0.687365, 0.688958, 0.69055, 0.692143, 0.693734, 0.695329, 0.69692, 0.698514, 0.700108, 
                         0.701697, 0.703289, 0.704884, 0.706475, 0.708068, 0.709657, 0.711253, 0.712844, 0.714433, 0.716026, 0.717617, 0.719212, 0.720801, 
                         0.722392, 0.723987, 0.725576, 0.727167, 0.728762, 0.73035, 0.731941, 0.733534, 0.735126, 0.736716, 0.738304, 0.739899, 0.741488, 
                         0.743079, 0.744668, 0.746259, 0.747852, 0.749444, 0.751032, 0.752624, 0.754212, 0.755803, 0.757391, 0.758982, 0.760574, 0.762164, 
                         0.76375, 0.765344, 0.76693, 0.768522, 0.770112, 0.771699, 0.773292, 0.774882, 0.776469, 0.778057, 0.779647, 0.781234, 0.782822, 
                         0.784412, 0.786004, 0.787591, 0.789175, 0.790766, 0.792353, 0.793941, 0.79553, 0.797121, 0.798708, 0.800296, 0.801879, 0.80347, 
                         0.805056, 0.806643, 0.808231, 0.80982, 0.811404, 0.81299, 0.814576, 0.816163, 0.817751, 0.819335, 0.820924, 0.822509, 0.824095, 
                         0.825681, 0.827267, 0.828854, 0.830437, 0.832025, 0.833608, 0.835192, 0.836781, 0.838366, 0.83995, 0.841535, 0.84312, 0.8447, 
                         0.846285, 0.847871, 0.849457, 0.851037, 0.852623, 0.854203, 0.855789, 0.857375, 0.858955, 0.860541, 0.862121, 0.863706, 0.865286, 
                         0.866871, 0.86845, 0.870034, 0.871618, 0.873196, 0.874779, 0.876362, 0.877944, 0.879526, 0.881101, 0.882689, 0.884269, 0.885848, 
                         0.887427, 0.889005, 0.890589, 0.892172, 0.893747, 0.895329, 0.896909, 0.898488, 0.900067, 0.901644, 0.903227, 0.904803, 0.906383, 
                         0.907957, 0.909535, 0.911113, 0.912695, 0.91427, 0.915851, 0.91743, 0.919001, 0.920584, 0.922158, 0.923732, 0.92531, 0.926888, 
                         0.928463, 0.930037, 0.931617, 0.933187, 0.934763, 0.936338, 0.937917, 0.939488, 0.941064, 0.942638, 0.944217, 0.945787, 0.947363, 
                         0.948936, 0.950507, 0.952084, 0.953659, 0.955231, 0.956801, 0.958376, 0.959949, 0.96152, 0.963089, 0.964662, 0.966234, 0.967802, 
                         0.969376, 0.970948, 0.972517, 0.974091, 0.975662, 0.977231, 0.978797, 0.980368, 0.981936, 0.98351, 0.985073, 0.986648, 0.988213, 
                         0.989783, 0.99135, 0.992914, 0.994483, 0.996049, 0.99762, 0.999188, 1.013, 1.01641, 1.01981, 1.02322, 1.02662, 1.03003, 1.03343, 
                         1.03684, 1.04025, 1.04366, 1.04707, 1.05047, 1.05388, 1.05729, 1.0607, 1.06411, 1.06752, 1.07093, 1.07434, 1.07775, 1.08116, 
                         1.08457, 1.08799, 1.0914, 1.09481, 1.09823, 1.10164, 1.10506, 1.10847, 1.11189, 1.1153, 1.11872, 1.12213, 1.12554, 1.12897, 
                         1.13238, 1.13579, 1.13922, 1.14263, 1.14605, 1.14947, 1.15289, 1.15631, 1.15973, 1.16314, 1.16657, 1.16998, 1.1734, 1.17682, 
                         1.18025, 1.18368, 1.18709, 1.19052, 1.19394, 1.19736, 1.20079, 1.20421, 1.20763, 1.21106, 1.21448, 1.21791, 1.22134, 1.22477, 
                         1.22819, 1.23161, 1.23504, 1.23847, 1.2419, 1.24532, 1.24876, 1.25219, 1.25561, 1.25904, 1.26248, 1.26591, 1.26933, 1.27277, 
                         1.2762, 1.27963, 1.28306, 1.28649, 1.28993, 1.29336, 1.2968, 1.30022, 1.30366, 1.30709, 1.31053, 1.31396, 1.3174, 1.32084, 
                         1.32428, 1.32771, 1.33115, 1.33458, 1.33803, 1.34146, 1.34489, 1.34834, 1.35178, 1.35521, 1.35866, 1.36209, 1.36554, 1.36898, 
                         1.37242, 1.37586, 1.3793, 1.38275, 1.38618, 1.38963, 1.39307, 1.39652, 1.39995, 1.40341, 1.40685, 1.41029, 1.41375, 1.41719, 
                         1.42063, 1.42407, 1.42752, 1.43098, 1.43442, 1.43786, 1.44131, 1.44477, 1.44821, 1.45165, 1.45511, 1.45855, 1.46201, 1.46546, 
                         1.4689, 1.47236, 1.47581, 1.47926, 1.48271, 1.48618, 1.48962, 1.49308, 1.49653, 1.49998, 1.50344, 1.50689, 1.51034, 1.51381, 
                         1.51726, 1.52072, 1.52418, 1.52763, 1.53108, 1.53455, 1.538, 1.54146, 1.54492, 1.54839, 1.55184, 1.5553, 1.55877, 1.56222, 1.56567, 
                         1.56914, 1.57261, 1.57606, 1.57952, 1.58299, 1.58645, 1.58991, 1.59338, 1.59685, 1.60031, 1.60377, 1.60724, 1.61071, 1.61417, 
                         1.61762, 1.62109, 1.62457, 1.62803, 1.6315, 1.63496, 1.63844, 1.64189, 1.64538, 1.64884, 1.65231, 1.65577, 1.65925, 1.66272, 
                         1.66619, 1.66966, 1.67313, 1.67659, 1.68007, 1.68354, 1.68702] 
                    
                    n = [2.23347, 2.25319, 2.2716, 2.28868, 2.30444, 2.31889, 2.33206, 2.34398, 2.35469, 2.36424, 2.37269, 2.38009, 2.38652, 2.39202, 
                         2.39667, 2.40053, 2.40366, 2.40613, 2.408, 2.40932, 2.41015, 2.41054, 2.41054, 2.4102, 2.40956, 2.40866, 2.40754, 2.40624, 
                         2.40479, 2.40321, 2.40155, 2.39981, 2.39803, 2.39622, 2.39441, 2.39262, 2.39087, 2.38916, 2.38752, 2.38596, 2.3845, 2.38313, 
                         2.38189, 2.38077, 2.3798, 2.37898, 2.37831, 2.37782, 2.37751, 2.3774, 2.37749, 2.3778, 2.37834, 2.37911, 2.38015, 2.38145, 
                         2.38303, 2.38491, 2.38711, 2.38964, 2.39251, 2.39576, 2.3994, 2.40345, 2.40792, 2.41283, 2.41821, 2.42406, 2.43039, 2.4372, 
                         2.44448, 2.45222, 2.46037, 2.46889, 2.4777, 2.48671, 2.4958, 2.50485, 2.5137, 2.52218, 2.53014, 2.53742, 2.5439, 2.54946, 
                         2.55405, 2.55765, 2.56029, 2.56202, 2.56295, 2.56318, 2.56285, 2.56209, 2.56101, 2.55974, 2.55837, 2.55699, 2.55566, 2.55443, 
                         2.55334, 2.55241, 2.55166, 2.55109, 2.55069, 2.55045, 2.55037, 2.55042, 2.55058, 2.55085, 2.55122, 2.55166, 2.55208, 2.55242, 
                         2.55262, 2.55266, 2.55249, 2.55208, 2.55141, 2.55044, 2.54916, 2.54754, 2.54557, 2.54324, 2.54054, 2.53749, 2.53408, 2.53035, 
                         2.52632, 2.52204, 2.51755, 2.51292, 2.50822, 2.50355, 2.499, 2.49471, 2.49081, 2.48746, 2.4849, 2.48354, 2.48331, 2.48391, 
                         2.48526, 2.48729, 2.48996, 2.49323, 2.49703, 2.50132, 2.50601, 2.51098, 2.51612, 2.52126, 2.5262, 2.53074, 2.53464, 2.53763, 
                         2.5395, 2.54001, 2.53898, 2.53632, 2.53197, 2.52599, 2.51849, 2.50965, 2.49973, 2.48901, 2.47777, 2.46632, 2.45496, 2.44399, 
                         2.43371, 2.42444, 2.41653, 2.41041, 2.4067, 2.40557, 2.40726, 2.41218, 2.42066, 2.43279, 2.44822, 2.46603, 2.48469, 2.50235,
                           2.51727, 2.52828, 2.53492, 2.53742, 2.53643, 2.53277, 2.52724, 2.52048, 2.51302, 2.50523, 2.49736, 2.48958, 2.482, 2.47468, 
                           2.46766, 2.46093, 2.45452, 2.4484, 2.44256, 2.437, 2.43169, 2.42662, 2.42178, 2.41714, 2.4127, 2.40844, 2.40435, 2.40041, 
                           2.39663, 2.39298, 2.38946, 2.38606, 2.38278, 2.3796, 2.37652, 2.37354, 2.37065, 2.36785, 2.36512, 2.36248, 2.35991, 2.35741, 
                           2.35499, 2.35263, 2.35033, 2.34809, 2.34589, 2.34375, 2.34165, 2.3396, 2.33758, 2.33561, 2.33368, 2.33178, 2.32992, 2.32809, 
                           2.32629, 2.32453, 2.32279, 2.32109, 2.31941, 2.31776, 2.31614, 2.31454, 2.31296, 2.31141, 2.30989, 2.30838, 2.3069, 2.30544, 
                           2.304, 2.30259, 2.30119, 2.29981, 2.29845, 2.29711, 2.29578, 2.29448, 2.29319, 2.29192, 2.29066, 2.28942, 2.2882, 2.287, 
                           2.28581, 2.28464, 2.28348, 2.28233, 2.2812, 2.28009, 2.27898, 2.27789, 2.27681, 2.27575, 2.2747, 2.27365, 2.27263, 2.27161, 
                           2.2706, 2.2696, 2.26862, 2.26764, 2.26668, 2.26572, 2.26478, 2.26384, 2.26292, 2.262, 2.2611, 2.2602, 2.25931, 2.25843, 
                           2.25756, 2.25669, 2.25584, 2.25499, 2.25415, 2.25332, 2.2525, 2.25168, 2.25087, 2.25007, 2.24927, 2.24849, 2.24771, 2.24693, 
                           2.24617, 2.24541, 2.24465, 2.2439, 2.24316, 2.24243, 2.2417, 2.24098, 2.24026, 2.23955, 2.23885, 2.23815, 2.23746, 2.23677, 
                           2.23609, 2.23541, 2.23474, 2.23407, 2.23341, 2.23275, 2.2321, 2.23146, 2.23081, 2.23018, 2.22955, 2.22892, 2.2283, 2.22768, 
                           2.22707, 2.22646, 2.22585, 2.22525, 2.22466, 2.22406, 2.22348, 2.22289, 2.22231, 2.22174, 2.22117, 2.2206, 2.22004, 2.21948, 
                           2.21892, 2.21837, 2.21782, 2.21727, 2.21673, 2.21619, 2.21566, 2.21513, 2.2146, 2.21408, 2.21356, 2.21304, 2.21252, 2.21201, 
                           2.2115, 2.211, 2.2105, 2.21, 2.20951, 2.20901, 2.20852, 2.20804, 2.20755, 2.20707, 2.20659, 2.20612, 2.20565, 2.20518, 2.20471, 
                           2.20424, 2.20378, 2.20333, 2.20287, 2.20241, 2.20196, 2.20151, 2.20107, 2.20062, 2.20018, 2.19974, 2.19931, 2.19887, 2.19844, 
                           2.19801, 2.19758, 2.19716, 2.19674, 2.1931, 2.19223, 2.19136, 2.19051, 2.18967, 2.18883, 2.188, 2.18718, 2.18637, 2.18556, 
                           2.18476, 2.18397, 2.18319, 2.18242, 2.18165, 2.18089, 2.18013, 2.17938, 2.17864, 2.17791, 2.17718, 2.17645, 2.17574, 2.17503, 
                           2.17432, 2.17362, 2.17293, 2.17224, 2.17156, 2.17088, 2.17021, 2.16954, 2.16887, 2.16822, 2.16756, 2.16691, 2.16627, 2.16563, 
                           2.165, 2.16437, 2.16374, 2.16312, 2.1625, 2.16188, 2.16127, 2.16067, 2.16007, 2.15947, 2.15887, 2.15828, 2.15769, 2.15711, 
                           2.15653, 2.15595, 2.15538, 2.15481, 2.15424, 2.15367, 2.15311, 2.15256, 2.152, 2.15145, 2.1509, 2.15035, 2.14981, 2.14927, 
                           2.14873, 2.14819, 2.14766, 2.14713, 2.1466, 2.14607, 2.14555, 2.14503, 2.14451, 2.14399, 2.14348, 2.14297, 2.14246, 2.14195, 
                           2.14145, 2.14094, 2.14044, 2.13994, 2.13944, 2.13895, 2.13846, 2.13796, 2.13747, 2.13699, 2.1365, 2.13602, 2.13553, 2.13505, 
                           2.13457, 2.13409, 2.13362, 2.13314, 2.13267, 2.1322, 2.13173, 2.13126, 2.13079, 2.13033, 2.12986, 2.1294, 2.12894, 2.12848, 
                           2.12802, 2.12756, 2.1271, 2.12665, 2.12619, 2.12574, 2.12529, 2.12484, 2.12439, 2.12394, 2.12349, 2.12304, 2.1226, 2.12215, 
                           2.12171, 2.12127, 2.12083, 2.12039, 2.11995, 2.11951, 2.11907, 2.11863, 2.1182, 2.11776, 2.11733, 2.11689, 2.11646, 2.11603, 
                           2.1156, 2.11517, 2.11474, 2.11431, 2.11388, 2.11345, 2.11302, 2.1126, 2.11217, 2.11174, 2.11132, 2.1109, 2.11047, 2.11005, 
                           2.10963, 2.1092, 2.10878, 2.10836, 2.10794, 2.10752, 2.1071, 2.10668, 2.10626, 2.10585, 2.10543, 2.10501, 2.10459, 2.10418, 
                           2.10376, 2.10335, 2.10293, 2.10251, 2.1021, 2.10168, 2.10127, 2.10086, 2.10044, 2.10003, 2.09962, 2.09921, 2.09879, 2.09838, 
                           2.09797, 2.09756, 2.09715, 2.09673, 2.09632, 2.09591, 2.0955, 2.09509, 2.09468, 2.09427, 2.09386, 2.09345, 2.09304, 2.09263, 
                           2.09222, 2.09181, 2.09141, 2.091, 2.09059] 
                    
                    k_index = [1.16012, 1.14322, 1.12573, 1.10778, 1.08948, 1.07096, 1.05231, 1.03364, 1.01503, 0.99659, 0.97837, 0.96045, 0.94289, 
                               0.92574, 0.90903, 0.89281, 0.8771, 0.86193, 0.8473, 0.83323, 0.81973, 0.80679, 0.79442, 0.78261, 0.77136, 0.76065, 0.75048, 
                               0.74083, 0.7317, 0.72306, 0.7149, 0.70722, 0.69998, 0.69319, 0.68681, 0.68085, 0.67528, 0.67009, 0.66527, 0.6608, 0.65666, 
                               0.65285, 0.64936, 0.64616, 0.64326, 0.64063, 0.63826, 0.63616, 0.63429, 0.63266, 0.63125, 0.63005, 0.62905, 0.62824, 0.6276, 
                               0.62713, 0.62681, 0.62662, 0.62655, 0.62658, 0.62669, 0.62686, 0.62706, 0.62725, 0.6274, 0.62748, 0.62743, 0.6272, 0.62673, 
                               0.62596, 0.6248, 0.62318, 0.62102, 0.61822, 0.61471, 0.6104, 0.60524, 0.59917, 0.59218, 0.58428, 0.57553, 0.56601, 0.55585, 
                               0.54521, 0.53426, 0.52318, 0.51215, 0.50134, 0.49088, 0.48087, 0.47139, 0.46247, 0.45413, 0.44636, 0.43911, 0.43235, 0.42602, 
                               0.42006, 0.41441, 0.40902, 0.40382, 0.39876, 0.3938, 0.38888, 0.38398, 0.37906, 0.37409, 0.36905, 0.3639, 0.35857, 0.35302, 
                               0.34729, 0.34136, 0.33529, 0.32907, 0.32274, 0.31633, 0.30986, 0.30338, 0.29693, 0.29054, 0.28428, 0.27818, 0.27231, 0.26673, 
                               0.26149, 0.25665, 0.25228, 0.24843, 0.24515, 0.2425, 0.24051, 0.23922, 0.23865, 0.23881, 0.23969, 0.24127, 0.24332, 0.24519, 
                               0.2468, 0.2481, 0.24902, 0.24952, 0.24949, 0.24887, 0.24755, 0.24544, 0.24244, 0.23845, 0.23341, 0.22726, 0.21998, 0.21159, 
                               0.20217, 0.19188, 0.18092, 0.16955, 0.15809, 0.14687, 0.13626, 0.12657, 0.11811, 0.11111, 0.10576, 0.10219, 0.10048, 0.10067, 
                               0.10277, 0.10675, 0.11259, 0.12022, 0.12956, 0.14026, 0.15174, 0.16373, 0.17569, 0.18686, 0.19614, 0.20228, 0.20404, 0.20062, 
                               0.1919, 0.17864, 0.1622, 0.14421, 0.1261, 0.10895, 0.09339, 0.07967, 0.06782, 0.05772, 0.04918, 0.04197, 0.03591, 0.03081, 
                               0.02651, 0.02288, 0.0198, 0.01718, 0.01495, 0.01304, 0.01141, 0.01, 0.00879, 0.00774, 0.00683, 0.00604, 0.00536, 0.00476, 
                               0.00424, 0.00378, 0.00338, 0.00303, 0.00273, 0.00246, 0.00223, 0.00203, 0.00185, 0.0017, 0.00157, 0.00146, 0.00136, 0.00128, 
                               0.00121, 0.00115, 0.00109, 0.00103, 0.000973, 0.000918, 0.000865, 0.000813, 0.000764, 0.000716, 0.00067, 0.000625, 0.000582, 
                               0.000541, 0.000502, 0.000464, 0.000428, 0.000393, 0.00036, 0.000329, 0.000299, 0.000271, 0.000244, 0.000219, 0.000195, 
                               0.000172, 0.000151, 0.000132, 0.000114, 9.7e-05, 8.2e-05, 6.8e-05, 5.5e-05, 4.4e-05, 3.4e-05, 2.5e-05, 1.8e-05, 1.2e-05, 7e-06, 3e-06, 1e-06, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

                # Method that calculates the refractive indices of the metals by linear interpolation
                # using the points contained in X, n e k_index previously described
                n_interp = interp(Lambda_i, X, n)
                k_interp = interp(Lambda_i, X, k_index)
                n = complex(n_interp, k_interp)
            
            elif material == 17:    # TiO2
                w = wi
                h = 4.13566743*1E-15    #eV
                c = 300000000   # m/s
                Ak = 101 # eV² 
                Bk = 1.2 # eV
                Ek = 6.2 # eV
                e_inf = 1
                j = complex(0,1)

                E_i = (h*c)/w

                e_TiO2 = e_inf + (Ak/(Ek**2 - E_i**2 - j*Bk*E_i))
                
                n = sqrt(e_TiO2)

            elif material == 18:    #ZnO
                w = wi
                c = 299792458   # m/s
                w = 2*pi*c / w
                e_inf = 3.4
                wp = 2*1E15
                gamma = 1.5*1E14
                j = complex(0,1)

                e_ZnO = e_inf - (wp**2)/(w**2 + gamma**2) + j*(gamma*wp**2)/((w**2 + gamma**2)*w)

                n = sqrt(e_ZnO)

            # Refractive index of the Water
            elif material == 19:
                n = 1.33

            # Refractive index of the Air
            elif material == 20:    #Air
                n = 1.0000

            # Refractive index of the LiF (Lithium Fluoride) according to the RefractiveIndex.info:
            # https://refractiveindex.info/
            elif material == 21:    #LiF
                B1, B2, B3, C1, C2, C3 = 0.92549, 6.96747, 0, 5.4405376E-3, 1075.1841, 0
                n = sqrt(1 + ((B1 * Lambda_i ** 2) / (Lambda_i ** 2 - C1)) + ((B2 * Lambda_i ** 2) / (Lambda_i ** 2 - C2))
                        + ((B3 * Lambda_i ** 2) / (Lambda_i ** 2 - C3)))

            elif material == 22:  # Cytop
                # According to the AGC chemicals company. Available in:
                # https://www.agc-chemicals.com/jp/en/fluorine/products/cytop/download/index.html
                X = [0.2, 2]

                n_cy = [1.34, 1.34]

                # Method that calculates the refractive indices of the metals by linear interpolation
                # using the points contained in X, n e k_index previously described
                n = complex(interp(Lambda_i, X, n_cy))


            self.real_part_index.setText(str(round(real(n), 5))) 
            self.imaginary_part_index.setText(str(round(imag(n), 5))) 

    def add_layers(self):
        try:
            if INTERROGATION_MODE == 1: #AIM
                material = self.cbox_material.currentText()
                thickness = self.thickness.text().replace(',','.')
                description = self.description.text()
                real = float(self.real_part_index.text().replace(',','.'))
                imag = float(self.imaginary_part_index.text().replace(',','.'))
                refractiveIndex = str(complex(real, imag)).replace('(',' ').replace(')',' ')
                
                self.material.append(material)
                self.material_id.append(self.cbox_material.currentIndex())
                self.d.append(float(thickness)*1e-9)
                self.indexRef.append(complex(real, imag))

                self.layers.append({"material": material, "thickness": thickness, "refractiveIndex": refractiveIndex, "description": description })
        
            else:   # WIM
                material = self.cbox_material_2.currentText()
                thickness = self.thickness_2.text().replace(',','.')
                description = self.description_2.text()
                
                self.material.append(material)
                self.material_id.append(self.cbox_material_2.currentIndex())
                self.d.append(float(thickness)*1e-9)
                self.indexRef.append(complex(0,0))
                
                self.layers.append({"material": material, "thickness": thickness, "refractiveIndex": '-', "description": description })
            
        except:
            self.warning.setHidden(False)
            if self.material != []:
                self.material.pop(-1)
                self.material_id.pop(-1)
            self.warning.setText(QtCore.QCoreApplication.translate("Widget", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:400; color:#d41010;\">* Fill in all required fields * </span></p></body></html>", None))

            if not self.thickness.text().isnumeric():
                self.thickness.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
            if not self.thickness_2.text().isnumeric():
                self.thickness_2.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
            if not self.imaginary_part_index.text().isnumeric():
                self.imaginary_part_index.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
            if not self.real_part_index.text().isnumeric():
                self.real_part_index.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
        
        self.nLayers = len(self.layers)

        self.show_layers()

        self.thickness.setText("")
        self.thickness_2.setText("")
        self.real_part_index.setText("")
        self.imaginary_part_index.setText("")
        self.description.setText("")
        self.description_2.setText("")

        if self.nLayers>0:
            self.btn_remove_layers.setEnabled(True)
            self.btn_remove_layers.setStyleSheet(u"QPushButton{\n"
                                             "	font: 400 11pt \"Ubuntu\";\n"
                                             "	color: rgb(255, 255,255);\n"
                                             "	background-color: rgb(0, 130, 180);\n"
                                             "	border-color: rgb(0, 100, 130);\n"
                                             "	border-width: 2px;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:hover{\n"
                                             "	background-color: rgb(200, 200, 70);\n"
                                             "	border-color: rgb(0, 120, 40);\n"
                                             "	width: 40;\n"
                                             "	height: 35;\n"
                                             "}")
            
            self.btn_edit_layers.setEnabled(True)
            self.btn_edit_layers.setStyleSheet(u"QPushButton{\n"
                                             "	font: 400 11pt \"Ubuntu\";\n"
                                             "	color: rgb(255, 255,255);\n"
                                             "	background-color: rgb(0, 130, 180);\n"
                                             "	border-color: rgb(0, 100, 130);\n"
                                             "	border-width: 2px;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:hover{\n"
                                             "	background-color: rgb(200, 200, 70);\n"
                                             "	border-color: rgb(0, 120, 40);\n"
                                             "	width: 40;\n"
                                             "	height: 35;\n"
                                             "}")

    def add_analyte(self):
        try:
            if INTERROGATION_MODE == 1: # AIM mode
                initial_index_analyte = self.Analyte_refractive_index.value()
                n_sample_analyte = self.n_sample_analyte.value()
                step_analyte = round(self.step_analyte.value(), 5)
                thickness = self.thickness_4.text().replace(',','.')
                description = self.description_3.text()
            
            else:   # WIM mode
                initial_index_analyte = self.Analyte_refractive_index_wim.value()
                n_sample_analyte = self.n_sample_analyte_wim.value()
                step_analyte = round(self.step_analyte_wim.value(),5)
                thickness = self.thickness_3.text().replace(',','.')
                description = self.description_4.text()
                        
            self.material.append("Analyte")
            self.material_id.append(19)
            self.d.append(float(thickness)*1e-9)
            self.indexRef.append(complex(initial_index_analyte, 0))
            
            for i in arange(n_sample_analyte):
                indice = initial_index_analyte + (i * step_analyte)
                self.index_ref_analyte.append(complex(round(indice, 4)))

            refractiveIndex = f"{round(initial_index_analyte,4)} - {round(real(self.index_ref_analyte[-1]),4)}" 

            self.layers.append({"material": "Analyte", "thickness": thickness, "refractiveIndex": refractiveIndex, "description": description })
            
            self.nLayers = len(self.layers)
        except:
            self.warning.setHidden(False)
            if self.material != []:
                self.material.pop(-1)
                self.material_id.pop(-1)
            self.warning.setText(QtCore.QCoreApplication.translate("Widget", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:400; color:#d41010;\">* Fill in all required fields *</span></p></body></html>", None))
            if not self.thickness_3.text().isnumeric():
                self.thickness_3.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
            if not self.thickness_4.text().isnumeric():
                self.thickness_4.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
        
        self.show_layers()

        self.description_3.setText("")
        self.thickness_4.setText("")
        self.description_4.setText("")
        self.thickness_3.setText("")


        if self.nLayers>0:
            self.btn_remove_layers.setEnabled(True)
            self.btn_remove_layers.setStyleSheet(u"QPushButton{\n"
                                             "	font: 400 11pt \"Ubuntu\";\n"
                                             "	color: rgb(255, 255,255);\n"
                                             "	background-color: rgb(0, 130, 180);\n"
                                             "	border-color: rgb(0, 100, 130);\n"
                                             "	border-width: 2px;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:hover{\n"
                                             "	background-color: rgb(200, 200, 70);\n"
                                             "	border-color: rgb(0, 120, 40);\n"
                                             "	width: 40;\n"
                                             "	height: 35;\n"
                                             "}")

            self.btn_edit_layers.setEnabled(True)
            self.btn_edit_layers.setStyleSheet(u"QPushButton{\n"
                                             "	font: 400 11pt \"Ubuntu\";\n"
                                             "	color: rgb(255, 255,255);\n"
                                             "	background-color: rgb(0, 130, 180);\n"
                                             "	border-color: rgb(0, 100, 130);\n"
                                             "	border-width: 2px;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:hover{\n"
                                             "	background-color: rgb(200, 200, 70);\n"
                                             "	border-color: rgb(0, 120, 40);\n"
                                             "	width: 40;\n"
                                             "	height: 35;\n"
                                             "}")

    def remove_layers(self):
        index_remove = self.tableWidget_layers.currentRow()
        if index_remove>=0:
            self.layers.pop(index_remove)
            
            if self.material[index_remove]=='Analyte':
                self.index_ref_analyte.pop(-1)
            
            self.material.pop(index_remove)
            self.material_id.pop(index_remove)
            self.d.pop(index_remove)
            self.indexRef.pop(index_remove)
            self.show_layers()
            self.nLayers = len(self.layers)
            
            if self.nLayers<1:
                self.btn_remove_layers.setEnabled(False)
                self.btn_remove_layers.setStyleSheet(u"QPushButton{\n"
                                            "	font: 400 11pt \"Ubuntu\";\n"
                                            "	color: rgb(255, 255,255);\n"
                                            "	background-color: #606060;\n"
                                            "	border-color: rgb(0, 100, 130);\n"
                                            "	border-width: 2px;\n"
                                            "	border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "	background-color: rgb(00, 140, 70);\n"
                                            "	border-color: rgb(0, 120, 40);\n"
                                            "	width: 40;\n"
                                            "	height: 35;\n"
                                            "}")
                
                self.btn_edit_layers.setEnabled(False)
                self.btn_edit_layers.setStyleSheet(u"QPushButton{\n"
                                            "	font: 400 11pt \"Ubuntu\";\n"
                                            "	color: rgb(255, 255,255);\n"
                                            "	background-color: #606060;\n"
                                            "	border-color: rgb(0, 100, 130);\n"
                                            "	border-width: 2px;\n"
                                            "	border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "	background-color: rgb(00, 140, 70);\n"
                                            "	border-color: rgb(0, 120, 40);\n"
                                            "	width: 40;\n"
                                            "	height: 35;\n"
                                            "}")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
        
            msg.setText("Select the layer to be deleted!")
            
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QtGui.QIcon('icons/LOGO.png'))
            msg.setStandardButtons(QMessageBox.Ok)
            
            retval = msg.exec_()

    def select_edit_layer(self):
        index_select = self.tableWidget_layers.currentRow()

        if index_select>=0:
            layer_edit = self.layers[index_select]
            if self.material[index_select]=='Analyte':
                self.set_Enable_True_2()
                if INTERROGATION_MODE == 1: # AIM mode
                    self.Analyte_refractive_index.setValue(real(self.index_ref_analyte[0]))
                    self.n_sample_analyte.setValue(len(self.index_ref_analyte))
                    self.step_analyte.setValue(real((self.index_ref_analyte[1])-(self.index_ref_analyte[0])))
                    self.thickness_4.setText(layer_edit["thickness"])
                    self.description_3.setText(layer_edit["description"])

                    self.btn_add_analyte.setEnabled(False)
                    self.btn_add_analyte.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: #606060;\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
                    self.btn_confirm_edit_2.setEnabled(True)
                    self.btn_confirm_edit_2.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: rgb(0, 130, 180);\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
                else:
                    self.Analyte_refractive_index_wim.setValue(real(self.index_ref_analyte[0]))
                    self.n_sample_analyte_wim.setValue(len(self.index_ref_analyte))
                    self.step_analyte_wim.setValue(real((self.index_ref_analyte[1])-(self.index_ref_analyte[0])))
                    self.thickness_3.setText(layer_edit["thickness"])
                    self.description_4.setText(layer_edit["description"])

                    self.btn_add_analyte_2.setEnabled(False)
                    self.btn_add_analyte_2.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: #606060;\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
                    self.btn_confirm_edit_4.setEnabled(True)
                    self.btn_confirm_edit_4.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: rgb(0, 130, 180);\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")

            else:
                self.set_Enable_True()

                if INTERROGATION_MODE == 1: # AIM mode
                    self.cbox_material.setCurrentText(layer_edit["material"])
                    self.thickness.setText(layer_edit["thickness"])
                    self.description.setText(layer_edit["description"])

                    if layer_edit["material"] == "Custom":
                        self.real_part_index.setEnabled(True)
                        self.imaginary_part_index.setEnabled(True)
                    
                    self.real_part_index.setText(f"{real(complex(layer_edit['refractiveIndex']))}")
                    self.imaginary_part_index.setText(f"{imag(complex(layer_edit['refractiveIndex']))}")

                    self.btn_new_layer.setEnabled(False)
                    self.btn_new_layer.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: #606060;\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
                    self.btn_add_layer.setEnabled(False)
                    self.btn_add_layer.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: #606060;\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
                    self.btn_confirm_edit.setEnabled(True)
                    self.btn_confirm_edit.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: rgb(0, 130, 180);\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
                
                else:   #WIM mode
                    self.cbox_material_2.setCurrentText(layer_edit["material"])
                    self.thickness_2.setText(layer_edit["thickness"])
                    self.description_2.setText(layer_edit["description"])

                    self.btn_new_layer_2.setEnabled(False)
                    self.btn_new_layer_2.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: #606060;\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
                    self.btn_add_layer_2.setEnabled(False)
                    self.btn_add_layer_2.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: #606060;\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
                    self.btn_confirm_edit_3.setEnabled(True)
                    self.btn_confirm_edit_3.setStyleSheet(u"QPushButton{\n"
                                                "	font: 400 11pt \"Ubuntu\";\n"
                                                "	color: rgb(255, 255,255);\n"
                                                "	background-color: rgb(0, 130, 180);\n"
                                                "	border-color: rgb(0, 100, 130);\n"
                                                "	border-width: 2px;\n"
                                                "	border-radius:10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "	background-color: rgb(00, 140, 70);\n"
                                                "	border-color: rgb(0, 120, 40);\n"
                                                "	width: 40;\n"
                                                "	height: 35;\n"
                                                "}")
        
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Select the layer to be edited!")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def edit_layer(self):
        try:
            index_select = self.tableWidget_layers.currentRow()
            if INTERROGATION_MODE == 1: #AIM
                material = self.cbox_material.currentText()
                thickness = self.thickness.text().replace(',','.')
                description = self.description.text()
                real = float(self.real_part_index.text().replace(',','.'))
                imag = float(self.imaginary_part_index.text().replace(',','.'))
                refractiveIndex = str(complex(real, imag)).replace('(',' ').replace(')',' ')
                
                self.material[index_select] = material
                self.material_id[index_select] = self.cbox_material.currentIndex()
                self.d[index_select] = float(thickness)*1e-9
                self.indexRef[index_select] = complex(real, imag)
                
                self.layers[index_select] = {"material": material, "thickness": thickness, "refractiveIndex": refractiveIndex, "description": description }
            
            else: #WIM
                material = self.cbox_material_2.currentText()
                thickness = self.thickness_2.text().replace(',','.')
                description = self.description_2.text()
                
                self.material[index_select] = material
                self.material_id[index_select] = self.cbox_material_2.currentIndex()
                self.d[index_select] = float(thickness)*1e-9
                self.indexRef[index_select] = complex(0, 0)
                
                self.layers[index_select] = {"material": material, "thickness": thickness, "refractiveIndex": "-", "description": description }
        except:
            self.warning.setHidden(False)
            self.warning.setText(QtCore.QCoreApplication.translate("Widget", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:400; color:#d41010;\">* Fill in all required fields *</span></p></body></html>", None))
            if not self.thickness.text().isnumeric():
                self.thickness.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
            if not self.thickness_2.text().isnumeric():
                self.thickness_2.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
            if not self.imaginary_part_index.text().isnumeric():
                self.imaginary_part_index.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
            if not self.real_part_index.text().isnumeric():
                self.real_part_index.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")

        self.show_layers()

        self.thickness.setText("")
        self.thickness_2.setText("")
        self.real_part_index.setText("")
        self.imaginary_part_index.setText("")
        self.description.setText("")
        self.description_2.setText("")

    def edit_analyte(self):
        try: 
            index_select = self.tableWidget_layers.currentRow()
            if INTERROGATION_MODE == 1: # AIM mode
                initial_index_analyte = self.Analyte_refractive_index.value()
                n_sample_analyte = self.n_sample_analyte.value()
                step_analyte = round(self.step_analyte.value(), 5)
                thickness = self.thickness_4.text().replace(',','.')
                description = self.description_3.text()
            else: #WIM
                initial_index_analyte = self.Analyte_refractive_index_wim.value()
                n_sample_analyte = self.n_sample_analyte_wim.value()
                step_analyte = round(self.step_analyte_wim.value(),5)
                thickness = self.thickness_3.text().replace(',','.')
                description = self.description_4.text()

            refractiveIndex = f"{round(initial_index_analyte,4)} - {round(n_sample_analyte,4)}" 
                            
            self.d[index_select] = float(thickness)*1e-9
            self.indexRef[index_select] = complex(initial_index_analyte, 0)

            indices = []

            for i in arange(n_sample_analyte):
                indices.append(initial_index_analyte + (i * step_analyte))
            
            indices = vectorize(lambda indices: complex(round(indices,4)))(indices)
            
            refractiveIndex = f"{round(initial_index_analyte,4)} - {round(real(indices[-1]),4)}" 
            
            self.index_ref_analyte = list(indices)
            self.layers[index_select] = {"material": "Analyte", "thickness": thickness, "refractiveIndex": refractiveIndex, "description": description }

        except:
            self.warning.setHidden(False)
            self.warning.setText(QtCore.QCoreApplication.translate("Widget", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:400; color:#d41010;\">* Fill in all required fields *</span></p></body></html>", None))
            if not self.thickness_3.text().isnumeric():
                self.thickness_3.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
            if not self.thickness_4.text().isnumeric():
                self.thickness_4.setStyleSheet(u" padding: 1px 18px 1px 3px;\n"
                                     "color: #aa0000;\n"
                                     "font: 700 12pt \"Ubuntu\";\n"
                                     " border: 2px solid;\n"
                                     "border-color: #aa0000;\n"
                                     "background-color: rgba(255, 255, 255,210);\n"
                                     "border-radius:10px;")
        
        self.show_layers()

        self.description_3.setText("")
        self.thickness_4.setText("")
        self.description_4.setText("")
        self.thickness_3.setText("")

    def change_spinbox(self, spin, slider):
        spin.setValue(float(slider.value()/10))
    
    def change_slider(self, spin, slider):
        slider.setValue(int(spin.value()*10))

    def change_range_slider(self, spin1, spin2, slider, label_warning):
        if spin2.value() <= spin1.value():
            label_warning.setHidden(False)
        else:
            label_warning.setHidden(True)
        slider.setValue((float(spin1.value()), float(spin2.value())))
    
    def change_range_slider2(self, spin1, spin2, slider, label_warning):
        if spin2.value() <= spin1.value():
            label_warning.setHidden(False)
        else:
            label_warning.setHidden(True)
        a0 = (spin1.value(), slider.value()[1])
        slider.setValue(a0)

    def change_range_spin(self, spin1, spin2, slider):
        spin1.setValue(float(slider.value()[0]))
        spin2.setValue(float(slider.value()[1]))

    def show_layers(self):
        self.tableWidget_layers.setRowCount(len(self.layers))
        for row, text in enumerate(self.layers):
            for column, data in enumerate(text):
                self.tableWidget_layers.setItem(row, column, QtWidgets.QTableWidgetItem(str(text[f'{data}'])))

    def start_simulation(self):
        self.progressBar.setHidden(False)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer_interval = 100  # Interval in miliseconds

        self.progress_value = 0
        self.progressBar.setValue(0)
        self.timer.start(self.timer_interval)
        
        self.Reflectance_ = []
        self.Resonance_Point = []
        self.sensibility = []
        self.critical_point = []
        self.Rmin = []  
        self.Fwhm = []
        self.fom = []
        self.da = []
        self.textBrowser.setText("Calculating...")

        polarization = "TM" if self.TM_polarization.isChecked() else "TE"
        
        self.init = time.perf_counter()

        if INTERROGATION_MODE == 1:
            self.reflectance_AIM(polarization)
        else:
            self.reflectance_WIM(polarization)
        
        self.final = time.perf_counter()
        self.show_graphs(polarization)
        self.btn_export_data.setEnabled(True)
        self.btn_export_data.setStyleSheet(u"QPushButton{\n"
                                            "	font: 400 11pt \"Ubuntu\";\n"
                                            "	color: rgb(255, 255,255);\n"
                                            "	background-color: rgba(0, 130, 180,160);\n"
                                            "	border-color: rgba(0, 100, 130,160);\n"
                                            "	border-width: 2px;\n"
                                            "	border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "	background-color: rgb(0, 130, 180);\n"
                                            "	width: 40;\n"
                                            "	height: 35;\n"
                                            "}")
        
        self.progress_value = 100
        self.progressBar.setValue(self.progress_value)
        QtWidgets.QApplication.processEvents()
        self.timer.stop()

    def update_progress(self):
        self.progressBar.setValue(self.progress_value)

    def reflectance_AIM(self, pol):
        global STEP
        STEP = 0.001*(pi/180)
        lambda_i = self.lambda_i.value()*1E-9
        a1 = self.a1_3.value()*(pi/180)
        a2 = self.a2_3.value()*(pi/180)
        theta_i = arange(a1, a2, STEP)
        
        for index_analyte in self.index_ref_analyte:
            layer_analyte = self.material.index('Analyte')
            self.indexRef[layer_analyte] = index_analyte
            self.textBrowser.append(f"Calculating for the analyte {index_analyte.real} RIU...")

            # It calculates the critical angle of attenuated total reflection
            self.critical_point.append(round(abs(arcsin(index_analyte / self.indexRef[0]) * (180 / pi)), 3))

            R_i = []

            for t in range(len(theta_i)):
                r_ = self.Reflectance(self.indexRef, theta_i[t], lambda_i, pol)
                R_i.append(r_)

                self.progress_value = int((t + 1) * 100 / len(theta_i))     
                QtWidgets.QApplication.processEvents()  # Atualiza a interface gráfica           

            self.Resonance_Point.append(round(self.Point_LMR(theta_i, R_i), 6))
            
            self.Reflectance_.append(R_i)

            self.Rmin.append(min(R_i))

            self.sensibility_graph(index_analyte)

            self.Fwhm.append(self.calc_FWHM(R_i, theta_i))

        self.indexRef[layer_analyte]=self.index_ref_analyte[0]

        for s in range(len(self.index_ref_analyte)):
            self.fom.append(round(abs(self.sensibility[s] / self.Fwhm[s]), 6))
            self.da.append(1/self.Fwhm[s])

    def sensibility_graph(self, index_analyte):
        # Sensibility obtained from the graph
            # It calculates the angular sensitivity (Resonance point variation)/(Refractive index variation)
        if index_analyte == self.index_ref_analyte[0]:
            # The first interaction is initialized to zero because the ratio would be 0/0
            self.sensibility.append(0)

        else:
            # Resonance point variation
            delta_X = abs(self.Resonance_Point[-2] - self.Resonance_Point[-1])
            # Refractive index variation
            delta_index = abs(self.index_ref_analyte[-2] - self.index_ref_analyte[-1])
            # Only after the second interaction is sensitivity considered.
            self.sensibility.append(round((delta_X / delta_index), 6))

            self.sensibility[0] = self.sensibility[1]
    
    def Point_LMR(self, axis_x, reflectance):
        # The method self.Point_LMR() returns the resonance point of the curve
        try:
            id_min = reflectance.index(min(reflectance))  # Position of the minimum point of the curve

            if INTERROGATION_MODE == 1:
               
                critical_point = self.critical_point[-1]

                list_x = asarray(axis_x)
                idx = (abs(list_x - (critical_point * pi / 180))).argmin()

                reflect_right_critical_point = reflectance[idx:-1]
                id_min = reflectance.index(min(reflect_right_critical_point))
                resonance_point = axis_x[id_min] * (180 / pi)

                return resonance_point  # Returns the angle in degrees
            else: 
                return axis_x[id_min] * 1E9  # Returns the wavelength in nanometers
        
        except ValueError:
            self.textBrowser.setText("---------------------- {!} ---------------------- "
                  "\nThere is no resonance in the specified range."
                  "\nGenerated value does not match the real value\n"
                  "------------------------------------------------- ")
            return -1 # Returns the angle in degrees

    def reflectance_WIM(self, pol):
        global STEP
        STEP = 0.1*1E-9
        theta_i = self.angle_incidence.value()*(pi/180)
        a1 = self.a1_2.value()*1E-9
        a2 = self.a2_2.value()*1E-9
        lambda_i = arange(a1, a2, STEP)

        for index_analyte in self.index_ref_analyte:
            layer_analyte = self.material.index('Analyte')
            self.textBrowser.append(f"Calculating for the analyte {index_analyte.real} RIU...")

            R_i = []

            for t in range(len(lambda_i)):
                self.indexRef = []  # Reset of refractive index for each wavelength

                for m in range(self.nLayers):  # Calculation of the new refractive index for each material
                    self.set_RefractiveIndex(self.material_id[m], lambda_i[t])
                    real = float(self.real_part_index.text().replace(',','.'))
                    imag = float(self.imaginary_part_index.text().replace(',','.'))
                    self.indexRef.append(complex(real,imag))
                self.indexRef[layer_analyte] = index_analyte
                
                r_ = self.Reflectance(self.indexRef, theta_i, lambda_i[t], pol)
                R_i.append(r_)

                self.progress_value = int((t + 1) * 100 / len(lambda_i)) 
                QtWidgets.QApplication.processEvents()  # Atualiza a interface gráfica
            
            self.Resonance_Point.append(round(self.Point_LMR(lambda_i, R_i), 6))
           
            self.Reflectance_.append(R_i)

            self.Rmin.append(min(R_i))

            self.sensibility_graph(index_analyte)

            self.Fwhm.append(self.calc_FWHM(R_i, lambda_i))

        for s in range(len(self.index_ref_analyte)):
            self.fom.append(abs(self.sensibility[s] / self.Fwhm[s]))
            self.da.append(1/self.Fwhm[s])
    
    def Reflectance(self, index, theta_i, wavelenght, pol):
        """ The numerical model is based on the attenuated total reflection method combined with the transfer matrix
            method for a multilayer system according to:
            * PALIWAL, N.; JOHN, J. Lossy mode resonance based fiber optic sensors. In: Fiber Optic Sensors.
            [S_TM.l.]: Springer, 2017. p. 31-50. DOI : 10.1007/978-3-319-42625-9_2."""

        j = complex(0, 1)  # Simplification for the complex number "j"
        k0 = (2 * pi) / wavelenght  # Wave number

        b = []  # b_j -> Phase shift in each layer
        q = []  # q_j -> Admittance in TM polarization

        Transfer_Matrix = []  # Transfer_Matrix_j -> Transfer matrix between each layer - TM polarization

        for layer in range(self.nLayers):
            y = sqrt((index[layer] ** 2) - ((index[0] * sin(theta_i)) ** 2))

            b.append(k0 * self.d[layer] * y)
            if pol == "TM":
                q.append(y / index[layer] ** 2)
            else:
                q.append(y)

            # Total Transfer Matrix
            if layer < (self.nLayers - 1):
                Transfer_Matrix.append(array([[cos(b[layer]), (-j / q[layer]) * sin(b[layer])],
                                   [-j * q[layer] * sin(b[layer]), cos(b[layer])]]))
                
        Total_Transfer_Matrix = Transfer_Matrix[0]  # Total_Transfer_Matrix -> Total Transfer Matrix 
        
        for k in range(self.nLayers - 2):
            Total_Transfer_Matrix = Total_Transfer_Matrix @ Transfer_Matrix[k + 1]

        num = (Total_Transfer_Matrix[0][0] + Total_Transfer_Matrix[0][1] * q[self.nLayers - 1]) * q[0] - (Total_Transfer_Matrix[1][0] + Total_Transfer_Matrix[1][1] * q[self.nLayers - 1])
        den = (Total_Transfer_Matrix[0][0] + Total_Transfer_Matrix[0][1] * q[self.nLayers - 1]) * q[0] + (Total_Transfer_Matrix[1][0] + Total_Transfer_Matrix[1][1] * q[self.nLayers - 1])

        r = num / den # 'r'-> Fresnel reflection coefficient 
            
        return float(abs(r) ** 2) # Reflectance
    
    def show_graphs(self, pol):
        graph = self.select_graphs.currentText()
        
        if INTERROGATION_MODE == 1:
            a1 = self.a1_3.value()*(pi/180) 
            a2 = self.a2_3.value()*(pi/180) 
            theta_i = arange(a1, a2, STEP)    

            self.ax_x =  theta_i* (180 / pi) 
            self.simbols = ("Angle", chr(952), "°")
        else:
            a1 = self.a1_2.value()*1E-9
            a2 = self.a2_2.value()*1E-9
            lambda_i = arange(a1, a2, STEP)

            self.ax_x = lambda_i*1E9
            self.simbols = ("Wavelength", chr(955), "nm")
        
        font=dict(size=5, family="Sans-Serif")
        plt.rc('font', **font)

        plt.subplots_adjust(left=0.160,
            bottom=0.195, 
            right=0.930, 
            top=0.950, 
            wspace=0.1, 
            hspace=0.2)
        
        match graph:
            case "Reflectance":
                self.figure_.clear()
                ax = self.figure_.add_subplot()
                if INTERROGATION_MODE == 1:
                    text = f"{self.simbols[1]}$_C$ = {self.critical_point[0]:.4f} {self.simbols[2]}"
                    x = self.Reflectance(self.indexRef, self.critical_point[0]*pi/180, self.lambda_i.value()*1E-9, pol)
                    ax.annotate(text=text, xy=(self.critical_point[0], x), xytext=(self.a1_3.value(), 0.6),bbox=dict(boxstyle="round4", fc="w"), arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=-0.2",))

                ax.plot(self.ax_x, self.Reflectance_[0])
                ax.grid(True, alpha=0.3)
                ax.set_xlabel(f'Incidence {self.simbols[0]} ({self.simbols[2]})', fontdict=font)
                ax.set_ylabel('Reflectance', fontdict=font)
                ax.set_yticks(arange(0, 1.20, 0.20))
                
                self.canvas_.draw() 
        
            case "FWHM vs. Analyte":
                self.figure_.clear()
                ax = self.figure_.add_subplot()

                plt.subplots_adjust(left=0.210,
                                    bottom=0.285, 
                                    right=0.900, 
                                    top=0.960, 
                                    wspace=0.1, 
                                    hspace=0.2)
                ax.tick_params(labelsize=5, labelrotation=45)
                
                ax.plot(real(self.index_ref_analyte), self.Fwhm, '-o', markersize=3)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('Analyte (RIU)', fontdict=font)
                ax.set_ylabel(f'FWHM ({self.simbols[2]})', fontdict=font)
                ax.set_yticks(self.Fwhm)
                ax.set_xticks(real(self.index_ref_analyte))
                self.canvas_.draw()
        
            case "Reflectance vs. Analyte":
                self.figure_.clear()
                ax = self.figure_.add_subplot()
                legend = list()
                for i in range(len(self.index_ref_analyte)):
                    ax.plot(self.ax_x, self.Reflectance_[i])
                    legend.append(fr"{self.index_ref_analyte[i].real:.3f}")
                ax.grid(True, alpha=0.3)
                ax.legend(legend, fontsize=6)
                ax.set_xlabel(f'Incidence {self.simbols[0]} ({self.simbols[2]})', fontdict=font)
                ax.set_ylabel('Reflectance', fontdict=font)
                ax.set_yticks(arange(0, 1.20, 0.20))
                self.canvas_.draw()
        
            case "Resonance point vs. Analyte":
                self.figure_.clear()
                ax = self.figure_.add_subplot()
                ax.tick_params(labelsize=5, labelrotation=45)
                
                plt.subplots_adjust(left=0.210,
                                    bottom=0.285, 
                                    right=0.900, 
                                    top=0.960, 
                                    wspace=0.1, 
                                    hspace=0.2)

                ax.plot(real(self.index_ref_analyte), self.Resonance_Point, '-o', markersize=3 )
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('Analyte (RIU)', fontdict=font)
                ax.set_ylabel(f'Resonance {self.simbols[0]} ({self.simbols[2]})', fontdict=font)
                ax.set_yticks(self.Resonance_Point)
                ax.set_xticks(real(self.index_ref_analyte))
                self.canvas_.draw()
                                
            case "Sensibility vs. Analyte":
                self.figure_.clear()
                ax = self.figure_.add_subplot()
                ax.tick_params(labelsize=5, labelrotation=45)
                
                plt.subplots_adjust(left=0.210,
                                    bottom=0.285, 
                                    right=0.900, 
                                    top=0.960, 
                                    wspace=0.1, 
                                    hspace=0.2)
    
                ax.plot(real(self.index_ref_analyte), self.sensibility, '-o', markersize=3)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('Analyte (RIU)', fontdict=font)
                ax.set_ylabel(f'Sensibility ({self.simbols[2]} RI$U^-$$^1$)', fontdict=font)
                ax.set_yticks(self.sensibility)
                ax.set_xticks(real(self.index_ref_analyte))
                self.canvas_.draw()
        
            case "Quality Factor vs. Analyte":
                self.figure_.clear()
                ax = self.figure_.add_subplot()
                ax.tick_params(labelsize=5, labelrotation=45)

                plt.subplots_adjust(left=0.210,
                                    bottom=0.285, 
                                    right=0.900, 
                                    top=0.960, 
                                    wspace=0.1, 
                                    hspace=0.2)
                
                ax.plot(real(self.index_ref_analyte), self.fom, '-o', markersize=3)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('Analyte (RIU)', fontdict=font)
                ax.set_ylabel(f'Quality Factor (RI$U^-$$^1$)', fontdict=font)
                ax.set_yticks(self.fom)
                ax.set_xticks(real(self.index_ref_analyte))
                self.canvas_.draw()
        
        self.textBrowser.setText(f"Runtime: {round(self.final - self.init, 6)} s\n"
                                f"{pol} Polarization\n\n"
                                f"Resonance {self.simbols[0]} ({self.simbols[2]}): {self.Resonance_Point}\n"
                                f"FWHM ({self.simbols[2]}): {self.Fwhm} \n"
                                f"DA: {self.da} \n"
                                f"Sensibility ({self.simbols[2]}/RIU): {self.sensibility}\n"
                                f"Quality Factor: {self.fom}\n")
                   
    def calc_FWHM(self, curve, xList):
        y = list(curve)

        id_min = y.index(min(y))  # Position of the minimum point of the curve
        reflect_right_critical_point = y
        
        if INTERROGATION_MODE == 1:
            critical_point = self.critical_point[-1]

            list_x = asarray(xList)
            idx = (abs(list_x - (critical_point * pi / 180))).argmin()
            reflect_right_critical_point = y[idx:-1]

            id_min = reflect_right_critical_point.index(min(reflect_right_critical_point))

        y_left = reflect_right_critical_point[0:(id_min+1)]
        y_right = reflect_right_critical_point[id_min:len(reflect_right_critical_point)]

        y_mx_left = max(y_left)
        y_mn_left = min(y_left)

        y_mx_right = max(y_right)
        y_mn_right = min(y_right)

        y_med_left = (y_mx_left + y_mn_left)/2
        y_med_right = (y_mx_right + y_mn_right)/2

        #y_med = (y_med_left + y_med_right)/2
        #y_med = (1+min(reflect_right_critical_point))/2    
        #y_med = (max(reflect_right_critical_point) + min(reflect_right_critical_point))/2 
        #y_med = max(reflect_right_critical_point)/2
        
        if (y_mx_left>y_mx_right):
            y_med = y_med_left
        else:
            y_med = y_med_right

        try:
            signs = sign(add(y, -y_med ))

            zero_crossings = (signs[0:-2] != signs[1:-1])
            zero_crossings_i = where(zero_crossings)[0]

            id1 = zero_crossings_i[-1]
            id2 = zero_crossings_i[-2]

            x1 = xList[id1] + (xList[id1+1] - xList[id1]) * ((y_med - y[id1]) / (y[id1+1] - y[id1]))
            x2 = xList[id2] + (xList[id2+1] - xList[id2]) * ((y_med - y[id2]) / (y[id2+1] - y[id2]))
            
            f = abs((x1 * 180 / pi) - (x2 * 180 / pi)) if INTERROGATION_MODE == 1 else abs(x2 - x1) * 1E9
            
            f = round(f, 6)
            
            return f

        except:
            return 1

    def save_table(self):
        from save_table import Ui_Dialog 
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog, self.layers)
        self.dialog.show()
    
    def open_from_extern_file(self):
        from instructions import Ui_Dialog_2
        self.new_window = QtWidgets.QWidget()
        self.ui_2 = Ui_Dialog_2()
        self.ui_2.setupUi(self.new_window)
        self.new_window.show()

    def export_data(self):
        from save_files import Ui_Dialog_Save
        self.save_window = QtWidgets.QDialog()
        self.ui_3 = Ui_Dialog_Save()
        polarization = "TM" if self.TM_polarization.isChecked() else "TE"
        self.ui_3.setupUi(self.save_window, self.index_ref_analyte, self.ax_x, self.Reflectance_, self.Fwhm, self.Resonance_Point, self.sensibility, self.fom, self.simbols, polarization)
        self.save_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Widget = MainWindow()
    Widget.show()
    app.exec()
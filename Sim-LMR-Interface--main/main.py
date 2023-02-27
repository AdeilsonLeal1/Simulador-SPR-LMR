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


COUPLING, INTERROGATION_MODE = 0, 0

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
        self.Reflectance_TM = list()     # List with reflectance values for plotting multiple curves in TM polarization
        self.Reflectance_TE = list()     # List with reflectance values for plotting multiple curves in TE polarization
        self.Resonance_Point_TM = list()  # Resonance angle or resonance wavelength  on TM polarization
        self.Resonance_Point_TE = list()  # Resonance angle or resonance wavelength  on TE polarization
        self.sensibility_TM = list()  # List with Sensibility values in TM polarization
        self.sensibility_TE = list()  # List with Sensibility values in TE polarization

        ## Window initialization parameters
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowIcon(QtGui.QIcon('icons/LOGO.png'))
        self.setWindowTitle("Sim-LMR")
        self.showMaximized()

        # Startup for graphics display
        self.figure = plt.figure(dpi=250)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.layout_graphs.addWidget(self.canvas)
        self.verticalLayout_12.addWidget(self.toolbar)

        ## APP EVENTS
        ########################################################################
        self.Stacked_windows.setCurrentIndex(4)
        self.stacked_layers.setCurrentIndex(0)
        self.Stacked_config_mode.setCurrentIndex(1)

        self.btn_close.clicked.connect(self.close)    # close window
        self.btn_minimize.clicked.connect(
            self.showMinimized)    # minimize window
        self.exit_btn.clicked.connect(self.close)    # close window
        self.start_btn.clicked.connect(lambda: self.Stacked_windows.setCurrentWidget(
            self.coupling_window))    # show coupling window

        # return to home window
        self.btn_home.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.home_window))
        self.btn_home_2.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.home_window))
        self.btn_home_3.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.home_window))
        self.btn_home_4.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.home_window))

        # return to coupling page
        self.btn_coupling.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))
        self.btn_coupling_2.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))
        self.btn_coupling_3.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))
        self.btn_coupling_4.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.coupling_window))

        # return to interrogation mode page
        self.btn_interrogation.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.interrogation_window))
        self.btn_interrogation_2.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.interrogation_window))
        self.btn_interrogation_3.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.interrogation_window))

        # return to setting layers page
        self.btn_setting_layers.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.layers_window))
        self.btn_setting_layers_2.clicked.connect(
            lambda: self.Stacked_windows.setCurrentWidget(self.layers_window))

        # Coupling page buttons
        self.prism_btn.clicked.connect(self.prism_btn_clicked)
        self.fiber_btn.clicked.connect(self.fiber_btn_clicked)
        self.prev_btn_coup.clicked.connect(lambda: self.previous_page())
        self.next_btn_coup.clicked.connect(
            lambda: self.next_page(op=COUPLING, warning=self.warning_2))

        # Interrogation mode page buttons
        self.aim_btn.clicked.connect(self.aim_btn_clicked)
        self.wim_btn.clicked.connect(self.wim_btn_clicked)
        self.prev_btn_inter.clicked.connect(self.previous_page)
        self.next_btn_inter.clicked.connect(lambda: self.next_page(
            op=INTERROGATION_MODE, warning=self.warning_inter))
        
        # Setting layers page buttons 
        self.prev_btn_config_layers.clicked.connect(self.previous_page)
        self.next_btn_config_layers.clicked.connect(lambda: self.next_page(
            op=INTERROGATION_MODE, warning=self.label_warning))

        ## Method that updates the incidence wavelength in AIM mode
        self.lambda_i_slider.valueChanged.connect(lambda: self.change_spinbox(self.lambda_i, self.lambda_i_slider))   
        self.lambda_i.valueChanged.connect(lambda: self.change_slider(self.lambda_i, self.lambda_i_slider))

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
        self.prev_btn_config_aim_4.clicked.connect(self.previous_page)
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
    
        ## Remove and edit table
        #self.tableWidget_layers.clicked.connect(self.select_row)
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

    # APP FUNCTIONS     

    def prism_btn_clicked(self):
        self.warning_2.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\">-</span><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\"> Coupling through prism selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:500; font-family:'monospace'; color:#37eb00;\">Next to continue...</span></pre></body></html>"))
        global COUPLING
        COUPLING = 1
        
    def fiber_btn_clicked(self):
        self.warning_2.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#37eb00;\">- Coupling through optical fiber under development - </span></pre></body></html>"))
        global COUPLING
        COUPLING = 0

    def next_page(self, op, warning):
        if op == 0:
            warning.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-weight:500; font-family:\'monospace\'; color:#B21222;\">- *! Select a valid option !* - </span></pre></body></html>"))
        else:
            if self.Stacked_windows.currentIndex() == 3:
                if self.nLayers < 3:
                    self.warning.setHidden(False)
                    self.warning.setText(f"## Insert more than 3 layers ## \n  ## {self.nLayers} Layers ##")
                else:
                    self.Stacked_windows.setCurrentIndex(self.Stacked_windows.currentIndex()+1)

            else:
                self.Stacked_windows.setCurrentIndex(self.Stacked_windows.currentIndex()+1)   
                self.figure.clear()
                self.canvas.draw()    
                if op == 1: # AIM mode
                    self.stacked_layers.setCurrentIndex(0)
                    self.Stacked_config_mode.setCurrentIndex(2)
                    self.btn_config_WIM_fiber.setText("Configure AIM mode")
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
                else:   #WIM mode
                    self.stacked_layers.setCurrentIndex(1)
                    self.Stacked_config_mode.setCurrentIndex(1)
                    self.btn_config_WIM_fiber.setText("Configure WIM mode")
                    self.textBrowser_2.setText("You have already selected PRISM coupling and WAVELENGTH INTERROGATION MODE."
                                    "\n\nTo continue your simulation:\n"
                                    "\n\t* Add at least 3 layers to build your sensor structure;"
                                    "\n\t* In the 'Layers' field, add optical substrate layers, thin films and adhesion layers;"
                                    "\n\t* Don't forget to add the analyte analysis range, in the 'Analyte refractive " "index range' field."
                                    "\n\nIn the table below you can see the added layers.")
                    self.textBrowser.setText("Select the wavelength range of the analysis in the 'Spectral range' field   and add the incidence angle in the 'Incidence angle' field;"
                                            "\nClick the 'Run' button to start the calculations;"
                                            "\nYou can choose which chart to view in the combobox below the chart area.")
            
    def previous_page(self):
        self.Stacked_windows.setCurrentIndex(self.Stacked_windows.currentIndex()-1)

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
        # This enable the cbox_material field 
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

        # This enable the cbox_material_2 field 
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

        self.description_4.setEnabled(True)
        self.description_4.setStyleSheet(u"color: rgb(10, 25, 90);\n"
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

        self.warning.setHidden(True)
        
    def set_Enable_True_2(self):
        # This enable the gb_analyte field  
        self.gb_analyte.setEnabled(True)
        self.gb_analyte.setToolTip("Analyte refractive index range")

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
        
        # This enable the btn_add_layer button 
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
        
        # This changes the button style btn_add_layer
        self.doubleSpinBox_7.setStyleSheet(u"\n"
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
        self.doubleSpinBox_8.setStyleSheet(u"\n"
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
        self.doubleSpinBox_9.setStyleSheet(u"\n"
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
        
        # This changes the button style btn_add_layer
        self.doubleSpinBox_4.setStyleSheet(u"\n"
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
        self.doubleSpinBox_5.setStyleSheet(u"\n"
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
        self.doubleSpinBox_6.setStyleSheet(u"\n"
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
        # This unenable the gb_analyte field 
        self.gb_analyte.setEnabled(False)
        self.gb_analyte.setToolTip("Click in 'New layer' to enable")
        self.doubleSpinBox_7.setStyleSheet(u"\n"
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
        self.doubleSpinBox_8.setStyleSheet(u"\n"
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
        self.doubleSpinBox_9.setStyleSheet(u"\n"
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

        # This unenable the gb_analyt_2 field 
        self.gb_analyte_2.setEnabled(False)
        self.gb_analyte_2.setToolTip("Click in 'New layer' to enable")
        self.doubleSpinBox_4.setStyleSheet(u"\n"
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
        self.doubleSpinBox_5.setStyleSheet(u"\n"
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
        self.doubleSpinBox_6.setStyleSheet(u"\n"
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

        #self.btn_add_analyte_2.setEnabled(False)
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
        
        if material == 19:
            self.real_part_index.setEnabled(True)
            self.real_part_index.setText("")
            self.imaginary_part_index.setEnabled(True)
            self.imaginary_part_index.setText("")
        else:
            wi = lambda_i 
            B1, B2, B3, C1, C2, C3, X, n, k_index = 0, 0, 0, 0, 0, 0, [], [], []  # Initialization of variables
            Lambda_i = wi * 1e6  # Incidence Wavelength in micrometers
            j = 0 + 1j

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

                elif material == 4:  # SF2
                    B1, B2, B3, C1, C2, C3 = 1.78922056, 3.28427448E-1, 2.01639441, 1.35163537E-2, 6.22729599E-2, 168.014713

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
            elif material == 10:
                B1, B2, B3, C1, C2, C3 = 2.356764950, -1.139969240E-2, 1.087416560E-2, 3.320669140E-5, 1.086093460E-5, 0
                n = sqrt(B1 + (B2 * Lambda_i ** 2) + (B3 / Lambda_i ** 2) + (C1 / Lambda_i ** 4) + (C2 / Lambda_i ** 6))

            # Metals
            elif 11 <= material < 15:
                """
                X - Wavelength in micrometers,
                n - Real part of the refractive index e k_index - Imaginary part of the refractive index
                according to Johnson and Christy, 1972
                """
                if material == 11:  # Refractive index of Aluminum according to the Drude model
                    LambdaP, LambdaC = 1.0657E-7, 2.4511E-5
                    n = sqrt(1 - (((wi ** 2) * LambdaC) / ((LambdaC + (j * wi)) * (LambdaP ** 2))))
                elif material == 12:  # Gold
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
                
                elif material == 13:  # Silver
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

                elif material == 14:  # Copper
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

                # Method that calculates the refractive indices of the metals by linear interpolation
                # using the points contained in X, n e k_index previously described
                n_interp = interp(Lambda_i, X, n)
                k_interp = interp(Lambda_i, X, k_index)
                n = complex(n_interp, k_interp)

            # Refractive index of the Water
            elif material == 15:
                n = 1.33

            # Refractive index of the Air
            elif material == 16:
                n = 1.0000

            # Refractive index of the LiF (Lithium Fluoride) according to the RefractiveIndex.info:
            # https://refractiveindex.info/
            elif material == 17:
                B1, B2, B3, C1, C2, C3 = 0.92549, 6.96747, 0, 5.4405376E-3, 1075.1841, 0
                n = sqrt(1 + ((B1 * Lambda_i ** 2) / (Lambda_i ** 2 - C1)) + ((B2 * Lambda_i ** 2) / (Lambda_i ** 2 - C2))
                        + ((B3 * Lambda_i ** 2) / (Lambda_i ** 2 - C3)))

            elif material == 18:  # Cytop
                # According to the AGC chemicals company. Available in:
                # https://www.agc-chemicals.com/jp/en/fluorine/products/cytop/download/index.html
                X = [0.2, 2]

                n_cy = [1.34, 1.34]

                # Method that calculates the refractive indices of the metals by linear interpolation
                # using the points contained in X, n e k_index previously described
                n = complex(interp(Lambda_i, X, n_cy))


            self.real_part_index.setText(str(round(real(n), 5) ).replace('.',',')) 
            self.imaginary_part_index.setText(str(round(imag(n), 5)).replace('.',',')) 

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
            self.material.pop(-1)
            self.material_id.pop(-1)
            self.warning.setText("Fill in all required fields *")
        
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
                initial_index_analyte = self.doubleSpinBox_7.value()
                final_index_analyte = self.doubleSpinBox_8.value()
                step_analyte = self.doubleSpinBox_9.value()
                thickness = self.thickness_4.text().replace(',','.')
                description = self.description_3.text()
            
            else:   # WIM mode
                initial_index_analyte = self.doubleSpinBox_6.value()
                final_index_analyte = self.doubleSpinBox_4.value()
                step_analyte = self.doubleSpinBox_5.value()
                thickness = self.thickness_3.text().replace(',','.')
                description = self.description_4.text()

            refractiveIndex = f"{round(initial_index_analyte,4)} - {round(final_index_analyte,4)}" 
                        
            self.material.append("Analyte")
            self.material_id.append(16)
            self.d.append(float(thickness)*1e-9)
            self.indexRef.append(complex(initial_index_analyte, 0))
            
            indices = arange(initial_index_analyte,final_index_analyte,step_analyte)
            indices = vectorize(lambda indices: complex(round(indices,4)))(indices)
            self.index_ref_analyte.append(list(indices))

            self.layers.append({"material": "Analyte", "thickness": thickness, "refractiveIndex": refractiveIndex, "description": description })
            
            self.nLayers = len(self.layers)
        except:
            self.warning.setHidden(False)
            self.material.pop(-1)
            self.material_id.pop(-1)
            self.warning.setText("Fill in all required fields *")
        
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
            
            msg.setStandardButtons(QMessageBox.Ok)
            
            retval = msg.exec_()

    def select_edit_layer(self):
        self.set_RefractiveIndex(self.cbox_material.currentIndex(), self.lambda_i.value()*1E-9)

        index_select = self.tableWidget_layers.currentRow()

        if index_select>=0:
            layer_edit = self.layers[index_select]
            if self.material[index_select]=='Analyte':
                self.set_Enable_True_2()
                if INTERROGATION_MODE == 1: # AIM mode
                    self.doubleSpinBox_7.setValue(real(self.index_ref_analyte[0][0]))
                    self.doubleSpinBox_8.setValue(real(self.index_ref_analyte[0][len(self.index_ref_analyte[0])-1]))
                    self.doubleSpinBox_9.setValue(real((self.index_ref_analyte[0][1])-(self.index_ref_analyte[0][0])))
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
                    self.doubleSpinBox_6.setValue(real(self.index_ref_analyte[0][0]))
                    self.doubleSpinBox_8.setValue(real(self.index_ref_analyte[0][len(self.index_ref_analyte[0])-1]))
                    self.doubleSpinBox_9.setValue(real((self.index_ref_analyte[0][1])-(self.index_ref_analyte[0][0])))
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
                else:
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

        self.show_layers()

        self.thickness.setText("")
        self.thickness_2.setText("")
        self.real_part_index.setText("")
        self.imaginary_part_index.setText("")
        self.description.setText("")
        self.description_2.setText("")

    def edit_analyte(self):
        index_select = self.tableWidget_layers.currentRow()
        if INTERROGATION_MODE == 1: # AIM mode
            initial_index_analyte = self.doubleSpinBox_7.value()
            final_index_analyte = self.doubleSpinBox_8.value()
            step_analyte = self.doubleSpinBox_9.value()
            thickness = self.thickness_4.text().replace(',','.')
            description = self.description_3.text()
        else: #WIM
            initial_index_analyte = self.doubleSpinBox_6.value()
            final_index_analyte = self.doubleSpinBox_4.value()
            step_analyte = self.doubleSpinBox_5.value()
            thickness = self.thickness_3.text().replace(',','.')
            description = self.description_4.text()

        refractiveIndex = f"{round(initial_index_analyte,4)} - {round(final_index_analyte,4)}" 
                        
        self.d[index_select] = float(thickness)*1e-9
        self.indexRef[index_select] = complex(initial_index_analyte, 0)
        
        indices = arange(initial_index_analyte,final_index_analyte,step_analyte)
        indices = vectorize(lambda indices: complex(round(indices,4)))(indices)
        self.index_ref_analyte[0] = list(indices)
        self.layers[index_select] = {"material": "Analyte", "thickness": thickness, "refractiveIndex": refractiveIndex, "description": description }
    
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
        self.Reflectance_TM = []
        self.Reflectance_TE = []
        self.Resonance_Point_TM = []
        self.Resonance_Point_TE = []
        self.sensibility_TM = []
        self.sensibility_TE = []
        self.critical_point = []
        
        if INTERROGATION_MODE == 1:
            self.reflectance_AIM()
            self.show_graphs()
        else:
            self.reflectance_WIM()
            self.show_graphs()
     
    def reflectance_AIM(self):
        STEP = 0.01*(pi/180)
        lambda_i = self.lambda_i.value()*1E-9
        a1 = self.a1_3.value()*(pi/180)
        a2 = self.a2_3.value()*(pi/180)
        theta_i = arange(a1, a2, STEP)
            
        for index_analyte in self.index_ref_analyte[0]:
            layer_analyte = self.material.index('Analyte')
            self.indexRef[layer_analyte] = index_analyte

            # It calculates the critical angle of attenuated total reflection
            self.critical_point.append(round(abs(arcsin(index_analyte / self.indexRef[0]) * (180 / pi)), 3))

            R_TM_i = []
            R_TE_i = []

            for t in range(len(theta_i)):
                r_tm, r_te = self.Reflectance(self.indexRef, theta_i[t], lambda_i)
                R_TM_i.append(r_tm)
                R_TE_i.append(r_te)
                

            self.Resonance_Point_TM.append(round(self.Point_LMR(theta_i, R_TM_i), 3))
            self.Resonance_Point_TE.append(round(self.Point_LMR(theta_i, R_TE_i), 3))
            
            self.Reflectance_TM.append(R_TM_i)
            self.Reflectance_TE.append(R_TE_i)

            self.sensibility_graph(index_analyte,layer_analyte)
        
        self.indexRef[layer_analyte]=self.index_ref_analyte[0][0]

    def sensibility_graph(self, index_analyte, layer_analyte):
        # Sensibility obtained from the graph

            # Resonance point variation
        delta_X_TM = self.Resonance_Point_TM[-1] - self.Resonance_Point_TM[0]
        delta_X_TE = self.Resonance_Point_TE[-1] - self.Resonance_Point_TE[0]

            # Refractive index variation
        delta_index = self.indexRef[layer_analyte].real - self.index_ref_analyte[0][0].real

            # It calculates the angular sensitivity (Resonance point variation)/(Refractive index variation)
        if index_analyte == self.index_ref_analyte[0][0]:
                # The first interaction is initialized to zero because the ratio would be 0/0
            self.sensibility_TM.append(0)
            self.sensibility_TE.append(0)

        else:
                # Only after the second interaction is sensitivity considered.
            self.sensibility_TM.append(delta_X_TM / delta_index)
            self.sensibility_TE.append(delta_X_TE / delta_index)

            self.sensibility_TM[0] = self.sensibility_TM[1]
            self.sensibility_TE[0] = self.sensibility_TE[1]
    
    def Point_LMR(self,axis_x ,reflectance):
        # The method self.Point_LMR() returns the resonance point of the curve
        try:
            id_min = reflectance.index(min(reflectance))  # Position of the minimum point of the curve

            if INTERROGATION_MODE == 1:
                min_point = axis_x[id_min] * (180 / pi)
                critical_point = self.critical_point[-1]
                # Checks if the minimum is before the critical point
                if min_point > critical_point:
                    resonance_point = min_point
                else:  # It adjusts to be the next minimum after the critical angle
                    lst = asarray(axis_x)
                    idx = (abs(lst - (critical_point * pi / 180))).argmin()

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

    def reflectance_WIM(self):
        STEP = 0.1*1E-9
        theta_i = self.angle_incidence.value()*(pi/180)
        a1 = self.a1_2.value()*1E-9
        a2 = self.a2_2.value()*1E-9
        lambda_i = arange(a1, a2, STEP)

        for index_analyte in self.index_ref_analyte[0]:
            layer_analyte = self.material.index('Analyte')

            R_TM_i = []
            R_TE_i = []

            for t in range(len(lambda_i)):
                self.indexRef = []  # Reset of refractive index for each wavelength

                for m in range(self.nLayers):  # Calculation of the new refractive index for each material
                    self.set_RefractiveIndex(self.material_id[m], lambda_i[t])
                    real = float(self.real_part_index.text().replace(',','.'))
                    imag = float(self.imaginary_part_index.text().replace(',','.'))
                    self.indexRef.append(complex(real,imag))
                self.indexRef[layer_analyte] = index_analyte
                
                r_tm, r_te = self.Reflectance(self.indexRef, theta_i, lambda_i[t])
                R_TM_i.append(r_tm)
                R_TE_i.append(r_te)
            
            self.Resonance_Point_TM.append(round(self.Point_LMR(lambda_i, R_TM_i), 3))
            self.Resonance_Point_TE.append(round(self.Point_LMR(lambda_i, R_TE_i), 3))

            self.Reflectance_TM.append(R_TM_i)
            self.Reflectance_TE.append(R_TE_i)

            self.sensibility_graph(index_analyte,layer_analyte)
    
    def Reflectance(self, index, theta_i, wavelenght):
        """ The numerical model is based on the attenuated total reflection method combined with the transfer matrix
            method for a multilayer system according to:
            * PALIWAL, N.; JOHN, J. Lossy mode resonance based fiber optic sensors. In: Fiber Optic Sensors.
            [S_TM.l.]: Springer, 2017. p. 31–50. DOI : 10.1007/978-3-319-42625-9_2."""

        j = complex(0, 1)  # Simplification for the complex number "j"
        k0 = (2 * pi) / wavelenght  # Wave number

        b = []  # b_j -> Phase shift in each layer
        q_TM = []  # q_TM_j -> Admittance in TM polarization
        q_TE = []  # q_TE_j -> Admittance in TE polarization

        Transfer_Matrix_TM = []  # Transfer_Matrix_TM_j -> Transfer matrix between each layer - TM polarization
        Transfer_Matrix_TE = []  # Transfer_Matrix_TE_j -> Transfer matrix between each layer - TM polarization
        for layer in range(self.nLayers):
            y = sqrt((index[layer] ** 2) - ((index[0] * sin(theta_i)) ** 2))

            b.append(k0 * self.d[layer] * y)
            q_TM.append(y / index[layer] ** 2)
            q_TE.append(y)

            # Total Transfer Matrix
            if layer < (self.nLayers - 1):
                Transfer_Matrix_TM.append(array([[cos(b[layer]), (-j / q_TM[layer]) * sin(b[layer])],
                                   [-j * q_TM[layer] * sin(b[layer]), cos(b[layer])]]))
                Transfer_Matrix_TE.append(array([[cos(b[layer]), (-j / q_TE[layer]) * sin(b[layer])],
                                   [-j * q_TE[layer] * sin(b[layer]), cos(b[layer])]]))

        Total_Transfer_Matrix_TM = Transfer_Matrix_TM[0]  # Total_Transfer_Matrix_TM -> Total Transfer Matrix - TM polarization
        Total_Transfer_Matrix_TE = Transfer_Matrix_TE[0]  # Total_Transfer_Matrix_TE -> Total Transfer Matrix - TE polarization
        for k in range(self.nLayers - 2):
            Total_Transfer_Matrix_TM = Total_Transfer_Matrix_TM @ Transfer_Matrix_TM[k + 1]
            Total_Transfer_Matrix_TE = Total_Transfer_Matrix_TE @ Transfer_Matrix_TE[k + 1]

        num_TM = (Total_Transfer_Matrix_TM[0][0] + Total_Transfer_Matrix_TM[0][1] * q_TM[self.nLayers - 1]) * q_TM[0] - (Total_Transfer_Matrix_TM[1][0] + Total_Transfer_Matrix_TM[1][1] * q_TM[self.nLayers - 1])
        den_TM = (Total_Transfer_Matrix_TM[0][0] + Total_Transfer_Matrix_TM[0][1] * q_TM[self.nLayers - 1]) * q_TM[0] + (Total_Transfer_Matrix_TM[1][0] + Total_Transfer_Matrix_TM[1][1] * q_TM[self.nLayers - 1])

        num_TE = (Total_Transfer_Matrix_TE[0][0] + Total_Transfer_Matrix_TE[0][1] * q_TE[self.nLayers - 1]) * q_TE[0] - (Total_Transfer_Matrix_TE[1][0] + Total_Transfer_Matrix_TE[1][1] * q_TE[self.nLayers - 1])
        den_TE = (Total_Transfer_Matrix_TE[0][0] + Total_Transfer_Matrix_TE[0][1] * q_TE[self.nLayers - 1]) * q_TE[0] + (Total_Transfer_Matrix_TE[1][0] + Total_Transfer_Matrix_TE[1][1] * q_TE[self.nLayers - 1])

        r_TM = num_TM / den_TM  # 'r_TM'-> Fresnel reflection coefficient - TM polarization
        r_TE = num_TE / den_TE  # 'r_TE'-> Fresnel reflection coefficient - TE polarization

        
        return abs(r_TM) ** 2, abs(r_TE) ** 2  # Reflectance - TM polarization, Reflectance - TE polarization
    
    def show_graphs(self):
        graph = self.select_graphs.currentText()
        self.textBrowser.setText(f"\nPontos de ressonancia-TM polarization: {self.Resonance_Point_TM}"
                                 f"\nPontos de ressonancia-TE polarization: {self.Resonance_Point_TE}"
                                 )
        
        if INTERROGATION_MODE == 1:
            STEP = 0.01*(pi/180)
            a1 = self.a1_3.value()*(pi/180) 
            a2 = self.a2_3.value()*(pi/180) 
            theta_i = arange(a1, a2, STEP)    

            ax_x =  theta_i* (180 / pi) 
            simbols = ("Angle", chr(952), "°")
        else:
            STEP = 0.1*1E-9
            a1 = self.a1_2.value()*1E-9
            a2 = self.a2_2.value()*1E-9
            lambda_i = arange(a1, a2, STEP)

            ax_x = lambda_i*1E9
            simbols = ("Wavelength", chr(955), "nm")

        font=dict(size=5, family="Sans-Serif")
        plt.rc('font', **font)

        plt.subplots_adjust(left=0.160,
            bottom=0.195, 
            right=0.930, 
            top=0.950, 
            wspace=0.1, 
            hspace=0.2)
        
        match graph:
            case "Reflectance - TM":
                self.figure.clear()
                if INTERROGATION_MODE == 1:
                    text = f"{simbols[1]}$_C$ = {self.critical_point[0]:.4f} {simbols[2]}"
                    x, y = self.Reflectance(self.indexRef, self.critical_point[0]*pi/180, self.lambda_i.value()*1E-9)
                    plt.annotate(text=text, xy=(self.critical_point[0], x), xytext=(self.a1_3.value(), 0.6),bbox=dict(boxstyle="round4", fc="w"), arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=-0.2",))

                plt.plot(ax_x, (self.Reflectance_TM[0]))
                plt.grid(True, alpha=0.3)
                plt.xlabel(f'Incidence {simbols[0]} ({simbols[2]})', fontdict=font)
                plt.ylabel('Reflectance', fontdict=font)
                plt.yticks(arange(0, 1.20, 0.20), fontsize=5)
                plt.xticks(fontsize=5)

                self.canvas.draw()  
            case "Reflectance - TE":
                self.figure.clear()
                if INTERROGATION_MODE == 1:
                    text = f"{simbols[1]}$_C$ = {self.critical_point[0]:.4f} {simbols[2]}"
                    x, y = self.Reflectance(self.indexRef, self.critical_point[0]*pi/180, self.lambda_i.value()*1E-9)
                    plt.annotate(text=text, xy=(self.critical_point[0], x), xytext=(self.a1_3.value(), 0.6),bbox=dict(boxstyle="round4", fc="w"), arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=-0.2",))
                
                plt.plot(ax_x, (self.Reflectance_TE[0]))
                plt.grid(True, alpha=0.3)
                plt.xlabel(f'Incidence {simbols[0]} ({simbols[2]})', fontdict=font)
                plt.ylabel('Reflectance', fontdict=font)
                plt.yticks(arange(0, 1.20, 0.20), fontsize=5 )
                plt.xticks(fontsize=5)
                
                self.canvas.draw()
            
            case "FWHM vs. Analyte - TM":

                self.figure.clear()
                   
                plt.title("TM-polarization")
                plt.xlabel('Incidence Angle (°)')
                plt.ylabel('Reflectivity')
                plt.yticks(arange(0, 1.20, 0.20))

                self.canvas.draw()

            case "FWHM vs. Analyte - TE":
                
                self.figure.clear()
               
                plt.title("TE-polarization")
                plt.xlabel('Incidence Angle (°)')
                plt.ylabel('Reflectivity')
                plt.yticks(arange(0, 1.20, 0.20))

                self.canvas.draw()
            
            case "Reflectance vs. Analyte - TM":
               
                self.figure.clear()
                
                legend = list()
                for i in range(len(self.index_ref_analyte[0])):
                    plt.plot(ax_x, self.Reflectance_TM[i])
                    legend.append(fr"{self.index_ref_analyte[0][i].real:.3f}")
                plt.grid(True, alpha=0.3)
                plt.legend(legend, fontsize=6)
                plt.xlabel(f'Incidence {simbols[0]} ({simbols[2]})', fontdict=font)
                plt.ylabel('Reflectance', fontdict=font)
                plt.yticks(arange(0, 1.20, 0.20), fontsize=5 )
                plt.xticks(fontsize=5)
                
                self.canvas.draw()
            
            case "Reflectance vs. Analyte - TE":
                
                self.figure.clear()
                
                legend = list()
                for i in range(len(self.index_ref_analyte[0])):
                    plt.plot(ax_x, self.Reflectance_TE[i])
                    legend.append(fr"{self.index_ref_analyte[0][i].real:.3f}")
                plt.grid(True, alpha=0.3)
                plt.legend(legend, fontsize=6)
                plt.xlabel(f'Incidence {simbols[0]} ({simbols[2]})', fontdict=font)
                plt.ylabel('Reflectance', fontdict=font)
                plt.yticks(arange(0, 1.20, 0.20), fontsize=5 )
                plt.xticks(fontsize=5)
                
                self.canvas.draw()
            
            case "Resonance point vs. Analyte - TM":
                self.figure.clear()
                plt.subplots_adjust(left=0.210,
                                    bottom=0.285, 
                                    right=0.900, 
                                    top=0.960, 
                                    wspace=0.1, 
                                    hspace=0.2)

                plt.plot(real(self.index_ref_analyte[0]), self.Resonance_Point_TM, '-o', markersize=3 )
                plt.grid(True, alpha=0.3)
                plt.xlabel('Analyte (RIU)', fontdict=font)
                plt.ylabel(f'Resonance {simbols[0]}', fontdict=font)
                plt.yticks(self.Resonance_Point_TM, fontsize=5 )
                plt.xticks(fontsize=5, rotation=45)
                
                self.canvas.draw()
            
            case "Resonance point vs. Analyte - TE":
                
                self.figure.clear()
                plt.subplots_adjust(left=0.210,
                                    bottom=0.285, 
                                    right=0.900, 
                                    top=0.960, 
                                    wspace=0.1, 
                                    hspace=0.2)
                
                plt.plot(real(self.index_ref_analyte[0]), self.Resonance_Point_TE, '-o', markersize=3 )
                plt.grid(True, alpha=0.3)
                plt.xlabel('Analyte (RIU)', fontdict=font)
                plt.ylabel(f'Resonance {simbols[0]}', fontdict=font)
                plt.yticks(self.Resonance_Point_TE, fontsize=5 )
                plt.xticks(fontsize=5, rotation=45)
                
                self.canvas.draw()
                      
            case "Sensibility vs. Analyte - TM":
                self.figure.clear()
                plt.subplots_adjust(left=0.210,
                                    bottom=0.285, 
                                    right=0.900, 
                                    top=0.960, 
                                    wspace=0.1, 
                                    hspace=0.2)
    
                plt.plot(real(self.index_ref_analyte[0]), self.sensibility_TM, '-o', markersize=3)
                plt.grid(True, alpha=0.3)
                plt.xlabel('Analyte (RIU)', fontdict=font)
                plt.ylabel(f'Sensibility ({simbols[2]} RI$U^-$$^1$)', fontdict=font)
                plt.yticks(self.sensibility_TM, fontsize=5 )
                plt.xticks(fontsize=5, rotation=45)

                self.canvas.draw()
            
            case "Sensibility vs. Analyte - TE":
                self.figure.clear()
                plt.subplots_adjust(left=0.210,
                                    bottom=0.285, 
                                    right=0.900, 
                                    top=0.960, 
                                    wspace=0.1, 
                                    hspace=0.2)
                
                plt.plot(real(self.index_ref_analyte[0]), self.sensibility_TE, '-o', markersize=3)
                plt.grid(True, alpha=0.3)
                plt.xlabel('Analyte (RIU)', fontdict=font)
                plt.ylabel(f'Sensibility ({simbols[2]} RI$U^-$$^1$)', fontdict=font)
                plt.yticks(self.sensibility_TE, fontsize=5 )
                plt.xticks(fontsize=5, rotation=45)

                self.canvas.draw()
            
            case "Quality Factor - TM":
                
                self.figure.clear()
                
      
                plt.title("TM-polarization")
                plt.xlabel('Incidence Angle (°)')
                plt.ylabel('Reflectivity')
                plt.yticks(arange(0, 1.20, 0.20))

                self.canvas.draw()
            
            case "Quality Factor - TE":
                
                self.figure.clear()
               
                plt.title("TE-polarization")
                plt.xlabel('Incidence Angle (°)')
                plt.ylabel('Reflectivity')
                plt.yticks(arange(0, 1.20, 0.20))

                self.canvas.draw()
    

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Widget = MainWindow()
    Widget.show()
    app.exec()
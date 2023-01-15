import icons_
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from Sim_LMR_interface import Ui_Widget
from dataBaseLayers import dataBaseLayers
import sys


COUPLING, INTERROGATION_MODE = 0, 0


class MainWindow(QWidget, Ui_Widget):
    def __init__(self):
        ## Variables
        self.layers = 0
        
        ## Application startup parameters
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showMaximized()

        ## APP EVENTS
        ########################################################################
        self.Stacked_windows.setCurrentIndex(3)
        self.stacked_layers.setCurrentIndex(1)
        self.Stacked_config_mode.setCurrentIndex(2)

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
        self.btn_add_analyte.clicked.connect(self.set_Enable_False)
        self.btn_add_layer.clicked.connect(self.set_Enable_False_2)
    
        self.btn_new_layer_2.clicked.connect(self.set_Enable_True)  
        self.btn_add_analyte_2.clicked.connect(self.set_Enable_False)
        self.btn_add_layer_2.clicked.connect(self.set_Enable_False_2)
        
        ## Add new layers
        self.btn_add_layer.clicked.connect(self.add_layers)
        self.btn_add_analyte.clicked.connect(self.add_analyte)
        self.btn_add_layer_2.clicked.connect(self.add_layers)
        self.btn_add_analyte_2.clicked.connect(self.add_analyte)
        self.btn_remove_layers.clicked.connect(self.remove_layers)
    
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
                if self.layers < 3:
                    self.warning.setHidden(False)
                    self.warning.setText(f"## Insert more than 3 layers ## \n  ## {self.layers} Layers ##")
                else:
                    self.Stacked_windows.setCurrentIndex(self.Stacked_windows.currentIndex()+1)
            else:
                self.Stacked_windows.setCurrentIndex(self.Stacked_windows.currentIndex()+1)       
                if op == 1: # AIM mode
                    self.stacked_layers.setCurrentIndex(0)
                    self.Stacked_config_mode.setCurrentIndex(2)
                    self.btn_config_WIM_fiber.setText("Configure AIM mode")
                else:   #WIM mode
                    self.stacked_layers.setCurrentIndex(1)
                    self.Stacked_config_mode.setCurrentIndex(1)
                    self.btn_config_WIM_fiber.setText("Configure WIM mode")
            
    def previous_page(self):
        self.Stacked_windows.setCurrentIndex(
            self.Stacked_windows.currentIndex()-1)

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
        # This enable the gb_analyte field  
        self.gb_analyte.setEnabled(True)
        self.gb_analyte.setToolTip("Analyte refractive index range")
        
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
        self.real_part_index.setEnabled(True)
        self.real_part_index.setStyleSheet(u"color: rgb(10, 25, 90);\n"
                                        "font: 700 12pt \"Ubuntu\";\n"
                                        "border: 2px solid;\n"
                                        "border-color: #FF17365D;\n"
                                        "background-color: rgba(255, 255, 255,210);\n"
                                        "border-radius:10px;")
        self.imaginary_part_index.setEnabled(True)
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
        self.description_3.setStyleSheet(u"color: rgb(10, 25, 90);\n"
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
        self.gb_analyte_2.setToolTip("Analyte refractive index range")
        
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
        
        # This enable the btn_add_layer_2 button 
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

    def add_layers(self):
        if INTERROGATION_MODE == 1: #AIM
            material = self.cbox_material.currentText()
            thickness = self.thickness.text()
            description = self.description.text()
            real = float(self.real_part_index.text().replace(',','.'))
            imag = float(self.imaginary_part_index.text().replace(',','.'))
        else:   # WIM
            material = self.cbox_material_2.currentText()
            thickness = self.thickness_2.text()
            description = self.description_2.text()
            real = 0
            imag = 0
        
        self.insert_layers(INTERROGATION_MODE, material, str(complex(real, imag)).replace('(',' ').replace(')',' '), thickness, description)
        self.layers = self.layers+1
        #self.warning.setText(f" ## {self.layers} Layers ##")
        if self.layers>0:
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

    def add_analyte(self):
        description = self.description_3.text() if INTERROGATION_MODE == 1 else self.description_4.text()

        self.insert_layers(INTERROGATION_MODE, "Analyte", f"{self.doubleSpinBox_7.value()} - {self.doubleSpinBox_8.value()}", '-', description )
        self.layers = self.layers+1
        #self.warning.setText(f" ## {self.layers} Layers ##")
        if self.layers>0:
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

    def remove_layers(self):
        if self.layers>=1:
            self.layers = self.layers-1
            self.warning.setText(f" ## {self.layers} Layers ##")
        else:
             self.warning.setText(f" Error! Check the layers\n ## {self.layers} Layers ##")
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
    
    def insert_layers(self, op, material, refractive_index, thickness, description):
        db = dataBaseLayers()
        db.connect()
        if op == 1: #AIM 
            fullDataSet = ( material, thickness, refractive_index, description )
        else:   #WIM
            fullDataSet = ( material, thickness, "-", description ) if material != 'Analyte' else ( material, thickness, refractive_index, description )
        ans = db.insert_layer(fullDataSet)
        
        ## show layers in table
        self.show_layers()
 
        if ans == 'ERROR':
            self.warning.setText(" Error Inserting Layer")
            db.close_connection()
        else:
            self.warning.setText(f"{ans}")
            db.close_connection()

    def show_layers(self):
        db = dataBaseLayers()
        db.connect()
        result = db.select_all_layers()

        self.tableWidget_layers.clearContents()
        self.tableWidget_layers.setRowCount(len(result))

        for row, text in enumerate(result):
            for column, data in enumerate(text):
                self.tableWidget_layers.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))
                self.tableWidget_graph.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))
        db.close_connection()

    
    def close(self) -> bool:
        db.connect()
        db.clear_dataset()
        db.close_connection()
        return super().close()



if __name__ == "__main__":
    db = dataBaseLayers()
    db.connect()
    db.create_table_layers()
    db.close_connection()

    app = QtWidgets.QApplication(sys.argv)
    Widget = MainWindow()
    Widget.show()
    app.exec()
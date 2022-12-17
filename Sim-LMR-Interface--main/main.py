import icons_
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from Sim_LMR_interface import Ui_Widget
import sys

COUPLING, INTERROGATION_MODE = 0, 0

class MainWindow(QWidget, Ui_Widget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showMaximized()

    ## APP EVENTS
    ########################################################################
        self.Stacked_windows.setCurrentIndex(3)
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
        self.btn_new_layer.clicked.connect(self.set_Enable_True)
        self.btn_add_analyte.clicked.connect(self.set_Enable_False)
        self.btn_add_layer.clicked.connect(self.set_Enable_False_2)

    # APP FUNCTIONS 
    def prism_btn_clicked(self):
        self.warning_2.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-family:'monospace'; color:#ffff64;\">-</span><span style=\" font-family:'monospace'; color:#ffff64;\"> Coupling through prism selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'monospace'; color:#ffff64;\">Next to continue...</span></pre></body></html>"))
        global COUPLING
        COUPLING = 1

    def fiber_btn_clicked(self):
        self.warning_2.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-family:\'monospace\'; color:#ffff64;\">- Coupling through optical fiber under development - </span></pre></body></html>"))
        global COUPLING
        COUPLING = 0

    def next_page(self, op, warning):
        if op == 0:
            warning.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-family:\'monospace\'; color:#ff9664;\">- *! Select a valid option !* - </span></pre></body></html>"))
        else:
            self.Stacked_windows.setCurrentIndex(
                self.Stacked_windows.currentIndex()+1)
            if op == 1:
                self.stacked_layers.setCurrentIndex(0)
            else:
                self.stacked_layers.setCurrentIndex(1)

    def previous_page(self):
        self.Stacked_windows.setCurrentIndex(
            self.Stacked_windows.currentIndex()-1)

    def aim_btn_clicked(self):
        global INTERROGATION_MODE
        self.warning_inter.setText(QtCore.QCoreApplication.translate(
            "Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-family:\'monospace\'; color:#ffff64;\">- Angular interrogation mode selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'monospace'; color:#ffff64;\">Next to continue...</span></pre></body></html>"))
        INTERROGATION_MODE = 1

    def wim_btn_clicked(self):
        global INTERROGATION_MODE
        self.warning_inter.setText(QtCore.QCoreApplication.translate("Widget", "<html><head/><body><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target-text-container\"/><span style=\" font-family:\'monospace\'; color:#ffff64;\">- Wavelength interrogation mode selected - </span></pre><pre align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'monospace'; color:#ffff64;\">Next to continue...</span></pre></body></html>"))
        INTERROGATION_MODE = 2

    def set_Enable_True(self):
        self.gb_analyte.setEnabled(True)
        self.gb_analyte.setToolTip("Analyte refractive index range")
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

    def set_Enable_False(self):
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

    def set_Enable_False_2(self):
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Widget = MainWindow()
    Widget.show()
    app.exec()
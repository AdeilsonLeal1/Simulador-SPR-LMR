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
        self.Stacked_windows.setCurrentIndex(0)
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
        self.prev_btn_inter.clicked.connect(lambda: self.previous_page())
        self.next_btn_inter.clicked.connect(lambda: self.next_page(
            op=INTERROGATION_MODE, warning=self.warning_inter))

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Widget = MainWindow()
    Widget.show()
    app.exec()
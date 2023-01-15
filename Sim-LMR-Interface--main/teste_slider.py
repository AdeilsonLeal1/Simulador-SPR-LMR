import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
                
        combo = QComboBox(self)
        combo.addItem("Apple")
        combo.addItem("Pear")
        combo.addItem("Lemon")
        combo.setStyleSheet(u"QComboBox::drop-down {\n"
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
                                         " border: 2px solid;\n"
                                         "border-color: #606060;\n"
                                         "background-color: rgba(255, 255, 255,210);\n"
                                         "border-radius:10px;\n"
                                         "}\n"
                                         "QComboBox::down-arrow { /* shift the arrow when popup is open */\n"
                                         "    top: 1px;\n"
                                         "	image: url(:/icons/icons/arrow-down.png);\n"
                                         "    left: 1px;\n"
                                         "}")

        combo.move(50, 50)

        self.qlabel = QLabel(self)
        self.qlabel.move(50,16)

        combo.activated[str].connect(self.onChanged)      

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("QLineEdit Example")
        self.show()

    def onChanged(self, text):
        self.qlabel.setText(text)
        self.qlabel.adjustSize()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
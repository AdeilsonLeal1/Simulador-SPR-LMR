import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget

class ProgressBarWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Barra de Progresso com Texto Maior à Direita')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)  # Mostra o texto na barra de progresso
        layout.addWidget(self.progress_bar)

        self.start_button = QPushButton('Iniciar')
        self.start_button.clicked.connect(self.start_progress)
        layout.addWidget(self.start_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Aplica o estilo CSS para posicionar o texto à direita da barra e aumentar o tamanho
        self.progress_bar.setStyleSheet("""
            QProgressBar::chunk {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(50, 100, 255, 255), stop:1 rgba(0, 0, 255, 255));
                margin-right: 2px;
            }

            QProgressBar {
                text-align: right;
            }

            QProgressBar::chunk:after {
                font-size: 14px;
                content: '%' ;
                position: absolute;
                top: 0;
                right: -10px;
            }
        """)

    def start_progress(self):
        self.progress_bar.setValue(0)
        self.progress_value = 0
        self.timer_interval = 100  # Intervalo em milissegundos
        self.timer = self.startTimer(self.timer_interval)

    def timerEvent(self, event):
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress_bar.setValue(self.progress_value)
        else:
            self.killTimer(self.timer.timerId())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBarWindow()
    window.show()
    sys.exit(app.exec_())

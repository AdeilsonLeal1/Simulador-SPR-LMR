from qtrangeslider._labeled import (
    QDoubleRangeSlider,
    QLabeledDoubleSlider,
    QLabeledRangeSlider,
    QLabeledSlider,
)
from qtrangeslider.qtcompat.QtCore import Qt
from qtrangeslider.qtcompat.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

app = QApplication([])

ORIENTATION = Qt.Horizontal

w = QWidget()


qlds = QLabeledDoubleSlider(ORIENTATION)
qlds.valueChanged.connect(lambda e: print("qlds valueChanged", e))
qlds.setRange(0, 90)
qlds.setValue(50)
qlds.setSingleStep(0.1)

qldrs = QDoubleRangeSlider(ORIENTATION)
qldrs.valueChanged.connect(lambda: print(qldrs.value()[0]))
qldrs.setRange(0, 1000)
qldrs.setSingleStep(1)
qldrs.setValue((200, 700))


w.setLayout(QVBoxLayout() if ORIENTATION == Qt.Horizontal else QHBoxLayout())

w.layout().addWidget(qlds)
w.layout().addWidget(qldrs)
w.show()
w.resize(500, 150)
app.exec_()
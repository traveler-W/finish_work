from PyQt5.QtWidgets import QApplication,QWidget
import sys

from ui import widget_rc

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QWidget()
    ui = widget_rc.Ui_Widget()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# hellow
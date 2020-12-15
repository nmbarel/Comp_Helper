from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from GUI_Windows import Log_In_Page

#class Log_In_window(QtWidgets.QMainWindow):
#    def __init__(self):
#        super().__init__()
#        self.resize(841, 299)
#        self.move(700, 300)
#        self.setWindowTitle("Log In Page")
#        self.setWindowIcon(QtGui.QIcon(r'C:\Users\User\PycharmProjects\crypepe.jpg'))

def test():
    print("test")
app = QtWidgets.QApplication(sys.argv)
Login = Log_In_Page()
Login.show()
sys.exit(app.exec_())
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import GUI_Windows

app = QtWidgets.QApplication(sys.argv)
Login = GUI_Windows.Log_In_Page()
Login.show()
app.exec_()
main_win = GUI_Windows.MainWindow()
main_win.show()
sys.exit(app.exec_())



from PyQt5 import QtCore, QtGui, QtWidgets
import Users
logged_user = None


class Log_In_Page(QtWidgets.QMainWindow):
    hide_password = False

    def __init__(self):
        super().__init__()
        self.UI_setup()
        self.retranslateUi()
        self.ButtonLoop()

    def UI_setup(self):
        self.setObjectName("Log In Page")
        self.resize(841, 299)
        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, -20, 491, 121))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, -40, 561, 241))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(210, 190, 181, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 220, 181, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(140, 190, 101, 21))
        font = QtGui.QFont()
        font.setFamily("David")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(105, 220, 101, 21))
        font = QtGui.QFont()
        font.setFamily("David")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.Log_In_button = QtWidgets.QPushButton(self.centralwidget)
        self.Log_In_button.setGeometry(QtCore.QRect(450, 180, 121, 71))
        self.Log_In_button.setObjectName("pushButton")
        self.Sign_Up_button = QtWidgets.QPushButton(self.centralwidget)
        self.Sign_Up_button.setGeometry(QtCore.QRect(590, 180, 121, 71))
        self.Sign_Up_button.setObjectName("pushButton_2")
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.HidePasswordButton = QtWidgets.QCheckBox(self.centralwidget)
        self.HidePasswordButton.setGeometry(400, 220, 40, 21)
        self.HidePasswordButton.setObjectName("Hide")
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Log In Page", "Log In Page"))
        self.label.setText(_translate("MainWindow", "Welcome to the Computer Helper! "))
        self.label_2.setText(_translate("MainWindow", "Please Log In to your user, or if you are new, sign up!"))
        self.label_3.setText(_translate("MainWindow", "Name:"))
        self.label_4.setText(_translate("MainWindow", "Password:"))
        self.Log_In_button.setToolTip(_translate("MainWindow", "Logs you in to the program"))
        self.Log_In_button.setText(_translate("MainWindow", "Log In"))
        self.Sign_Up_button.setToolTip(_translate("MainWindow", "Creates a user for you"))
        self.Sign_Up_button.setText(_translate("MainWindow", "Sign Up"))
        self.HidePasswordButton.setToolTip(_translate("MainWindow", "Hides the password"))
        self.HidePasswordButton.setText(_translate("MainWindow", "Hide"))

    def ButtonLoop(self):
        self.HidePasswordButton.clicked.connect(lambda: self.pass_state(self.HidePasswordButton.isChecked()))
        self.Log_In_button.clicked.connect(lambda: self.login_button(self.lineEdit.text(), self.lineEdit_2.text()))
        self.Sign_Up_button.clicked.connect((lambda: self.sign_button(self.lineEdit.text(), self.lineEdit_2.text())))

    def pass_state(self, toggled):
        if toggled:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        if not toggled:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)

    def pop_window(self, win_name, win_msg):
        new_win = QtWidgets.QMessageBox()
        new_win.setWindowTitle(win_name)
        new_win.setText(win_msg)
        new_win.exec_()

    def sign_button(self, name, password):
        global logged_user
        logged_user = Users.User(name, password)
        if logged_user.checkname():
            self.pop_window("Error", "This name is already in the system, please pick a different one")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
        elif name is None or name.find(" ") != -1 or name == "" or len(name) > 20:
            self.pop_window("Error", "This name is not valid, please make sure there are no space bars and it is no "
                                     "more than 20 characters!")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
        elif password is None or password.find(" ") != -1:
            self.pop_window("Error", "This password is not valid, please make sure there are no space bars!")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
        else:
            logged_user.register()
            self.pop_window("Success", "You are now registered!")
            self.lineEdit.clear()
            self.lineEdit_2.clear()

    def login_button(self, name, password):
        global logged_user
        logged_user = Users.User(name, password)
        if logged_user.checkname(): #logs you in and opens main window
            print("the name is " + logged_user.get_name())
            print("the pass is " + logged_user.get_pass())
            if logged_user.return_user() == logged_user.get_name() \
                    and logged_user.checkpass():
                self.pop_window("Success", "You are now logged in!")
                self.close()
            else:
                self.pop_window("Error", "This password is incorrect, please insert it again")
        else:
            self.pop_window("Error", "There is no user by that name in the system, please see the you wrote it "
                                     "correctly or if you are new, please register")
            self.lineEdit.clear()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        global logged_user
        self.setObjectName("MainWindow")
        labellength = logged_user.get_name()
        self.resize(450 + (30 * len(labellength)), 272)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 80, 241, 101))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 80, 30 * len(labellength), 101))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1061, 21))
        self.menubar.setObjectName("menubar")
        self.menuUser = QtWidgets.QMenu(self.menubar)
        self.menuUser.setObjectName("menuUser")
        self.menuApplications = QtWidgets.QMenu(self.menubar)
        self.menuApplications.setObjectName("menuApplications")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionUser_Info = QtWidgets.QAction(self)
        self.actionUser_Info.setObjectName("actionUser_Info")
        self.actionCustomize = QtWidgets.QAction(self)
        self.actionCustomize.setObjectName("actionCustomize")
        self.actionLog_Out = QtWidgets.QAction(self)
        self.actionLog_Out.setObjectName("actionLog_Out")
        self.actionPassword_Manager = QtWidgets.QAction(self)
        self.actionPassword_Manager.setObjectName("actionPassword_Manager")
        self.actionDownload_Tracker = QtWidgets.QAction(self)
        self.actionDownload_Tracker.setObjectName("actionDownload_Tracker")
        self.actionWebstibe_Blocker = QtWidgets.QAction(self)
        self.actionWebstibe_Blocker.setObjectName("actionWebstibe_Blocker")
        self.actionCalender = QtWidgets.QAction(self)
        self.actionCalender.setObjectName("actionCalender")
        self.actionTorrent_Downloader = QtWidgets.QAction(self)
        self.actionTorrent_Downloader.setObjectName("Torrent Downloader")
        self.menuUser.addAction(self.actionUser_Info)
        self.menuUser.addSeparator()
        self.menuUser.addAction(self.actionCustomize)
        self.menuUser.addSeparator()
        self.menuUser.addAction(self.actionLog_Out)
        self.menuApplications.addAction(self.actionPassword_Manager)
        self.menuApplications.addSeparator()
        self.menuApplications.addAction(self.actionDownload_Tracker)
        self.menuApplications.addSeparator()
        self.menuApplications.addAction(self.actionWebstibe_Blocker)
        self.menuApplications.addSeparator()
        self.menuApplications.addAction(self.actionCalender)
        self.menuApplications.addSeparator()
        self.menuApplications.addAction(self.actionTorrent_Downloader)
        self.menubar.addAction(self.menuUser.menuAction())
        self.menubar.addAction(self.menuApplications.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        global logged_user
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome "))
        self.label_2.setText(_translate("MainWindow", logged_user.name))
        self.menuUser.setTitle(_translate("MainWindow", "User"))
        self.menuApplications.setTitle(_translate("MainWindow", "Applications"))
        self.actionUser_Info.setText(_translate("MainWindow", "User Info"))
        self.actionCustomize.setText(_translate("MainWindow", "Customize"))
        self.actionLog_Out.setText(_translate("MainWindow", "Log Out"))
        self.actionPassword_Manager.setText(_translate("MainWindow", "Password Manager"))
        self.actionDownload_Tracker.setText(_translate("MainWindow", "Download Tracker"))
        self.actionWebstibe_Blocker.setText(_translate("MainWindow", "Webstibe Blocker"))
        self.actionTorrent_Downloader.setText(_translate("MainWindow", "Torrent Downloader"))
        self.actionCalender.setText(_translate("MainWindow", "Calender "))

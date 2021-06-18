# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(345, 526)
        self.centralwidget = QtWidgets.QWidget(Login)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.input_fields_frame = QtWidgets.QFrame(self.centralwidget)
        self.input_fields_frame.setMinimumSize(QtCore.QSize(0, 50))
        self.input_fields_frame.setStyleSheet("QFrame{\n"
"    \n"
"    background-color: rgb(255, 255, 255);\n"
"border:2px solid rgb(103, 19, 118);\n"
"border-radius: 20px; \n"
" }\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.input_fields_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.input_fields_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.input_fields_frame.setObjectName("input_fields_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.input_fields_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_4 = QtWidgets.QFrame(self.input_fields_frame)
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_4.setStyleSheet("border:None;\n"
"border-radius: None; ")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.btn_close = QtWidgets.QPushButton(self.frame_4)
        self.btn_close.setGeometry(QtCore.QRect(270, 0, 31, 31))
        self.btn_close.setStyleSheet("\n"
"QPushButton:hover{\n"
"    \n"
"    background-color: rgb(234, 234, 234);\n"
"}\n"
"")
        self.btn_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/x.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_close.setIcon(icon)
        self.btn_close.setIconSize(QtCore.QSize(30, 30))
        self.btn_close.setObjectName("btn_close")
        self.verticalLayout_3.addWidget(self.frame_4)
        self.profile_icon_frame = QtWidgets.QFrame(self.input_fields_frame)
        self.profile_icon_frame.setMinimumSize(QtCore.QSize(100, 100))
        self.profile_icon_frame.setMaximumSize(QtCore.QSize(300, 300))
        self.profile_icon_frame.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"background-image: url(:/icons/icons/login_icon.png);\n"
"background-repeat:no-repeat;\n"
"background-position: center;\n"
"border :solid  none\n"
"\n"
" ")
        self.profile_icon_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.profile_icon_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.profile_icon_frame.setObjectName("profile_icon_frame")
        self.verticalLayout_3.addWidget(self.profile_icon_frame)
        self.frame_2 = QtWidgets.QFrame(self.input_fields_frame)
        self.frame_2.setStyleSheet("border:None;\n"
"border-radius: None;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.username_line = QtWidgets.QLineEdit(self.frame_2)
        self.username_line.setMinimumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.username_line.setFont(font)
        self.username_line.setStyleSheet("padding-bottom:7px;\n"
"border:None;\n"
"background-color: rgba(0,0,0,0);\n"
"border-bottom: 2px solid rgba(46,82,101,200); \n"
"color:rgba(0,0,0,240);\n"
"")
        self.username_line.setAlignment(QtCore.Qt.AlignCenter)
        self.username_line.setObjectName("username_line")
        self.verticalLayout_2.addWidget(self.username_line)
        self.password_line = QtWidgets.QLineEdit(self.frame_2)
        self.password_line.setMinimumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.password_line.setFont(font)
        self.password_line.setStyleSheet("padding-bottom:7px;\n"
"border:None;\n"
"background-color: rgba(0,0,0,0);\n"
"border-bottom: 2px solid rgba(46,82,101,200); \n"
"color:rgba(0,0,0,240);")
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setAlignment(QtCore.Qt.AlignCenter)
        self.password_line.setObjectName("password_line")
        self.verticalLayout_2.addWidget(self.password_line)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.input_fields_frame)
        self.frame.setStyleSheet("QFrame{\n"
"    border:none;\n"
"}\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(30, -1, 30, -1)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.login_erorr = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.login_erorr.setFont(font)
        self.login_erorr.setStyleSheet("color: rgb(191, 0, 0);")
        self.login_erorr.setObjectName("login_erorr")
        self.gridLayout.addWidget(self.login_erorr, 3, 0, 1, 1)
        self.check_login = QtWidgets.QCheckBox(self.frame)
        self.check_login.setStyleSheet("QCheckBox{\n"
"    color: rgb(255,255,255);\n"
"    padding: 10px;\n"
"    \n"
"    \n"
"    background-color: rgb(27, 27, 27);\n"
"    \n"
"    border-radius: 15px; \n"
"}\n"
"\n"
"")
        self.check_login.setObjectName("check_login")
        self.gridLayout.addWidget(self.check_login, 4, 0, 1, 1)
        self.btn_login = QtWidgets.QPushButton(self.frame)
        self.btn_login.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_login.setFont(font)
        self.btn_login.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad,x1:0, y1:0.505682,x2:1,y2:0.477,stop:0 rgba(11,131,120.219),stop:1 rgna(85,98,112,226));\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius:15px;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad,x1:0, y1:0.505682,x2:1,y2:0.477,stop:0 rgba(11,123,111.219),stop:1 rgna(85,81,84,226));\n"
"}\n"
"QPushButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(150,123,111,255);\n"
"}")
        self.btn_login.setObjectName("btn_login")
        self.gridLayout.addWidget(self.btn_login, 5, 0, 1, 1)
        self.btn_forgot = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_forgot.setFont(font)
        self.btn_forgot.setStyleSheet("QPushButton{border:None;}\n"
"QPushButton:hover{\n"
"color: rgb(255, 30, 30);}")
        self.btn_forgot.setObjectName("btn_forgot")
        self.gridLayout.addWidget(self.btn_forgot, 6, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame)
        self.verticalLayout.addWidget(self.input_fields_frame)
        Login.setCentralWidget(self.centralwidget)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "MainWindow"))
        self.username_line.setPlaceholderText(_translate("Login", "Username"))
        self.password_line.setPlaceholderText(_translate("Login", "Password"))
        self.login_erorr.setText(_translate("Login", "Authentication Failed"))
        self.check_login.setText(_translate("Login", "Keep me logged in"))
        self.btn_login.setText(_translate("Login", "Login"))
        self.btn_forgot.setText(_translate("Login", "Forgot password ?"))
import traffic_rc

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nike_splashtEWCnn.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import os

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# Conver qrc resource file to python resource file
os.system('Pyrcc5 nike_app.qrc -o nike_app_rc.py')

import nike_app_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(561, 385)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.shoe_border_frame = QFrame(self.centralwidget)
        self.shoe_border_frame.setObjectName(u"shoe_border_frame")
        self.shoe_border_frame.setGeometry(QRect(310, 10, 250, 250))
        self.shoe_border_frame.setStyleSheet(u"border: 7px solid rgb(0, 92, 157);\n"
"border-radius: 20px;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.989, x2:0.977273, y2:0.051, stop:0 rgba(35, 25, 73, 255), stop:1 rgba(0, 91, 156, 81));")
        self.shoe_border_frame.setFrameShape(QFrame.StyledPanel)
        self.shoe_border_frame.setFrameShadow(QFrame.Raised)
        self.main_bg_frame = QFrame(self.centralwidget)
        self.main_bg_frame.setObjectName(u"main_bg_frame")
        self.main_bg_frame.setGeometry(QRect(0, 60, 401, 200))
        self.main_bg_frame.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0.25, x2:1, y2:0.472, stop:0 rgba(214, 214, 249, 255), stop:1 rgba(27, 14, 76, 255));\n"
"border-radius: 20px;\n"
"border-bottom: 5px solid rgb(0, 92, 157);\n"
"border-right: 5px solid rgb(1, 159, 236);\n"
"border-top: 5px solid rgb(0, 92, 157);\n"
"border-left: 5px solid rgb(0, 92, 157);")
        self.main_bg_frame.setFrameShape(QFrame.StyledPanel)
        self.main_bg_frame.setFrameShadow(QFrame.Raised)
        self.logo_frame = QFrame(self.main_bg_frame)
        self.logo_frame.setObjectName(u"logo_frame")
        self.logo_frame.setGeometry(QRect(10, 10, 120, 80))
        self.logo_frame.setStyleSheet(u"image: url(:/images/images/nike_logo.png);\n"
"background-color: none;\n"
"border: none; /*remove borders*/")
        self.logo_frame.setFrameShape(QFrame.StyledPanel)
        self.logo_frame.setFrameShadow(QFrame.Raised)
        self.middele_circle_frame = QFrame(self.main_bg_frame)
        self.middele_circle_frame.setObjectName(u"middele_circle_frame")
        self.middele_circle_frame.setGeometry(QRect(20, 20, 400, 400))
        self.middele_circle_frame.setStyleSheet(u"background-color: none;\n"
"border: 10px solid rgb(43, 31, 91);\n"
"border-radius: 200px; /*50% of it's size*/")
        self.middele_circle_frame.setFrameShape(QFrame.StyledPanel)
        self.middele_circle_frame.setFrameShadow(QFrame.Raised)
        self.shoe_frame = QFrame(self.centralwidget)
        self.shoe_frame.setObjectName(u"shoe_frame")
        self.shoe_frame.setGeometry(QRect(269, 10, 291, 301))
        self.shoe_frame.setStyleSheet(u"image: url(:/images/images/nike_shoe.png);")
        self.shoe_frame.setFrameShape(QFrame.StyledPanel)
        self.shoe_frame.setFrameShadow(QFrame.Raised)
        self.more_info_frame = QFrame(self.centralwidget)
        self.more_info_frame.setObjectName(u"more_info_frame")
        self.more_info_frame.setGeometry(QRect(0, 250, 401, 131))
        self.more_info_frame.setStyleSheet(u"background-color: rgb(43, 31, 91);\n"
"border-radius: 20px;\n"
"border: 5px solid rgb(0, 92, 157)")
        self.more_info_frame.setFrameShape(QFrame.StyledPanel)
        self.more_info_frame.setFrameShadow(QFrame.Raised)
        self.app_info = QLabel(self.more_info_frame)
        self.app_info.setObjectName(u"app_info")
        self.app_info.setGeometry(QRect(10, 90, 371, 31))
        font = QFont()
        font.setFamily(u"Montserrat Alternates Black")
        self.app_info.setFont(font)
        self.app_info.setStyleSheet(u"border: none;\n"
"background-color: transparent;\n"
"color: rgb(28, 20, 59);")
        self.app_info.setAlignment(Qt.AlignCenter)
        self.loadingstatus = QLabel(self.more_info_frame)
        self.loadingstatus.setObjectName(u"loadingstatus")
        self.loadingstatus.setGeometry(QRect(40, 10, 341, 51))
        font1 = QFont()
        font1.setFamily(u"a_Concepto")
        font1.setPointSize(15)
        self.loadingstatus.setFont(font1)
        self.loadingstatus.setStyleSheet(u"border: none;\n"
"background-color: transparent;\n"
"color: rgb(255, 255, 255);")
        self.loadingstatus.setAlignment(Qt.AlignCenter)
        self.loading_progress = QLabel(self.more_info_frame)
        self.loading_progress.setObjectName(u"loading_progress")
        self.loading_progress.setGeometry(QRect(250, 50, 91, 31))
        self.loading_progress.setStyleSheet(u"border: none;\n"
"background-color: transparent;\n"
"color: rgb(255, 255, 255);")
        self.welcome_label = QLabel(self.centralwidget)
        self.welcome_label.setObjectName(u"welcome_label")
        self.welcome_label.setGeometry(QRect(30, 196, 371, 81))
        font2 = QFont()
        font2.setFamily(u"a_Concepto")
        font2.setPointSize(27)
        font2.setBold(True)
        font2.setWeight(75)
        self.welcome_label.setFont(font2)
        self.welcome_label.setStyleSheet(u"border-left:  25px solid rgb(43, 31, 91);\n"
"border-right:   25px solid rgb(43, 31, 91);;\n"
"border-radius: 30px;\n"
"border-bottom: 30px solid rgb(43, 31, 91);")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.more_info_frame.raise_()
        self.shoe_border_frame.raise_()
        self.main_bg_frame.raise_()
        self.welcome_label.raise_()
        self.shoe_frame.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.app_info.setText(QCoreApplication.translate("MainWindow", u"Designed By Spinn Design(Yuotube Spnn Tv)", None))
        self.loadingstatus.setText(QCoreApplication.translate("MainWindow", u"Initializing Nike-Desk App ", None))
        self.loading_progress.setText(QCoreApplication.translate("MainWindow", u"Please wait....", None))
        self.welcome_label.setText(QCoreApplication.translate("MainWindow", u"WELCOME", None))
    # retranslateUi


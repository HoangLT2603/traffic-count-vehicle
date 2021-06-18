import random
import re
import smtplib, ssl
import sys
import os
from calendar import monthrange

from PyQt5 import sip
import requests
import telegram
import time
import datetime as dt
from typing import *
import numpy as np
import cv2
import pyodbc
from pandas import DataFrame
from PySide2 import QtCore, QtGui, QtWidgets, QtCharts
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, Signal, QThread, QSortFilterProxyModel, QSettings)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QImage, QPen)
from PySide2.QtWidgets import *
from PySide2.QtCharts import *
import PySide2.QtGui as QtGui
import ast
# GUI FILE
import model
from threading import Thread
from app import *
from form_stream import *
from setting import *
from login import *
from forgot import *
from register import *
from changepass import *
import pyautogui



# GLOBAL
WINDOW_SIZE = 0


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # Set background to transparent
        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)


        self.setting = SettingWindow()
        self.lst_lable = []
        self.start = False
        self.grid = QGridLayout(self.ui.page_watch)
        self.grid.setContentsMargins(5, 5, 5, 5)
        self.grid.setSpacing(5)
        self.bot = telegram.Bot(token="1890279979:AAGdIhB_FkFBkSyx5AV0eXCmmjD6nZUCTH0")
        #set width column of table stream
        self.ui.table_stream.setColumnWidth(0, 35)
        self.ui.table_stream.setColumnWidth(1, 35)
        self.ui.table_stream.setColumnWidth(2, 35)
        self.ui.table_stream.setColumnWidth(3, 80)
        self.ui.table_stream.setColumnWidth(4, 300)
        self.ui.table_stream.setColumnWidth(5, 350)
        self.ui.table_stream.setColumnWidth(6, 150)
        self.ui.table_stream.setColumnWidth(7, 100)
        self.ui.table_stream.horizontalHeader().setVisible(True)
        self.ui.tableView_data.horizontalHeader().setVisible(True)


        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_close.clicked.connect(lambda: app.exit())
        self.ui.btn_menu.clicked.connect(lambda: self.slideleftmenu())
        self.ui.btn_logout.clicked.connect(lambda : self.logout())

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        self.watch_page()
        self.ui.btn_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_home))
        self.ui.btn_watch.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.page_watch), self.clear_label(), self.start_stream()])
        self.ui.btn_stream.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_stream))
        self.ui.btn_report.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_report))
        self.ui.btn_setting.clicked.connect(self.show_setting_window)
        self.ui.btn_export.clicked.connect(self.export_data)
        self.ui.btn_submit.clicked.connect(self.submit_data)
        self.load_data_cmb()
        self.ui.btn_add_stream.clicked.connect(self.show_stream_window)
        self.thread: List[thread_cam] = []
        self.report_page()
        self.stream_page()
        self.add_cam()
        # self.showFullScreen()
    def start_stream(self):
        if self.start == False:
            self.run_thread()
            # th = saveData()
            # th.start()
            self.start = True
    def logout(self):
        self.close()
        window.show()
    def add_cam(self):
        self.cams = {}
        conn, cur = self.connect_db()
        query = "select ID, Name, Source, Threshold, Status, Point_Box from Stream where Status = 'Running'"
        cur.execute(query)
        self.source = cur.fetchall()
        cur.close()
        conn.close()
        key = 0
        for x in self.source:
            self.cams[key] = x
            key = key+1
    def report_page(self, name="All", year="All Year", month="All Month", day="All Day"):

        if year == "All Year":
            year = "> 0"
        else:
            year = "="+year
        if month == "All Month":
            month = "> 0"
        else:
            month = "="+month
        if day == "All Day":
            day = "> 0"
        else:
            day = "="+day
        data_main = []
        conn, cur = self.connect_db()
        if name == 'All':
            query = "select Name, time, numCar,numMoto, numBus, numTruck, (numCar+numMoto+numBus+numTruck) as Total from dataStream join Stream on dataStream.IDcam = Stream.ID where year(time) {} and month(time) {} and day(time) {}".format(
                year, month, day)
            cur.execute(query)
            data = cur.fetchall()
            data_main.extend(data)
        else:
            for i in name:
                query = "select Name, time, numCar,numMoto, numBus, numTruck, (numCar+numMoto+numBus+numTruck) as Total from dataStream join Stream on dataStream.IDcam = Stream.ID where name = '{}' and year(time) {} and month(time) {} and day(time) {}".format(
                    i, year, month, day)
                cur.execute(query)
                data = cur.fetchall()
                data_main.extend(data)
        cur.close()
        conn.close()

        roww = 0
        lst = ["Cam name", "Date time", "Car number", "Moto number", "Bus number", "Truck number", "Total"]

        model = QtGui.QStandardItemModel(len(data_main), 7)
        model.setHorizontalHeaderLabels(lst)
        for row in data_main:
            for index in range(len(row)):
                item = QtGui.QStandardItem(str(row[index]))
                model.setItem(roww, index, item)
            roww = roww + 1


        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterKeyColumn(1)

        self.ui.tableView_data.setModel(filter_proxy_model)
        self.ui.txtSearch.textChanged.connect(filter_proxy_model.setFilterRegExp)
        self.ui.tableView_data.setColumnWidth(0, 200)
        self.ui.tableView_data.setColumnWidth(1, 200)
    def submit_data(self):
        name_cam = []
        for x in self.ckb:
            if x.isChecked():
                name_cam.append(x.text())
        year = self.ui.cmbYear.currentText()
        month = self.ui.cmbMonth.currentIndex()

        if month == 0:
            month = "All Month"
        else:
            month = str(month)
        day = self.ui.cmbDay.currentText()
        self.report_page(name_cam, year, month, day)
        self.check_chart(name_cam, year, month, day)
    def load_data_cmb(self):
        conn, cur = self.connect_db()
        query1 = "select distinct Name from  Stream "
        cur.execute(query1)
        data_name = cur.fetchall()
        query2 = "select distinct year(time) from dataStream "
        cur.execute(query2)
        self.data_year = cur.fetchall()
        cur.close()
        conn.close()
        self.ckb = []
        self.ui.cmbYear.addItem("All Year")
        for x in data_name:
            ckb_name = QCheckBox(self.ui.frame_checkbox)
            ckb_name.setText(x[0])
            font = QtGui.QFont()
            font.setPointSize(13)
            ckb_name.setFont(font)
            self.ui.gridLayout_10.addWidget(ckb_name)
            self.ckb.append(ckb_name)
        for z in self.data_year:
            self.ui.cmbYear.addItem(str(z[0]))
    def export_data(self):
        columnHeaders = ["Cam name", "Date time", "Car number", "Moto number", "Bus number", "Truck number", "Total"]
        self.df = DataFrame(columns=columnHeaders)
        for row in range(self.ui.tableView_data.model().rowCount()):
            for col in range(self.ui.tableView_data.model().columnCount()):
                self.df.at[row, columnHeaders[col]]= self.ui.tableView_data.model().index(row, col).data()
        self.dfsff.to_excel('Data stream.xlsx', index= False)
    def stream_page(self):
        conn, cur = self.connect_db()
        query = "select * from Stream"
        cur.execute(query)
        self.stream = cur.fetchall()
        cur.close()
        conn.close()

        self.ui.table_stream.setRowCount(len(self.stream))
        icon_trash = QtGui.QIcon()
        icon_trash.addPixmap(QtGui.QPixmap(":/icons/icons/icon-trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon_pause = QtGui.QIcon()
        icon_pause.addPixmap(QtGui.QPixmap(":/icons/icons/icon-stop2.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon_play = QtGui.QIcon()
        icon_play.addPixmap(QtGui.QPixmap(":/icons/icons/icon-start.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon_edit = QtGui.QIcon()
        icon_edit.addPixmap(QtGui.QPixmap(":/icons/icons/icon-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        roww = 0
        for row in self.stream:
            for index in range(3, 9):
                item1 = QTableWidgetItem(str(row[index-3]))
                if index == 3:
                    item1.setTextAlignment(Qt.AlignCenter)
                self.ui.table_stream.setItem(roww, index, item1)

            self.btn_edit = IndexedButtonWidget('')
            self.btn_edit.setStyleSheet("background-color: rgb(110, 110, 110);")
            self.btn_edit.setIcon(icon_edit)
            self.btn_edit.setIconSize(QtCore.QSize(20, 20))
            self.btn_edit.button_row = roww
            self.btn_edit.button_column = 1
            self.btn_edit.clicked.connect(self.edit_stream)
            self.ui.table_stream.setCellWidget(roww, 1, self.btn_edit)

            self.btn_remove_stream = IndexedButtonWidget('')
            self.btn_remove_stream.setStyleSheet("background-color: rgb(110, 110, 110);")
            self.btn_remove_stream.setIcon(icon_trash)
            self.btn_remove_stream.setIconSize(QtCore.QSize(20, 20))
            self.btn_remove_stream.button_row = roww
            self.btn_remove_stream.button_column = 2
            self.btn_remove_stream.clicked.connect(self.remove_stream)
            self.ui.table_stream.setCellWidget(roww, 2, self.btn_remove_stream)

            if row[4] == "Running":
                self.btn_run_stop = IndexedButtonWidget('')
                self.btn_run_stop.setStyleSheet("background-color: rgb(110, 110, 110)")
                self.btn_run_stop.setIcon(icon_pause)
                self.btn_run_stop.setIconSize(QtCore.QSize(24, 24))
                self.btn_edit.setEnabled(False)
            else:
                self.btn_run_stop = IndexedButtonWidget('')
                self.btn_run_stop.setStyleSheet("background-color: rgb(110, 110, 110)")
                self.btn_run_stop.setIcon(icon_play)
                self.btn_run_stop.setIconSize(QtCore.QSize(24, 24))
                self.btn_edit.setEnabled(True)
            self.btn_run_stop.button_row = roww
            self.btn_run_stop.button_column = 0
            self.btn_run_stop.clicked.connect(self.run_stop_stream)
            self.ui.table_stream.setCellWidget(roww, 0, self.btn_run_stop)
            roww = roww + 1
    def run_stop_stream(self):

        button = self.sender()
        row = button.button_row
        status = self.ui.table_stream.item(row, 7).text()
        id = self.ui.table_stream.item(row, 3).text()
        if status == "Running":
            status = "Stop"
        else:
            status = "Running"
        conn, cur = self.connect_db()
        query = "Update Stream Set Status = '{}' Where ID = {}".format(status, int(id))
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        self.Stop_thread()
        self.stream_page()
        self.add_cam()
        self.run_thread()
    def edit_stream(self):
        button = self.sender()
        row = button.button_row
        id = self.ui.table_stream.item(row, 3).text()
        conn, cur = self.connect_db()
        query = "select Name, Source, Threshold, Description, Point_Box from Stream where ID = {}".format(int(id))
        cur.execute(query)
        stream = cur.fetchall()
        cur.close()
        conn.close()

        name = stream[0][0]
        source = stream[0][1]
        threshold = stream[0][2]
        description = stream[0][3]
        point = stream[0][4]

        self.wd = StreamWindow(id, name, source, str(threshold), description, point)
        self.wd.show()
    def remove_stream(self):
        button = self.sender()
        row = button.button_row
        id = self.ui.table_stream.item(row, 3).text()
        self.ui.table_stream.removeRow(row)
        conn, cur = self.connect_db()
        query = "Delete From Stream Where ID = {}".format(int(id))
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        self.Stop_thread()
        self.stream_page()
        self.add_cam()
        self.run_thread()
    def clear_label(self):
        for x in self.lst_lable:
            x.clear()
    def run_thread(self):
        row, col = self.get_w_h_grid()
        for index, value in self.cams.items():
            if index <= 4:
                ID, Name, link, threshold, status, point = value
                slot = thread_cam(self, index, ID, Name, link, threshold, point)
                slot.ImageUpdate.connect(self.ImageUpdateSlot)
                self.thread.append(slot)
        if len(self.thread) > 0:
            for x in self.thread:
                x.start()
    def ImageUpdateSlot(self, Image, index: int):
        self.lst_lable[index].setPixmap(QPixmap.fromImage(Image))
    def Stop_thread(self):
        if len(self.thread) > 0:
            for x in self.thread:
                x.stop()
    def slideleftmenu(self):
        width = self.ui.left_menu.width()

        if width == 60:
            newwidth = 150
        else:
            newwidth = 60

        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newwidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
    def slidesetting(self):
        width = self.ui.setting.width()
        if width == 0:
            newwidth = 300
        else:
            newwidth = 0
        self.animation1 = QPropertyAnimation(self.ui.setting, b"minimumWidth")
        self.animation1.setDuration(250)
        self.animation1.setStartValue(width)
        self.animation1.setEndValue(newwidth)
        self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation1.start()
    def connect_db(self):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server= HOANG-LAMBOR;'
                              'Database=Traffic;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        return conn, cursor
    def show_setting_window(self):
        self.s = SettingWindow()
        width, height = pyautogui.size()
        self.s.setGeometry(width- 400, 60, 400, 500)
        self.s.show()
    def show_stream_window(self):
        self.w = StreamWindow()
        self.w.show()
    def watch_page(self, rl='2 x 2'):
        self.rl = rl

        row, col = self.get_w_h_grid()
        self.lst_lable.clear()
        self.deleteLayout(self.grid)
        for i in range(row):
            for j in range(col):
                lable = QLabel()
                lable.setStyleSheet("background-color: rgb(162, 162, 162);")
                self.grid.addWidget(lable, i, j)
                self.lst_lable.append(lable)
    def get_w_h_grid(self):
        rl = self.rl
        row = int(rl[0])
        col = int(rl[-1])
        self.W = (self.ui.page_watch.width() - 5 * (col + 1)) / col
        self.H = (self.ui.page_watch.height() - 5 * (row + 1)) / row
        return row, col
    def deleteLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
    def create_piechart(self, data= {}):
        children = self.ui.formLayout_pie.takeAt(0)
        del children
        series = QtCharts.QPieSeries()
        total_moto = 0
        total_car = 0
        total_truck = 0
        total_bus = 0
        for name_cam, value_cam in data.items():
            for row in value_cam:
                print(row[0])
                total_moto += row[0]
                total_car += row[1]
                total_truck += row[2]
                total_bus += row[3]
        series.append('Moto', total_moto)
        series.append('Car', total_car)
        series.append('Truck', total_truck)
        series.append('Car', total_car)
        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        series.setLabelsVisible(True)
        series.setLabelsPosition(QtCharts.QPieSlice.LabelOutside)   #LabelInsideHorizontal
        for slice in series.slices():
            slice.setLabel("{:.1f}%".format(100 * slice.percentage()))
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        chart.setTitle("Total of each vehicles")
        chart.setTitleFont('Arial')
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart.legend().markers(series)[0].setLabel("Moto")
        chart.legend().markers(series)[1].setLabel("Car")
        chart.legend().markers(series)[2].setLabel("Truck")
        chart.legend().markers(series)[3].setLabel("Bus")
        chart.legend().setFont('Arial')
        chartview = QtCharts.QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        chartview.setMaximumSize(self.ui.frame_piechart.width(), self.ui.frame_piechart.height())
        self.ui.frame_piechart.setMaximumSize(self.ui.frame_piechart.width(), self.ui.frame_piechart.height())
        self.ui.formLayout_pie.addWidget(chartview)
    def bar_chart(self, data= {}, axisx= [], check_chart=1):
        children = self.ui.formLayout_bar.takeAt(0)
        del children

        set0 = QtCharts.QBarSet("moto")
        set1 = QtCharts.QBarSet("car")
        set2 = QtCharts.QBarSet("truck")
        set3 = QtCharts.QBarSet("bus")
        for name_cam, value_cam in data.items():
            for row in value_cam:
                if row[0] is None:
                    set0.append(0)
                else:
                    set0.append(row[0])

                if row[1] is None:
                    set1.append(0)
                else:
                    set1.append(row[1])

                if row[2] is None:
                    set2.append(0)
                else:
                    set2.append(row[2])

                if row[3] is None:
                    set3.append(0)
                else:
                    set3.append(row[3])

        series = QtCharts.QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)

        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setTitleFont('Times')
        if check_chart == 1:
            chart.setTitle("Total each vehicles of each camera")
        elif check_chart == 2:
            chart.setTitle("Total each vehicles of each camera by year")
        elif check_chart == 3:
            chart.setTitle("Total each vehicles of each camera by month")
        elif check_chart == 4:
            chart.setTitle("Total each vehicles of each camera by day")

        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)


        axis = QtCharts.QBarCategoryAxis()
        axis.append(axisx)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setFont('Arial')
        chartView = QtCharts.QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setMaximumSize(self.ui.frame_barchart.width(), self.ui.frame_barchart.height())
        self.ui.frame_barchart.setMaximumSize(self.ui.frame_barchart.width(), self.ui.frame_barchart.height())
        self.ui.formLayout_bar.addWidget(chartView)
    def line_chart(self, data={}, axis=[], check_chart=1):
        if isinstance(axis[0], str):
            axis_new = [x for x in range(1, 13)]
        else:
            axis_new = axis
        children = self.ui.formLayout_linechart.takeAt(0)
        del children
        chart = QtCharts.QChart()
        for name_cam, value_cam in data.items():
            line = QtCharts.QLineSeries(self)
            ax = {x[0]:x[1] for x in value_cam}
            key = list(ax.keys())
            for i in axis_new:
                if i in key:
                    line.append(i, ax[i])
                else:
                    line.append(i, 0)
            line.setName(name_cam)
            chart.addSeries(line)

        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        chart.setTitleFont('Times')

        if check_chart == 1:
            chart.setTitle("Total vehicles of each camera by year")
        elif check_chart == 2:
            chart.setTitle("Total vehicles of each camera by month")
        elif check_chart == 3:
            chart.setTitle("Total vehicles of each camera by day")
        elif check_chart == 4:
            chart.setTitle("Total vehicles of each camera by hour")

        chart.createDefaultAxes()  # Use the default coordinate system
        axisX = QtCharts.QBarCategoryAxis()

        if isinstance(axis[0],str) == False:
            axis = list(map(str, axis))
        axisX.append(axis)
        chart.setAxisX(axisX)
        axisX.setRange(axis[0], axis[-1])
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setFont('Arial')
        chartView = QtCharts.QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        chartView.setMaximumSize(self.ui.frame_linechart.width(), self.ui.frame_linechart.height())
        self.ui.frame_linechart.setMaximumSize(self.ui.frame_linechart.width(), self.ui.frame_linechart.height())
        self.ui.frame_linechart.setStyleSheet("QFormLayout{border:None;}")
        self.ui.formLayout_linechart.addWidget(chartView)
    def check_chart(self, name="All", year="All Year", month="All Month", day="All Day"):
        conn, cursor = self.connect_db()
        data = {}
        data_barchart = {}
        data_piechart = {}
        axis_x = []
        check_chart = 0
        if year == "All Year":
            for y in self.data_year:
                axis_x.append(y[0])
            for cam in name:
                query = "select year(time),sum(numCar)+sum(numMoto)+sum(numBus)+sum(numTruck) from dataStream join Stream on dataStream.IDcam = Stream.ID WHERe name = '{}'  group by year(time)".format(
                    cam)
                query_barchart = "select sum(numMoto),sum(numCar),sum(numTruck),sum(numBus) from dataStream join Stream on dataStream.IDcam = Stream.ID WHERe name = '{}'".format(cam)

                # query_piechart = "select sum(numCar)+sum(numMoto)+sum(numBus)+sum(numTruck) from dataStream join Stream on dataStream.IDcam = Stream.ID WHERe name = '{}'".format(cam)
                cursor.execute(query)
                dt_line = cursor.fetchall()
                data[cam] = dt_line
                cursor.execute(query_barchart)
                dt_bar = cursor.fetchall()
                if dt_bar[0][0] != None:
                    data_barchart[cam] = dt_bar

            check_chart = 1
        else:
            if month == "All Month":
                axis_x = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                      "November", "December"]
                for cam in name:
                    query = "select month(time),sum(numCar)+sum(numMoto)+sum(numBus)+sum(numTruck) from dataStream join Stream on dataStream.IDcam = Stream.ID WHERe name = '{}' and year(time) ={} group by month(time)".format(
                        cam,year)
                    query_barchart = "select sum(numMoto),sum(numCar),sum(numTruck),sum(numBus) from dataStream join Stream on dataStream.IDcam = Stream.ID WHERe name = '{}' and year(time)={}".format(
                        cam,year)
                    cursor.execute(query)
                    dt = cursor.fetchall()
                    data[cam] = dt
                    cursor.execute(query_barchart)
                    dt_bar = cursor.fetchall()
                    data_barchart[cam] = dt_bar
                check_chart = 2


            else:
                if day == "All Day":
                    num_days = monthrange(int(year), int(month))[1]
                    axis_x = [x for x in range(1, num_days + 1)]
                    for cam in name:
                        query = "select day(Time),sum(numCar)+sum(numMoto)+sum(numBus)+sum(numTruck) from dataStream join Stream on dataStream.IDcam = Stream.ID WHERE year(Time) = {} and MONTH(Time)= {} AND name = '{}' group by day(Time)".format(
                            year, month, cam)
                        query_barchart = "select sum(numMoto),sum(numCar),sum(numTruck),sum(numBus) from dataStream join Stream on dataStream.IDcam = Stream.ID WHERe name = '{}' and year(time)={} and MONTH(Time)= {}".format(
                            cam, year,month)
                        cursor.execute(query)
                        dt = cursor.fetchall()
                        data[cam] = dt

                        cursor.execute(query_barchart)
                        dt_bar = cursor.fetchall()
                        data_barchart[cam] = dt_bar
                        print(data)
                        print(data_barchart)
                    check_chart=3
                else:
                    axis_x = [str(x)+":00" for x in range(24)]
                    for cam in name:
                        query = "SELECT DATEPART(Hour, Time),sum(numCar)+sum(numMoto)+sum(numBus)+sum(numTruck)  from dataStream join Stream on dataStream.IDcam = Stream.ID where year(Time)= {} and  month(Time) = {} and DAY(Time) = {} and name = '{}' GROUP BY DATEPART(Hour, Time)".format(year,month,day,cam)
                        query_barchart = "select sum(numMoto),sum(numCar),sum(numTruck),sum(numBus) from dataStream join Stream on dataStream.IDcam = Stream.ID WHERe name = '{}' and year(time)={} and MONTH(Time)= {} and DAY(Time) = {}".format(
                            cam, year, month, day)
                        cursor.execute(query)
                        dt = cursor.fetchall()
                        data[cam] = dt

                        cursor.execute(query_barchart)
                        dt_bar = cursor.fetchall()
                        data_barchart[cam] = dt_bar
                    check_chart = 4

        cursor.close()
        conn.close()

        self.line_chart(data, axis_x, check_chart)
        self.bar_chart(data_barchart, name, check_chart)
        self.create_piechart(data_barchart)

class thread_cam(QThread):
    ImageUpdate = Signal(QImage, int, bool)
    def __init__(self, parent: QWidget,index:int, id:int, name: str, link: str, threshold: int, point: str) -> None:
        QThread.__init__(self, parent)
        self.index = index
        self.id = id
        self.parent = parent
        self.ThreadActive = True
        self.name = name
        self.link = link
        self.threshold = threshold
        self.point = ast.literal_eval(point)
        self.frame_count = 0
        self.max = 0
        self.min = 0
        self.car_number = 0
        self.moto_number = 0
        self.bus_number = 0
        self.truck_number = 0
        self.total_number = 0
        self.obj_cnt = 0
        self.curr_trackers = []
        self.check_thresh = False
        pts = np.array(self.point)
        self.mask = np.zeros((500, 700), np.uint8)
        cv2.drawContours(self.mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    def run(self):

        Capture = cv2.VideoCapture(self.link)
        while self.ThreadActive:
            ret, frame = Capture.read()
            frame = cv2.resize(frame, (700, 500))
            cv2.putText(frame, self.name, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            if ret:
                frame = self.tracking_detect(frame)
                ConvertToQtFormat = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
                pic = ConvertToQtFormat.scaled(window.wd_main.W, window.wd_main.H, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic, self.index, self.ThreadActive)

    def stop(self):
        self.ThreadActive = False
        self.quit()

    def tracking_detect(self, frame):
        start = time.time()

        n = len(self.point)
        if n >= 3:
            cv2.circle(frame, (self.point[0][0], self.point[0][1]), 5, (0, 0, 255), thickness=-1)
            for i in range(1, n):
                cv2.line(frame, (self.point[i][0], self.point[i][1]), (self.point[i-1][0], self.point[i-1][1]), (0, 255, 255), 2)
                cv2.circle(frame, (self.point[i][0], self.point[i][1]), 5, (0, 0, 255), thickness=-1)
            cv2.line(frame, (self.point[0][0], self.point[0][1]), (self.point[-1][0], self.point[-1][1]), (0, 255, 255), 2)


        self.boxes = []
        self.imH = 500
        self.imW = 700
        self.old_trackers = self.curr_trackers
        self.curr_trackers = []

        # duyệt qua các tracker cũ
        for car in self.old_trackers:
            self.tracker = car['tracker']
            (_, box) = self.tracker.update(frame)
            self.boxes.append(box)

            self.new_obj = dict()
            self.new_obj['tracker_class'] = car['tracker_class']
            self.new_obj['tracker'] = self.tracker
            class_name = self.new_obj['tracker_class']

            # tính toán tâm đối tượng
            x, y, w, h, center_X, center_Y = model.get_box_info(box)

            if self.mask[center_Y][center_X] == 0 or w > 150:
                continue
            else:
                cv2.putText(frame, class_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Ve hinh tron tai tam doi tuong
                cv2.circle(frame, (center_X, center_Y), 4, (0, 255, 0), -1)
                # Con khong thi track tiep
                self.curr_trackers.append(self.new_obj)
                if class_name == "car":
                    self.car_number += 1
                elif class_name == "motor":
                    self.moto_number += 1
                elif class_name == "bus":
                    self.bus_number += 1
                elif class_name == "truck":
                    self.truck_number += 1

        # Thuc hien object detection moi 5 frame
        if self.frame_count % 5 == 0:
            # Detect doi tuong
            boxes_d, classed = model.get_object(frame, detect_fn)

            for i in range(len(boxes_d)):
                #old_obj = False

                xd, yd, wd, hd, center_Xd, center_Yd = model.get_box_info(boxes_d[i])
                #cv2.rectangle(frame, (xd, yd), ((xd + wd), (yd + hd)), (0, 255, 255), 2)
                # Duyet qua cac box, neu sai lech giua doi tuong detect voi doi tuong da track ko qua max_distance thi coi nhu 1 doi tuong
                if not model.is_old(center_Xd, center_Yd, self.boxes):
                    #cv2.rectangle(frame, (xd, yd), ((xd + wd), (yd + hd)), (0, 255, 255), 2)
                    # Tao doi tuong tracker moi

                    tracker = cv2.TrackerMOSSE_create()
                    self.obj_cnt += 1
                    new_obj = dict()
                    tracker.init(frame, tuple(boxes_d[i]))

                    new_obj['tracker_class'] = classed[i]
                    new_obj['tracker'] = tracker

                    self.curr_trackers.append(new_obj)
        end = time.time()
        #fps = int(1 / (end - start))
        total = self.car_number + self.moto_number + self.truck_number + self.bus_number
        if total > self.max:
            self.max = total
        cv2.putText(frame, "Total: " + str(total), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (21, 232, 42), 2)
        cv2.putText(frame, "Max: " + str(self.max), (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (21, 232, 42), 2)
        # cv2.putText(frame, "Min: " + str(self.id), (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 3)
        # cv2.putText(frame, str(self.id), (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        self.frame_count += 1

        if total > self.threshold and self.check_thresh == False:
            print(self.name + " tắc đường rồi !!!")
            text = self.name + " đang bị tắc đường, cần hỗ trợ gấp !!!"
            cv2.imwrite('photo.jpg', frame)
            window.wd_main.bot.sendMessage(chat_id="-563799949", text=text)
            window.wd_main.bot.sendPhoto(chat_id="-563799949", photo=open("photo.jpg", "rb"))
            self.check_thresh = True
        elif total < self.threshold and self.check_thresh == True:
            self.check_thresh = False

        return frame

class IndexedButtonWidget(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.button_row = 0
        self.button_column = 0

class StreamWindow(QMainWindow):
    def __init__(self, id= '', name= '', source= '', threshold = '', description= '', point =[]):
        QMainWindow.__init__(self)
        self.ui = Ui_Stream()
        self.ui.setupUi(self)

        self.setGeometry(QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            self.size(),
            QtGui.QGuiApplication.primaryScreen().availableGeometry(),
        ))
        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.centralwidget.setStyleSheet("border-radius: 15px;")

        self.id = id
        self.name = name
        self.source = source
        self.threshold = threshold
        self.description = description
        self.point = point

        self.ui.btn_close.clicked.connect(self.close)
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.ui.btn_folder_stream.clicked.connect(self.new_dialog)
        self.ui.btn_draw.setEnabled(False)
        self.ui.btn_draw.clicked.connect(self.draw)
        self.ui.btn_remove_draw.setEnabled(False)
        self.ui.btn_remove_draw.clicked.connect(self.remove_draw)
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_reset.clicked.connect(self.reset)

        self.check_draw = False
        self.list_point = []
        self.check_event = False

        if id != '':
            self.edit_stream()

    def edit_stream(self):
        self.ui.edit_name.setText(self.name)
        self.ui.edit_source.setText(self.source)
        self.ui.edit_threshold.setText(self.threshold)
        self.ui.edit_description.setText(self.description)
        self.list_point = ast.literal_eval(self.point)
        Capture = cv2.VideoCapture(self.ui.edit_source.text())
        _, frame = Capture.read(0)
        frame = cv2.resize(frame, (700, 500))
        self.ConvertToQtFormat = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.pix = QPixmap(self.ConvertToQtFormat)
        self.ui.lbl_frame_draw.setPixmap(self.pix)
        qp = QPainter(self.pix)
        pen = QPen(Qt.yellow, 3)
        qp.setPen(pen)
        for i in range(len(self.list_point) - 1):
            x1 = self.list_point[i][0]
            y1 = self.list_point[i][1]
            x2 = self.list_point[i + 1][0]
            y2 = self.list_point[i + 1][1]
            qp.drawLine(x1, y1, x2, y2)
            self.ui.lbl_frame_draw.setPixmap(self.pix)
        x1 = self.list_point[0][0]
        y1 = self.list_point[0][1]
        x2 = self.list_point[-1][0]
        y2 = self.list_point[-1][1]
        qp.drawLine(x1, y1, x2, y2)
        self.ui.lbl_frame_draw.setPixmap(self.pix)
        self.ui.btn_remove_draw.setEnabled(True)
    def remove_draw(self):
        self.list_point.clear()
        self.ui.btn_draw.setEnabled(True)
        self.pix = QPixmap(self.ConvertToQtFormat)
        self.ui.lbl_frame_draw.setPixmap(self.pix)
        self.check_event = False
        self.check_draw = False
        self.ui.btn_draw.setText("Draw")
    def draw(self):
        if self.check_draw == False:
            self.check_draw = True
            self.check_event = True
            self.ui.btn_draw.setText("Complete")
            self.press_event()
        else:
            self.check_draw = False
            self.check_event = False
            self.ui.btn_draw.setText("Draw")
            self.ui.btn_draw.setEnabled(False)
            qp = QPainter(self.pix)
            pen = QPen(Qt.yellow, 3)
            qp.setPen(pen)
            x1 = self.list_point[0][0]
            y1 = self.list_point[0][1]
            x2 = self.list_point[-1][0]
            y2 = self.list_point[-1][1]
            qp.drawLine(x1, y1, x2, y2)
            self.ui.lbl_frame_draw.setPixmap(self.pix)
    def press_event(self):
        self.ui.lbl_frame_draw.mousePressEvent = self.getPixel
    def getPixel(self, event):
        if self.check_event == True:
            x = event.pos().x()
            y = event.pos().y()
            qp = QPainter(self.pix)
            pen = QPen(Qt.yellow, 3)
            qp.setPen(pen)
            self.list_point.append((x, y))
            if len(self.list_point) >= 2:
                for i in range(len(self.list_point)-1):
                    x1 = self.list_point[i][0]
                    y1 = self.list_point[i][1]
                    x2 = self.list_point[i+1][0]
                    y2 = self.list_point[i+1][1]
                    qp.drawLine(x1, y1, x2, y2)
                    self.ui.lbl_frame_draw.setPixmap(self.pix)


    def new_dialog(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open file', 'D:/KLTN/Qt5/main/images', "Video Files (*.avi *.mp4 *.flv *.mov  )")
        self.ui.edit_source.setText(filePath)
        Capture = cv2.VideoCapture(filePath)
        _, frame = Capture.read(0)
        frame = cv2.resize(frame, (700, 500))
        self.ConvertToQtFormat = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.pix = QPixmap(self.ConvertToQtFormat)
        self.ui.lbl_frame_draw.setPixmap(self.pix)
        self.ui.btn_draw.setEnabled(True)
        self.ui.btn_remove_draw.setEnabled(True)

    def save(self):

        ls = str(self.list_point)
        con, cur = MainWindow.connect_db(self)
        if self.id == '':
            query1 = """INSERT INTO Stream (Name, Source, Threshold, Description, Status, Point_Box) 
                                    VALUES('{}','{}', {},'{}','{}', '{}')""".format(self.ui.edit_name.text(), self.ui.edit_source.text(), int(self.ui.edit_threshold.text()), self.ui.edit_description.toPlainText(), "Stop", ls)
        else:
            query1 = """Update Stream Set Name = '{}', Source = '{}', Threshold = {}, Description = '{}', Point_Box = '{}'
                        Where ID = {}""".format(self.ui.edit_name.text(), self.ui.edit_source.text(), int(self.ui.edit_threshold.text()), self.ui.edit_description.toPlainText(), ls, int(self.id))
        cur.execute(query1)
        con.commit()
        cur.close()
        con.close()
        window.wd_main.stream_page()
        self.destroy()
    def reset(self):
        self.ui.edit_name.clear()
        self.ui.edit_source.clear()
        self.ui.edit_description.clear()
        self.ui.lbl_frame_draw.clear()
        self.ui.edit_threshold.clear()
        self.list_point.clear()
        self.ui.btn_draw.setEnabled(False)
        self.ui.btn_remove_draw.setEnabled(False)
        self.check_event = False
        self.check_draw = False
        self.ui.btn_draw.setText("Draw")

class SettingWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Setting()
        self.ui.setupUi(self)

        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.ui.cmb_gridLayout.currentIndexChanged.connect(lambda: window.wd_main.watch_page(self.ui.cmb_gridLayout.currentText()))
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_register.clicked.connect(self.showSettingForm)
    def showSettingForm(self):
        register = Register()
        register.show()
        self.close()

class Forgot(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Forgot()
        self.ui.setupUi(self)

        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.ui.login_erorr.hide()
        self.code = 0
        self.ui.btn_sencode.clicked.connect(lambda: self.check_forgot())
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.show()

    def valid_email(self, email):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

    def check_forgot(self):
        email = self.ui.email_line.text()
        code = self.ui.code_line.text()
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server= HOANG-LAMBOR;'
                              'Database=traffic;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        data = cursor.execute('SELECT * FROM account WHERE email=?', [email])
        data = cursor.fetchmany(2)
        if len(email) == 0:
            self.ui.login_erorr.setText("Email has not been filled in")
            self.ui.login_erorr.show()
            return
        else:
            if self.valid_email(email) == False:
                self.ui.login_erorr.setText("Invalid email")
                self.ui.login_erorr.show()
                return
            else:
                data = cursor.execute('SELECT * FROM account WHERE email=?', [email])
                data = cursor.fetchmany(2)
                if len(data) == 0:
                    self.ui.login_erorr.setText("Email does not exist")
                    self.ui.login_erorr.show()
                    return
        if len(code) == 0:
            if self.ui.btn_sencode.text() == "Verify":
                return
            self.send_mail(email)
            self.ui.login_erorr.setText("Let check mail")
            self.ui.login_erorr.show()
            self.ui.btn_sencode.setText("Verify")
        else:
            print(self.code)
            print(code)
            if int(code) == self.code:
                changepass = ChangePass(email)
                changepass.show()
                self.close()
            else:
                self.ui.login_erorr.setText("Fail")
                self.ui.login_erorr.show()

    def send_mail(self, email):
        gmail_user = 'thaihoang9499@gmail.com'
        gmail_password = 'hoang134'
        sent_from = gmail_user
        to = [email]
        subject = 'Your OTP'
        self.code = random.randrange(100000, 999999)
        body = 'Your OTP is ' + str(self.code)

        email_text = """\
        From: %s

        Subject: %s

        %s
        """ % (sent_from, subject, body)
        #context = ssl.create_default_context()
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print('Email sent!')
        except Exception as e:
            print(e)

class Register(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Register()
        self.ui.setupUi(self)

        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.ui.btn_register.clicked.connect(lambda: self.check_register())
        self.ui.login_erorr.hide()
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.show()

    def valid_email(self, email):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

    def check_register(self):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server= HOANG-LAMBOR;'
                              'Database=Traffic;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        username = self.ui.username_line.text()
        email = self.ui.email_line.text()
        print(email)
        password = self.ui.password_line.text()
        repassword = self.ui.repassword_line.text()
        data = cursor.execute('SELECT * FROM account WHERE username=? or email=?', [username, email])
        data = cursor.fetchmany(2)

        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(repassword) == 0:
            self.ui.login_erorr.setText("information has not been filled in")
            self.ui.login_erorr.show()
            return
        if len(data) == 0:
            self.ui.login_erorr.setText("Success")
            self.ui.login_erorr.show()
        else:
            self.ui.login_erorr.setText("Username or email already exists")
            self.ui.login_erorr.show()
            return
        if self.valid_email(email) == False:
            self.ui.login_erorr.setText("Invalid email")
            self.ui.login_erorr.show()
            return
        if password != repassword:
            self.ui.login_erorr.setText("Passwords do not match")
            self.ui.login_erorr.show()
            return
        role = 'user'
        if self.ui.rd_admin.isChecked() == True:
            role = 'admin'
        cursor.execute("insert into account values('{}','{}','{}','{}')".format(username, password, email, role))
        conn.commit()

class LoginForm(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.keeplogin = QSettings('MyQtApp', 'App1')
        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        if len(self.keeplogin.value('username')) != 0:
            self.ui.check_login.setChecked(True)
        else:
            self.ui.check_login.setChecked(False)
        self.ui.username_line.setText(self.keeplogin.value('username'))
        self.ui.password_line.setText(self.keeplogin.value('password'))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.ui.login_erorr.hide()
        self.ui.btn_login.clicked.connect(self.button_click)
        self.ui.btn_forgot.clicked.connect(lambda: [self.show_forgot(),self.close()])
        self.show()

    def show_forgot(self):
        forgot = Forgot()
        forgot.show()

    def show_new_window(self):
        self.close()
        self.wd_main = MainWindow()
        self.wd_main.showFullScreen()

    def button_click(self):
        a = self.ui.username_line.text()
        b = self.ui.password_line.text()

        self.check_login(a, b)

    def show_error(self):
        self.ui.login_erorr.show()

    def check_login(self, username1, password1):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server= HOANG-LAMBOR;'
                              'Database=traffic;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()

        data = cursor.execute('SELECT * FROM account WHERE username=? and password = ?', username1, password1)

        data = cursor.fetchmany(2)
        id = ""
        passw = ""
        role = -1
        for row in data:
            id = row[0]
            passw = row[1]
            role = row[3]
        if username1 == id and password1 == passw:
            if role == 'admin':
                self.ui.login_erorr.setText("mày là admin")
                self.ui.login_erorr.show()
            else:
                self.ui.login_erorr.setText("mày là cùi bắp :3")
                self.ui.login_erorr.show()
            if self.ui.check_login.isChecked():
                self.keeplogin.setValue('username', self.ui.username_line.text())
                self.keeplogin.setValue('password', self.ui.password_line.text())
            else:
                self.keeplogin.setValue('username', "")
                self.keeplogin.setValue('password', "")

            self.show_new_window()
        else:
            self.ui.login_erorr.show()
            if self.check_fail_login >= 4:
                self.show_forgot()
                self.close()
            self.check_fail_login += 1

class ChangePass(QMainWindow):
    def __init__(self,email):
        QMainWindow.__init__(self)
        self.ui = Ui_ChangePass()
        self.ui.setupUi(self)

        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.ui.login_erorr.hide()

        self.ui.btn_changepass.clicked.connect(lambda: self.check_changepass(email))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.show()
    def check_changepass(self,email):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server= HOANG-LAMBOR;'
                              'Database=traffic;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        password = self.ui.password_line.text()
        repassword = self.ui.repassword_line.text()

        if password != repassword:
            self.ui.login_erorr.setText("Passwords do not match")
            self.ui.login_erorr.show()
            return
        cursor.execute("update account set password = '{}' where Email = '{}'".format(password, email))
        conn.commit()
        loginwindow = LoginForm()
        loginwindow.show()
        self.close()

class saveData(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.save()
    def save(self):
        print("ok")
        # thr = window.wd_main.thread
        # if len(thr) > 0:
        #     con, cur = MainWindow.connect_db(self)
        #     for t in thr:
        #
        #         query1 = """INSERT INTO dataStream (IDcam, numCar, numMoto, numBus, numTruck)
        #                                                         VALUES('{}','{}','{}','{}','{}')""".format(t.id,
        #                                                                                                    t.car_number,
        #                                                                                                    t.moto_number,
        #                                                                                                    t.bus_number,
        #                                                                                                    t.truck_number)
        #         print("save success")
        #         cur.execute(query1)
        #         con.commit()
        #     cur.close()
        #     con.close()
        time.sleep(20)
        self.save()


if __name__ == "__main__":

    # detect_fn = model.load_model()
    detect_fn = ""
    app = QApplication(sys.argv)
    window = LoginForm()
    sys.exit(app.exec_())



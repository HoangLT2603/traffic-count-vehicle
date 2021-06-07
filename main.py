

import sys
import os
import platform
import time
import datetime as dt
from typing import *
import numpy as np
import cv2
import pyodbc
from pandas import DataFrame
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, Signal, QThread, QSortFilterProxyModel)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QImage, QPen)
from PySide2.QtWidgets import *
import PySide2.QtGui as QtGui
import ast
# GUI FILE
import model
from app import *
from form_stream import *


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

        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_close.clicked.connect(lambda: app.exit())
        self.ui.btn_menu.clicked.connect(lambda: self.slideleftmenu())

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        self.ui.btn_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_home))
        self.ui.btn_watch.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.page_watch), self.clear_label()])
        self.ui.btn_stream.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_stream))
        self.ui.btn_report.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_model))
        self.ui.btn_setting.clicked.connect(self.run_thread)

        #self.ui.btn_stop.clicked.connect(self.Stop_thread)
        self.ui.pushButton_2.clicked.connect(self.export_data)
        self.ui.btn_submit_data.clicked.connect(self.submit_data)
        self.load_data_cmb()
        self.ui.btn_add_stream.clicked.connect(self.show_new_window)
        self.thread: List[thread_cam] = []
        self.report_page()
        self.stream_page()
        self.add_cam()

        self.showFullScreen()


    def add_cam(self):
        self.cams = {}
        conn, cur = self.connect_db()
        query = "select ID, Name, Source, Status, Point_Box from Stream where Status = 'Running'"
        cur.execute(query)
        self.source = cur.fetchall()
        cur.close()
        conn.close()
        key = 0
        for x in self.source:
            self.cams[key] = x
            key = key+1

    def report_page(self, name="All", year="All", month="All", day="All"):

        if year == "All":
            year = "> 0"
        else:
            year = "="+year
        if month == "All":
            month = "> 0"
        else:
            month = "="+month
        if day == "All":
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
        self.ui.table_data.setColumnWidth(1, 250)
        self.ui.table_data.setRowCount(len(data_main))
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

        self.ui.tableView.setModel(filter_proxy_model)
        self.ui.txt_search.textChanged.connect(filter_proxy_model.setFilterRegExp)


    def submit_data(self):
        name_cam = []
        for x in self.ckb:
            if x.isChecked():
                name_cam.append(x.text())
        year = self.ui.cmb_year.currentText()
        month = self.ui.cmb_month.currentIndex()

        if month == 0:
            month = "All"
        else:
            month = str(month)
        day = self.ui.cmb_day.currentText()
        self.report_page(name_cam, year, str(month), day)
    def load_data_cmb(self):
        conn, cur = self.connect_db()
        query1 = "select distinct Name from  Stream "
        cur.execute(query1)
        data_name = cur.fetchall()
        query2 = "select distinct year(time) from dataStream "
        cur.execute(query2)
        data_year = cur.fetchall()
        cur.close()
        conn.close()
        self.ckb = []
        self.ui.cmb_year.addItem("All")
        for x in data_name:
            ckb_name = QCheckBox(self.ui.frame_3)
            ckb_name.setText(x[0])
            font = QtGui.QFont()
            font.setPointSize(13)
            ckb_name.setFont(font)
            self.ui.formLayout_3.addWidget(ckb_name)
            self.ckb.append(ckb_name)
        for z in data_year:
            self.ui.cmb_year.addItem(str(z[0]))
    def export_data(self):
        columnHeaders = ["Cam name", "Date time", "Car number", "Moto number", "Bus number", "Truck number", "Total"]
        self.df = DataFrame(columns=columnHeaders)
        for row in range(self.ui.tableView.model().rowCount()):
            for col in range(self.ui.tableView.model().columnCount()):
                self.df.at[row, columnHeaders[col]]= self.ui.tableView.model().index(row, col).data()
        self.dfsff.to_excel('Data stream.xlsx', index= False)


    def stream_page(self):

        conn, cur = self.connect_db()
        query = "select * from Stream"
        cur.execute(query)
        self.stream = cur.fetchall()
        cur.close()
        conn.close()
        roww = 1
        for row in self.stream:
            for index in range(len(row)):
                item1 = QTableWidgetItem(str(row[index]))
                self.ui.table_stream.setItem(roww, index, item1)
            if row[4] == "Running":
                self.btn_run_stop = IndexedButtonWidget('Stop')
                self.btn_run_stop.setStyleSheet("background-color: rgb(255,0,0);")
            else:
                self.btn_run_stop = IndexedButtonWidget('Running')
                self.btn_run_stop.setStyleSheet("background-color: rgb(0,255,0);")
            self.btn_run_stop.button_row = roww
            self.btn_run_stop.button_column = 5
            self.btn_run_stop.clicked.connect(self.run_stop_stream)
            self.ui.table_stream.setCellWidget(roww, 6, self.btn_run_stop)

            self.btn_remove_stream= IndexedButtonWidget('Remove')
            self.btn_remove_stream.setStyleSheet("background-color: rgb(255,0,0);")
            self.btn_remove_stream.button_row = roww
            self.btn_remove_stream.button_column = 5
            self.btn_remove_stream.clicked.connect(self.remove_stream)
            self.ui.table_stream.setCellWidget(roww, 5, self.btn_remove_stream)
            roww = roww + 1



    def run_stop_stream(self):

        button = self.sender()
        row = button.button_row
        status = self.ui.table_stream.item(row, 4).text()
        id = self.ui.table_stream.item(row, 0).text()
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

    def clear_label(self):
        self.ui.lable_image.clear()
        self.ui.lable_image_2.clear()
        self.ui.lable_image_3.clear()
        self.ui.lable_image_4.clear()

    def remove_stream(self):
        button = self.sender()
        row = button.button_row
        id = self.ui.table_stream.item(row, 0).text()
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
    def run_thread(self):
        #id = 0
        for index, value in self.cams.items():
            if index <= 4:
                ID, Name, link, status, point = value

                slot = thread_cam(self, index, ID, Name, link, point)
                slot.ImageUpdate.connect(self.ImageUpdateSlot)

                self.thread.append(slot)
               # id += 1
        if len(self.thread) > 0:
            for x in self.thread:
                x.start()

    def ImageUpdateSlot(self, Image, index: int):
        if index == 0:
            self.ui.lable_image.setPixmap(QPixmap.fromImage(Image))
        if index == 1:
            self.ui.lable_image_2.setPixmap(QPixmap.fromImage(Image))
        if index == 2:
            self.ui.lable_image_3.setPixmap(QPixmap.fromImage(Image))
        if index == 3:
            self.ui.lable_image_4.setPixmap(QPixmap.fromImage(Image))

    def Stop_thread(self):
        if len(self.thread) > 0:
            for x in self.thread:
                x.stop()


    def slideleftmenu(self):
        width = self.ui.left_menu.width()

        if width == 50:
            newwidth = 150
        else:
            newwidth = 50

        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newwidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def connect_db(self):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server= HOANG-LAMBOR;'
                              'Database=Traffic;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        return conn, cursor


    def show_new_window(self):
        self.w = AnotherWindow()
        self.w.show()

class thread_cam(QThread):
    ImageUpdate = Signal(QImage, int, bool)
    def __init__(self, parent: QWidget,index:int, id:int, name: str, link: str, point: str) -> None:
        QThread.__init__(self, parent)
        self.index = index
        self.id = id
        self.parent = parent
        self.ThreadActive = True
        self.name = name
        self.link = link
        self.point = ast.literal_eval(point)
        self.frame_count = 0

        self.obj_cnt = 0
        self.curr_trackers = []
        pts = np.array(self.point)
        self.mask = np.zeros((500,700), np.uint8)
        cv2.drawContours(self.mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    def run(self):
        W = window.ui.lable_image.width()
        H = window.ui.lable_image.height()
        Capture = cv2.VideoCapture(self.link)
        while self.ThreadActive:
            ret, frame = Capture.read()
            frame = cv2.resize(frame, (700, 500))
            cv2.putText(frame, self.name, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            if ret:
                frame = self.tracking_detect(frame)
                ConvertToQtFormat = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
                pic = ConvertToQtFormat.scaled(W, H, Qt.KeepAspectRatio)
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

        self.car_number = 0
        self.moto_number = 0
        self.bus_number = 0
        self.truck_number = 0
        self.total_number = 0
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
                if self.index == 0:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                elif self.index == 1:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                elif self.index == 2:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                elif self.index == 3:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
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
        if self.index == 0:
            window.ui.value_car.setText(str(self.car_number))
            window.ui.value_moto.setText(str(self.moto_number))
            window.ui.value_bus.setText(str(self.bus_number))
            window.ui.value_truck.setText(str(self.truck_number))
            window.ui.value_total.setText(str(self.car_number + self.moto_number + self.bus_number + self.truck_number))
        if self.index == 1:
            window.ui.value_car_2.setText(str(self.car_number))
            window.ui.value_moto_2.setText(str(self.moto_number))
            window.ui.value_bus_2.setText(str(self.bus_number))
            window.ui.value_truck_2.setText(str(self.truck_number))
            window.ui.value_total_2.setText(str(self.car_number + self.moto_number + self.bus_number + self.truck_number))
        if self.index == 2:
            window.ui.value_car_3.setText(str(self.car_number))
            window.ui.value_moto_3.setText(str(self.moto_number))
            window.ui.value_bus_3.setText(str(self.bus_number))
            window.ui.value_truck_3.setText(str(self.truck_number))
            window.ui.value_total_3.setText(str(self.car_number + self.moto_number + self.bus_number + self.truck_number))
        if self.index == 3:
            window.ui.value_car_4.setText(str(self.car_number))
            window.ui.value_moto_4.setText(str(self.moto_number))
            window.ui.value_bus_4.setText(str(self.bus_number))
            window.ui.value_truck_4.setText(str(self.truck_number))
            window.ui.value_total_4.setText(str(self.car_number + self.moto_number + self.bus_number + self.truck_number))
        #fps = int(1 / (end - start))
        cv2.putText(frame, str(self.id), (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if self.frame_count % 30 == 0:
            con, cur = MainWindow.connect_db(self)
            query1 = """INSERT INTO dataStream (IDcam, numCar, numMoto, numBus, numTruck) 
                                                VALUES('{}','{}','{}','{}','{}')""".format(self.id,
                                                                                           self.car_number,
                                                                                           self.moto_number,
                                                                                           self.bus_number,
                                                                                           self.truck_number)
            cur.execute(query1)
            con.commit()
            cur.close()
            con.close()

        self.frame_count += 1
        return frame

class IndexedButtonWidget(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.button_row = 0
        self.button_column = 0

class AnotherWindow(QMainWindow):
    def __init__(self):

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
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 120))

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
            self.list_point.append((x,y))
            if len(self.list_point) >= 2:
                for i in range(len(self.list_point)-1):
                    x1 = self.list_point[i][0]
                    y1 = self.list_point[i][1]
                    x2 = self.list_point[i+1][0]
                    y2 = self.list_point[i+1][1]
                    qp.drawLine(x1,y1,x2,y2)
                    self.ui.lbl_frame_draw.setPixmap(self.pix)


    def new_dialog(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open file', 'D:/KLTN/Qt5/main/images', "Video Files (*.avi *.mp4 *.flv *.mov  )")
        self.ui.edit_source.setText(filePath)
        Capture = cv2.VideoCapture(filePath)
        _, frame = Capture.read(0)
        frame = cv2.resize(frame,(700,500))
        self.ConvertToQtFormat = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.pix = QPixmap(self.ConvertToQtFormat)
        self.ui.lbl_frame_draw.setPixmap(self.pix)
        self.ui.btn_draw.setEnabled(True)
        self.ui.btn_remove_draw.setEnabled(True)

    def save(self):

        ls = str(self.list_point)
        con, cur = MainWindow.connect_db(self)
        query1 = """INSERT INTO Stream (Name, Source, Description, Status, Point_Box) 
                                    VALUES('{}','{}','{}','{}','{}')""".format(self.ui.edit_name.text(), self.ui.edit_source.text(), self.ui.edit_description.text(), "Stop", ls)
        cur.execute(query1)
        con.commit()
        query2 = "select * from Stream"
        cur.execute(query2)
        stream = cur.fetchall()
        cur.close()
        con.close()
        window.stream_page()
        self.destroy()
    def reset(self):
        self.ui.edit_name.clear()
        self.ui.edit_source.clear()
        self.ui.edit_description.clear()
        self.ui.lbl_frame_draw.clear()
        self.list_point.clear()
        self.ui.btn_draw.setEnabled(False)
        self.ui.btn_remove_draw.setEnabled(False)
        self.check_event = False
        self.check_draw = False
        self.ui.btn_draw.setText("Draw")

if __name__ == "__main__":

    #detect_fn = model.load_model()
    detect_fn=""
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())



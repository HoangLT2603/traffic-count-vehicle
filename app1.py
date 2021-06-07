import math
import sys
import os
import platform
from typing import *

import cv2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, Signal, QThread)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QImage)
from PySide2.QtWidgets import *
import time
# GUI FILE
import model
from app import *

import psycopg2

# GLOBAL
WINDOW_SIZE = 0


class MainWindow(QMainWindow):
    def __init__(self, cam : Dict[int, str]) -> None:
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cams = cam


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

        self.ui.btn_minimize.clicked.connect(lambda :self.showMinimized())
        self.ui.btn_close.clicked.connect(lambda :self.close())
        self.ui.btn_menu.clicked.connect(lambda :self.slideleftmenu())

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        self.ui.btn_home.clicked.connect(lambda :self.ui.stackedWidget.setCurrentWidget(self.ui.page_home))
        self.ui.btn_watch.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_watch))
        self.ui.btn_stream.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_stream))
        self.ui.btn_model.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_model))
        #self.ui.btn_setting.clicked.connect(self.show_new_window)
        self.ui.btn_stop.clicked.connect(self.CancelFeed)
        self.ui.btn_start.clicked.connect(self.run_thread)





        self.showFullScreen()

    def run_thread(self):
        global W, H
        W = self.ui.lable_image.width()
        H = self.ui.lable_image.height()

        self.cameras: Dict[int, List[Any]] = OrderedDict()
        index = 0
        for cam_id, link in cams.items():
            self.cameras[index] = [cam_id, link, False]
            index += 1
        self.thread: List[thread_cam] = []
        for index, value in self.cameras.items():
            cam_id, link, active = value
            slot = thread_cam(self, index, cam_id, link)
            slot.ImageUpdate.connect(self.ImageUpdateSlot)
            self.thread.append(slot)
        for x in self.thread:
            x.start()
    def ImageUpdateSlot(self, Image, index: int, cam_id: int, active: bool)-> None:
        if index == 0:
            self.ui.lable_image.setPixmap(QPixmap.fromImage(Image))
        if index ==1 :
            self.ui.lable_image_2.setPixmap(QPixmap.fromImage(Image))
        if index ==2 :
            self.ui.lable_image_3.setPixmap(QPixmap.fromImage(Image))
        if index ==3 :
            self.ui.lable_image_4.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.thread_cam.stop()

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






class thread_cam(QThread):
    ImageUpdate = Signal(QImage, int, int , bool)
    def __init__(self, parent: QWidget, index: int, cam_id: int, link: str) -> None:
        QThread.__init__(self, parent)
        self.parent = parent
        self.index = index
        self.cam_id = cam_id
        self.link = link
        self.ThreadActive = True
        self.frame_count = 0
        self.car_number = 0
        self.obj_cnt = 0
        self.curr_trackers = []
    def run(self):
        Capture = cv2.VideoCapture(self.link)
        while self.ThreadActive:
            ret, frame = Capture.read()
            start = time.time()
            frame = cv2.resize(frame, (700, 500))

            if ret:

                frame = self.tracking_detect(frame)

                ConvertToQtFormat = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
                pic = ConvertToQtFormat.scaled(W, H, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic, self.index, self.cam_id, self.ThreadActive)
                end = time.time()
                print("FPS: {}".format(int(1/(end - start))))
    def stop(self):
        self.ThreadActive = False
        self.quit()

    def tracking_detect(self, frame):

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
            self.new_obj['tracker_id'] = car['tracker_id']
            self.new_obj['tracker'] = self.tracker

            # tính toán tâm đối tượng
            x, y, w, h, center_X, center_Y = model.get_box_info(box)

            # Ve hinh chu nhat quanh doi tuong
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Ve hinh tron tai tam doi tuong
            cv2.circle(frame, (center_X, center_Y), 4, (0, 255, 0), -1)

            if center_X > self.imW -10 or center_X < 10 or center_Y < 10 or center_Y > self.imH -10:
                # Neu vuot qua thi khong track nua ma dem xe
                laser_line_color = (0, 255, 255)
                self.car_number += 1

            else:
                # Con khong thi track tiep
                self.curr_trackers.append(self.new_obj)

        # Thuc hien object detection moi 5 frame
        if self.frame_count % 5 == 0:
            # Detect doi tuong
            boxes_d, classed = model.get_object(frame, detect_fn)

            for box in boxes_d:
                #old_obj = False

                xd, yd, wd, hd, center_Xd, center_Yd = model.get_box_info(box)
                #cv2.rectangle(frame, (xd, yd), ((xd + wd), (yd + hd)), (0, 255, 255), 2)
                # Duyet qua cac box, neu sai lech giua doi tuong detect voi doi tuong da track ko qua max_distance thi coi nhu 1 doi tuong
                if not model.is_old(center_Xd, center_Yd, self.boxes):
                    #cv2.rectangle(frame, (xd, yd), ((xd + wd), (yd + hd)), (0, 255, 255), 2)
                    # Tao doi tuong tracker moi

                    tracker = cv2.TrackerMOSSE_create()
                    self.obj_cnt += 1
                    new_obj = dict()
                    tracker.init(frame, tuple(box))

                    new_obj['tracker_id'] = self.obj_cnt
                    new_obj['tracker'] = tracker

                    self.curr_trackers.append(new_obj)

        # Tang frame
        self.frame_count += 1
        return frame


if __name__ == "__main__":
    cams : Dict[int, Any] = OrderedDict()
    cams[1] = 'images/cam2.mp4'
    #cams[2] = 'images/cam2.mp4'
    #cams[3] = 'images/cam3.mp4'
   # cams[4] = 'images/cam4.mp4'




    detect_fn = ""
    app = QApplication(sys.argv)
    window = MainWindow(cam=cams)
    sys.exit(app.exec_())

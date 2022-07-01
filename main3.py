
from os import path
import time
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.uic import loadUiType
from PyQt5.uic import loadUi
from connexion_sqlite import Comunication
import sqlite3
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, QTimer
import os.path
import sqlite3
import cv2
import string
import time



class Function:
    def loading(self):
        self.screen = SplashScreen()
        self.screen.show()
        for i in range(100):
            self.screen.progressBar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.1)
        self.screen.close()

class SplashScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spash Screen Example')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40)  # x, y
        self.labelTitle.setText('Splash Screen')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Working on Task #1</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('loading...')

        self.setStyleSheet('''
                        #LabelTitle {
                            font-size: 60px;
                            color: #93deed;
                        }

                        #LabelDesc {
                            font-size: 30px;
                            color: #c2ced1;
                        }

                        #LabelLoading {
                            font-size: 30px;
                            color: #e8e8eb;
                        }

                        QFrame {
                            background-color: #2F4454;
                            color: rgb(220, 220, 220);
                        }

                        QProgressBar {
                            background-color: #DA7B93;
                            color: rgb(200, 200, 200);
                            border-style: none;
                            border-radius: 10px;
                            text-align: center;
                            font-size: 30px;
                        }

                        QProgressBar::chunk {
                            border-radius: 10px;
                            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
                        }
                    ''')

class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout_window = QVBoxLayout()
        self.setLayout(layout_window)
        self.button = QPushButton("Open", self)
        layout_window.addWidget(self.button)
        self.button.clicked.connect(self.open)

    def open(self):
        self.function = Function()
        self.function.loading()


class MainApp(QtWidgets.QMainWindow):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir,"data.db")
    dbConnection = ''


    def initDBConnection(self):
        self.dbConnection = sqlite3.connect(self.db_path)



    def __init__(self):
        super(MainApp, self).__init__()
        FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main5.ui"))  # there is no error here!
        loadUi("main5.ui", self)
        self.btn_menu.clicked.connect(self.mover_menu)
        self.data = Comunication()
        self.btn_minus.hide()
        self.table_one.setColumnWidth(0,100)
        self.table_one.setColumnWidth(1, 200)
        self.table_one.setColumnWidth(2, 200)
        self.table_one.setColumnWidth(3, 300)
        self.btn_refresh.clicked.connect(self.aff_employee)
        self.btn_ADD.clicked.connect(self.register_employee)
        self.btn_camera.clicked.connect(self.takePicture)
        # Update time
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.date_label.setText(current_date)
        self.time_label.setText(current_time)

        self.image = None
        self.btn_start.clicked.connect(self.start_webcom)
        self.btn_stop.clicked.connect(self.stop_webcom)
        #self.btn_search.clicked.connect(self.searchByID_employee)
        #self.initDBConnection()

        # controle zone 'header'

        self.btn_min.clicked.connect(self.control_btn_min)
        self.btn_minus.clicked.connect(self.control_btn_normal)
        self.btn_max.clicked.connect(self.control_btn_max)
        self.btn_exit.clicked.connect(lambda: self.close())
        # set a little changement on style of main window
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #size Grip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # move header
        self.frame_header.mouseMoveEvent = self.mover_process
        # shifting between pages
        self.btn_base.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_list))
        self.btn_add.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_register))
        #self.btn_eliminate.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_delete))
        self.btn_attendance.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_attend))
        # get adoptable colomuns
        self.table_two.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_one.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def open(self):
        self.window = Window()
        self.window.show()

    def control_btn_min(self):
        self.showMinimized()

    def control_btn_normal(self):
        self.showNormal()
        self.btn_minus.hide()
        self.btn_max.show()

    def control_btn_max(self):
        self.showMaximized()
        self.btn_max.hide()
        self.btn_minus.show()
        

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # mover menu
    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def mover_process(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position == event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10:
            self.showMaximized()
            self.btn_max.hide()
            self.btn_minus.show()
        else:
            self.showNormal()
            self.btn_minus.hide()
            self.btn_max.show()


    def mover_menu(self, event):
        if True:
            width = self.frame_menu.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animation = QtCore.QPropertyAnimation(self.frame_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(extender)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def aff_employee(self):
        result = self.data.affichage_employee()
        for row_number,row_data in enumerate(result):
            self.table_one.insertRow(row_number)
            for column_number,column_data in enumerate(row_data):
                it = str(column_data)
                self.table_one.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(it))


    def register_employee(self):
        code = self.reg_code.text()
        first_name = self.reg_first_name.text()
        last_name = self.reg_last_name.text()
        mail = self.reg_email.text()
        con = sqlite3.connect("data.db")
        c = con.cursor()
        new_data = (code, first_name, last_name, mail)
        sql = ("INSERT INTO employees(RH_code,Last_Name,Start_Name,Email) VALUES(?,?,?,?);")
        c.execute(sql,new_data)
        self.signal_register.setText('REGISTRED')
        con.commit()
        con.close()
        self.reg_code.clear()
        self.reg_first_name.clear()
        self.reg_last_name.clear()
        self.reg_email.clear()



    def takePicture(self):
        last_record = self.data.fetch_last_row()
        full_name ='_'.join([str(item) for item in last_record])
        full_name2 =full_name.replace("(", "")
        full_name3 = full_name2.replace(")", "")
        full_name4 = full_name3.replace("'", "")
        full_name5 = full_name4.replace(",", "_")
        full_name6 = full_name5.replace(" ", "")
        print(full_name6)
        cap = cv2.VideoCapture(0)
        time.sleep(3)
        nframes = 3
        interval = 5

        for i in range(nframes):
            ret, img = cap.read()
            cv2.imshow("IMAGE", img)
            time.sleep(8)
            # save file
            path = 'C:/Users/user/Desktop/stage_pfe/attendance_system/test_image'
            cv2.imwrite(os.path.join(path, full_name6 + str(i) +'.jpg'), img)
            # wait 5 seconds
            time.sleep(interval)


    def start_webcom(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,550)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,350)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)


    def update_frame(self):
        ret,self,image = self.capture.read()
        self.image = cv2.flip(self.image,1)
        self.displayImage(self.image, 1)


    def displayImage(self,img,window=1):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4 :
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outImage = QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)

        outImage = outImage.rgbSwapped()

        if window == 1:
            self.label_camera.setPixmap(QPixmap.fromImage(outImage))
            self.label_camera.setScaledContents(True)


    def stop_webcom(self):
        self.timer.stop()



#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    main_app = MainApp()
#    main_app.show()
#    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MainApp()
    myapp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')












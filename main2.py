from os import path
import time
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QLabel, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.uic import loadUiType
from PyQt5.uic import loadUi

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Attendance system')
        self.setFixedSize(900, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300  # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

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
        self.labelTitle.setText('Face recognition')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Attendance system</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('loading...')

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Created By</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Jazi Safa</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)
            self.myApp = MainApp()
            self.myApp.show()


        self.counter += 1


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__),
                                             "main3.ui"))  # there is no error here!
        loadUi("main3.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton.clicked.connect(lambda: app.exit())
        self.pushButton_2.clicked.connect(lambda: self.showMaximized())
        self.pushButton_3.clicked.connect(lambda: self.showMinimized())
        self.Side_Menu_Num = 0
        self.toolButton.clicked.connect(lambda: self.Side_Menu_Num_Def_0())


    def Side_Menu_Num_Def_0(self):
        if self.Side_Menu_Num == 0:
            self.animation1 = QtCore.QPropertyAnimation(self.frame_4,b"maximumWidth")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(40)
            self.animation1.setEndValue(125)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation1.start()

            self.animation2 = QtCore.QPropertyAnimation(self.frame_4, b"minimumWidth")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(40)
            self.animation2.setEndValue(125)
            self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation2.start()
            self.Side_Menu_Num = 1
        else:

            self.animation1 = QtCore.QPropertyAnimation(self.frame_4, b"maximumWidth")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(125)
            self.animation1.setEndValue(40)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation1.start()

            self.animation2 = QtCore.QPropertyAnimation(self.frame_4, b"minimumWidth")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(125)
            self.animation2.setEndValue(40)
            self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation2.start()
        code = self.reg_code.text().upper()
            self.Side_Menu_Num = 0


    def register_employee(self):
        first_name = self.reg_first_name.text().upper()
        last_name = self.reg_last_name.text().upper()
        mail = self.reg_email.text().upper()
        if code != '' and first_name != '' and last_name != '' and mail != '':
            self.data.insert_employee(code, first_name, last_name, mail)
            self.signal_register.setText('registred')
            self.reg_code.clear()
            self.reg_last_name.clear()
            self.reg_last_name.clear()
            self.reg_email.clear()
        else:
            self.signal_register.setText('Empty space(s)')

    def searchByID_employee(self):
        id_employee = self.research_delete.text().upper()
        id_employee = str("'" + id_employee + "'")
        employee = self.data.chercher_employee(id_employee)
        self.table_two.setRowCount(len(employee))
        if len(employee) == 0:
            self.signal_delete.setText('No Exist')
        else:
            self.signal_delete.setText('Selected')
        tablerow = 0
        for row in employee:
            self.employee_del= row[2]
            self.table_two.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.table_two.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.table_two.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.table_two.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[4]))
            tablerow += 1

    def delete_employee(self):
        self.row_flag = self.table_two.currentRow()
        if self.row_flag == 0:
            self.table_two.removeRow(0)
            self.data.delete_employee("'" + self.employee_del + "'")
            self.signal_delete.setText('Deleted')
            self.research_delete.setText('')





if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
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

    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')



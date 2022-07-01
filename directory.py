import os.path
from os import path
import time
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.uic import loadUiType
from PyQt5.uic import loadUi
import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main5.ui"))

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_refresh_button(self
                                   )



def handle_refresh_button(self):
    self.btn_refresh.clicked.connect(self.GET_DATA)


    def GET_DATA(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        command = ''' SELECT * FROM employees '''
        result = cursor.execute(command)
        self.table_one.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table_one.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = str(column_data)
                self.table_one.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
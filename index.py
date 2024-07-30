from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import numpy as np
import pandas as pd
import sys
from pathlib import Path
# from res_rc import *  # Import the resource module
from PyQt5.uic import loadUiType

ui, _ = loadUiType('main.ui')

class MainApp(QMainWindow, ui):

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.resize(1450, 900)
        self.handel_buttons()
        self.ui_changes()

    def ui_changes(self):
        self.tabWidget.tabBar().setVisible(False)

    def handel_buttons(self):
        self.close_left_frame.clicked.connect(self.toggle_side_bar)
        self.pushButton.clicked.connect(self.open_tab_1)
        self.pushButton_2.clicked.connect(self.open_tab_2)
        self.pushButton_3.clicked.connect(self.open_tab_3)
        self.pushButton_4.clicked.connect(self.open_tab_4)
        self.tabWidget_5.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        print(index)
        self.tabWidget_5.removeTab(index)
    # def create_table_of_signals(self):
    #     self.table_of_signals.setColumnCount(4)
    #     self.table_of_signals.setHorizontalHeaderLabels(('Frequency', 'Amplitude', 'Shift', ''))
    #     self.table_of_signals.setColumnWidth(0, 130)
    #     self.table_of_signals.setColumnWidth(1, 130)
    #     self.table_of_signals.setColumnWidth(2, 100)
    #     self.table_of_signals.setColumnWidth(3, 70)
    #     self.add_row()
    #
    # def add_row(self):
    #     row = self.table_of_signals.rowCount()
    #     self.table_of_signals.setRowCount(row + 1)
    #     self.table_of_signals.setRowHeight(row, 30)
    #
    #     for col in range(4):  # Add buttons to all columns (0, 1, 2, 3)
    #         if col == 3:  # For the last column (index 3), add the delete button
    #             button = QPushButton()
    #             button.setObjectName(f'delete_btn{row}')
    #             button.setIcon(QIcon('icons/trash copy.svg'))
    #             button.setStyleSheet("QPushButton{background-color: rgba(255,255,255,0); border:1px solid rgba(255,255,255,0);} QPushButton:pressed{margin-top:2px }")
    #             self.table_of_signals.setCellWidget(row, col, button)
    #             button.clicked.connect(lambda _, row=row: self.delete_row(row))
    #
    # def delete_row(self, row):
    #     if row >= 0 and row < self.table_of_signals.rowCount():
    #         for col in range(4):  # Remove widgets/items from all columns (0, 1, 2, 3)
    #             if col == 3:
    #                 button = self.table_of_signals.cellWidget(row, col)
    #                 if button is not None:
    #                     button.deleteLater()
    #             else:
    #                 item = self.table_of_signals.item(row, col)
    #                 if item is not None:
    #                     item = None
    #         self.table_of_signals.removeRow(row)
    #
    #         # Update the button object names and click connections for the remaining rows
    #         for i in range(row, self.table_of_signals.rowCount()):
    #             button = self.table_of_signals.cellWidget(i, 3)
    #             if button is not None:
    #                 button.setObjectName(f'delete_btn{i}')
    #                 button.clicked.disconnect()  # Disconnect previous click connection
    #                 button.clicked.connect(lambda _, row=i: self.delete_row(row))  # Connect a new click connection
    # In the above code:
    # - We remove the widgets/items from the row that is being deleted, including the delete button.
    # - We then update the button object names and click connections for the remaining rows.
    # - By disconnecting the previous click connection and connecting a new one, we ensure that the lambda function captures the correct row index for each button.


    ##################################open taps#############################################
    def open_tab_1(self):
        self.tabWidget.setCurrentIndex(0)

    def open_tab_2(self):
        self.tabWidget.setCurrentIndex(1)

    def open_tab_3(self):
        self.tabWidget.setCurrentIndex(2)

    def open_tab_4(self):
        self.tabWidget.setCurrentIndex(3)



    def toggle_side_bar(self):
        if self.left_frame.width() == 0:
            new_width = 250
        else:
            new_width = 0
        self.animation = QPropertyAnimation(self.left_frame, b"minimumWidth")
        self.animation.setDuration(40)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
        self.left_frame.update()





def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

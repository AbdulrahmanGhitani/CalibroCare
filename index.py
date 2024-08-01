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
        self.tab_buttons_list = [self.operation_btn, self.clinics_btn, self.anesthesia_btn, self.blood_btn, self.IVF_btn]
        self.handel_buttons()
        self.ui_changes()
        self.create_defibrialtor_table()
    def ui_changes(self):
        self.main_tabWidget.tabBar().setVisible(False)

    def handel_buttons(self):
        self.close_left_frame.clicked.connect(self.toggle_side_bar)

        for i, btn in enumerate(self.tab_buttons_list):
            btn.clicked.connect(lambda _, index=i: self.open_tab(index))



        self.add_defibrilator_btn.clicked.connect(self.add_row)
        self.operation_tabWidget.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        print(index)
        self.operation_tabWidget.removeTab(index)

    def create_defibrialtor_table(self):
        self.defibrilator_table.setColumnCount()
        self.defibrilator_table.setHorizontalHeaderLabels(('Name', 'Serial', 'Shift', ''))
        self.defibrilator_table.setColumnWidth(0, 130)
        self.defibrilator_table.setColumnWidth(1, 130)
        self.defibrilator_table.setColumnWidth(2, 100)
        self.defibrilator_table.setColumnWidth(3, 70)
        self.add_row()

    def add_row(self):
        row = self.defibrilator_table.rowCount()
        self.defibrilator_table.setRowCount(row + 1)
        self.defibrilator_table.setRowHeight(row, 30)

        for col in range(4):  # Add buttons to all columns (0, 1, 2, 3)
            if col == 3:  # For the last column (index 3), add the delete button
                button = QPushButton()
                button.setObjectName(f'delete_btn{row}')
                button.setIcon(QIcon('icons/trash copy.svg'))
                button.setStyleSheet("QPushButton{background-color: rgba(255,255,255,0); border:1px solid rgba(255,255,255,0);} QPushButton:pressed{margin-top:2px }")
                self.defibrilator_table.setCellWidget(row, col, button)
                button.clicked.connect(lambda _, row=row: self.delete_row(row))

    def delete_row(self, row):
        if row >= 0 and row < self.defibrilator_table.rowCount():
            for col in range(4):  # Remove widgets/items from all columns (0, 1, 2, 3)
                if col == 3:
                    button = self.defibrilator_table.cellWidget(row, col)
                    if button is not None:
                        button.deleteLater()
                else:
                    item = self.defibrilator_table.item(row, col)
                    if item is not None:
                        item = None
            self.defibrilator_table.removeRow(row)

            # Update the button object names and click connections for the remaining rows
            for i in range(row, self.defibrilator_table.rowCount()):
                button = self.defibrilator_table.cellWidget(i, 3)
                if button is not None:
                    button.setObjectName(f'delete_btn{i}')
                    button.clicked.disconnect()  # Disconnect previous click connection
                    button.clicked.connect(lambda _, row=i: self.delete_row(row))  # Connect a new click connection
    # In the above code:
    # - We remove the widgets/items from the row that is being deleted, including the delete button.
    # - We then update the button object names and click connections for the remaining rows.
    # - By disconnecting the previous click connection and connecting a new one, we ensure that the lambda function captures the correct row index for each button.


    ##################################open taps#############################################
    # Define the open_tab function
    def open_tab(self, tab_index):
        self.main_tabWidget.setCurrentIndex(tab_index)



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

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
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

WINDOW_SIZE = 0

class MainApp(QMainWindow, ui):

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.resize(1450, 900)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.tab_buttons_list = [self.operation_btn, self.clinics_btn, self.anesthesia_btn, self.blood_btn,
                                 self.IVF_btn]
        self.devices_tables_list = [self.ventilator_table, self.vaporizer_table, self.ultrasound_operation_table,
                                    self.suction_table, self.monitor_operation_table, self.electrosurgery_table,
                                    self.diathermy_table, self.defibrilator_table, self.incubator_table,
                                    self.autoclave_table, self.monitor_sterilization_table,
                                    self.sphygmomanometer_sterilization_table, self.ecg_sterilization_table,
                                    self.ultrasound_clinics_table, self.ecg_table, self.sphygmomanometer_clinics_table,
                                    self.thermometer_table, self.laminar_IVF_table, self.freezing_table,
                                    self.laminar_blood_table, self.balance_table, self.centrifuge_table]

        self.add_device_btn_list = [self.add_ventilator_btn, self.add_vaporizer_btn, self.add_ultrasound_operation_btn,
                                    self.add_suction_btn, self.add_monitor_operation_btn, self.add_electrosurgery_btn,
                                    self.add_diathermy_btn, self.add_defibrilator_btn, self.add_incubator_btn,
                                    self.add_autoclave_btn, self.add_monitor_sterilization_btn,
                                    self.add_sphygmomanometer_sterilization_btn, self.add_ecg_sterilization_btn,
                                    self.add_ultrasound_clinics_btn, self.add_ecg_btn, self.add_sphygmomanometer_clinics_btn,
                                    self.add_thermometer_btn, self.add_laminar_IVF_btn, self.add_freezing_btn,
                                    self.add_laminar_blood_btn, self.add_balance_btn, self.add_centrifuge_btn]

        self.handel_buttons()
        self.ui_changes()
        self.create_tables()

    def ui_changes(self):
        self.main_tabWidget.tabBar().setVisible(False)

    def handel_buttons(self):
        self.close_left_frame.clicked.connect(self.toggle_side_bar)

        # connect each btn in left frame with corresponding tab
        for i, btn in enumerate(self.tab_buttons_list):
            btn.clicked.connect(lambda _, index=i: self.open_tab(index))

        # connect each add_row btn with add_row function and with it is table
        for btn, table in zip(self.add_device_btn_list, self.devices_tables_list):
            btn.clicked.connect(lambda _, table=table: self.add_row(table))

        self.restore_btn.clicked.connect(lambda: self.restore_or_maximize_window())
        self.close_btn.clicked.connect(lambda: self.close())
        self.minimize_btn.clicked.connect(lambda: self.showMinimized())

        self.operation_tabWidget.tabCloseRequested.connect(self.close_tab)

    # Restore or maximize your window
    def restore_or_maximize_window(self):
        # Global windows state
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
        else:
            WINDOW_SIZE = 0
            self.showNormal()

    def close_tab(self, index):
        print(index)
        self.operation_tabWidget.removeTab(index)

    def create_tables(self):
        for table in (self.devices_tables_list):
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(('Name', 'Serial', 'Shift', '', ''))

            # Stretch the first three columns to fill the available space
            header = table.horizontalHeader()
            for i in range(3):  # Columns 0 to 2
                header.setSectionResizeMode(i, QHeaderView.Stretch)

            # Set the last column to a fixed width
            for i in range(3, 5):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)  # Column 3
                table.setColumnWidth(i, 120)
            self.add_row(table)

    def add_row(self, table):
        row = table.rowCount()
        table.setRowCount(row + 1)
        table.setRowHeight(row, 30)

        for col in range(5):  # Add buttons to all columns (0, 1, 2, 3)
            if col == 3:  # For the last column (index 3), add the delete button
                button = QPushButton()
                button.setObjectName(f'delete_btn{row}')
                button.setIcon(QIcon('icons/trash copy.svg'))
                button.setStyleSheet(
                    "QPushButton{background-color: rgba(255,255,255,0); border:1px solid rgba(255,255,255,0);} QPushButton:pressed{margin-top:2px }")
                table.setCellWidget(row, col, button)
                button.clicked.connect(lambda _, row=row: self.delete_row(table, row))
            elif col == 4:
                button = QPushButton()
                button.setObjectName(f'delete_btn{row}')
                button.setIcon(QIcon('icons/trash copy.svg'))
                button.setStyleSheet(
                    "QPushButton{background-color: rgba(255,255,255,0); border:1px solid rgba(255,255,255,0);} QPushButton:pressed{margin-top:2px }")
                table.setCellWidget(row, col, button)
                button.clicked.connect(lambda _, row=row: self.delete_row(table, row))

    def delete_row(self, table, row):
        if row >= 0 and row < table.rowCount():
            for col in range(4):  # Remove widgets/items from all columns (0, 1, 2, 3)
                if col == 3:
                    button = table.cellWidget(row, col)
                    if button is not None:
                        button.deleteLater()
                else:
                    item = table.item(row, col)
                    if item is not None:
                        item = None
            table.removeRow(row)

            # Update the button object names and click connections for the remaining rows
            for i in range(row, table.rowCount()):
                button = table.cellWidget(i, 3)
                if button is not None:
                    button.setObjectName(f'delete_btn{i}')
                    button.clicked.disconnect()  # Disconnect previous click connection
                    button.clicked.connect(
                        lambda _, row=i: self.delete_row(table, row))  # Connect a new click connection

    # In the above code:
    # - We remove the widgets/items from the row that is being deleted, including the delete button.
    # - We then update the button object names and click connections for the remaining rows.
    # - By disconnecting the previous click connection and connecting a new one, we ensure that the lambda function captures the correct row index for each button.

    ##################################open taps#############################################
    # Define the open_tab function
    def open_tab(self, tab_index):
        self.main_tabWidget.setCurrentIndex(tab_index)

    def toggle_side_bar(self):
        width = self.left_frame.width()
        if width == 60:
            new_width = 300
        else:
            new_width = 60
        self.animation = QPropertyAnimation(self.left_frame, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
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

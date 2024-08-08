from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# import pyqtgraph as pg
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
# from pathlib import Path
from res_rc import *  # Import the resource module
from PyQt5.uic import loadUiType
from models import *
from collections import defaultdict


# Load the main window UI
MainUI, _ = loadUiType('main.ui')
# Load the add device form UI
FormUI, _ = loadUiType('addDeviceForm.ui')

WINDOW_SIZE = 0


class MainApp(QMainWindow, MainUI):

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.resize(1450, 900)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.tab_buttons_list = [self.operation_btn, self.clinics_btn, self.anesthesia_btn, self.blood_btn,
                                 self.IVF_btn]

        self.devices_tables_dict = {
            "Operations": [
                ("Ventilator", self.ventilator_table),  # 1
                ("Vaporizer", self.vaporizer_table),  # 2
                ("Ultrasound", self.ultrasound_operation_table),  # 3
                ("Suction", self.suction_table),  # 4
                ("Monitor", self.monitor_operation_table),  # 5
                ("Electrosurgery", self.electrosurgery_table),  # 6
                ("Diathermy", self.diathermy_table),  # 7
                ("Defibrillator", self.defibrilator_table)  # 8
            ],
            "Sterilization and Recovery": [
                ("Incubator", self.incubator_table),  # 9
                ("Autoclave", self.autoclave_table),  # 10
                ("Monitor", self.monitor_sterilization_table),  # 11
                ("Sphygmomanometer",
                 self.sphygmomanometer_sterilization_table),  # 12
                ("ECG", self.ecg_sterilization_table)  # 13
            ],
            "Clinics": [
                ("Ultrasound", self.ultrasound_clinics_table),  # 14
                ("ECG", self.ecg_table),  # 15
                ("Sphygmomanometer",
                 self.sphygmomanometer_clinics_table)  # 16
            ],
            "IVF lab": [
                ("Digital Thermometer", self.thermometer_table),  # 17
                ("Laminar", self.laminar_IVF_table)  # 18
            ],
            "Blood and Andrology": [
                ("Freezing", self.freezing_table),  # 19
                ("Laminar", self.laminar_blood_table),  # 20
                ("Balance", self.balance_table),  # 21
                ("Centrifuge", self.centrifuge_table)  # 22
            ]
        }

        self.tables_list = [
            table for devices in self.devices_tables_dict.values() for _, table in devices]

        self.add_device_btn_list = [self.add_ventilator_btn, self.add_vaporizer_btn, self.add_ultrasound_operation_btn,
                                    self.add_suction_btn, self.add_monitor_operation_btn, self.add_electrosurgery_btn,
                                    self.add_diathermy_btn, self.add_defibrilator_btn, self.add_incubator_btn,
                                    self.add_autoclave_btn, self.add_monitor_sterilization_btn,
                                    self.add_sphygmomanometer_sterilization_btn, self.add_ecg_sterilization_btn,
                                    self.add_ultrasound_clinics_btn, self.add_ecg_btn,
                                    self.add_sphygmomanometer_clinics_btn,
                                    self.add_thermometer_btn, self.add_laminar_IVF_btn, self.add_freezing_btn,
                                    self.add_laminar_blood_btn, self.add_balance_btn, self.add_centrifuge_btn]

        self.side_bar_icons = {
            'Operations': QIcon('icons/operation.png'),
            'Clinics': QIcon('icons/clinics.png'),
            'Sterilization and Recovery': QIcon('icons/anesthesia.png'),
            'Blood and Andrology': QIcon('icons/blood.png'),
            'IVF lab': QIcon('icons/ivf.png')
        }

        self.handle_buttons()
        self.ui_changes()
        self.create_tables()
        self.fill_table()

        self.clickPosition = None
        # Set the mouse move event handler for upper_frame
        self.upper_frame.mouseMoveEvent = self.move_window

        # Departmets for database
        self.depts = [
            "Operations", "Clinics", "Sterilization and Recovery", "Blood and Andrology", "IVF lab"
        ]

        self.devices_names = [
            "Ventilator", "Vaporizer", "Suction", "Electrosurgery",
            "Diathermy", "Defibrillator", "Incubator", "Autoclave", "Monitor",
            "Sphygmomanometer", "Ultrasound", "ECG",
            "Digital Thermometer", "Laminar", "Freezing",
            "Balance", "Centrifuge"
        ]

        self.return_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPosition = event.globalPos()

    def move_window(self, event):
        if self.isMaximized():
            return
        if event.buttons() == Qt.LeftButton and self.clickPosition is not None:
            # Move the window
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    def ui_changes(self):
        self.main_tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        self.close_left_frame.clicked.connect(self.toggle_side_bar)

        # connect each btn in left frame with corresponding tab
        for i, btn in enumerate(self.tab_buttons_list):
            btn.clicked.connect(lambda _, index=i: self.open_tab(index))

        # connect each add_device btn with open form function and with it is table
        for btn, table in zip(self.add_device_btn_list, self.tables_list):
            btn.clicked.connect(lambda _, table=table: self.open_form(table))

        self.restore_btn.clicked.connect(lambda: self.restore_or_maximize_window())
        self.close_btn.clicked.connect(lambda: self.close())
        self.minimize_btn.clicked.connect(lambda: self.showMinimized())

        self.operation_tabWidget.tabCloseRequested.connect(self.close_tab)

    def open_form(self, table):
        # Create and show the form dialog
        form_dialog = FormDialog(self, table)
        form_dialog.exec_()

    # Restore or maximize your window
    def restore_or_maximize_window(self):
        # Global windows state
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
            self.restore_btn.setIcon(QIcon("icons/white-restore.svg"))
        else:
            WINDOW_SIZE = 0
            self.showNormal()
            self.restore_btn.setIcon(QIcon("icons/white_maximize.svg"))

    def close_tab(self, index):
        print(index)
        self.operation_tabWidget.removeTab(index)

    # why there are create table and fill table they can be a one function
    def create_tables(self):
        for table in self.tables_list:
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionMode(QTableWidget.SingleSelection)
            table.setSelectionBehavior(QTableWidget.SelectRows)

            table.setColumnCount(6)
            table.setHorizontalHeaderLabels(('Name', 'Serial', 'Department', 'Recommendation', '', ''))

            # Stretch the first three columns to fill the available space
            header = table.horizontalHeader()
            for i in range(4):  # Columns 0 to 3
                header.setSectionResizeMode(i, QHeaderView.Stretch)

            # Set the last column to a fixed width
            for i in range(4, 6):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)  # Column 3
                table.setColumnWidth(i, 120)

            # table.cellClicked.connect(lambda row, column, table=table: self.open_device_reading(row, table))
            # self.add_row(table)

    def add_row(self, table, device):
        row = table.rowCount()
        table.setRowCount(row + 1)
        table.setRowHeight(row, 45)

        # Create QTableWidgetItem for each column and center-align text
        serial_item = QTableWidgetItem(device.serial)
        serial_item.setTextAlignment(Qt.AlignCenter)  # Align text center

        name_item = QTableWidgetItem(device.name)
        name_item.setTextAlignment(Qt.AlignCenter)

        dept_item = QTableWidgetItem(device.dept)
        dept_item.setTextAlignment(Qt.AlignCenter)

        recom_item = QTableWidgetItem("Calibrate it every " + str(device.recommendation) + " year/s")
        recom_item.setTextAlignment(Qt.AlignCenter)

        # Add items to the table
        table.setItem(row, 0, name_item)
        table.setItem(row, 1, serial_item)
        table.setItem(row, 2, dept_item)
        table.setItem(row, 3, recom_item)

        # Delete Button
        delete_button = QPushButton()
        delete_button.setObjectName(f'delete_btn{row}')
        delete_button.setIcon(QIcon('icons/trash copy.svg'))
        delete_button.setIconSize(QSize(30, 30))
        delete_button.setStyleSheet(
            "QPushButton{background-color: rgba(255,255,255,0); border:1px solid rgba(255,255,255,0);} QPushButton:pressed{margin-top:2px }")
        table.setCellWidget(row, 4, delete_button)
        delete_button.clicked.connect(lambda _, row=row: self.delete_row(table, row))

        # Open Button
        open_button = QPushButton()
        open_button.setObjectName(f'delete_btn{row}')
        open_button.setIcon(QIcon('icons/open.svg'))
        open_button.setIconSize(QSize(30, 30))
        open_button.setStyleSheet(
            "QPushButton{background-color: rgba(255,255,255,0); border:1px solid rgba(255,255,255,0);} QPushButton:pressed{margin-top:2px }")
        table.setCellWidget(row, 5, open_button)
        open_button.clicked.connect(lambda _, row=row: self.open_device_reading(row, device))


    def delete_row(self, table, row):
        if row >= 0 and row < table.rowCount():
            # delete from data_base
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle('Confirm Deletion')
            msg_box.setText(f"Are you sure you want to delete the device with serial"
                            f" '{table.item(row, 0).text()}-{table.item(row, 1).text()}'?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)

            # Show the message box and capture the user's response
            result = msg_box.exec_()

            if result == QMessageBox.Yes:
                device = Device.get(serial=table.item(row, 0).text())
                device.delete_instance()
                # delete from UI
                for col in range(5):  # Remove widgets/items from all columns (0, 1, 2, 3)
                    if col == 4:
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
                    button = table.cellWidget(i, 4)
                    if button is not None:
                        button.setObjectName(f'delete_btn{i}')
                        button.clicked.disconnect()  # Disconnect previous click connection
                        button.clicked.connect(
                            lambda _, row=i: self.delete_row(table, row))  # Connect a new click connection
            else:
                QMessageBox.information(None, "Cancelled", "Deletion was cancelled.", QMessageBox.Ok)

    # In the above code:
    # - We remove the widgets/items from the row that is being deleted, including the delete button.
    # - We then update the button object names and click connections for the remaining rows.
    # - By disconnecting the previous click connection and connecting a new one, we ensure that the lambda function captures the correct row index for each button.

    def device_readings_from_query(self, serial):
        query = Reading.select().where(Reading.device_serial == serial)
        query_result = [reading.__data__ for reading in query]
        unit = ""
        if query_result[0]["unit"]:
            unit = query_result[0]["unit"]
        else:
            unit = "unitless"

        # Add synthetic year data (this step is just for demonstration purposes)
        for i, record in enumerate(query_result):
            record['year'] = 2017 + i % 6

        # Create a defaultdict to hold the aggregated data
        aggregated_data = defaultdict(lambda: defaultdict(list))

        # Aggregate the data
        for record in query_result:
            year = record['year']
            ref_value = record['ref_value']
            value = record['value']
            aggregated_data[ref_value][year].append(value)

        # Calculate the average for each year and reference value
        final_data = defaultdict(dict)
        for ref_value, years in aggregated_data.items():
            for year, values in years.items():
                final_data[ref_value][year] = sum(values) / len(values)

        # Create a DataFrame from the final_data
        ref_values = sorted(final_data.keys())
        years = sorted({year for years in final_data.values() for year in years})

        data_dict = {f"Reference readings \n({unit})": ref_values}
        for year in years:
            data_dict[str(year)] = [final_data[ref].get(year, None) for ref in ref_values]
        print(data_dict)
        df = pd.DataFrame(data_dict)
        return df, unit

    def open_device_reading(self, row, device):
        self.stackedWidget.setCurrentIndex(1)
        # data = {
        #     "Reference readings (joule)": [5, 10, 20, 50],
        #     "2017": [4.9, 9.8, 19.3, 48.4],
        #     "2018": [8.314133, 14.19761, 24.43751, 52],
        #     "2019": [6.375011, 12.18851, 22.46305, 50.9],
        #     "2020": [5.2, 10.1, 20.1, 50.4],
        #     "2021": [5.1, 10.3, 21.27883111, 51.27627017],
        #     "2022": [5.2, 10.1, 21.15801041, 50.72123629]
        # }

        df, unit = self.device_readings_from_query(device.serial)

        self.fill_readings_table(df)

        # Convert to DataFrame
        # df = pd.DataFrame(data)
        print(df)

        # Calculate mean and standard deviation for each row
        df['mean'] = df.mean(axis=1)
        df['std'] = df.std(axis=1)

        # Calculate UCL and LCL
        df['UCL'] = df['mean'] + 2 * df['std']
        df['LCL'] = df['mean'] - 2 * df['std']

        print(df)

        for index, row in df.iterrows():
            for value in row[1:-4]:  # Exclude 'mean', 'std', 'UCL', 'LCL', and 'recom' columns
                if value > row['UCL'] or value < row['LCL']:
                    device.recommendation = 1
                    break

        # Create a Matplotlib Figure and Canvas
        self.figure, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)

        # Embed the canvas into the QWidget
        self.plot_layout = QVBoxLayout(self.plot_widget_1)

        self.plot_layout.addWidget(self.canvas)

        # Plot the control chart
        self.plot_control_chart(df, unit)

    def plot_control_chart(self, df, unit):
        """Plot the control chart."""
        # Plot each reference reading series with its own x-axis labels
        for i, reference in enumerate(df[f"Reference readings \n({unit})"]):
            x = [f'{year} ({reference})' for year in df.columns[1:7]]
            y = df.iloc[i, 1:7]
            self.ax.plot(x, y, marker='o', label=f'{reference} {unit}')
            self.ax.plot(x, [df['mean'][i]] * len(x), linestyle='--', color='orange',
                         label=f'Mean {reference} {unit}' if i == 0 else "")
            self.ax.plot(x, [df['UCL'][i]] * len(x), linestyle='--', color='grey',
                         label=f'UCL {reference} {unit}' if i == 0 else "")
            self.ax.plot(x, [df['LCL'][i]] * len(x), linestyle='--', color='grey',
                         label=f'LCL {reference} {unit}' if i == 0 else "")

        # Add plot settings here
        self.ax.set_title('Control Chart')
        self.ax.set_xlabel('Year and Reference Reading')
        self.ax.set_ylabel('Readings')
        self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=90)
        self.ax.legend()
        self.ax.grid(True)

        # Refresh the canvas to show the plot
        self.canvas.draw()

    def fill_readings_table(self, df):
        self.readings_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Set the number of rows and columns
        self.readings_table.setRowCount(len(df.columns))
        self.readings_table.setColumnCount(len(df))

        # Set the horizontal header labels
        self.readings_table.setVerticalHeaderLabels(df.columns.tolist())

        # Fill the table with DataFrame data
        for row in range(len(df)):
            for column in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iat[row, column]))  # Convert each item to string
                item.setTextAlignment(Qt.AlignCenter)  # Center align text
                self.readings_table.setItem(column, row, item)

        # Resize the columns to fit the content
        header = self.readings_table.verticalHeader()
        for column in range(len(df.columns)):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)

    def fill_table(self):
        for dept in self.devices_tables_dict:
            for device, table in self.devices_tables_dict[dept]:
                devices = Device.select().where((Device.name == device) & (Device.dept == dept))
                for element in devices:
                    self.add_row(table, element)

    ##################################open taps#############################################
    # Define the open_tab function
    def open_tab(self, tab_index):
        self.main_tabWidget.setCurrentIndex(tab_index)

    def toggle_side_bar(self):
        width = self.left_frame.width()
        if width == 70:
            new_width = 350
            self.close_left_frame.setIcon(
                QIcon('icons/white_sidebar_fill.svg'))
        else:
            new_width = 70
            self.close_left_frame.setIcon(
                QIcon('icons/white_sidebar_stroke.svg'))
        self.animation = QPropertyAnimation(self.left_frame, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
        self.left_frame.update()


class FormDialog(QDialog, FormUI):
    def __init__(self, parent=None, table=None):
        super(FormDialog, self).__init__(parent)
        self.setupUi(self)
        self.table = table
        self.dept = None

        # display department and it is devices when he click add device button
        for dept in self.parent().devices_tables_dict:
            for device, table in self.parent().devices_tables_dict[dept]:
                if table == self.table:
                    self.dept = dept
                    break
        index = self.dept_comboBox.findText(self.dept)
        if index != -1:
            self.dept_comboBox.setCurrentIndex(index)
            self.change_devices_according_to_dept()

        # handel buttons
        self.dept_comboBox.currentTextChanged.connect(self.change_devices_according_to_dept)
        self.buttonBox.accepted.connect(self.saveDevice)

    def change_devices_according_to_dept(self):
        self.device_comboBox.clear()
        self.dept = self.dept_comboBox.currentText()
        for device, table in self.parent().devices_tables_dict[self.dept]:
            self.device_comboBox.addItem(device)
            if table == self.table:
                index = self.device_comboBox.findText(device)
                if index != -1:
                    self.device_comboBox.setCurrentIndex(index)
    def saveDevice(self):
        # Get data from form
        serial = self.serial_lineEdit.text().strip()
        if not serial:
            QMessageBox.critical(None, "Error", "You should enter the serial number", QMessageBox.Ok)
            return

        try:
            # Check if the device with the given serial number already exists
            Device.get(Device.serial == serial)
            QMessageBox.warning(None, "Warning", "A device with this serial number already exists.", QMessageBox.Ok)

        except Device.DoesNotExist:
            # add device to database
            new_device = Device.create(serial=self.serial_lineEdit.text(), dept=self.dept,
                                       name=self.device_comboBox.currentText(), brand=self.brand_lineEdit.text())
            # add row to ui
            for device, table in self.parent().devices_tables_dict[self.dept]:
                if device == self.device_comboBox.currentText():
                    self.parent().add_row(table, new_device)
                    break

        self.accept()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

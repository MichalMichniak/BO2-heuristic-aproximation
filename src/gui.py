#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import threading
import multiprocessing
from typing import List

global_y = []
global_progress = [0]
global_rdy_flag = [0]
global_edit_1 = ["ds"]
global_arg = [50, 100, 50]
global_exit = [0]

class PlotData:
    def __init__(self, data):
        self.data_x = data[0]
        self.data_y = data[1]


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.layout = QtWidgets.QGridLayout()
        self.set_window()
        self.add_label()
        self.add_plot()
        self.add_progress_bar()
        self.add_start()
        self.add_edit1()
        self.add_edit2()
        self.add_edit3()
        self.setLayout(self.layout)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        # self.graphWidget.setBackground('w')

    def update_plot_data(self):
        self.edit1_label.setText("crossing = " + str(global_arg[0]))
        self.edit2_label.setText("hard mutation = " + str(global_arg[1]))
        self.edit3_label.setText("nearby mutation = " + str(global_arg[2]))
        self.progress_bar.setValue(global_progress[0])
        if len(global_y) > 0:
            self.label.setText("Wartość funkcji celu: \n" + "{:3.2f}".format(global_y[-1]))
        self.data_line.setData([i for i in range(len(global_y))], global_y)  # Update the data.

    def set_window(self):
        self.setWindowTitle("Funkcja celu")
        self.setMaximumWidth(2000)
        self.setMinimumWidth(400)
        self.setMaximumHeight(2000)
        self.setMinimumHeight(400)

    def add_label(self):
        self.label = QtWidgets.QLabel("Wartość funkcji celu: \n ------")
        self.label.setFont(self.label.font())
        font = self.label.font()
        font.setPointSize(30)
        self.label.setFont(font)
        self.layout.addWidget(self.label, 7, 0)

    def add_progress_bar(self):
        self.progress_bar = QtWidgets.QProgressBar()
        self.layout.addWidget(self.progress_bar, 9, 1)

    def add_plot(self):
        self.graphWidget = pg.PlotWidget()
        self.x = [0]
        self.y = [0]
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.layout.addWidget(self.graphWidget, 0, 1, 8, 1)

    def add_start(self):
        self.push_button = QtWidgets.QPushButton()
        self.push_button.setFont(QtGui.QFont("Times", 20))
        self.push_button.setText("Start")
        self.push_button.clicked.connect(self.start_butt)
        self.layout.addWidget(self.push_button, 6, 0)

    def start_butt(self):
        if not global_rdy_flag[0]:
            self.edit1_meth()
            self.edit2_meth()
            self.edit3_meth()
        global_rdy_flag[0] = 1

    def add_edit1(self):
        self.edit1_label = QtWidgets.QLabel()
        self.edit1_label.setText("crossing = " + str(global_arg[0]))
        self.edit1 = QtWidgets.QLineEdit()
        self.edit1.returnPressed.connect(self.edit1_meth)
        self.layout.addWidget(self.edit1, 1, 0)
        self.layout.addWidget(self.edit1_label, 0, 0)

    def add_edit2(self):
        self.edit2_label = QtWidgets.QLabel()
        self.edit2_label.setText("hard mutation = " + str(global_arg[1]))
        self.edit2 = QtWidgets.QLineEdit()
        self.edit2.returnPressed.connect(self.edit2_meth)
        self.layout.addWidget(self.edit2, 3, 0)
        self.layout.addWidget(self.edit2_label, 2, 0)

    def add_edit3(self):
        self.edit3_label = QtWidgets.QLabel()
        self.edit3_label.setText("nearby mutation = " + str(global_arg[2]))
        self.edit3 = QtWidgets.QLineEdit()
        self.edit3.returnPressed.connect(self.edit3_meth)
        self.layout.addWidget(self.edit3_label, 4, 0)
        self.layout.addWidget(self.edit3, 5, 0)


    def edit1_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit1.text()) > 0:
                global_arg[0] = float(self.edit1.text())

    def edit2_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit2.text()) > 0:
                global_arg[1] = float(self.edit2.text())

    def edit3_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit3.text()) > 0:
                global_arg[2] = float(self.edit3.text())

    def set_main_widget(self):
        pass


def start():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

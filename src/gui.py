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
global_no_threads = [0]
global_population = [0]
global_maxit = [0]

class PlotData:
    def __init__(self, data):
        self.data_x = data[0]
        self.data_y = data[1]


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.best_y = 300000000
        self.label = None
        self.layout = QtWidgets.QGridLayout()
        self.set_window()
        self.add_label()
        self.add_plot()
        self.add_progress_bar()
        self.add_start()
        self.add_edit1()
        self.add_edit2()
        self.add_edit3()
        self.add_edit4()
        self.add_edit5()
        self.add_edit6()
        self.add_edit7()
        self.add_edit8()
        self.add_edit9()
        self.add_edit10()
        self.add_edit11()
        self.setLayout(self.layout)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        # self.graphWidget.setBackground('w')

    def update_plot_data(self):
        self.edit1_label.setText("crossing = " + str(global_arg[0]))
        self.edit2_label.setText("hard mutation = " + str(global_arg[1]))
        self.edit3_label.setText("nearby mutation = " + str(global_arg[2]))
        self.edit4_label.setText("argument mutation = " + str(global_arg[3]))
        self.edit5_label.setText("Restrictions = " + str(global_arg[4]))
        self.edit6_label.setText("Type of surviving: \n" + str(global_arg[5]))
        self.edit7_label.setText("T_max: \n" + str(global_arg[6]))
        self.edit8_label.setText("Architecture: \n" + str(global_arg[7]))
        self.edit9_label.setText("Population: " + str(global_population[0]))
        self.edit10_label.setText("Number of threads: " + str(global_no_threads[0]))
        self.edit11_label.setText("Max no iterations: " + str(global_maxit[0]))
        self.progress_bar.setValue(global_progress[0])
        if len(global_y) > 0:
            self.label.setText("Aktualna wartość: \n" + "{:3.2f}".format(global_y[-1]))
            self.best_y = min(self.best_y, global_y[-1])
            self.label_best.setText("Najlepsza wartość: \n" + "{:3.2f}".format(self.best_y))
        self.data_line.setData([i for i in range(len(global_y))], global_y)  # Update the data.
        # print(global_y)

    def set_window(self):
        self.setWindowTitle("Heuristic Aproximation")
        self.setMaximumWidth(2000)
        self.setMinimumWidth(400)
        self.setMaximumHeight(2000)
        self.setMinimumHeight(400)

    def add_label(self):
        self.label = QtWidgets.QLabel("Aktualna wartość: \n ------")
        self.label.setFont(self.label.font())
        font = self.label.font()
        font.setPointSize(13)
        self.label.setFont(font)
        self.layout.addWidget(self.label, 12, 0, 1, 1)

        self.label_best = QtWidgets.QLabel("Najlepsza wartość: \n ------")
        self.label_best.setFont(self.label.font())
        font = self.label_best.font()
        font.setPointSize(13)
        self.label_best.setFont(font)
        self.layout.addWidget(self.label_best, 12, 1, 1, 1)

    def add_progress_bar(self):
        self.progress_bar = QtWidgets.QProgressBar()
        self.layout.addWidget(self.progress_bar, 11, 2)

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
        self.layout.addWidget(self.graphWidget, 0, 2, 10, 1)

    def add_start(self):
        self.push_button = QtWidgets.QPushButton()
        self.push_button.setFont(QtGui.QFont("Times", 20))
        self.push_button.setText("Start")
        self.push_button.clicked.connect(self.start_butt)
        self.layout.addWidget(self.push_button, 13, 0, 1, 2)

    def start_butt(self):
        if not global_rdy_flag[0]:
            self.edit1_meth()
            self.edit2_meth()
            self.edit3_meth()
            self.edit4_meth()
            self.edit5_meth()
            self.edit6_meth()

        global_rdy_flag[0] = 1

    def add_edit1(self):
        self.edit1_label = QtWidgets.QLabel()
        self.edit1_label.setFont(QtGui.QFont("Times", 13))
        self.edit1_label.setText("crossing = " + str(global_arg[0]))
        self.edit1 = QtWidgets.QLineEdit()
        self.edit1.returnPressed.connect(self.edit1_meth)
        self.layout.addWidget(self.edit1, 1, 0)
        self.layout.addWidget(self.edit1_label, 0, 0)

    def add_edit2(self):
        self.edit2_label = QtWidgets.QLabel()
        self.edit2_label.setFont(QtGui.QFont("Times", 13))
        self.edit2_label.setText("hard mutation = " + str(global_arg[1]))
        self.edit2 = QtWidgets.QLineEdit()
        self.edit2.returnPressed.connect(self.edit2_meth)
        self.layout.addWidget(self.edit2, 3, 0)
        self.layout.addWidget(self.edit2_label, 2, 0)

    def add_edit3(self):
        self.edit3_label = QtWidgets.QLabel()
        self.edit3_label.setFont(QtGui.QFont("Times", 13))
        self.edit3_label.setText("nearby mutation = " + str(global_arg[2]))
        self.edit3 = QtWidgets.QLineEdit()
        self.edit3.returnPressed.connect(self.edit3_meth)
        self.layout.addWidget(self.edit3_label, 4, 0)
        self.layout.addWidget(self.edit3, 5, 0)

    def add_edit4(self):
        self.edit4_label = QtWidgets.QLabel()
        self.edit4_label.setFont(QtGui.QFont("Times", 13))
        self.edit4_label.setText("argument mutation = " + str(global_arg[3]))
        self.edit4 = QtWidgets.QLineEdit()
        self.edit4.returnPressed.connect(self.edit4_meth)
        self.layout.addWidget(self.edit4, 1, 1)
        self.layout.addWidget(self.edit4_label, 0, 1)

    def add_edit5(self):
        self.edit5_label = QtWidgets.QLabel()
        self.edit5_label.setFont(QtGui.QFont("Times", 13))
        self.edit5_label.setText("Restrictions = " + str(global_arg[4]))
        self.edit5 = QtWidgets.QComboBox()
        self.edit5.addItem("True")
        self.edit5.addItem("False")
        self.edit5.activated.connect(self.edit5_meth)
        self.layout.addWidget(self.edit5, 3, 1)
        self.layout.addWidget(self.edit5_label, 2, 1)

    def add_edit6(self):
        self.edit6_label = QtWidgets.QLabel()
        self.edit6_label.setFont(QtGui.QFont("Times", 13))
        self.edit6_label.setText("PLACEHOLDER")
        self.edit6 = QtWidgets.QComboBox()
        self.edit6.addItem("roulette")
        self.edit6.addItem("best surviving")
        self.edit6.addItem("tournament")
        self.edit6.activated.connect(self.edit6_meth)
        self.layout.addWidget(self.edit6_label, 4, 1)
        self.layout.addWidget(self.edit6, 5, 1)

    def add_edit7(self):
        self.edit7_label = QtWidgets.QLabel()
        self.edit7_label.setFont(QtGui.QFont("Times", 13))
        self.edit7_label.setText("T_max = " + str(global_arg[6]))
        self.edit7 = QtWidgets.QLineEdit()
        self.edit7.returnPressed.connect(self.edit7_meth)
        self.layout.addWidget(self.edit7_label, 6, 1)
        self.layout.addWidget(self.edit7, 7, 1)

    def add_edit8(self):
        self.edit8_label = QtWidgets.QLabel()
        self.edit8_label.setFont(QtGui.QFont("Times", 13))
        self.edit8_label.setText("Architecture = " + str(global_arg[7]))
        self.edit8 = QtWidgets.QLineEdit()
        self.edit8.returnPressed.connect(self.edit8_meth)
        self.layout.addWidget(self.edit8_label, 6, 0)
        self.layout.addWidget(self.edit8, 7, 0)

    def add_edit9(self):
        self.edit9_label = QtWidgets.QLabel()
        self.edit9_label.setFont(QtGui.QFont("Times", 13))
        self.edit9_label.setText("Population = ")
        self.layout.addWidget(self.edit9_label, 10, 0)
        self.edit9 = QtWidgets.QLineEdit()
        self.edit9.returnPressed.connect(self.edit9_meth)
        self.layout.addWidget(self.edit9, 11, 0)
    def add_edit10(self):
        self.edit10_label = QtWidgets.QLabel()
        self.edit10_label.setFont(QtGui.QFont("Times", 13))
        self.edit10_label.setText("Number of processes = ")
        self.layout.addWidget(self.edit10_label, 10, 1)
        self.edit10 = QtWidgets.QLineEdit()
        self.edit10.returnPressed.connect(self.edit10_meth)
        self.layout.addWidget(self.edit10, 11, 1)

    def add_edit11(self):
        self.edit11_label = QtWidgets.QLabel()
        self.edit11_label.setFont(QtGui.QFont("Times", 13))
        self.edit11_label.setText("Max number of iterations = " + str(global_maxit[0]))
        self.edit11 = QtWidgets.QLineEdit()
        self.edit11.returnPressed.connect(self.edit11_meth)
        self.layout.addWidget(self.edit11_label, 8, 0)
        self.layout.addWidget(self.edit11, 9, 0)
    def edit1_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit1.text()) > 0:
                try:
                    argg = float(self.edit1.text())
                    if argg < 0: argg = 0.0
                    if argg > 1: argg = 1.0
                    global_arg[0] = argg
                except ValueError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Must be number from 0 to 1")
                    x = msg.exec_()

    def edit2_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit2.text()) > 0:
                try:
                    argg = float(self.edit2.text())
                    if argg < 0: argg = 0.0
                    if argg > 1: argg = 1.0
                    global_arg[1] = argg
                except ValueError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Must be number from 0 to 1")
                    x = msg.exec_()

    def edit3_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit3.text()) > 0:
                try:
                    argg = float(self.edit3.text())
                    if argg < 0: argg = 0.0
                    if argg > 1: argg = 1.0
                    global_arg[2] = argg
                except ValueError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Must be number from 0 to 1")
                    x = msg.exec_()

    def edit4_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit4.text()) > 0:
                try:
                    argg = float(self.edit4.text())
                    if argg < 0: argg = 0.0
                    if argg > 1: argg = 1.0
                    global_arg[3] = float(argg)
                except ValueError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Must be number from 0 to 1")
                    x = msg.exec_()

    def edit5_meth(self):
        if not global_rdy_flag[0]:
            if self.edit5.currentText() == "True":
                global_arg[4] = True
            else:
                global_arg[4] = False

    def edit6_meth(self):
        if not global_rdy_flag[0]:
            global_arg[5] = self.edit6.currentText()

    def edit7_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit7.text()) > 0:
                try:
                    argg = float(self.edit7.text())
                    if argg < 0: argg = 0.0
                    global_arg[6] = float(argg)
                except ValueError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Must be number")
                    x = msg.exec_()

    def edit8_meth(self):
        if len(self.edit8.text()) > 0:
            try:
                arg_lst = []
                argg = self.edit8.text().split(" ")
                print(argg)
                for i in range(len(argg)):
                    arg_lst.append(int(argg[i]))
                global_arg[7] = arg_lst
            except:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Must be list of integers greater than 0 and separated by space")
                x = msg.exec_()

    def edit9_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit9.text()) > 0:
                try:
                    argg = int(self.edit9.text())
                    if argg < 1: argg = 1
                    if argg > 1000: argg = 1000
                    global_population[0] = argg
                except ValueError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Must be integer greater than 0")
                    x = msg.exec_()

    def edit10_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit10.text()) > 0:
                try:
                    argg = int(self.edit10.text())
                    if argg < 1: argg = 1
                    if argg > 200: argg = 200
                    global_no_threads[0] = argg
                except ValueError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Must be integer greater than 0")
                    x = msg.exec_()

    def edit11_meth(self):
        if not global_rdy_flag[0]:
            if len(self.edit11.text()) > 0:
                try:
                    argg = int(self.edit11.text())
                    if argg < 1: argg = 1
                    if argg > 1000: argg = 1000
                    global_maxit[0] = argg
                except ValueError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Must be integer greater than 0")
                    x = msg.exec_()
    def set_main_widget(self):
        pass


def start():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

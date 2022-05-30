from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, \
                            QLineEdit, QSizePolicy, QVBoxLayout, \
                            QListWidget
from PyQt5.QtGui import QFont, QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt

from helper import cb_functions
from function import RF
from SODE import SODE
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolBar
from matplotlib.figure import Figure
import numpy as np
#import random
import os

class SODEW(QWidget):
	def __init__(self):
		try:
			super(QWidget, self).__init__()
			self.setWindowTitle('SODE window')
			self.setFixedSize(1300,650)
			self.font = QFont()
			self.font.setPixelSize(15)
			self.font1 = QFont()
			self.font1.setPixelSize(20)
			self.font2 = QFont()
			self.font2.setPixelSize(10)

			# SECTION 1
			self.label10 = QLabel(self)
			self.label10.setText('ODE:')
			self.label10.setFont(self.font1)
			self.label10.move(300,30)

			self.label11 = QLabel(self)
			self.label11.setFont(self.font1)
			self.label11.move(50,70)

			self.label12 = QLabel(self)
			self.label12.setFont(self.font1)
			self.label12.move(50,100)

			self.label13 = QLabel(self)
			self.label13.setFont(self.font1)
			self.label13.move(50,130)

			self.solve_btn = QPushButton(self)
			self.solve_btn.setText('SOLVE')
			self.solve_btn.move(500,130)
			self.solve_btn.clicked.connect(self.solveODE)

			# SECTION 2
			self.label20 = QLabel(self)
			self.label20.setText('construct ODE')
			self.label20.setFont(self.font1)
			self.label20.move(50,210)

			self.label21 = QLabel(self)
			self.label21.setText('y\'\' + a(x)*y\' + b(x)*y = c(x)')
			self.label21.setFont(self.font)
			self.label21.move(50,250)

			self.label22 = QLabel(self)
			self.label22.setText('y(0) = y0')
			self.label22.setFont(self.font)
			self.label22.move(50,275)

			self.label23 = QLabel(self)
			self.label23.setText('y(1) = y1')
			self.label23.setFont(self.font)
			self.label23.move(50,300)

			self.ca_lbl = QLabel(self)
			self.ca_lbl.setText('a(x) = ')
			self.ca_lbl.setFont(self.font)
			self.ca_lbl.move(50,350)

			self.ca_cb = QComboBox(self)
			for sf in cb_functions:
				self.ca_cb.addItem(sf)
			self.ca_cb.move(100,350)
			self.ca_cb.activated[str].connect(self.ca_cb_edit)

			self.ca_le = QLineEdit(self)
			self.ca_le.resize(30,20)
			self.ca_le.move(170,350)
			self.ca_le.setText('1')
			self.ca_le.hide()
			self.ca_le.textChanged[str].connect(self.ca_le_edit)

			self.ca_err_le = QLabel(self)
			self.ca_err_le.setFont(self.font2)
			self.ca_err_le.setStyleSheet('color: red')
			self.ca_err_le.move(205,352)

			self.cb_lbl = QLabel(self)
			self.cb_lbl.setText('b(x) = ')
			self.cb_lbl.setFont(self.font)
			self.cb_lbl.move(50,375)

			self.cb_cb = QComboBox(self)
			for sf in cb_functions:
				self.cb_cb.addItem(sf)
			self.cb_cb.move(100,375)
			self.cb_cb.activated[str].connect(self.cb_cb_edit)

			self.cb_le = QLineEdit(self)
			self.cb_le.resize(30,20)
			self.cb_le.move(170,375)
			self.cb_le.setText('1')
			self.cb_le.hide()
			self.cb_le.textChanged[str].connect(self.cb_le_edit)

			self.cb_err_le = QLabel(self)
			self.cb_err_le.setFont(self.font2)
			self.cb_err_le.setStyleSheet('color: red')
			self.cb_err_le.move(205,377)

			self.cc_lbl = QLabel(self)
			self.cc_lbl.setText('c(x) = ')
			self.cc_lbl.setFont(self.font)
			self.cc_lbl.move(50,400)

			self.cc_cb = QComboBox(self)
			for sf in cb_functions:
				self.cc_cb.addItem(sf)
			self.cc_cb.move(100,400)
			self.cc_cb.activated[str].connect(self.cc_cb_edit)

			self.cc_le = QLineEdit(self)
			self.cc_le.resize(30,20)
			self.cc_le.move(170,400)
			self.cc_le.setText('1')
			self.cc_le.hide()
			self.cc_le.textChanged[str].connect(self.cc_le_edit)

			self.cc_err_le = QLabel(self)
			self.cc_err_le.setFont(self.font2)
			self.cc_err_le.setStyleSheet('color: red')
			self.cc_err_le.move(205,402)

			self.bc_lbl1 = QLabel(self)
			self.bc_lbl1.setText('y0   = ')
			self.bc_lbl1.setFont(self.font)
			self.bc_lbl1.move(50,425)

			self.bc_le1 = QLineEdit(self)
			self.bc_le1.resize(58,20)
			self.bc_le1.move(100,425)
			self.bc_le1.setText('0')
			self.bc_le1.textChanged[str].connect(self.bc_le1_edit)

			self.bc_errlbl1 = QLabel(self)
			self.bc_errlbl1.setFont(self.font2)
			self.bc_errlbl1.setStyleSheet('color: red')
			self.bc_errlbl1.move(170,427)
			
			self.bc_lbl2 = QLabel(self)
			self.bc_lbl2.setText('y1   = ')
			self.bc_lbl2.setFont(self.font)
			self.bc_lbl2.move(50,450)

			self.bc_le2 = QLineEdit(self)
			self.bc_le2.resize(58,20)
			self.bc_le2.move(100,450)
			self.bc_le2.setText('1')
			self.bc_le2.textChanged[str].connect(self.bc_le2_edit)

			self.bc_errlbl2 = QLabel(self)
			self.bc_errlbl2.setFont(self.font2)
			self.bc_errlbl2.setStyleSheet('color: red')
			self.bc_errlbl2.move(170,452)

			self.set_btn = QPushButton(self)
			self.set_btn.setText('SET')
			self.set_btn.move(75,480)
			self.set_btn.clicked.connect(self.setCurrentODE)

			# SECTION 3
			self.gale_lbl = QLabel(self)
			self.gale_lbl.setText('Galerkin method')
			self.gale_lbl.setFont(self.font1)
			self.gale_lbl.move(400,210)

			self.ser_lbl = QLabel(self)
			self.ser_pic = QPixmap('miscellaneous/formula1.gif')
			self.ser_lbl.setPixmap(self.ser_pic)
			self.ser_lbl.adjustSize()
			self.ser_lbl.move(375,250)

			self.label31 = QLabel(self)
			self.label31.setText('Number of terms of expansion (n < 101):')
			self.label31.setFont(self.font)
			self.label31.move(360,375)

			self.n_lbl = QLabel(self)
			self.n_lbl.setText('n = ')
			self.n_lbl.setFont(self.font)
			self.n_lbl.move(360,400)

			self.n_le = QLineEdit(self)
			self.n_le.resize(30,20)
			self.n_le.move(390,400)
			self.n_le.setText('3')
			self.n_le.textChanged[str].connect(self.n_le_edit)

			self.n_err_lbl = QLabel(self)
			self.n_err_lbl.setFont(self.font2)
			self.n_err_lbl.setStyleSheet('color: red')
			self.n_err_lbl.move(430,402)

			# SECTION 4
			self.his_lbl = QLabel(self)
			self.his_lbl.setFont(self.font1)
			self.his_lbl.setText('History')
			self.his_lbl.move(50,535)

			self.save_btn = QPushButton(self)
			self.save_btn.setText('Save')
			self.save_btn.move(50,575)
			self.save_btn.setEnabled(False)
			self.save_btn.clicked.connect(self.save_btn_event)

			self.load_btn = QPushButton(self)
			self.load_btn.setText('Load')
			self.load_btn.move(150,575)
			self.load_btn.clicked.connect(self.load_btn_event)

			self.del_btn = QPushButton(self)
			self.del_btn.setText('Delete')
			self.del_btn.move(250,575)
			self.del_btn.clicked.connect(self.del_btn_event)

			# SECTION PLOT
			self.sc = MplCanvas(self, width=6.3, height=5)
			self.toolbar = NavigationToolBar(self.sc, self)
			layout = QVBoxLayout()
			layout.addWidget(self.sc)
			layout.addWidget(self.toolbar)
			self.plot = QWidget(self)
			self.plot.setLayout(layout)
			self.plot.move(652,0)

			self.res_norm = QLabel(self)
			self.res_norm.setFont(self.font1)
			self.res_norm.move(675, 600)

			# SECTION VARIABLES
			self.a = self.getFunction(cb_functions[0])
			self.b = self.getFunction(cb_functions[0])
			self.c = self.getFunction(cb_functions[0])
			self.a_str = cb_functions[0]
			self.b_str = cb_functions[0]
			self.c_str = cb_functions[0]
			self.y0_str = '0'
			self.y1_str = '1'
			self.y0 = 0.0
			self.y1 = 1.0
			self.n_str = '3'
			self.n = 3
			self.a_param_str = '1'
			self.a_param = 1
			self.b_param_str = '1'
			self.b_param = 1
			self.c_param_str = '1'
			self.c_param = 1
			self.filename = None
			self.x = None
			self.y = None
			self.r_norm = None

			self.setCurrentODE()

		except Exception as e:
			print(e)
			pass

	def save_btn_event(self):
		try:
			self.savew = QWidget()
			self.savew.setWindowModality(2)
			self.savew.setWindowTitle('Save figure')
			self.savew.setFixedSize(300,100)

			self.savew_lbl = QLabel(self.savew)
			self.savew_lbl.setText('name:')
			self.savew_lbl.setFont(self.font)
			self.savew_lbl.move(30,30)

			self.savew_le = QLineEdit(self.savew)
			self.savew_le.resize(100,20)
			self.savew_le.move(80,30)
			self.savew_le.textChanged[str].connect(self.filename_ev)

			self.savew_btn = QPushButton(self.savew)
			self.savew_btn.setText('Save')
			self.savew_btn.move(190,28)
			self.savew_btn.clicked.connect(self.save_event)

			self.savew_lbl1 = QLabel(self.savew)
			self.savew_lbl1.setText('Saved!')
			self.savew_lbl1.setFont(self.font)
			self.savew_lbl1.setStyleSheet('color: green')
			self.savew_lbl1.move(130,60)
			self.savew_lbl1.hide()

			self.savew.show()
		except Exception as e:
			print(e)
			pass

	def load_btn_event(self):
		try:
			self.loadw = QWidget()
			self.loadw.setWindowModality(2)
			self.loadw.setWindowTitle('Load figure')
			self.loadw.setFixedSize(300,400)

			self.loadw_list = QListWidget(self.loadw)
			self.loadw_list.resize(300,300)
			files = os.listdir('saves')
			self.loadw_list.addItems(list(map(lambda x: x[:-4], files)))
			self.loadw_list.itemClicked.connect(self.filename_ev2)

			self.loadw_btn = QPushButton(self.loadw)
			self.loadw_btn.setText('Load')
			self.loadw_btn.move(200,330)
			self.loadw_btn.clicked.connect(self.load_event)
			self.loadw_btn.setEnabled(False)

			self.loadw_lbl1 = QLabel(self.loadw)
			self.loadw_lbl1.setText('Loaded!')
			self.loadw_lbl1.setFont(self.font)
			self.loadw_lbl1.setStyleSheet('color: green')
			self.loadw_lbl1.move(70,330)
			self.loadw_lbl1.hide()

			self.loadw.show()

		except Exception as e:
			print(e)
			pass

	def del_btn_event(self):
		try:
			self.delw = QWidget()
			self.delw.setWindowModality(2)
			self.delw.setWindowTitle('Delete figure')
			self.delw.setFixedSize(300,400)

			self.delw_list = QListWidget(self.delw)
			self.delw_list.resize(300,300)
			files = os.listdir('saves')
			self.delw_list.addItems(list(map(lambda x: x[:-4], files)))
			self.delw_list.itemClicked.connect(self.filename_ev3)

			self.delw_btn = QPushButton(self.delw)
			self.delw_btn.setText('Delete')
			self.delw_btn.move(200,330)
			self.delw_btn.clicked.connect(self.del_event)
			self.delw_btn.setEnabled(False)

			self.delw_lbl1 = QLabel(self.delw)
			self.delw_lbl1.setText('Deleted!')
			self.delw_lbl1.setFont(self.font)
			self.delw_lbl1.setStyleSheet('color: green')
			self.delw_lbl1.move(70,330)
			self.delw_lbl1.hide()

			self.delw.show()

		except Exception as e:
			print(e)
			pass



	def filename_ev(self, text):
		self.savew_lbl1.hide()
		self.filename = 'saves/{0}.txt'.format(text)

	def filename_ev2(self, item):
		self.loadw_btn.setEnabled(True)
		self.loadw_lbl1.hide()
		self.filename = 'saves/{0}.txt'.format(item.text())

	def filename_ev3(self, item):
		self.delw_btn.setEnabled(True)
		self.delw_lbl1.hide()
		self.filename = 'saves/{0}.txt'.format(item.text())

	def save_event(self):
		with open(self.filename, 'w') as f:
			f.write(self.a_str + '\n')
			f.write(self.a_param_str + '\n')
			f.write(self.b_str + '\n')
			f.write(self.b_param_str + '\n')
			f.write(self.c_str + '\n')
			f.write(self.c_param_str + '\n')
			f.write(self.y0_str + '\n')
			f.write(self.y1_str + '\n')
			f.write(self.n_str + '\n')
			f.write(str(self.r_norm) + '\n')

			for i in range(99):
				f.write(str(self.y[i]) + '\n')

		self.sc.axes.set_title(self.filename[6:-4])
		self.sc.draw()
		self.savew_lbl1.show()

	def load_event(self):
		try:
			with open(self.filename, 'r') as f:
				self.a_str = f.readline().strip()
				self.a_param_str = f.readline().strip()
				self.b_str = f.readline().strip()
				self.b_param_str = f.readline().strip()
				self.c_str = f.readline().strip()
				self.c_param_str = f.readline().strip()
				self.y0_str = f.readline().strip()
				self.y1_str = f.readline().strip()
				self.n_str = f.readline().strip()
				self.r_norm = float(f.readline().strip())
				y = []
				for i in range(99):
					y.append(float(f.readline().strip()))
				self.y = y

			self.setFields()
			self.setCurrentODE()
			m = 100
			self.x = np.arange(1/m, 1, 1/m)
			self.sc.axes.cla()
			self.sc.axes.set_title(self.filename[6:-4])
			self.sc.axes.plot(self.x, self.y, label='approx')
			self.sc.axes.legend()
			self.sc.draw()
			self.res_norm.setText('Residue norm = {0}'.format(self.r_norm))
			self.res_norm.adjustSize()
			self.save_btn.setEnabled(True)
			self.loadw_lbl1.show()
		except Exception as e:
			print(e)
			pass

	def del_event(self):
		os.remove(self.filename)
		files = os.listdir('saves')
		self.delw_list.takeItem(self.delw_list.currentRow())
		self.delw_lbl1.show()

	def setFields(self):
		self.ca_cb.setCurrentIndex(cb_functions.index(self.a_str))
		self.ca_le.setText(self.a_param_str)
		self.cb_cb.setCurrentIndex(cb_functions.index(self.b_str))
		self.cb_le.setText(self.b_param_str)
		self.cc_cb.setCurrentIndex(cb_functions.index(self.c_str))
		self.cc_le.setText(self.c_param_str)
		self.bc_le1.setText(self.y0_str)
		self.bc_le2.setText(self.y1_str)
		self.n_le.setText(self.n_str)


	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		pen = QPen(Qt.black, 2, Qt.SolidLine)
		qp.setPen(pen)
		qp.drawLine(650,0,650,650)
		qp.drawLine(0,190,650,190)
		qp.drawLine(0,530,650,530)
		qp.drawLine(330,190,330,530)
		qp.end()

	def ca_cb_edit(self, text):
		self.ca_err_le.setText('')
		if text == '0' or text == '1' or text == 'x':
			self.ca_le.hide()
		else:
			self.ca_le.show()
		self.a_str = text

	def cb_cb_edit(self, text):
		self.cb_err_le.setText('')
		if text == '0' or text == '1' or text == 'x':
			self.cb_le.hide()
		else:
			self.cb_le.show()
		self.b_str = text

	def cc_cb_edit(self, text):
		self.cc_err_le.setText('')
		if text == '0' or text == '1' or text == 'x':
			self.cc_le.hide()
		else:
			self.cc_le.show()
		self.c_str = text

	def ca_le_edit(self, text):
		self.ca_err_le.setText('')
		self.a_param_str = text.strip()

	def cb_le_edit(self, text):
		self.cb_err_le.setText('')
		self.b_param_str = text.strip()

	def cc_le_edit(self, text):
		self.cc_err_le.setText('')
		self.c_param_str = text.strip()

	def bc_le1_edit(self, text):
		self.bc_errlbl1.setText('')
		self.y0_str = text.strip()

	def bc_le2_edit(self, text):
		self.bc_errlbl2.setText('')
		self.y1_str = text.strip()

	def n_le_edit(self, text):
		self.n_err_lbl.setText('')
		self.n_str = text.strip()

	def setCurrentODE(self):
		b0, err0 = self.checkBC(self.y0_str)
		b1, err1 = self.checkBC(self.y1_str)
		b2, err2 = self.checkCS(self.a_str, self.a_param_str)
		b3, err3 = self.checkCS(self.b_str, self.b_param_str)
		b4, err4 = self.checkCS(self.c_str, self.c_param_str)
		if not b0:
			self.bc_errlbl1.setText(err0)
			self.bc_errlbl1.adjustSize()
		if not b1:
			self.bc_errlbl2.setText(err1)
			self.bc_errlbl2.adjustSize()
		if not b2:
			self.ca_err_le.setText(err2)
			self.ca_err_le.adjustSize()
		if not b3:
			self.cb_err_le.setText(err3)
			self.cb_err_le.adjustSize()
		if not b4:
			self.cc_err_le.setText(err4)
			self.cc_err_le.adjustSize()
		if not (b0 and b1 and b2 and b3 and b4):
			return
		self.a_param = float(self.a_param_str)
		self.b_param = float(self.b_param_str)
		self.c_param = float(self.c_param_str)
		self.a = self.getFunction(self.a_str, self.a_param)
		self.b = self.getFunction(self.b_str, self.b_param)
		self.c = self.getFunction(self.c_str, self.b_param)
		self.y0 = float(self.y0_str)
		self.y1 = float(self.y1_str)

		a_full = self.getFunctionText(self.a_str, self.a_param)
		b_full = self.getFunctionText(self.b_str, self.b_param)
		c_full = self.getFunctionText(self.c_str, self.c_param)
		ode = 'y\'\' + {0} * y\' + {1} * y = {2}'.format(a_full, \
			                                         b_full, \
			                                         c_full)
		bc0 = 'y(0) = {0}'.format(str(self.y0))
		bc1 = 'y(1) = {0}'.format(str(self.y1))
		self.label11.setText(ode)
		self.label12.setText(bc0)
		self.label13.setText(bc1)
		self.label11.adjustSize()
		self.label12.adjustSize()
		self.label13.adjustSize()

	def checkBC(self, text):
		err1 = 'entered value is not a number!'
		err2 = 'entered string is too long! (>30)'
		if not self.isNotTooLong(text, 30):
			return False, err2
		if not self.parseNumber(text):
			return False, err1
		return True, 'OK'

	def checkCS(self, fun, param):
		err1 = 'should be a number!'
		err2 = 'string is too long! (>10)'
		err3 = 'should be positive integer!'
		if not self.isNotTooLong(param, 10):
			return False, err2
		if not self.parseNumber(param):
			return False, err1
		#if fun == 'pow':
		#	if not param.isdigit() or float(param) <= 0:
		#		return False, err3
		return True, 'OK'

	def isNotTooLong(self, string, l):
		return len(string) <= l

	def parseNumber(self, string):
		if string.isdigit():
			return True
		else:
			try:
				float(string)
				return True
			except ValueError:
				return False

	def solveODE(self):
		if not (self.n_str.isdigit() and self.n_str != '0'):
			self.n_err_lbl.setText('entered value is not a positive integer!')
			self.n_err_lbl.adjustSize()
			return
		if int(self.n_str) > 100:
			self.n_err_lbl.setText('entered value is too large!')
			self.n_err_lbl.adjustSize()
			return
		self.n = int(self.n_str)
		ode = SODE((self.a, self.b, self.c), (self.y0, self.y1))
		f, self.r_norm, R = ode.solve(self.n)
		m = 100
		self.x = np.arange(1/m, 1, 1/m)
		self.y = list(map(f, self.x))

		self.res_norm.setText('Residue norm = {0}'.format(self.r_norm))
		self.res_norm.adjustSize()
		self.sc.axes.cla()
		self.sc.axes.plot(self.x, self.y, label='approx')
		if self.r_norm == None:
			self.sc.axes.plot(x, list(map(R, self.x)), label='residue')
		self.sc.axes.legend()
		self.sc.draw()

		self.save_btn.setEnabled(True)

		#plt.plot(x,y)
		#plt.show()

	def getFunction(self, string, param=None):
		if string == 'sin(x)':
			return RF.sin() @ (param * RF.id())
		if string == 'cos(x)':
			return RF.cos() @ (param * RF.id())
		if string == 'exp(x)':
			return RF.exp() @ (param * RF.id())
		if string == '0':
			return RF.const(0)
		if string == '1':
			return RF.const(1)
		if string == 'x':
			return RF.id()
		if string == 'const':
			return RF.const(param)
		if string == 'gamma(x)':
			return RF.gamma()
		if string == 'pow':
			return RF.pow(param)

	def getFunctionText(self, fun, param):
		if fun == 'sin(x)':
			return 'sin({0}x)'.format(param)
		if fun == 'cos(x)':
			return 'cos({0}x)'.format(param)
		if fun == 'exp(x)':
			return 'exp({0}x)'.format(param)
		if fun == '0':
			return '0'
		if fun == '1':
			return '1'
		if fun == 'x':
			return 'x'
		if fun == 'const':
			return str(param)
		if fun == 'gamma(x)':
			return 'gamma(x)'
		if fun == 'pow':
			return 'x^({0})'.format(param)

	def closew(self):
		self.close()
		self.destroy()

class MplCanvas(FigureCanvasQTAgg):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		FigureCanvasQTAgg.__init__(self, fig)
		self.setParent(parent)

		FigureCanvasQTAgg.setSizePolicy(self,
			QSizePolicy.Expanding,
			QSizePolicy.Expanding)
		FigureCanvasQTAgg.updateGeometry(self)

	def plot(self):
		data = ([0,1],[0,1])
		ax = self.figure.add_subplot(111)
		ax.plot(data[0], data[1])
		ax.set_title('test')
		self.draw()


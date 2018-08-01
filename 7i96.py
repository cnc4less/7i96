#!/usr/bin/python3
# -*- coding: utf-8 -*-

version = 0.8

import sys, os, configparser
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QLineEdit,
	QSpinBox, QCheckBox)
import setup, loadini

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		uic.loadUi("7i96.ui", self)
		self.config = configparser.ConfigParser(strict=False)
		self.linuxcncDir = os.path.expanduser('~/linuxcnc')
		self.configsDir = os.path.expanduser('~/linuxcnc/configs')

		self.buildWidgets()
		self.setupConnections()
		self.show()

	# Auto connected menu action callbacks
	@pyqtSlot()
	def on_actionFileNew_triggered(self):
		print('File New')

	@pyqtSlot()
	def on_actionOpen_triggered(self):
		if not os.path.isdir(self.configsDir):
			self.configsDir = os.path.expanduser('~/')
		fileName = QFileDialog.getOpenFileName(self,
		caption="Select Configuration INI File", directory=self.configsDir,
		filter='*.ini', options=QFileDialog.DontUseNativeDialog,)
		if fileName:
			iniFile = (fileName[0])
			if self.config.read(iniFile):
				self.iniLoad()

	@pyqtSlot()
	def on_actionSave_triggered(self):
		pass

	@pyqtSlot()
	def on_actionAbout_triggered(self):
		pass

	@pyqtSlot()
	def on_actionCheck_triggered(self):
		pass

	@pyqtSlot()
	def on_actionBuild_triggered(self):
		pass

	@pyqtSlot()
	def on_actionSaveAs_triggered(self):
		 print('File Save As')

	@pyqtSlot()
	def on_actionExit_triggered(self):
		exit()

	def setupConnections(self):
		self.configName.textChanged[str].connect(self.onConfigNameChanged)

	def onConfigNameChanged(self, text):
		# update the iniDictionary when text is changed
		if text:
			self.configName = text.replace(' ','_')
			self.configPath = self.configsDir + '/' + self.configName
			self.pathLabel.setText(self.configPath)
		else:
			self.pathLabel.setText('')

	def buildWidgets(self):
		for item in setup.setupCombo('ipCombo'):
			self.ipCombo.addItem(item[0], item[1])
		#print(setup.setupCombo('ipCombo'))
		for i in range(5):
			for item in setup.setupCombo('axis'):
				getattr(self, 'axis_' + str(i)).addItem(item[0], item[1])
		for i in range(5):
			for item in setup.setupCombo('direction'):
				getattr(self, 'stepDir_' + str(i)).addItem(item[0], item[1])
		for i in range(11):
			for item in setup.setupCombo('input'):
				getattr(self, 'input_' + str(i)).addItem(item[0], item[1])
		for i in range(5):
			for item in setup.setupCombo('output'):
				getattr(self, 'output_' + str(i)).addItem(item[0], item[1])
		for i in range(11):
			for item in setup.setupCombo('axis'):
				getattr(self, 'inputaxis_' + str(i)).addItem(item[0], item[1])

	def iniLoad(self):
		# iniList section, item, value
		for item in loadini.iniList():
			if self.config.has_option(item[0], item[1]):
				#print(item[0], item[1])
				if isinstance(getattr(self, item[2]), QLineEdit):
					getattr(self, item[2]).setText(self.config[item[0]][item[1]])
				if isinstance(getattr(self, item[2]), QSpinBox):
					getattr(self, item[2]).setValue(int(self.config[item[0]][item[1]]))
				if isinstance(getattr(self, item[2]), QCheckBox):
					#print(self.config[item[0]][item[1]])
					if self.config[item[0]][item[1]] in ['YES', 'yes']:
						getattr(self, item[2]).setChecked(True)
					else:
						getattr(self, item[2]).setChecked(False)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())

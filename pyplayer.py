#!/usr/bin/env python
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.phonon import Phonon

class MainWindow(QtGui.QMainWindow):
	
	def __init__(self, win_parent=None):
		QtGui.QMainWindow.__init__(self, win_parent)
		self.create_widgets()
		
	def create_widgets(self):
		# Widgets
		self.label = QtGui.QLabel("ply music player")
		self.fs_button = QtGui.QPushButton("FileSystem", self)
		self.ws_button = QtGui.QPushButton("WebStream", self)
		
		# Phonon actions
		self.mediaObject = Phonon.MediaObject(self)
		self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
		self.path = Phonon.createPath(self.mediaObject, self.audioOutput)
		self.effect = Phonon.Effect(Phonon.BackendCapabilities.availableAudioEffects()[0], self)
		self.path.insertEffect(self.effect)
		
		# Connect signal
		self.fs_button.clicked.connect(self.on_fs_clicked)
		self.mediaObject.stateChanged.connect(self.handleStateChanged)		
		self.ws_button.clicked.connect(self.on_ws_clicked)
		
		# Vertical layout (manages the layout automatically)
		v_box = QtGui.QVBoxLayout()
		v_box.addWidget(self.fs_button)
		v_box.addWidget(self.ws_button)
		
		# Create central widget, add layout and set
		central_widget = QtGui.QWidget()
		central_widget.setLayout(v_box)
		self.setCentralWidget(central_widget)
		
	def on_fs_clicked(self):
		if self.mediaObject.state() == Phonon.PlayingState:
			self.mediaObject.stop()
		else:
			files = QtGui.QFileDialog.getOpenFileNames(self, self.fs_button.text())
			if files:
				songs = []
				for file in files:
					songs.append(Phonon.MediaSource(file))
				self.mediaObject.setQueue(songs)
				self.mediaObject.play()
				self.fs_button.setText("FileSystem")
				
	def handleStateChanged(self, newstate, oldstate):
		if newstate == Phonon.PlayingState:
			pass
		elif newstate == Phonon.StoppedState:
			pass
		elif newstate == Phonon.ErrorState:
			source = self.mediaObject.currentSource().fileName()
			print "ERROR: ", self.mediaObject.errorType()
			print "ERROR: could not play:", source.toLocal8Bit().data()
		
		
	def on_ws_clicked(self):
		if self.mediaObject.state() == Phonon.PlayingState:
			self.mediaObject.stop()
		else:
			songs = []
			path = "http://dr5huvbk6x9di.cloudfront.net/cloudfront_songs/"
			for i in range(1,31):
				song = "file%d.ogg" % i
				songs.append(Phonon.MediaSource(path + song))
			self.mediaObject.enqueue(songs)
			self.mediaObject.play()
			self.path.insertEffect(self.effect)
	
if __name__ == "__main__":
	ply = QtGui.QApplication(sys.argv)
	ply.setApplicationName("Ply")
	ply.setQuitOnLastWindowClosed(True)
	main_window = MainWindow()
	main_window.show()
	sys.exit(ply.exec_())
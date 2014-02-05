#!/usr/bin/env python
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.phonon import Phonon

class MainWindow(QtGui.QMainWindow):

    def __init__(self, win_parent=None):
        QtGui.QMainWindow.__init__(self, win_parent)
        
        # Phonon actions
        self.media_object = Phonon.MediaObject(self)
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.path = Phonon.createPath(self.media_object, self.audio_output)
        
        self.media_object.stateChanged.connect(self.handleStateChanged)
		
		
        
        self.setup_actions()
        self.setup_user_interface()
		
		# Connect signal
        self.fs_button.clicked.connect(self.on_fs_clicked)
        self.ws_button.clicked.connect(self.on_ws_clicked)
    
    def setup_user_interface(self):
        
        bar = QtGui.QToolBar()
        bar.addAction(self.play_action)
        bar.addAction(self.pause_action)
        bar.addAction(self.stop_action)
    
        # Widgets
        self.label = QtGui.QLabel("pyplayer")
        self.fs_button = QtGui.QPushButton("FileSystem", self)
        self.ws_button = QtGui.QPushButton("WebStream", self)
            
        playback_layout = QtGui.QHBoxLayout()
        playback_layout.addWidget(bar)
        playback_layout.addStretch()
        
        # Vertical layout (manages the layout automatically)
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.fs_button)
        main_layout.addWidget(self.ws_button)
        main_layout.addLayout(playback_layout)
        
        # Create central widget, add layout and set
        central_widget = QtGui.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("PyPlayer")
        
        
        
    def setup_actions(self):
        self.play_action = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "Play",
            self, shortcut="Ctrl+P", enabled=False,
            triggered=self.media_object.play)
        
        self.stop_action = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_MediaStop), "Stop",
            self, shortcut="Ctrl+S", enabled=False,
            triggered=self.media_object.stop)
            
        self.pause_action = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_MediaPause), "Pause",
            self, shortcut="Ctrl+A", enabled=False,
            triggered=self.media_object.pause)
        
    def on_fs_clicked(self):
        
        if self.media_object.state() == Phonon.PlayingState:
            self.media_object.stop()
        
        files = QtGui.QFileDialog.getOpenFileNames(self, self.fs_button.text())
        if files:
            songs = []
            for file in files:
                songs.append(Phonon.MediaSource(file))
            self.media_object.setCurrentSource(songs[0])
            self.media_object.setQueue(songs[1:])
            self.media_object.play()
            self.fs_button.setText("FileSystem")
                
    def handleStateChanged(self, new_state, old_state):
        if new_state == Phonon.PlayingState:
            self.play_action.setEnabled(False)
            self.pause_action.setEnabled(True)
            self.stop_action.setEnabled(True)
        elif new_state == Phonon.StoppedState:
            self.play_action.setEnabled(True)
            self.pause_action.setEnabled(False)
            self.stop_action.setEnabled(False)
        elif new_state == Phonon.PausedState:
            self.play_action.setEnabled(True)
            self.pause_action.setEnabled(False)
            self.stop_action.setEnabled(True)
            
        elif new_state == Phonon.ErrorState:
            source = self.media_object.currentSource().fileName()
            if self.media_object.errorType() == Phonon.FatalError:
                QtGui.QMessageBox.warning(self, "Fatal Error",
                        self.media_object.errorString())
            else:
                QtGui.QMessageBox.warning(self, "Error",
                        self.media_object.errorString())
            print "ERROR: could not play:", source.toLocal8Bit().data()
        
        
    def on_ws_clicked(self):
        if self.media_object.state() == Phonon.PlayingState:
            self.media_object.stop()
        
        songs = []
        path = "http://dr5huvbk6x9di.cloudfront.net/cloudfront_songs/"
        for i in range(1,31):
            song = "file%d.ogg" % i
            songs.append(Phonon.MediaSource(path + song))
        self.media_object.setCurrentSource(songs[0])
        self.media_object.setQueue(songs[1:])
        self.media_object.play()
    
if __name__ == "__main__":
    ply = QtGui.QApplication(sys.argv)
    ply.setApplicationName("Ply")
    ply.setQuitOnLastWindowClosed(True)
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(ply.exec_())
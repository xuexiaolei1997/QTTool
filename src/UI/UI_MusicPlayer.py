# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Desktop\QTTool\src\UI\MusicPlayer.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MusicPlayer(object):
    def setupUi(self, MusicPlayer):
        MusicPlayer.setObjectName("MusicPlayer")
        MusicPlayer.resize(616, 476)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(MusicPlayer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_ChangeDir = QtWidgets.QPushButton(MusicPlayer)
        self.pushButton_ChangeDir.setObjectName("pushButton_ChangeDir")
        self.horizontalLayout.addWidget(self.pushButton_ChangeDir)
        self.line = QtWidgets.QFrame(MusicPlayer)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lineEdit_SearchMusic = QtWidgets.QLineEdit(MusicPlayer)
        self.lineEdit_SearchMusic.setObjectName("lineEdit_SearchMusic")
        self.horizontalLayout.addWidget(self.lineEdit_SearchMusic)
        self.checkBox_DarkTheme = QtWidgets.QCheckBox(MusicPlayer)
        self.checkBox_DarkTheme.setObjectName("checkBox_DarkTheme")
        self.horizontalLayout.addWidget(self.checkBox_DarkTheme)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_Music = QtWidgets.QTableView(MusicPlayer)
        self.tableView_Music.setObjectName("tableView_Music")
        self.verticalLayout.addWidget(self.tableView_Music)
        self.widget_MediaPlayer = QtWidgets.QWidget(MusicPlayer)
        self.widget_MediaPlayer.setObjectName("widget_MediaPlayer")
        self.verticalLayout.addWidget(self.widget_MediaPlayer)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(MusicPlayer)
        QtCore.QMetaObject.connectSlotsByName(MusicPlayer)

    def retranslateUi(self, MusicPlayer):
        _translate = QtCore.QCoreApplication.translate
        MusicPlayer.setWindowTitle(_translate("MusicPlayer", "MusicPlayer"))
        self.pushButton_ChangeDir.setText(_translate("MusicPlayer", "ChangeDir"))
        self.lineEdit_SearchMusic.setPlaceholderText(_translate("MusicPlayer", "Search"))
        self.checkBox_DarkTheme.setText(_translate("MusicPlayer", "DarkTheme"))

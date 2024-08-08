# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Desktop\QTTool\src\UI\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1584, 964)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/排版版面.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.MainWidget = QtWidgets.QWidget(MainWindow)
        self.MainWidget.setObjectName("MainWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.MainWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.workspace = QtWidgets.QMdiArea(self.MainWidget)
        self.workspace.setObjectName("workspace")
        self.verticalLayout_4.addWidget(self.workspace)
        MainWindow.setCentralWidget(self.MainWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1584, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuNew = QtWidgets.QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")
        self.menuOpen = QtWidgets.QMenu(self.menuFile)
        self.menuOpen.setObjectName("menuOpen")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuOperation = QtWidgets.QMenu(self.menuView)
        self.menuOperation.setObjectName("menuOperation")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuCustomTool = QtWidgets.QMenu(self.menubar)
        self.menuCustomTool.setObjectName("menuCustomTool")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_Left = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_Left.setMinimumSize(QtCore.QSize(200, 238))
        self.dockWidget_Left.setFloating(False)
        self.dockWidget_Left.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockWidget_Left.setObjectName("dockWidget_Left")
        self.dockWidget_Resource = QtWidgets.QWidget()
        self.dockWidget_Resource.setObjectName("dockWidget_Resource")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidget_Resource)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.dockWidget_Left.setWidget(self.dockWidget_Resource)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_Left)
        self.dockWidget_Bottom = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_Bottom.setMinimumSize(QtCore.QSize(145, 200))
        self.dockWidget_Bottom.setObjectName("dockWidget_Bottom")
        self.dockWidget_Operation = QtWidgets.QWidget()
        self.dockWidget_Operation.setObjectName("dockWidget_Operation")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidget_Operation)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dockWidget_Bottom.setWidget(self.dockWidget_Operation)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_Bottom)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.dockWidget_Draw = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_Draw.setMinimumSize(QtCore.QSize(200, 165))
        self.dockWidget_Draw.setObjectName("dockWidget_Draw")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dockWidget_Draw.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_Draw)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setCheckable(False)
        self.actionAbout.setObjectName("actionAbout")
        self.actionResource = QtWidgets.QAction(MainWindow)
        self.actionResource.setCheckable(True)
        self.actionResource.setChecked(True)
        self.actionResource.setObjectName("actionResource")
        self.actionOpen_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")
        self.actionDraw = QtWidgets.QAction(MainWindow)
        self.actionDraw.setCheckable(True)
        self.actionDraw.setChecked(True)
        self.actionDraw.setObjectName("actionDraw")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionOpenText_File = QtWidgets.QAction(MainWindow)
        self.actionOpenText_File.setObjectName("actionOpenText_File")
        self.actionOpenCsv_Excel_File = QtWidgets.QAction(MainWindow)
        self.actionOpenCsv_Excel_File.setObjectName("actionOpenCsv_Excel_File")
        self.actionNewText_File = QtWidgets.QAction(MainWindow)
        self.actionNewText_File.setObjectName("actionNewText_File")
        self.actionNewCsv_Excel_File = QtWidgets.QAction(MainWindow)
        self.actionNewCsv_Excel_File.setObjectName("actionNewCsv_Excel_File")
        self.actionNew_Terminal = QtWidgets.QAction(MainWindow)
        self.actionNew_Terminal.setObjectName("actionNew_Terminal")
        self.actionMusicPlayer = QtWidgets.QAction(MainWindow)
        self.actionMusicPlayer.setObjectName("actionMusicPlayer")
        self.menuNew.addAction(self.actionNewText_File)
        self.menuNew.addAction(self.actionNewCsv_Excel_File)
        self.menuOpen.addAction(self.actionOpenText_File)
        self.menuOpen.addAction(self.actionOpenCsv_Excel_File)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addAction(self.menuOpen.menuAction())
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addAction(self.actionClose)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionUndo)
        self.menuOperation.addAction(self.actionNew_Terminal)
        self.menuView.addAction(self.actionResource)
        self.menuView.addAction(self.actionDraw)
        self.menuView.addAction(self.menuOperation.menuAction())
        self.menuHelp.addAction(self.actionAbout)
        self.menuCustomTool.addAction(self.actionMusicPlayer)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuCustomTool.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.actionResource.triggered['bool'].connect(self.dockWidget_Left.setVisible) # type: ignore
        self.dockWidget_Left.visibilityChanged['bool'].connect(self.actionResource.setChecked) # type: ignore
        self.actionDraw.toggled['bool'].connect(self.dockWidget_Draw.setVisible) # type: ignore
        self.dockWidget_Draw.visibilityChanged['bool'].connect(self.actionDraw.setChecked) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TOOL-X"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuNew.setTitle(_translate("MainWindow", "New"))
        self.menuOpen.setTitle(_translate("MainWindow", "Open"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuOperation.setTitle(_translate("MainWindow", "Operation"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuCustomTool.setTitle(_translate("MainWindow", "CustomTool"))
        self.dockWidget_Left.setWindowTitle(_translate("MainWindow", "Resource"))
        self.dockWidget_Bottom.setWindowTitle(_translate("MainWindow", "Operation"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidget_Draw.setWindowTitle(_translate("MainWindow", "Draw"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionResource.setText(_translate("MainWindow", "Resource"))
        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder"))
        self.actionOpen_Folder.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionDraw.setText(_translate("MainWindow", "Draw"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionOpenText_File.setText(_translate("MainWindow", "Text File"))
        self.actionOpenCsv_Excel_File.setText(_translate("MainWindow", "Csv/Excel File"))
        self.actionNewText_File.setText(_translate("MainWindow", "Text File"))
        self.actionNewCsv_Excel_File.setText(_translate("MainWindow", "Csv/Excel File"))
        self.actionNew_Terminal.setText(_translate("MainWindow", "New Terminal"))
        self.actionMusicPlayer.setText(_translate("MainWindow", "MusicPlayer"))
import pictures_rc

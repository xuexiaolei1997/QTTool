# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Desktop\QTTool\src\UI\ShowDraw.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DrawPaint(object):
    def setupUi(self, DrawPaint):
        DrawPaint.setObjectName("DrawPaint")
        DrawPaint.resize(925, 562)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icons/照片相片.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DrawPaint.setWindowIcon(icon)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(DrawPaint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_Draw = QtWidgets.QVBoxLayout()
        self.verticalLayout_Draw.setObjectName("verticalLayout_Draw")
        self.verticalLayout_3.addLayout(self.verticalLayout_Draw)

        self.retranslateUi(DrawPaint)
        QtCore.QMetaObject.connectSlotsByName(DrawPaint)

    def retranslateUi(self, DrawPaint):
        _translate = QtCore.QCoreApplication.translate
        DrawPaint.setWindowTitle(_translate("DrawPaint", "ShowDialog"))
import pictures_rc

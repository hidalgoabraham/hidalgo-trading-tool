# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana_historial.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 536)
        MainWindow.setMaximumSize(QtCore.QSize(455, 536))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icono.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mainScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainScrollArea.sizePolicy().hasHeightForWidth())
        self.mainScrollArea.setSizePolicy(sizePolicy)
        self.mainScrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.mainScrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mainScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainScrollArea.setLineWidth(0)
        self.mainScrollArea.setWidgetResizable(True)
        self.mainScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.mainScrollArea.setObjectName("mainScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 437, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setMaximumSize(QtCore.QSize(437, 16777215))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.mainGroupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.mainGroupBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainGroupBox.sizePolicy().hasHeightForWidth())
        self.mainGroupBox.setSizePolicy(sizePolicy)
        self.mainGroupBox.setMinimumSize(QtCore.QSize(437, 500))
        self.mainGroupBox.setMaximumSize(QtCore.QSize(437, 500))
        self.mainGroupBox.setStyleSheet("")
        self.mainGroupBox.setTitle("")
        self.mainGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.mainGroupBox.setFlat(False)
        self.mainGroupBox.setCheckable(False)
        self.mainGroupBox.setObjectName("mainGroupBox")
        self.lstw_historial = QtWidgets.QListWidget(self.mainGroupBox)
        self.lstw_historial.setGeometry(QtCore.QRect(20, 20, 401, 441))
        self.lstw_historial.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.lstw_historial.setMovement(QtWidgets.QListView.Free)
        self.lstw_historial.setObjectName("lstw_historial")
        self.pbtn_guardar_historial = QtWidgets.QPushButton(self.mainGroupBox)
        self.pbtn_guardar_historial.setGeometry(QtCore.QRect(20, 470, 111, 21))
        self.pbtn_guardar_historial.setObjectName("pbtn_guardar_historial")
        self.gridLayout.addWidget(self.mainGroupBox, 0, 0, 1, 1)
        self.mainScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.mainScrollArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hidalgo Trading Tool - Historial"))
        self.pbtn_guardar_historial.setText(_translate("MainWindow", "Guardar historial"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(310, 163)
        MainWindow.setMinimumSize(QtCore.QSize(310, 163))
        MainWindow.setMaximumSize(QtCore.QSize(310, 163))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icono.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.linedit_api_secret = QtWidgets.QLineEdit(self.centralwidget)
        self.linedit_api_secret.setGeometry(QtCore.QRect(90, 80, 191, 20))
        self.linedit_api_secret.setObjectName("linedit_api_secret")
        self.lbl_api_secret = QtWidgets.QLabel(self.centralwidget)
        self.lbl_api_secret.setGeometry(QtCore.QRect(30, 80, 61, 20))
        self.lbl_api_secret.setObjectName("lbl_api_secret")
        self.lbl_api_key = QtWidgets.QLabel(self.centralwidget)
        self.lbl_api_key.setGeometry(QtCore.QRect(30, 50, 47, 20))
        self.lbl_api_key.setObjectName("lbl_api_key")
        self.linedit_api_key = QtWidgets.QLineEdit(self.centralwidget)
        self.linedit_api_key.setGeometry(QtCore.QRect(90, 50, 191, 20))
        self.linedit_api_key.setObjectName("linedit_api_key")
        self.lbl_credenciales_binance = QtWidgets.QLabel(self.centralwidget)
        self.lbl_credenciales_binance.setGeometry(QtCore.QRect(30, 15, 251, 20))
        self.lbl_credenciales_binance.setObjectName("lbl_credenciales_binance")
        self.pbtn_aceptar = QtWidgets.QPushButton(self.centralwidget)
        self.pbtn_aceptar.setGeometry(QtCore.QRect(120, 120, 75, 30))
        self.pbtn_aceptar.setObjectName("pbtn_aceptar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hidalgo Trading Tool"))
        self.lbl_api_secret.setText(_translate("MainWindow", "API secret:"))
        self.lbl_api_key.setText(_translate("MainWindow", "API key:"))
        self.lbl_credenciales_binance.setText(_translate("MainWindow", "Ingrese la información de la cuenta de Binance:"))
        self.pbtn_aceptar.setText(_translate("MainWindow", "Aceptar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


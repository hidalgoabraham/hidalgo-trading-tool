# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(195, 205)
        MainWindow.setMinimumSize(QtCore.QSize(195, 205))
        MainWindow.setMaximumSize(QtCore.QSize(195, 205))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icono.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pbtn_aceptar = QtWidgets.QPushButton(self.centralwidget)
        self.pbtn_aceptar.setGeometry(QtCore.QRect(60, 160, 75, 30))
        self.pbtn_aceptar.setObjectName("pbtn_aceptar")
        self.cbx_vela = QtWidgets.QComboBox(self.centralwidget)
        self.cbx_vela.setGeometry(QtCore.QRect(50, 20, 51, 20))
        self.cbx_vela.setObjectName("cbx_vela")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.cbx_vela.addItem("")
        self.spnbx_nprsi = QtWidgets.QSpinBox(self.centralwidget)
        self.spnbx_nprsi.setGeometry(QtCore.QRect(90, 50, 42, 20))
        self.spnbx_nprsi.setMinimum(2)
        self.spnbx_nprsi.setMaximum(499)
        self.spnbx_nprsi.setProperty("value", 8)
        self.spnbx_nprsi.setObjectName("spnbx_nprsi")
        self.lbl_vela = QtWidgets.QLabel(self.centralwidget)
        self.lbl_vela.setGeometry(QtCore.QRect(20, 20, 31, 20))
        self.lbl_vela.setObjectName("lbl_vela")
        self.lbl_nprsi = QtWidgets.QLabel(self.centralwidget)
        self.lbl_nprsi.setGeometry(QtCore.QRect(20, 50, 71, 20))
        self.lbl_nprsi.setObjectName("lbl_nprsi")
        self.spnbx_npt = QtWidgets.QSpinBox(self.centralwidget)
        self.spnbx_npt.setGeometry(QtCore.QRect(120, 80, 42, 20))
        self.spnbx_npt.setMinimum(2)
        self.spnbx_npt.setMaximum(499)
        self.spnbx_npt.setProperty("value", 30)
        self.spnbx_npt.setObjectName("spnbx_npt")
        self.lbl_npt = QtWidgets.QLabel(self.centralwidget)
        self.lbl_npt.setGeometry(QtCore.QRect(20, 80, 101, 20))
        self.lbl_npt.setObjectName("lbl_npt")
        self.lbl_N_monedas = QtWidgets.QLabel(self.centralwidget)
        self.lbl_N_monedas.setGeometry(QtCore.QRect(20, 110, 111, 20))
        self.lbl_N_monedas.setObjectName("lbl_N_monedas")
        self.spnbx_N_monedas = QtWidgets.QSpinBox(self.centralwidget)
        self.spnbx_N_monedas.setGeometry(QtCore.QRect(130, 110, 51, 20))
        self.spnbx_N_monedas.setMinimum(1)
        self.spnbx_N_monedas.setObjectName("spnbx_N_monedas")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.cbx_vela.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hidalgo Trading Tool"))
        self.pbtn_aceptar.setText(_translate("MainWindow", "Aceptar"))
        self.cbx_vela.setCurrentText(_translate("MainWindow", "1m"))
        self.cbx_vela.setItemText(0, _translate("MainWindow", "1m"))
        self.cbx_vela.setItemText(1, _translate("MainWindow", "3m"))
        self.cbx_vela.setItemText(2, _translate("MainWindow", "5m"))
        self.cbx_vela.setItemText(3, _translate("MainWindow", "15m"))
        self.cbx_vela.setItemText(4, _translate("MainWindow", "30m"))
        self.cbx_vela.setItemText(5, _translate("MainWindow", "1h"))
        self.cbx_vela.setItemText(6, _translate("MainWindow", "2h"))
        self.cbx_vela.setItemText(7, _translate("MainWindow", "4h"))
        self.cbx_vela.setItemText(8, _translate("MainWindow", "6h"))
        self.cbx_vela.setItemText(9, _translate("MainWindow", "8h"))
        self.cbx_vela.setItemText(10, _translate("MainWindow", "12h"))
        self.cbx_vela.setItemText(11, _translate("MainWindow", "1d"))
        self.cbx_vela.setItemText(12, _translate("MainWindow", "3d"))
        self.cbx_vela.setItemText(13, _translate("MainWindow", "1w"))
        self.cbx_vela.setItemText(14, _translate("MainWindow", "1M"))
        self.lbl_vela.setText(_translate("MainWindow", "Vela:"))
        self.lbl_nprsi.setText(_translate("MainWindow", "Periodos RSI:"))
        self.lbl_npt.setText(_translate("MainWindow", "Periodos tendencia:"))
        self.lbl_N_monedas.setText(_translate("MainWindow", "N??mero de monedas:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


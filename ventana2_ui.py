# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(180, 110)
        MainWindow.setMinimumSize(QtCore.QSize(180, 110))
        MainWindow.setMaximumSize(QtCore.QSize(180, 110))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icono.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_modo = QtWidgets.QLabel(self.centralwidget)
        self.lbl_modo.setGeometry(QtCore.QRect(30, 20, 31, 20))
        self.lbl_modo.setObjectName("lbl_modo")
        self.cbx_modo = QtWidgets.QComboBox(self.centralwidget)
        self.cbx_modo.setGeometry(QtCore.QRect(70, 20, 81, 20))
        self.cbx_modo.setObjectName("cbx_modo")
        self.cbx_modo.addItem("")
        self.cbx_modo.addItem("")
        self.pbtn_aceptar = QtWidgets.QPushButton(self.centralwidget)
        self.pbtn_aceptar.setGeometry(QtCore.QRect(50, 60, 75, 30))
        self.pbtn_aceptar.setObjectName("pbtn_aceptar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.cbx_modo.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hidalgo Trading Tool"))
        self.lbl_modo.setText(_translate("MainWindow", "Modo:"))
        self.cbx_modo.setItemText(0, _translate("MainWindow", "Simulación"))
        self.cbx_modo.setItemText(1, _translate("MainWindow", "Real"))
        self.pbtn_aceptar.setText(_translate("MainWindow", "Aceptar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


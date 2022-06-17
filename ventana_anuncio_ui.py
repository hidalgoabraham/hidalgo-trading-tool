# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana_anuncio.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(288, 137)
        Dialog.setMinimumSize(QtCore.QSize(288, 137))
        Dialog.setMaximumSize(QtCore.QSize(288, 137))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icono.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.pbtn = QtWidgets.QPushButton(Dialog)
        self.pbtn.setGeometry(QtCore.QRect(110, 80, 71, 30))
        self.pbtn.setObjectName("pbtn")
        self.lbl = QtWidgets.QLabel(Dialog)
        self.lbl.setGeometry(QtCore.QRect(10, 10, 265, 51))
        self.lbl.setText("")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Hidalgo Trading Bot"))
        self.pbtn.setText(_translate("Dialog", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


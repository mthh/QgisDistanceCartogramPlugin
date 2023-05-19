# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(620, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 265, 580, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.mainContentLabel = QtWidgets.QLabel(Dialog)
        self.mainContentLabel.setGeometry(QtCore.QRect(20, 10, 590, 191))
        self.mainContentLabel.setObjectName("mainContentLabel")
        self.matrixPathTextEdit = QtWidgets.QTextEdit(Dialog)
        self.matrixPathTextEdit.setGeometry(QtCore.QRect(20, 210, 580, 49))
        self.matrixPathTextEdit.setReadOnly(True)
        self.matrixPathTextEdit.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse
        )
        self.matrixPathTextEdit.setObjectName("matrixPathTextEdit")
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Distance Cartogram sample dataset"))
        self.mainContentLabel.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="justify"><a name="result_box"/>Two layers have been added.</p><p align="justify">- &quot;<span style=" font-weight:600; font-style:italic;">department</span>&quot; is a layer of <span style=" font-style:italic;">MultiPolygons</span>.<br>This is the background layer to be deformed.</p><p align="justify">- &quot;<span style=" font-weight:600; font-style:italic;">prefecture</span>&quot; is a layer of <span style=" font-style:italic;">Points</span>.<br/>It is between these points that the matrix of travel time by road was calculated.<br/>Its identifier field to use is &quot;<span style=" font-style:italic;">NOM_COM</span>&quot;.</p><p align="justify"><br/>To use Distance Cartogram you will also need to add the <span style=" font-weight:600; font-style:italic;">travel time matrix</span>.<br/>It\'s path is:</p></body></html>',
            )
        )


class DatasetDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(DatasetDialog, self).__init__(parent)
        self.setupUi(self)

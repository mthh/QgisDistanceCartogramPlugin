# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dist_cartogram_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DistCartogramDialogBase(object):
    def setupUi(self, DistCartogramDialogBase):
        DistCartogramDialogBase.setObjectName("DistCartogramDialogBase")
        DistCartogramDialogBase.resize(793, 702)
        self.button_box = QtWidgets.QDialogButtonBox(DistCartogramDialogBase)
        self.button_box.setGeometry(QtCore.QRect(530, 660, 251, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.label_5 = QtWidgets.QLabel(DistCartogramDialogBase)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 781, 41))
        self.label_5.setObjectName("label_5")
        self.gridTabWidget = QtWidgets.QTabWidget(DistCartogramDialogBase)
        self.gridTabWidget.setGeometry(QtCore.QRect(0, 60, 791, 531))
        self.gridTabWidget.setTabBarAutoHide(False)
        self.gridTabWidget.setObjectName("gridTabWidget")
        self.tabPtsMatrix = QtWidgets.QWidget()
        self.tabPtsMatrix.setObjectName("tabPtsMatrix")
        self.layoutWidget = QtWidgets.QWidget(self.tabPtsMatrix)
        self.layoutWidget.setGeometry(QtCore.QRect(7, 7, 771, 481))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(300, 0))
        self.label.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.backgroundLayerComboBox = gui.QgsMapLayerComboBox(self.layoutWidget)
        self.backgroundLayerComboBox.setMinimumSize(QtCore.QSize(370, 0))
        self.backgroundLayerComboBox.setMaximumSize(QtCore.QSize(400, 16777215))
        self.backgroundLayerComboBox.setObjectName("backgroundLayerComboBox")
        self.gridLayout.addWidget(self.backgroundLayerComboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(300, 0))
        self.label_2.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pointLayerComboBox = gui.QgsMapLayerComboBox(self.layoutWidget)
        self.pointLayerComboBox.setMinimumSize(QtCore.QSize(370, 0))
        self.pointLayerComboBox.setMaximumSize(QtCore.QSize(400, 16777215))
        self.pointLayerComboBox.setObjectName("pointLayerComboBox")
        self.gridLayout.addWidget(self.pointLayerComboBox, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setMinimumSize(QtCore.QSize(300, 0))
        self.label_8.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.mFieldComboBox = gui.QgsFieldComboBox(self.layoutWidget)
        self.mFieldComboBox.setMinimumSize(QtCore.QSize(370, 0))
        self.mFieldComboBox.setMaximumSize(QtCore.QSize(400, 16777215))
        self.mFieldComboBox.setObjectName("mFieldComboBox")
        self.gridLayout.addWidget(self.mFieldComboBox, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(300, 0))
        self.label_3.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.matrixQgsFileWidget = gui.QgsFileWidget(self.layoutWidget)
        self.matrixQgsFileWidget.setMinimumSize(QtCore.QSize(370, 0))
        self.matrixQgsFileWidget.setMaximumSize(QtCore.QSize(400, 27))
        self.matrixQgsFileWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.matrixQgsFileWidget.setObjectName("matrixQgsFileWidget")
        self.gridLayout.addWidget(self.matrixQgsFileWidget, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(300, 0))
        self.label_4.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.refFeatureComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.refFeatureComboBox.setMinimumSize(QtCore.QSize(370, 0))
        self.refFeatureComboBox.setMaximumSize(QtCore.QSize(400, 16777215))
        self.refFeatureComboBox.setObjectName("refFeatureComboBox")
        self.gridLayout.addWidget(self.refFeatureComboBox, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setMinimumSize(QtCore.QSize(300, 0))
        self.label_7.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.doubleSpinBoxDeplacement = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxDeplacement.setMinimumSize(QtCore.QSize(100, 0))
        self.doubleSpinBoxDeplacement.setMaximumSize(QtCore.QSize(200, 16777215))
        self.doubleSpinBoxDeplacement.setProperty("value", 1.0)
        self.doubleSpinBoxDeplacement.setObjectName("doubleSpinBoxDeplacement")
        self.gridLayout.addWidget(self.doubleSpinBoxDeplacement, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(300, 0))
        self.label_6.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.doubleSpinBoxGridPrecision = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxGridPrecision.setMinimumSize(QtCore.QSize(100, 0))
        self.doubleSpinBoxGridPrecision.setMaximumSize(QtCore.QSize(200, 16777215))
        self.doubleSpinBoxGridPrecision.setMinimum(0.5)
        self.doubleSpinBoxGridPrecision.setMaximum(5.0)
        self.doubleSpinBoxGridPrecision.setProperty("value", 1.0)
        self.doubleSpinBoxGridPrecision.setObjectName("doubleSpinBoxGridPrecision")
        self.gridLayout.addWidget(self.doubleSpinBoxGridPrecision, 6, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setMinimumSize(QtCore.QSize(140, 0))
        self.label_9.setMaximumSize(QtCore.QSize(270, 60))
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxResult = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBoxResult.setEnabled(False)
        self.checkBoxResult.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBoxResult.setCheckable(True)
        self.checkBoxResult.setChecked(True)
        self.checkBoxResult.setTristate(False)
        self.checkBoxResult.setObjectName("checkBoxResult")
        self.verticalLayout.addWidget(self.checkBoxResult)
        self.checkBoxImagePointLayer = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBoxImagePointLayer.setObjectName("checkBoxImagePointLayer")
        self.verticalLayout.addWidget(self.checkBoxImagePointLayer)
        self.checkBoxSourceGrid = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBoxSourceGrid.setObjectName("checkBoxSourceGrid")
        self.verticalLayout.addWidget(self.checkBoxSourceGrid)
        self.checkBoxTransformedGrid = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBoxTransformedGrid.setObjectName("checkBoxTransformedGrid")
        self.verticalLayout.addWidget(self.checkBoxTransformedGrid)
        self.gridLayout.addLayout(self.verticalLayout, 7, 1, 1, 1)
        self.gridTabWidget.addTab(self.tabPtsMatrix, "")
        self.tabSourceImage = QtWidgets.QWidget()
        self.tabSourceImage.setObjectName("tabSourceImage")
        self.layoutWidget1 = QtWidgets.QWidget(self.tabSourceImage)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 7, 771, 481))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBoxResult_2 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.checkBoxResult_2.setEnabled(False)
        self.checkBoxResult_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBoxResult_2.setCheckable(True)
        self.checkBoxResult_2.setChecked(True)
        self.checkBoxResult_2.setTristate(False)
        self.checkBoxResult_2.setObjectName("checkBoxResult_2")
        self.verticalLayout_2.addWidget(self.checkBoxResult_2)
        self.checkBoxSourceGrid_2 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.checkBoxSourceGrid_2.setObjectName("checkBoxSourceGrid_2")
        self.verticalLayout_2.addWidget(self.checkBoxSourceGrid_2)
        self.checkBoxTransformedGrid_2 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.checkBoxTransformedGrid_2.setObjectName("checkBoxTransformedGrid_2")
        self.verticalLayout_2.addWidget(self.checkBoxTransformedGrid_2)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 7, 1, 1, 1)
        self.mFieldComboBox_2 = gui.QgsFieldComboBox(self.layoutWidget1)
        self.mFieldComboBox_2.setMinimumSize(QtCore.QSize(400, 0))
        self.mFieldComboBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.mFieldComboBox_2.setObjectName("mFieldComboBox_2")
        self.gridLayout_3.addWidget(self.mFieldComboBox_2, 2, 1, 1, 1)
        self.doubleSpinBoxGridPrecision_2 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.doubleSpinBoxGridPrecision_2.setMinimumSize(QtCore.QSize(100, 0))
        self.doubleSpinBoxGridPrecision_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.doubleSpinBoxGridPrecision_2.setMinimum(0.5)
        self.doubleSpinBoxGridPrecision_2.setMaximum(5.0)
        self.doubleSpinBoxGridPrecision_2.setProperty("value", 1.0)
        self.doubleSpinBoxGridPrecision_2.setObjectName("doubleSpinBoxGridPrecision_2")
        self.gridLayout_3.addWidget(self.doubleSpinBoxGridPrecision_2, 5, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_10.setMinimumSize(QtCore.QSize(190, 0))
        self.label_10.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 5, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_14.setMinimumSize(QtCore.QSize(140, 0))
        self.label_14.setMaximumSize(QtCore.QSize(270, 60))
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 7, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_12.setMinimumSize(QtCore.QSize(300, 0))
        self.label_12.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_17.setMinimumSize(QtCore.QSize(300, 0))
        self.label_17.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 3, 0, 1, 1)
        self.pointLayerComboBox_2 = gui.QgsMapLayerComboBox(self.layoutWidget1)
        self.pointLayerComboBox_2.setMinimumSize(QtCore.QSize(400, 0))
        self.pointLayerComboBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.pointLayerComboBox_2.setObjectName("pointLayerComboBox_2")
        self.gridLayout_3.addWidget(self.pointLayerComboBox_2, 1, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_16.setMinimumSize(QtCore.QSize(300, 0))
        self.label_16.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 1, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_15.setMinimumSize(QtCore.QSize(300, 27))
        self.label_15.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 2, 0, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_32.setMinimumSize(QtCore.QSize(300, 0))
        self.label_32.setMaximumSize(QtCore.QSize(320, 16777215))
        self.label_32.setObjectName("label_32")
        self.gridLayout_3.addWidget(self.label_32, 4, 0, 1, 1)
        self.imagePointLayerComboBox_2 = gui.QgsMapLayerComboBox(self.layoutWidget1)
        self.imagePointLayerComboBox_2.setMinimumSize(QtCore.QSize(400, 0))
        self.imagePointLayerComboBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.imagePointLayerComboBox_2.setObjectName("imagePointLayerComboBox_2")
        self.gridLayout_3.addWidget(self.imagePointLayerComboBox_2, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem, 6, 1, 1, 1)
        self.mImageFieldComboBox_2 = gui.QgsFieldComboBox(self.layoutWidget1)
        self.mImageFieldComboBox_2.setMinimumSize(QtCore.QSize(400, 0))
        self.mImageFieldComboBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.mImageFieldComboBox_2.setObjectName("mImageFieldComboBox_2")
        self.gridLayout_3.addWidget(self.mImageFieldComboBox_2, 4, 1, 1, 1)
        self.backgroundLayerComboBox_2 = gui.QgsMapLayerComboBox(self.layoutWidget1)
        self.backgroundLayerComboBox_2.setMinimumSize(QtCore.QSize(400, 0))
        self.backgroundLayerComboBox_2.setMaximumSize(QtCore.QSize(400, 27))
        self.backgroundLayerComboBox_2.setObjectName("backgroundLayerComboBox_2")
        self.gridLayout_3.addWidget(self.backgroundLayerComboBox_2, 0, 1, 1, 1)
        self.gridTabWidget.addTab(self.tabSourceImage, "")
        self.button_box_help = QtWidgets.QDialogButtonBox(DistCartogramDialogBase)
        self.button_box_help.setGeometry(QtCore.QRect(10, 660, 91, 32))
        self.button_box_help.setStandardButtons(QtWidgets.QDialogButtonBox.Help)
        self.button_box_help.setObjectName("button_box_help")
        self.verticalLayoutWidget = QtWidgets.QWidget(DistCartogramDialogBase)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 590, 791, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.bottomVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.bottomVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomVerticalLayout.setObjectName("bottomVerticalLayout")

        self.retranslateUi(DistCartogramDialogBase)
        self.gridTabWidget.setCurrentIndex(0)
        self.button_box.accepted.connect(DistCartogramDialogBase.accept)
        self.button_box.rejected.connect(DistCartogramDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(DistCartogramDialogBase)
        DistCartogramDialogBase.setTabOrder(self.gridTabWidget, self.backgroundLayerComboBox)
        DistCartogramDialogBase.setTabOrder(self.backgroundLayerComboBox, self.pointLayerComboBox)
        DistCartogramDialogBase.setTabOrder(self.pointLayerComboBox, self.mFieldComboBox)
        DistCartogramDialogBase.setTabOrder(self.mFieldComboBox, self.matrixQgsFileWidget)
        DistCartogramDialogBase.setTabOrder(self.matrixQgsFileWidget, self.refFeatureComboBox)
        DistCartogramDialogBase.setTabOrder(self.refFeatureComboBox, self.doubleSpinBoxDeplacement)
        DistCartogramDialogBase.setTabOrder(self.doubleSpinBoxDeplacement, self.doubleSpinBoxGridPrecision)
        DistCartogramDialogBase.setTabOrder(self.doubleSpinBoxGridPrecision, self.checkBoxImagePointLayer)
        DistCartogramDialogBase.setTabOrder(self.checkBoxImagePointLayer, self.checkBoxSourceGrid)
        DistCartogramDialogBase.setTabOrder(self.checkBoxSourceGrid, self.checkBoxTransformedGrid)
        DistCartogramDialogBase.setTabOrder(self.checkBoxTransformedGrid, self.backgroundLayerComboBox_2)
        DistCartogramDialogBase.setTabOrder(self.backgroundLayerComboBox_2, self.pointLayerComboBox_2)
        DistCartogramDialogBase.setTabOrder(self.pointLayerComboBox_2, self.mFieldComboBox_2)
        DistCartogramDialogBase.setTabOrder(self.mFieldComboBox_2, self.imagePointLayerComboBox_2)
        DistCartogramDialogBase.setTabOrder(self.imagePointLayerComboBox_2, self.mImageFieldComboBox_2)
        DistCartogramDialogBase.setTabOrder(self.mImageFieldComboBox_2, self.doubleSpinBoxGridPrecision_2)
        DistCartogramDialogBase.setTabOrder(self.doubleSpinBoxGridPrecision_2, self.checkBoxSourceGrid_2)
        DistCartogramDialogBase.setTabOrder(self.checkBoxSourceGrid_2, self.checkBoxTransformedGrid_2)

    def retranslateUi(self, DistCartogramDialogBase):
        _translate = QtCore.QCoreApplication.translate
        DistCartogramDialogBase.setWindowTitle(_translate("DistCartogramDialogBase", "DistCartogram"))
        self.label_5.setText(_translate("DistCartogramDialogBase", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Distance cartogram creation </span></p></body></html>"))
        self.label.setToolTip(_translate("DistCartogramDialogBase", "The layer to be deformed"))
        self.label.setText(_translate("DistCartogramDialogBase", "Background layer"))
        self.label_2.setText(_translate("DistCartogramDialogBase", "Point layer"))
        self.label_8.setText(_translate("DistCartogramDialogBase", "Point layer id field"))
        self.label_3.setToolTip(_translate("DistCartogramDialogBase", "Path to a .csv document containing a time matrix between the points from the layer previously selected."))
        self.label_3.setText(_translate("DistCartogramDialogBase", "Time matrix"))
        self.label_4.setToolTip(_translate("DistCartogramDialogBase", "The reference feature (it\'s location will stay unchanged)"))
        self.label_4.setText(_translate("DistCartogramDialogBase", "Reference feature"))
        self.label_7.setText(_translate("DistCartogramDialogBase", "Displacement factor"))
        self.label_6.setText(_translate("DistCartogramDialogBase", "Grid precision"))
        self.label_9.setText(_translate("DistCartogramDialogBase", "Output"))
        self.checkBoxResult.setText(_translate("DistCartogramDialogBase", "Transformed layer"))
        self.checkBoxImagePointLayer.setText(_translate("DistCartogramDialogBase", "Image point layer"))
        self.checkBoxSourceGrid.setText(_translate("DistCartogramDialogBase", "Source grid"))
        self.checkBoxTransformedGrid.setText(_translate("DistCartogramDialogBase", "Transformed grid"))
        self.gridTabWidget.setTabText(self.gridTabWidget.indexOf(self.tabPtsMatrix), _translate("DistCartogramDialogBase", "From source points and time matrix"))
        self.checkBoxResult_2.setText(_translate("DistCartogramDialogBase", "Transformed layer"))
        self.checkBoxSourceGrid_2.setText(_translate("DistCartogramDialogBase", "Source grid"))
        self.checkBoxTransformedGrid_2.setText(_translate("DistCartogramDialogBase", "Transformed grid"))
        self.label_10.setText(_translate("DistCartogramDialogBase", "Grid precision"))
        self.label_14.setText(_translate("DistCartogramDialogBase", "Output"))
        self.label_12.setToolTip(_translate("DistCartogramDialogBase", "The layer to be deformed"))
        self.label_12.setText(_translate("DistCartogramDialogBase", "Background layer"))
        self.label_17.setToolTip(_translate("DistCartogramDialogBase", "Path to a .csv document containing a time matrix between the points from the layer previously selected."))
        self.label_17.setText(_translate("DistCartogramDialogBase", "Image points layer"))
        self.label_16.setText(_translate("DistCartogramDialogBase", "Source points layer"))
        self.label_15.setText(_translate("DistCartogramDialogBase", "Source points layer id field"))
        self.label_32.setText(_translate("DistCartogramDialogBase", "Image points layer id field"))
        self.gridTabWidget.setTabText(self.gridTabWidget.indexOf(self.tabSourceImage), _translate("DistCartogramDialogBase", "From source points and image points"))

from qgis import gui

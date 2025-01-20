# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DistanceCartogram
                                 A QGIS plugin
 Compute distance cartogram
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-07-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Matthieu Viry
        email                : matthieu.viry@cnrs.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import numpy as np
import csv
import os.path

from PyQt5.QtCore import (
    QCoreApplication,
    QSettings,
    Qt,
    QThread,
    QTranslator,
    QUrl,
    qVersion,
)
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import (
    QAction,
    QDialogButtonBox,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QListWidgetItem,
)
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsMapLayerProxyModel,
    QgsMessageLog,
    QgsProject,
    QgsMapLayerType,
)
from qgis.gui import QgsMessageBar

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .dist_cartogram_dialog import DistCartogramDialog

# Code for the small dialog displayed when sample dataset is added
from .dist_cartogram_dataset_boxUi import DatasetDialog

# QThread worker to compute the cartogram in background
from .worker import DistCartogramWorker

# Helpers to manipulate data to prepare for bidimensionnal regression
from .utils import (
    create_image_points,
    extract_source_image,
    get_total_features,
    get_merged_extent,
)


class DistanceCartogram:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "DistanceCartogram_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = DistCartogramDialog()

        self.dlg.msg_bar = QgsMessageBar()
        self.dlg.msg_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.dlg.bottomVerticalLayout.addWidget(self.dlg.msg_bar)
        self.col_ix = None
        self.line_ix = None
        self.time_matrix = None

        # Params for first tab:
        self.dlg.backgroundLayersListWidget.currentRowChanged.connect(
            self.state_ok_button
        )
        self.dlg.backgroundLayersListWidget.itemChanged.connect(self.state_ok_button)
        self.dlg.pointLayerComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.dlg.pointLayerComboBox.layerChanged.connect(self.fill_field_combo_box)

        self.dlg.matrixQgsFileWidget.setFilter("*.csv")
        self.dlg.matrixQgsFileWidget.fileChanged.connect(self.read_matrix)

        self.dlg.mFieldComboBox.fieldChanged.connect(self.state_ok_button)

        self.dlg.refFeatureComboBox.currentIndexChanged.connect(self.state_ok_button)

        self.dlg.refFeatureComboBox.activated.connect(self.state_ok_button)

        # Params for second tab:
        self.dlg.backgroundLayersListWidget_2.currentRowChanged.connect(
            self.state_ok_button
        )
        self.dlg.backgroundLayersListWidget_2.itemChanged.connect(self.state_ok_button)
        self.dlg.pointLayerComboBox_2.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.dlg.pointLayerComboBox_2.layerChanged.connect(
            self.fill_field_combo_box_source
        )

        self.dlg.imagePointLayerComboBox_2.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.dlg.imagePointLayerComboBox_2.layerChanged.connect(
            self.fill_field_combo_box_image
        )

        self.dlg.mFieldComboBox_2.fieldChanged.connect(self.state_ok_button)

        self.dlg.mImageFieldComboBox_2.fieldChanged.connect(self.state_ok_button)

        self.dlg.button_box_help.helpRequested.connect(self.show_help)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("&DistanceCartogram")
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar("DistanceCartogram")
        self.toolbar.setObjectName("DistanceCartogram")
        self.fill_file_widget_with_sample_value = False

        def update_layers_in_list():
            # List the layers
            layers = [
                layer
                for layer in QgsProject.instance().mapLayers().values()
                if layer.type() == QgsMapLayerType.VectorLayer
            ]
            items = [f"{i.name()} [{i.crs().authid()}]" for i in layers]

            # Clean the content of the widgets
            self.dlg.backgroundLayersListWidget.clear()
            self.dlg.backgroundLayersListWidget_2.clear()

            # Add them in our QListWidget:
            for s in items:
                items = [QListWidgetItem(s), QListWidgetItem(s)]
                for i in items:
                    i.setFlags(i.flags() | Qt.ItemIsUserCheckable)
                    i.setCheckState(Qt.Unchecked)
                self.dlg.backgroundLayersListWidget.addItem(items[0])
                self.dlg.backgroundLayersListWidget_2.addItem(items[1])

        # The logic to keep the layers in our QListWidget synced with the
        # layers in the QGIS project
        QgsProject.instance().layersAdded.connect(update_layers_in_list)
        QgsProject.instance().layersRemoved.connect(update_layers_in_list)
        update_layers_in_list()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("DistanceCartogram", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ":/plugins/dist_cartogram/icon.png"
        self.add_action(
            icon_path,
            text=self.tr("Create distance cartogram"),
            callback=self.run,
            parent=self.iface.mainWindow(),
        )
        self.add_action(
            icon_path,
            text=self.tr("Add sample dataset"),
            callback=self.add_sample_dataset,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
        )

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(self.tr("&DistanceCartogram"), action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def show_help(self):
        """Display application help to the user."""
        help_file = "file:///{}/help/index.html".format(self.plugin_dir)
        QDesktopServices.openUrl(QUrl(help_file))

    def add_sample_dataset(self):
        base_uri = "|".join(
            [
                os.path.join(self.plugin_dir, "data", "prefecture_FRA.gpkg"),
                "layername={}",
            ]
        )

        layerDpt = self.iface.addVectorLayer(
            base_uri.format("departement"), "departement", "ogr"
        )

        layerPref = self.iface.addVectorLayer(
            base_uri.format("prefecture"), "prefecture", "ogr"
        )

        crs = QgsCoordinateReferenceSystem("EPSG:2154")

        layerDpt.setCrs(crs)
        layerPref.setCrs(crs)

        csv_path = os.path.join(self.plugin_dir, "data", "mat.csv")

        dataset_dialog = DatasetDialog()
        dataset_dialog.show()
        dataset_dialog.activateWindow()
        dataset_dialog.matrixPathTextEdit.setText(csv_path)
        _rv = dataset_dialog.exec_()
        self.fill_file_widget_with_sample_value = True

    def fill_field_combo_box(self, layer):
        self.dlg.mFieldComboBox.setLayer(layer)
        self.state_ok_button()

    def fill_field_combo_box_source(self, layer):
        self.dlg.mFieldComboBox_2.setLayer(layer)
        self.state_ok_button()

    def fill_field_combo_box_image(self, layer):
        self.dlg.mImageFieldComboBox_2.setLayer(layer)
        self.state_ok_button()

    def check_layers_crs(self, layers):
        crs = []
        for lyr in layers:
            proj = lyr.crs()
            crs.append((proj.authid(), proj.isGeographic()))

        self.dlg.msg_bar.clearWidgets()

        if not all([crs[0][0] == authid[0] for authid in crs]):
            self.dlg.msg_bar.pushCritical(
                self.tr("Error"),
                self.tr("Layers have to be in the same (projected) crs"),
            )
            return False

        elif any([a[1] for a in crs]):
            self.dlg.msg_bar.pushCritical(
                self.tr("Error"), self.tr("Layers have to be in a projected crs")
            )
            return False

        return True

    def check_values_id_field(self, layer, id_field):
        if not self.line_ix:
            return
        ids = [str(ft[id_field]) for ft in layer.getFeatures()]
        if not any(_id in self.line_ix for _id in ids):
            self.dlg.msg_bar.clearWidgets()
            self.dlg.msg_bar.pushCritical(
                self.tr("Error"),
                self.tr("No match between point layer ID and matrix ID"),
            )
            return False
        self.dlg.msg_bar.clearWidgets()
        self.dlg.msg_bar.pushSuccess(
            self.tr("Success"),
            self.tr("Matches found between point layer ID and matrix ID"),
        )
        return True

    def check_match_id_image_source(self, src_lyr, src_id_field, img_lyr, img_id_field):
        source_ids = [ft[src_id_field] for ft in src_lyr.getFeatures()]
        image_ids = [ft[img_id_field] for ft in img_lyr.getFeatures()]
        set_source_ids = set(source_ids)
        set_image_ids = set(image_ids)

        self.dlg.msg_bar.clearWidgets()

        if len(source_ids) != len(set_source_ids) or len(image_ids) != len(
            set_image_ids
        ):
            self.dlg.msg_bar.pushCritical(
                self.tr("Error"), self.tr("Identifiant values have to be uniques")
            )
            return False

        if len(set_source_ids.intersection(set_image_ids)) < 3:
            self.dlg.msg_bar.pushCritical(
                self.tr("Error"),
                self.tr(
                    "Not enough matching features between " "source and image layer"
                ),
            )
            return False

        return True

    def read_matrix(self, filepath):
        self.col_ix = None
        self.line_ix = None
        self.time_matrix = None
        col_ix = {}
        line_ix = {}

        if not filepath:
            return

        self.dlg.msg_bar.clearWidgets()

        if not os.path.exists(filepath) or os.path.isdir(filepath):
            self.dlg.msg_bar.pushCritical(
                self.tr("Error"), self.tr("File {} not found".format(filepath))
            )
            return
        try:
            with open(filepath, "r") as dest_f:
                data_iter = csv.reader(dest_f, quotechar='"')
                header = next(data_iter)

                for i, _id in enumerate(header):
                    if i == 0:
                        continue
                    col_ix[str(_id)] = i - 1

                d = []

                for i, data in enumerate(data_iter):
                    d.append(data[1:])
                    line_ix[data[0]] = i
                try:
                    self.time_matrix = np.array(d, dtype=float)

                except ValueError as err:
                    self.dlg.msg_bar.pushCritical(
                        self.tr("Error"),
                        self.tr(
                            "Error while reading the matrix - All values "
                            "(excepting columns/lines id) must be numbers"
                        ),
                    )

                    QgsMessageLog.logMessage(
                        "{}: {}".format(err.__class__, err),
                        level=Qgis.Critical,
                        tag="Plugins",
                    )
                    return

        except Exception as err:
            self.dlg.msg_bar.pushCritical(
                self.tr("Error"),
                self.tr(
                    "An unexpected error has occurred while reading the "
                    "CSV matrix. Please see the “Plugins” section of the "
                    "message log for details."
                ),
            )
            QgsMessageLog.logMessage(
                "{}: {}".format(err.__class__, err), level=Qgis.Critical, tag="Plugins"
            )
            return

        if not any(k in line_ix for k in col_ix.keys()):
            self.time_matrix = None
            self.dlg.msg_bar.pushCritical(
                self.tr("Error"),
                self.tr(
                    "Lines and columns index have to be (at least partially) the same"
                ),
            )
            return

        self.dlg.refFeatureComboBox.clear()
        self.dlg.refFeatureComboBox.addItems(list(sorted(line_ix.keys())))
        self.dlg.refFeatureComboBox.setCurrentIndex(0)
        self.col_ix = col_ix
        self.line_ix = line_ix
        self.state_ok_button()

    def updateStatusMessage(self, message=""):
        try:
            self.statusMessageLabel.setText("DistanceCartogram: " + message)
        except:
            pass

    def updateProgressBar(self, increase=1):
        try:
            self.progressBar.setValue(self.progressBar.value() + increase)
        except:
            pass

    def reset_fields(self):
        # self.dlg.pointLayerComboBox.setCurrentIndex(-1)
        # self.dlg.backgroundLayerComboBox.setCurrentIndex(-1)
        # self.dlg.refFeatureComboBox.setCurrentIndex(-1)
        layer = self.dlg.pointLayerComboBox.currentLayer()
        nb_field = self.dlg.mFieldComboBox.count()
        if nb_field < 1 and layer:
            self.fill_field_combo_box(layer)
        layer_source = self.dlg.pointLayerComboBox.currentLayer()
        nb_field = self.dlg.mFieldComboBox_2.count()
        if nb_field < 1 and layer_source:
            self.fill_field_combo_box_source(layer_source)
        layer_image = self.dlg.pointLayerComboBox.currentLayer()
        nb_field = self.dlg.mImageFieldComboBox_2.count()
        if nb_field < 1 and layer_image:
            self.fill_field_combo_box_image(layer_image)
        self.state_ok_button()

    def has_layers_selected(self, which):
        widget = getattr(self.dlg, which)
        for n in range(widget.count()):
            if widget.item(n).checkState() == Qt.Checked:
                return True

    def get_layers_selected(self, which):
        widget = getattr(self.dlg, which)
        layers = []
        for n in range(widget.count()):
            if widget.item(n).checkState() == Qt.Checked:
                name = widget.item(n).text().rpartition(" ")[0]
                layer = QgsProject.instance().mapLayersByName(name)[0]
                layers.append(layer)
        return layers

    def state_ok_button(self):
        result = False

        if self.dlg.gridTabWidget.currentIndex() == 0:
            a = self.dlg.pointLayerComboBox.currentIndex()
            b = self.has_layers_selected("backgroundLayersListWidget")
            c = self.dlg.refFeatureComboBox.currentIndex()
            d = self.dlg.mFieldComboBox.currentIndex()
            e = self.dlg.matrixQgsFileWidget.filePath()

            if a == -1 or not b:
                result = False

            else:
                result = self.check_layers_crs(
                    (
                        self.dlg.pointLayerComboBox.currentLayer(),
                        *self.get_layers_selected("backgroundLayersListWidget"),
                    )
                )

                if (
                    c == -1
                    or d == -1
                    or not self.check_values_id_field(
                        self.dlg.pointLayerComboBox.currentLayer(),
                        self.dlg.mFieldComboBox.currentField(),
                    )
                    or not e
                ):
                    result = False

        else:
            a = self.has_layers_selected("backgroundLayersListWidget_2")
            b = self.dlg.pointLayerComboBox_2.currentIndex()
            c = self.dlg.mFieldComboBox_2.currentIndex()
            d = self.dlg.imagePointLayerComboBox_2.currentIndex()
            e = self.dlg.mImageFieldComboBox_2.currentIndex()

            if (
                not a
                or b == -1
                or c == -1
                or d == -1
                or e == -1
                or not self.check_match_id_image_source(
                    self.dlg.pointLayerComboBox_2.currentLayer(),
                    self.dlg.mFieldComboBox_2.currentField(),
                    self.dlg.imagePointLayerComboBox_2.currentLayer(),
                    self.dlg.mImageFieldComboBox_2.currentField(),
                )
            ):
                result = False
            else:
                result = self.check_layers_crs(
                    (
                        self.dlg.pointLayerComboBox_2.currentLayer(),
                        *self.get_layers_selected("backgroundLayersListWidget"),
                    )
                )

        self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(result)

    def startWorker(self, src_pts, img_pts, precision, max_extent, layers, total_features):
        worker = DistCartogramWorker(
            src_pts, img_pts, precision, max_extent, layers, self.display, self.tr, total_features,
        )
        thread = QThread()
        worker.moveToThread(thread)

        # connecting signals+slots
        worker.finished.connect(self.workerFinished)
        worker.resultComplete.connect(self.cartogram_complete)
        worker.error.connect(self.workerError)
        worker.progress.connect(self.updateProgressBar)
        worker.status.connect(self.updateStatusMessage)
        thread.started.connect(worker.run)
        thread.start()

        self.worker = worker
        self.thread = thread

    def stopWorker(self):
        if hasattr(self, "worker"):
            self.worker.stopped = True

    def push_error(self, e, exceptionString):
        self.iface.messageBar().pushCritical(
            self.tr("Error"),
            self.tr(
                "An error occurred during distance cartogram creation. "
                + "Please see the “Plugins” section of the message "
                + "log for details."
            ),
        )
        QgsMessageLog.logMessage(exceptionString, level=Qgis.Critical, tag="Plugins")

    def workerError(self, e, exceptionString):
        self.push_error(e, exceptionString)
        self.workerFinished()

    def workerFinished(self):
        try:
            self.worker.deleteLater()
        except:
            pass
        self.thread.quit()
        self.thread.wait()
        self.thread.terminate()
        self.thread.deleteLater()
        self.iface.messageBar().popWidget(self.messageBarItem)

    def cartogram_complete(
        self, result_layers=None, source_grid_layer=None, trans_grid_layer=None
    ):
        if (
            hasattr(self, "worker")
            and hasattr(self.worker, "stopped")
            and self.worker.stopped
        ):
            return
        if result_layers is not None:
            if self.display["source_grid"]:
                QgsProject.instance().addMapLayer(source_grid_layer)
            if self.display["trans_grid"]:
                QgsProject.instance().addMapLayer(trans_grid_layer)

            for result_layer in result_layers:
                QgsProject.instance().addMapLayer(result_layer)

            if self.display["image_points"]:
                QgsProject.instance().addMapLayer(self.image_layer)

            self.iface.messageBar().popWidget(self.messageBarItem)
        else:
            QgsMessageLog.logMessage(
                self.tr("DistanceCartogram computation cancelled by user")
            )

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # If the last action was to add the sample dataset, pref-fill the
        # dedicated QgsFileWidget with the path of the sample csv matrix
        if self.fill_file_widget_with_sample_value:
            self.fill_file_widget_with_sample_value = False
            csv_path = os.path.join(self.plugin_dir, "data", "mat.csv")
            self.dlg.matrixQgsFileWidget.setFilePath(csv_path)
            self.dlg.mFieldComboBox.setField("NOM_COM")
        # ...
        self.reset_fields()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            if not self.dlg.button_box.button(QDialogButtonBox.Ok).isEnabled():
                return
            # set up all widgets for status reporting
            self.progressBar = QProgressBar()
            self.progressBar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.progressBar.setMaximum(100)

            self.statusMessageLabel = QLabel(self.tr("Starting..."))
            self.statusMessageLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            cancelButton = QPushButton(self.tr("Cancel"))
            cancelButton.clicked.connect(self.stopWorker)

            self.messageBarItem = self.iface.messageBar().createMessage("")
            self.messageBarItem.layout().addWidget(self.statusMessageLabel)
            self.messageBarItem.layout().addWidget(self.progressBar)
            self.messageBarItem.layout().addWidget(cancelButton)

            self.iface.messageBar().pushWidget(self.messageBarItem, Qgis.Info)

            self.updateStatusMessage(self.tr("Starting"))

            if self.dlg.gridTabWidget.currentIndex() == 0:
                if self.time_matrix is None:
                    self.read_matrix(self.dlg.matrixQgsFileWidget.filePath())
                background_layers = self.get_layers_selected(
                    "backgroundLayersListWidget"
                )
                source_layer = self.dlg.pointLayerComboBox.currentLayer()
                id_ref_feature = self.dlg.refFeatureComboBox.currentText()
                id_field = self.dlg.mFieldComboBox.currentField()
                source_idx, dest_idx = self.line_ix, self.col_ix
                mat_extract = self.time_matrix[source_idx[id_ref_feature]]
                precision = self.dlg.doubleSpinBoxGridPrecision.value()
                deplacement_factor = self.dlg.doubleSpinBoxDeplacement.value()

                total_features = get_total_features(background_layers)

                self.progressBar.setMaximum(int(0.20 * total_features + total_features))

                self.display = {
                    "source_grid": self.dlg.checkBoxSourceGrid.isChecked(),
                    "trans_grid": self.dlg.checkBoxTransformedGrid.isChecked(),
                    "image_points": self.dlg.checkBoxImagePointLayer.isChecked(),
                }
                self.updateStatusMessage(self.tr("Creation of image points layer"))
                # We create the layer of 'image' points from the layer
                # of 'source' points.
                # We (obviously) skip features whose geometry is Null / empty
                # (and return a count of them in the unused_points variable).
                # As these points aren't displayed on the map, I think
                # it is not necessary to warn the user about that
                # (but this may change in the future).
                (
                    source_to_use,
                    image_to_use,
                    image_layer,
                    unused_points,
                ) = create_image_points(
                    source_layer,
                    id_field,
                    mat_extract,
                    id_ref_feature,
                    dest_idx,
                    deplacement_factor,
                    self.display["image_points"],
                )
                self.updateProgressBar(int(0.05 * total_features))
                if len(source_to_use) == 0 or len(image_to_use) == 0:
                    self.iface.messageBar().pushCritical(
                        self.tr("Error"),
                        self.tr(
                            "DistanceCartogram: "
                            'The "image" point layer is empty.'
                            "This is probably due to a problem of "
                            "non-correspondence between the identifiers of the"
                            " features the point layer and the identifiers in "
                            "the provided matrix."
                        ),
                    )
                    return
                self.image_layer = image_layer
                extent = get_merged_extent(background_layers + [source_layer])
                max_extent = (
                    extent.xMinimum(),
                    extent.yMinimum(),
                    extent.xMaximum(),
                    extent.yMaximum(),
                )
                self.startWorker(
                    source_to_use,
                    image_to_use,
                    precision,
                    max_extent,
                    background_layers,
                    total_features,
                )

            else:
                background_layers = self.get_layers_selected(
                    "backgroundLayersListWidget_2"
                )
                source_layer = self.dlg.pointLayerComboBox_2.currentLayer()
                id_field_source = self.dlg.mFieldComboBox_2.currentField()
                image_layer = self.dlg.imagePointLayerComboBox_2.currentLayer()
                id_field_image = self.dlg.mImageFieldComboBox_2.currentField()
                precision = self.dlg.doubleSpinBoxGridPrecision_2.value()
                #
                self.display = {
                    "source_grid": self.dlg.checkBoxSourceGrid_2.isChecked(),
                    "trans_grid": self.dlg.checkBoxTransformedGrid_2.isChecked(),
                    "image_points": False,
                }

                total_features = get_total_features(background_layers)

                self.progressBar.setMaximum(int(0.20 * total_features + total_features))

                if source_layer.featureCount() != image_layer.featureCount():
                    self.updateStatusMessage(
                        self.tr(
                            "Number of features differ between source and image "
                            "layers - Only feature with matching ids will be "
                            "taken into account"
                        )
                    )
                source_to_use, image_to_use = extract_source_image(
                    source_layer, image_layer, id_field_source, id_field_image
                )

                self.updateProgressBar(int(0.05 * total_features))

                extent = get_merged_extent(
                    background_layers + [source_layer, image_layer]
                )
                max_extent = (
                    extent.xMinimum(),
                    extent.yMinimum(),
                    extent.xMaximum(),
                    extent.yMaximum(),
                )
                self.startWorker(
                    source_to_use,
                    image_to_use,
                    precision,
                    max_extent,
                    background_layers,
                    total_features,
                )

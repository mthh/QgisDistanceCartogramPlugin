#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /***************************************************************************
# DistanceCartogram
#
# Compute distance cartogram
# 							 -------------------
# 		begin				: 2018-07-13
# 		git sha				: $Format:%H$
# 		copyright			: (C) 2018 by Matthieu Viry
# 		email				: matthieu.viry@cnrs.fr
# ***************************************************************************/
#
# /***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

from math import sqrt
import traceback

from PyQt5.QtCore import pyqtSignal, QObject, QVariant

from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
    QgsWkbTypes,
)

from .grid import Grid


class DistCartogramWorker(QObject):
    resultComplete = pyqtSignal(object, object, object)
    finished = pyqtSignal()
    error = pyqtSignal(Exception, str)
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

    def __init__(
        self, src_pts, image_pts, precision, extent, layers_to_transform, to_display, tr
    ):
        QObject.__init__(self)

        self.src_pts = src_pts
        self.image_pts = image_pts
        self.precision = precision
        self.extent = extent
        self.layers_to_transform = layers_to_transform
        self.to_display = to_display
        self.tr = tr

    def get_transformed_layers(self):
        transformed_layers = []
        for background_layer in self.layers_to_transform:
            _t = QgsWkbTypes.displayString(background_layer.wkbType())

            result_layer = QgsVectorLayer(
                "{}?crs={}".format(_t, background_layer.crs().authid()),
                "{}_cartogram".format(background_layer.name()),
                "memory",
            )
            features_to_add = []
            result_layer.setCrs(background_layer.crs())
            pr_result_layer = result_layer.dataProvider()
            pr_result_layer.addAttributes(background_layer.fields().toList())
            result_layer.updateFields()

            for ix, ft in enumerate(background_layer.getFeatures()):
                ref_geom = ft.geometry()
                ref_coords = ref_geom.__geo_interface__["coordinates"]
                if ref_geom.__geo_interface__["type"] == "Point":
                    new_geom = QgsGeometry.fromPointXY(QgsPointXY(*self.g._interp_point(*ref_coords)))
                elif ref_geom.__geo_interface__["type"] == "MultiPoint":
                    new_geom = QgsGeometry.fromMultiPointXY(
                        [
                            QgsPointXY(*self.g._interp_point(*ref_coords[ix_coords]))
                            for ix_coords in range(len(ref_coords))
                        ]
                    )
                elif ref_geom.__geo_interface__["type"] == "LineString":
                    new_geom = QgsGeometry.fromPolyLineXY(
                        [
                            QgsPointXY(*self.g._interp_point(*ref_coords[ix_coords]))
                            for ix_coords in range(len(ref_coords))
                        ]
                    )
                elif ref_geom.__geo_interface__["type"] == "MultiLineString":
                    lines = []
                    for ix_line in range(len(ref_coords)):
                        lines.append(
                            [
                                QgsPointXY(
                                    *self.g._interp_point(
                                        *ref_coords[ix_line][ix_coords]
                                    )
                                )
                                for ix_coords in range(len(ref_coords[ix_line]))
                            ]
                        )
                    new_geom = QgsGeometry.fromMultiPolylineXY(lines)
                elif ref_geom.__geo_interface__["type"] == "Polygon":
                    rings = []
                    for ix_ring in range(len(ref_coords)):
                        rings.append(
                            [
                                QgsPointXY(
                                    *self.g._interp_point(
                                        *ref_coords[ix_ring][ix_coords]
                                    )
                                )
                                for ix_coords in range(len(ref_coords[ix_ring]))
                            ]
                        )
                    new_geom = QgsGeometry.fromPolygonXY(rings)

                elif ref_geom.__geo_interface__["type"] == "MultiPolygon":
                    polys = []
                    for ix_poly in range(len(ref_coords)):
                        rings = []
                        for ix_ring in range(len(ref_coords[ix_poly])):
                            rings.append(
                                [
                                    QgsPointXY(
                                        *self.g._interp_point(
                                            *ref_coords[ix_poly][ix_ring][ix_coords]
                                        )
                                    )
                                    for ix_coords in range(
                                        len(ref_coords[ix_poly][ix_ring])
                                    )
                                ]
                            )
                        polys.append(rings)
                    new_geom = QgsGeometry.fromMultiPolygonXY(polys)
                else:
                    self.status.emit("Geometry type error")
                    continue
                feature = QgsFeature()
                feature.setGeometry(new_geom)
                feature.setAttributes(ft.attributes())
                features_to_add.append(feature)
                self.progress.emit(1)
            pr_result_layer.addFeatures(features_to_add)
            result_layer.updateExtents()
            transformed_layers.append(result_layer)
        return transformed_layers

    def run(self):
        try:
            def _get_inter_nb_iter(coef_iter):
                return int(coef_iter * sqrt(len(self.src_pts)))

            self.status.emit(self.tr("Creation of interpolation grid..."))
            self.g = Grid(self.src_pts, self.precision, self.extent)
            self.status.emit(self.tr("Interpolation process..."))
            self.progress.emit(((self.precision * len(self.image_pts)) / 3))
            self.g.interpolate(self.image_pts, _get_inter_nb_iter(4))
            self.progress.emit(((self.precision * len(self.image_pts)) / 3))
            self.status.emit(self.tr("Transforming layers..."))
            transformed_layers = self.get_transformed_layers()

            self.status.emit(self.tr("Preparing results for displaying..."))
            if self.to_display["source_grid"]:
                polys = self.g._get_grid_coords("source")
                source_grid_layer = make_grid_layer(
                    polys, self.layers_to_transform[0].crs(), "source"
                )
            else:
                source_grid_layer = None

            self.progress.emit(5)
            if self.to_display["trans_grid"]:
                polys = self.g._get_grid_coords("interp")
                trans_grid_layer = make_grid_layer(
                    polys, self.layers_to_transform[0].crs(), "interp"
                )
            else:
                trans_grid_layer = None

            self.resultComplete.emit(
                transformed_layers,
                source_grid_layer,
                trans_grid_layer,
            )
            self.finished.emit()
        except Exception as e:
            self.error.emit(e, traceback.format_exc())


def make_grid_layer(polys, crs, _type_grid):
    result_layer = QgsVectorLayer(
        "Polygon?crs={}&field=ID:integer".format(crs.authid()),
        "{}_grid".format(_type_grid),
        "memory",
    )

    result_layer.startEditing()
    result_layer.setCrs(crs)
    for ix, geom in enumerate(polys):
        new_geom = QgsGeometry.fromPolygonXY(
            [
                [
                    QgsPointXY(*geom[ix_ring][ix_coords])
                    for ix_coords in range(len(geom[ix_ring]))
                ]
                for ix_ring in range(len(geom))
            ]
        )
        feature = QgsFeature()
        feature.setGeometry(new_geom)
        feature.setAttributes([QVariant(ix)])
        result_layer.addFeature(feature, QgsFeatureSink.FastInsert)
    result_layer.commitChanges()
    return result_layer

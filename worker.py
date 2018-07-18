#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /***************************************************************************
# DistCartogram
#
# Compute distance cartogram
#							 -------------------
#		begin				: 2018-07-13
#		git sha				: $Format:%H$
#		copyright			: (C) 2018 by Matthieu Viry
#		email				: matthieu.viry@cnrs.fr
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

from PyQt5.QtCore import (
    pyqtSignal,
    QObject,
    QVariant
)

from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer
)

from .grid import Grid


class DistCartogramWorker(QObject):
    resultComplete = pyqtSignal(list, object, object)
    finished = pyqtSignal()
    error = pyqtSignal(Exception, str)
    progress = pyqtSignal(int)
#    status = pyqtSignal(str)

    def __init__(self,
                 src_pts,
                 image_pts,
                 precision,
                 extent,
                 layers_to_transform,
                 to_display):
        QObject.__init__(self)

        self.src_pts = src_pts
        self.image_pts = image_pts
        self.precision = precision
        self.extent = extent
        self.layers_to_transform = layers_to_transform
        self.to_display = to_display

    def get_transformed_layers(self):
        transformed_layers = []
        for background_layer in self.layers_to_transform:
            result_layer = QgsVectorLayer(
                "MultiPolygon?crs={}".format(background_layer.crs().authid()),
                "result_cartogram",
                "memory")

            pr_result_layer = result_layer.dataProvider()
            pr_result_layer.addAttributes(background_layer.fields().toList())
            result_layer.updateFields()
            result_layer.startEditing()
            result_layer.setCrs(background_layer.crs())
            for ft in background_layer.getFeatures():
                ref_geom = ft.geometry()
                ref_coords = ref_geom.__geo_interface__['coordinates']
                if ref_geom.__geo_interface__['type'] == 'Polygon':
                    rings = []
                    for ix_ring in range(len(ref_coords)):
                        rings.append([
                            QgsPointXY(
                                *self.g._interp_point(*ref_coords[ix_ring][ix_coords]))
                            for ix_coords in range(len(ref_coords[ix_ring]))
                        ])
                    new_geom = QgsGeometry.fromPolygonXY(rings)

                elif ref_geom.__geo_interface__['type'] == 'MultiPolygon':
                    polys = []
                    for ix_poly in range(len(ref_coords)):
                        rings = []
                        for ix_ring in range(len(ref_coords[ix_poly])):
                            rings.append([
                                QgsPointXY(
                                    *self.g._interp_point(
                                        *ref_coords[ix_poly][ix_ring][ix_coords]))
                                for ix_coords in range(len(ref_coords[ix_poly][ix_ring]))
                            ])
                        polys.append(rings)
                    new_geom = QgsGeometry.fromMultiPolygonXY(polys)
                feature = QgsFeature()
                feature.setGeometry(new_geom)
                feature.setAttributes(ft.attributes())
                result_layer.addFeature(feature, QgsFeatureSink.FastInsert)
            result_layer.commitChanges()
            transformed_layers.append(result_layer)
        return transformed_layers

    def run(self):
        try:
            _get_inter_nb_iter = \
                lambda coef_iter: int(
                    coef_iter * sqrt(len(self.src_pts)))
            self.g = Grid(self.src_pts, self.precision, self.extent)
            self.g.interpolate(self.image_pts, _get_inter_nb_iter(4))
            self.progress.emit(10)
            transformed_layers = self.get_transformed_layers()
            self.progress.emit(10)

            if self.to_display['source_grid']:
                polys = self.g._get_grid_coords('source')
                source_grid_layer = make_grid_layer(
                    polys, self.layers_to_transform[0].crs(), 'source')
            else:
                source_grid_layer = None

            if self.to_display['trans_grid']:
                polys = self.g._get_grid_coords('interp')
                trans_grid_layer = make_grid_layer(
                    polys, self.layers_to_transform[0].crs(), 'interp')
            else:
                trans_grid_layer = None

            self.resultComplete.emit(
                transformed_layers, source_grid_layer, trans_grid_layer)
            self.finished.emit()
        except Exception as e:
            self.error.emit(e, traceback.format_exc())


def make_grid_layer(polys, crs, _type_grid):
    result_layer = QgsVectorLayer(
        "Polygon?crs={}&field=ID:integer".format(crs.authid()),
        "{}_grid".format(_type_grid),
        "memory")

    result_layer.startEditing()
    result_layer.setCrs(crs)
    for ix, geom in enumerate(polys):
        new_geom = QgsGeometry.fromPolygonXY([
            [QgsPointXY(*geom[ix_ring][ix_coords])
             for ix_coords in range(len(geom[ix_ring]))]
            for ix_ring in range(len(geom))
        ])
        feature = QgsFeature()
        feature.setGeometry(new_geom)
        feature.setAttributes([QVariant(ix)])
        result_layer.addFeature(feature, QgsFeatureSink.FastInsert)
    result_layer.commitChanges()
    return result_layer

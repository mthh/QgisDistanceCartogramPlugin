#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#/***************************************************************************
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
#/***************************************************************************
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
    resultComplete = pyqtSignal(object, object, object)
    finished = pyqtSignal()
    error = pyqtSignal(Exception, str)
    progress = pyqtSignal(int)
#    status = pyqtSignal(str)

    def __init__(self, source_to_use, image_to_use, precision, max_extent, background_layer):
        QObject.__init__(self)

        self.source_to_use = source_to_use
        self.image_to_use = image_to_use
        self.precision = precision
        self.max_extent = max_extent
        self.background_layer = background_layer

    def get_transformed_layer(self):
        background_layer = self.background_layer
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
        return result_layer

    def run(self):
        try:
            _get_inter_nb_iter = \
                lambda coef_iter: int(coef_iter * sqrt(len(self.source_to_use)))
            self.g = Grid(self.source_to_use, self.precision, self.max_extent)
            self.g.interpolate(self.image_to_use, _get_inter_nb_iter(4))
            self.progress.emit(10)
            result_layer = self.get_transformed_layer()
            self.progress.emit(10)

    #        if display_source_grid:
            polys = self.g._get_grid_coords('source')
            source_grid_layer = make_grid_layer(
                polys, self.background_layer.crs(), 'source')
    #            QgsProject.instance().addMapLayer(grid_layer)

    #        if display_trans_grid:
            polys = self.g._get_grid_coords('interp')
            trans_grid_layer = make_grid_layer(
                polys, self.background_layer.crs(), 'interp')
    #            QgsProject.instance().addMapLayer(grid_layer)

            self.resultComplete.emit(
                result_layer, source_grid_layer, trans_grid_layer)
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

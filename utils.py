import numpy as np
from PyQt5.QtCore import QVariant
from .grid import Point
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsRectangle,
    QgsVectorLayer,
)


def extrapole_line(p1, p2, ratio):
    return QgsGeometry.fromWkt(
        """LINESTRING ({} {}, {} {})""".format(
            p1[0],
            p1[1],
            p1[0] + ratio * (p2[0] - p1[0]),
            p1[1] + ratio * (p2[1] - p1[1]),
        )
    )


def get_merged_extent(layers):
    extent = QgsRectangle()
    for layer in layers:
        extent.combineExtentWith(layer.extent())
    return extent


def get_total_features(layers):
    total = 0
    for layer in layers:
        total += layer.featureCount()
    return total


def extract_source_image(source_lyr, image_lyr, id_source, id_image):
    source_to_use = []
    image_to_use = []
    temp_source = []
    temp_image = {}

    for ft in source_lyr.getFeatures():
        temp_source.append(
            (ft[id_source], ft.geometry().__geo_interface__["coordinates"])
        )

    for ft in image_lyr.getFeatures():
        temp_image[ft[id_image]] = ft.geometry().__geo_interface__["coordinates"]

    for _id_source, geom_source in temp_source:
        geom_image = temp_image.get(_id_source, None)
        if not geom_image:
            continue
        source_to_use.append(Point(geom_source[0], geom_source[1]))
        image_to_use.append(Point(geom_image[0], geom_image[1]))

    return (source_to_use, image_to_use)


def create_image_points(
    source_layer,
    id_field,
    mat_extract,
    id_ref_feature,
    dest_idx,
    factor,
    display_image_points,
):
    type_id_field = [
        i.typeName().lower()
        for i in source_layer.fields().toList()
        if i.name() == id_field
    ][0]
    source_layer_dict = {}

    for ft in source_layer.getFeatures():
        id_value = str(ft[id_field])
        if id_value not in dest_idx:
            continue
        source_layer_dict[id_value] = {
            "geometry": ft.geometry(),
            "dist_euclidienne": None,
            "deplacement": None,
            "time": mat_extract[dest_idx[id_value]],
        }
    ref_geometry = source_layer_dict[id_ref_feature]["geometry"]
    for ix in source_layer_dict.keys():
        if ix == id_ref_feature:
            continue
        source_layer_dict[ix]["dist_euclidienne"] = ref_geometry.distance(
            source_layer_dict[ix]["geometry"]
        )
        source_layer_dict[ix]["vitesse"] = (
            source_layer_dict[ix]["dist_euclidienne"] / source_layer_dict[ix]["time"]
        )
    ref_vitesse = np.nanmean(
        [i["vitesse"] for i in source_layer_dict.values() if "vitesse" in i]
    )
    for ix in source_layer_dict.keys():
        if ix == id_ref_feature:
            continue
        source_layer_dict[ix]["deplacement"] = (
            ref_vitesse / source_layer_dict[ix]["vitesse"]
        )
    source_to_use, image_to_use = [], []
    unused_point = 0
    res_geoms = []
    ids = []
    image_layer = None
    coords = ref_geometry.__geo_interface__["coordinates"]
    x1, y1 = coords[0], coords[1]
    p1 = (x1, y1)
    for ix in source_layer_dict.keys():
        if ix == id_ref_feature:
            ids.append(ix)
            if display_image_points:
                res_geoms.append(ref_geometry)
            source_to_use.append(Point(x1, y1))
            image_to_use.append(Point(x1, y1))
            continue
        item = source_layer_dict[ix]
        deplacement = item["deplacement"]
        if not item["geometry"].isNull() and not item["geometry"].isEmpty():
            coords = item["geometry"].__geo_interface__["coordinates"]
            if deplacement < 1:
                deplacement = 1 + (deplacement - 1) * factor
                li = QgsGeometry.fromWkt(
                    """LINESTRING ({} {}, {} {})""".format(
                        p1[0], p1[1], coords[0], coords[1]
                    )
                )
                p = li.interpolate(deplacement * item["dist_euclidienne"])
            else:
                deplacement = 1 + (deplacement - 1) * factor
                p2 = (coords[0], coords[1])
                li = extrapole_line(p1, p2, 2 * deplacement)
                p = li.interpolate(deplacement * item["dist_euclidienne"])
            _coords = p.__geo_interface__["coordinates"]
            ids.append(ix)
            if display_image_points:
                res_geoms.append(p)
            source_to_use.append(Point(coords[0], coords[1]))
            image_to_use.append(Point(_coords[0], _coords[1]))
        else:
            unused_point += 1

    if display_image_points:
        image_layer = QgsVectorLayer(
            "Point?crs={}&field={}:{}".format(
                source_layer.crs().authid(), id_field, type_id_field
            ),
            "image_layer",
            "memory",
        )

        image_layer.startEditing()
        image_layer.setCrs(source_layer.crs())

        for ix, geom in zip(ids, res_geoms):
            feature = QgsFeature()
            feature.setGeometry(geom)
            feature.setAttributes([QVariant(ix)])
            image_layer.addFeature(feature, QgsFeatureSink.FastInsert)
        image_layer.commitChanges()

    return (source_to_use, image_to_use, image_layer, unused_point)

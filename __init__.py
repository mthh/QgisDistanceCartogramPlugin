# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DistCartogram
                                 A QGIS plugin
 Compute distance cartogram
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-07-13
        copyright            : (C) 2018 by Matthieu Viry
        email                : matthieu.viry@cnrs.fr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load DistCartogram class from file DistCartogram.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .dist_cartogram import DistCartogram
    return DistCartogram(iface)

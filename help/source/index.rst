.. DistCartogram documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DistCartogram QGIS Plugin Documentation
============================================

.. toctree::
   :maxdepth: 2

.. index:: Introduction

Introduction
=================
DistCartogram aims to create cartogram from:

* a **layer of points** and a **time matrix between them** (used to create the image point layer)
* **2 layer of related points** : the source points and the image points.

The resulting cartogram shows the local deformations (calculated using Waldo Tobler's bidimensional regression) to fit image points to source points.


The relation between the source points and the image points must depend on the studied theme: positions in access time or estimated positions in spatial cognition for example.


This kind of cartogram is often defined as a **distance cartogram**.

.. image:: img/screenshot500.png


.. index:: Data

Expected data
=================


.. image:: img/source_point_table.png

.. image:: img/matrix.png


.. index:: Examples

Examples
=================



.. index:: References

References
=================




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

## QgisDistanceCartogramPlugin


**DistanceCartogram QGIS plugin** aims to create what is often defined as a **distance cartogram**.

This is done by extending (by interpolation) to the layer(s) of the study area (territorial divisions, network...) the
local displacement between the source coordinates and the image coordinates, derived from the distances between each pair
of homologous points (source / image points).

The relation between the source points and the image points must depend on the studied theme: positions in access time or estimated positions in spatial cognition for example.

**DistanceCartogram QGIS plugin** is currently available in two languages (English and French) and allows you to create distance cartograms in two ways:

* by providing **2 layers of homologous points** : the source points and the image points,
* by providing a **layer of points** and the durations between a reference point and the other points of the layer (used to create the image points layer).


![png1](help/source/img/screenshot500.png)

![png2](help/source/img/cartogram-train.png)

Note about the method:

> This is a port of [Darcy](https://thema.univ-fcomte.fr/productions/software/darcy/) software regarding the bidimensional regression and the backgrounds layers deformation.  
All credits goes to **Waldo Tobler** *(University of California, Santa Barbara)* and **Colette Cauvin** *(Théma - Univ. Franche-Comté)* and for the reference Java implementation goes to **Gilles Vuidel** *(Théma - Univ. Franche-Comté)*.

for the contribution of the method and to *Gilles Vuidel* for the reference implementation.

## Installation

This plugin is available in the official [QGIS plugin repository](https://plugins.qgis.org/plugins/dist_cartogram/).

To install the plugin, you can use the QGIS plugin manager and simply search for `DistanceCartogram`.

## Instruction for developers

To install the plugin for development, you can clone the repository and manage the various actions with the `Makefile` provided.

Note that you need to have:
- pyqt5-dev-tools installed (`sudo apt install pyqt5-dev-tools`) to use the `pyrcc5` command,
- sphinx installed (`pip install sphinx` or `sudo apt install python3-sphinx`) to generate the documentation.

## License

[GPL-3.0](LICENSE).

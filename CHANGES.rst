Changes
=======

0.8 (2025-01-20)
----------------

- Fix the reading of the CSV durations matrix when the first cell isn't empty.

- Fix the listening of changes in the QlistWidget that allows the user to select the layer to deform.

- Improve progression of the progress bar during the cartogram creation.

- Make the main QDialog non-resizable (since the content does not resize according to the size of the QDialog).


0.7 (2025-01-08)
----------------

- Replace median with mean for computing the displacement of points for unipolar distance cartogram (from a layer of points and a duration matrix).

- Enable the deformation of multiple background layers (previously only one background layer was allowed).

- Improve wording in the README and in the documentation.


0.6 (2024-12-09)
----------------

- Fix bug in the `add` method of Rectangle2D.

- Fix links to Darcy software in README and in documentation.

- Format code with `black` + apply some `ruff` suggestions.


0.5 (2023-01-05)
----------------

- Skip points with null / empty geometry when creating layer of 'image' points
  (fixes a bug occurring when the layer of 'source' points contains empty geometries).


0.4 (2022-12-29)
-----------------

- Fixes the displacement of source point when the image point is very distant.

- Fix some numpy deprecation warning.

- Slightly change strategy for activating the OK button in the dialog.

- Use __geo_interface__ instead of asJson when extracting coordinates of source / image points.


0.3 (2022-12-26)
------------------

- Fix bug with displacement in some conditions

- Fix bug with argument of progressBar setMaximum (which expects integer value).


0.2 (2018-11-23)
------------------

- Ensure the background layer and the point layer are in the same projected CRS.

- Allow to use non-squared distance matrix as input (#3).

- Enhance the reference feature selection by sorting the list alphabetically (#4).

- Ensure the "sample dataset" dialog is put on top of the current Qgis window.


0.1 (2018-08-29)
------------------

- First Release.

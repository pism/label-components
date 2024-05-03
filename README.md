Python (Cython) module implementing the serial connected component labeling algorithm used in PISM to identify "icebergs", label shelves in PICO, etc.

Run

```
python3 setup.py build_ext --inplace
```
to build in place.

Unlike PISM's version, this code uses `short int` instead of `double` arrays to speed it up. See `pism_label_components.label()`.

In addition to this, it also contains the helper function `pism_label_components.update_max_depth()` that (together with `label()`) can be used to estimate "ocean access depths" as in

> L. Nicola, R. Reese, M. Kreuzer, T. Albrecht, and R. Winkelmann, "Oceanic gateways to Antarctic grounding lines – Impact of critical access depths on sub-shelf melt," EGUsphere, vol. 2023, pp. 1–30, 2023, doi: 10.5194/egusphere-2023-2583.

See `max_depth.py`. The function `update_max_depth()` would be just as
easy to write in Python, but this version (in Cython) is significantly
faster.

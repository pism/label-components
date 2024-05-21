Python (Cython) module implementing the _serial_ connected component labeling (CCL) algorithm used in PISM. In addition to _labeling_ connected components, our implementation can perform one kind of connected component _analysis_ (CCA) needed to identify icebergs, lakes, areas connected to the open ocean, etc.

The method implemented here is very similar to the one in _He et al, 2010_, but using 4-connectivity.[^1]

``` 
@Article{He2010,
  author    = {He, Lifeng and Chao, Yuyan and Suzuki, Kenji},
  journal   = {International Journal of Pattern Recognition and Artificial Intelligence},
  title     = {A run-based one-and-a-half-scan connected-component labeling algorithm},
  year      = {2010},
  month     = {jun},
  number    = {04},
  pages     = {557--579},
  volume    = {24},
  doi       = {10.1142/s0218001410008032},
  publisher = {World Scientific},
}
```

Given a threshold `A`, all pixels with values greater than `A` are interpreted as "foreground" pixels.

For a pixel `p(row,col)`, the four pixels `p(row-1,col)`, `p(row+1,col)`, `p(row,col-1)`, `p(row,col+1)` are called 4-neighbors of `p(row,col)`. Two foreground pixels `u` and `v` are 4-connected if there is a sequence of foreground pixels `p[0] = u, ..., p[i], p[i+1], ..., p[n] = v` such that `p[i+1]` is a 4-neighbor of `p[i]` for all `i`.

A 4-connected component is the maximum set of foreground pixels such that any two pixels in the set are 4-connected.

This implementation has two modes:

1. Given a threshold `A` and defining "foreground" pixels accordingly, assign unique consecutive integer labels to all 4-connected components in the input.

2. Given thresholds `A` and `B` (`A < B`), define "foreground" pixels accordingly. Let a foreground pixel be "marked" if its value is greater than `B`. Label all foreground pixels *not* 4-connected to a "marked" pixel with `1`, the rest with `0`.

Run

```
python3 setup.py build_ext --inplace
```
to build this module "in place."

Unlike PISM's version, this code uses `short int` instead of `double` arrays to speed it up. See `pism_label_components.label()`.

In addition to this, it also contains the helper function `pism_label_components.update_max_depth()` that (together with `label()`) can be used to estimate "ocean access depths" as in

> L. Nicola, R. Reese, M. Kreuzer, T. Albrecht, and R. Winkelmann, "Oceanic gateways to Antarctic grounding lines – Impact of critical access depths on sub-shelf melt," EGUsphere, vol. 2023, pp. 1–30, 2023, doi: 10.5194/egusphere-2023-2583.

See `max_depth.py`. The function `update_max_depth()` would be just as easy to write in Python, but this version (in Cython) is significantly faster.

[^1]: There are so many variations of CCL algorithms that it's hard to find a citation that is a perfect fit.

# cython: language_level=3, embedsignature=True
# distutils: language = c++

import numpy as np

from decl cimport label as cxx_label
from decl cimport update_max_depth as cxx_update_max_depth

def label(input_array, mark_isolated_components, foreground_threshold, attached_threshold, output_array):
    """Label connected components in `input_array` (array of `short` integers).

    In `input_array`, areas where `input_array > foreground_threshold`
    are "foreground" pixels that make up components to isolate. If
    `mark_isolated_components` is `false`, each component gets a
    unique label (an integer).

    If `mark_isolated_components` is true, components *not* reachable
    from areas satisfying `input_array > attached_threshold` are
    labeled with `1`, the rest with `0`.

    Does *not* modify background pixels in `output_array`.
    """
    cdef int nrows = input_array.shape[0]
    cdef int ncols = input_array.shape[1]
    cdef short [:,::1] data = input_array
    cdef short [:,::1] data_out = output_array

    cxx_label(&data[0,0], nrows, ncols, mark_isolated_components, foreground_threshold, attached_threshold, &data_out[0,0])

def update_max_depth(depth, mask, current_depth, max_depth):
    """Update `max_depth`.

    Each call sets `max_depth = max(max_depth, current_depth)` in all
    areas where `depth > current_depth` and reachable from the "deep
    ocean" according to `mask`.
    """
    cdef int nrows = depth.shape[0]
    cdef int ncols = depth.shape[1]

    cdef short [:,::1] depth_ = depth
    cdef short [:,::1] mask_ = mask
    cdef short [:,::1] max_depth_ = max_depth

    cxx_update_max_depth(&depth_[0,0], &mask_[0,0], nrows, ncols, current_depth, &max_depth_[0,0])

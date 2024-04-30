from libcpp cimport bool

cdef extern from "src/label_components.cc":
    void label(short *input_array, int nrows, int ncols, bool mark_isolated_components, short foreground_threshold, short attached_threshold, short *output_array)

    void update_max_depth(short *depth_, short *mask_, int nrows, int ncols, short depth_threshold, short *output_array)

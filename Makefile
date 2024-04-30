all: module

module: pism_label_components.pyx src/label_components_impl.hh src/label_components.cc
	CFLAGS="-O3 -march=native -mtune=native" python3 setup.py build_ext --inplace

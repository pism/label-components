all: module

module: pism_label_components.pyx src/label_components_impl.hh src/label_components.cc
	python3 setup.py build_ext --inplace

clean:
	python3 setup.py clean --all

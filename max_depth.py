#!/usr/bin/env python3

"""Estimate "access depths" for all locations below the sea level
using a gridded bed topography (bathymetry) dataset such as
BedMachineAntarctica-v3.nc or BedMachineGreenland-v5.nc.

See the preprint

L. Nicola, R. Reese, M. Kreuzer, T. Albrecht, and R. Winkelmann,
"Oceanic gateways to Antarctic grounding lines – Impact of critical
access depths on sub-shelf melt," EGUsphere, vol. 2023, pp. 1–30,
2023, doi: 10.5194/egusphere-2023-2583.
"""

from pism_label_components import label, update_max_depth
import netCDF4
import numpy as np
import sys

dtype=np.int16

def find_max_depth(depth, depth_thresholds, open_ocean_depth):

    max_depth = np.zeros_like(depth, dtype=dtype)
    max_depth[:] = -1
    mask = np.zeros_like(depth, dtype=dtype)

    for D in depth_thresholds:
        sys.stderr.write(f"Processing depth {D}...\n")

        mask[:] = 0
        label(depth, True, D, open_ocean_depth, mask)
        update_max_depth(depth, mask, D, max_depth)

    return max_depth

def prepare_output(input_filename, output_filename):
    df = netCDF4.Dataset(input_filename, "r")
    out = netCDF4.Dataset(output_filename, "w")

    out.createDimension("x", len(df.dimensions["x"]))
    out.createDimension("y", len(df.dimensions["y"]))

    x = out.createVariable("x", datatype=np.float64, dimensions=("x",))
    y = out.createVariable("y", datatype=np.float64, dimensions=("y",))
    max_depth = out.createVariable("max_depth", datatype=dtype, dimensions=("y", "x"), complevel=9)

    x[:] = df.variables["x"][:]
    y[:] = df.variables["y"][:]

    return out

if __name__ == "__main__":

    if len(sys.argv) == 3:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    elif len(sys.argv) == 2:
        input_filename = sys.argv[1]
        output_filename = "max_depth.nc"
    else:
        input_filename = "BedMachineAntarctica-v3.nc"
        output_filename = "max_depth.nc"

    sys.stderr.write(f"Reading from {input_filename}...\n")
    dataset = netCDF4.Dataset(input_filename)
    bed = dataset.variables["bed"][:]
    dataset.close()
    sys.stderr.write(f"Done.\n")

    depth = -1 * np.array(bed, dtype=dtype)
    del bed

    # Depth of the "open ocean" used to identify whether an area below
    # a certain depth threshold has a connection to the open ocean.
    # Should be a) greater than the deepest depression in the interior
    # of Antarctica or Greenland, but small enough so that there
    # `depth > open_ocean_depth` is true somewhere on the grid.
    open_ocean_depth = 4000

    # Vertical resolution (currently: one meter). This implementation
    # uses 16 bit integers to represent ocean depth, so this is the
    # highest resolution achievable without scaling the input depth
    step = 1

    # Number of vertical steps (iterations) to use. Should be large
    # enough so `step * n_steps` is greater than the depth of the deepest
    # depression in the interior.
    n_steps = 4000

    assert open_ocean_depth >= n_steps * step
    assert np.any(depth > open_ocean_depth)

    depth_thresholds = np.linspace(0, step * n_steps, n_steps + 1)

    import time
    start = time.time()
    max_depth = find_max_depth(depth, depth_thresholds, open_ocean_depth)
    end = time.time()

    print(f"Doing {n_steps} steps took {end - start} seconds. Average: {(end - start) / n_steps}")

    dataset = prepare_output(input_filename, output_filename)
    dataset.variables["max_depth"][:] = max_depth
    dataset.close()

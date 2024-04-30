/* Copyright (C) 2019, 2020, 2021, 2022, 2023, 2024 PISM Authors
 *
 * This file is part of PISM.
 *
 * PISM is free software; you can redistribute it and/or modify it under the
 * terms of the GNU General Public License as published by the Free Software
 * Foundation; either version 3 of the License, or (at your option) any later
 * version.
 *
 * PISM is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License
 * along with PISM; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

#include "label_components_impl.hh"

using data_t = short;

using array_t = connected_components::details::CArray<data_t>;
using array_label_t = connected_components::details::CArray<data_t>;

/*!
 * Label connected components in `input_array` (array of size `nrows * ncols`).
 *
 * In `input_array`, areas where `input_array > foreground_threshold`
 * are "foreground" pixels that make up components to isolate. If
 * `mark_isolated_components` is `false`, each component gets a unique
 * label (an integer).
 *
 * If `mark_isolated_components` is true, components *not* reachable
 * from areas satisfying `input_array > attached_threshold` are
 * labeled with `1`, the rest with `0`.
 *
 * Does *not* modify background pixels in `output_array`.
 */
void label(data_t *input_array, int nrows, int ncols, bool mark_isolated_components,
           data_t foreground_threshold, data_t attached_threshold, data_t *output_array) {
  using mask = connected_components::details::Mask<array_t>;

  array_t input(input_array, nrows, ncols);
  array_label_t output(output_array, nrows, ncols);

  int min_label = 1;
  label(mask(input, foreground_threshold, attached_threshold),
        mark_isolated_components, min_label, output);
}

/*!
 * Update `max_depth_`.
 *
 * Each call sets `max_depth = max(max_depth, current_depth)` in all
 * areas where `depth > current_depth` and reachable from the "deep
 * ocean" according to `mask_`.
 *
 * @param[in] depth_ ocean depth
 * @param[in] mask_ mask identifying areas *not* reachable from the deep ocean depth
 * @param[in] nrows number of rows in `depth_` and `mask_`
 * @param[in] ncols number of columns in `depth_` and `mask_`
 * @param[in] current_depth current depth
 * @param[in,out] max_depth_ maximum depth (input-output)
 */
void update_max_depth(data_t *depth_, data_t *mask_, int nrows, int ncols,
                      data_t current_depth, data_t *max_depth_) {

  array_t depth(depth_, nrows, ncols);
  array_label_t isolated(mask_, nrows, ncols);

  array_t max_depth(max_depth_, nrows, ncols);

  for (int r = 0; r < nrows; ++r) {
    for (int c = 0; c < ncols; ++c) {
      bool reachable = (depth(r, c) > current_depth) and (isolated(r, c) == 0);
      if (reachable) {
        max_depth(r, c) = std::max(max_depth(r, c), current_depth);
      }
    }
  }
}

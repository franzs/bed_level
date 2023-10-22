#!/usr/bin/env python

import numpy as np
import os
import pickle

import bed_level

with open(os.path.join(bed_level.OBJS_DIR, 'objects.pickle'), 'rb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    objects = pickle.load(f)

mean_values = objects['mean_values']

print("G28 ; Auto Home")

for iy, ix in np.ndindex(mean_values.shape):
    print(f"G29 W I{ix} J{iy} Z{mean_values[iy, ix]:.05f}")

#!/usr/bin/env python

import numpy as np
import os
import pickle
import plotly.graph_objects as go

import bed_level

with open(os.path.join(bed_level.OBJS_DIR, 'objects.pickle'), 'rb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    objects = pickle.load(f)

positions = objects['positions']
min_values = objects['min_values']
max_values = objects['max_values']
mean_values = objects['mean_values']
std_dev_values = objects['std_dev_values']

# Generate x, y, and z coordinates for the 3D surface plot
x_coords = np.arange(positions.shape[0])
y_coords = np.arange(positions.shape[1])
x, y = np.meshgrid(x_coords, y_coords)

# Create 3D surface plots for minimum, maximum, mean, and standard deviation
min_surface = go.Surface(x=x, y=y, z=min_values, name='Minimum')
max_surface = go.Surface(x=x, y=y, z=max_values, name='Maximum')
mean_surface = go.Surface(x=x, y=y, z=mean_values, name='Mean')
std_dev_surface = go.Surface(x=x, y=y, z=std_dev_values, name='Standard Deviation')

# Create the figure and add surfaces to it
#fig = go.Figure(data=[min_surface, max_surface, mean_surface])
fig = go.Figure(data=[std_dev_surface])

# Set plot layout and labels
fig.update_layout(
    scene=dict(
        xaxis_title='Position',
        yaxis_title='Row',
        zaxis_title='Value',
    ),
    title='3D Surface Plot with Mean and Standard Deviation',
)

# Show the plot
fig.show()

#!/usr/bin/env python

import numpy as np
import os
import pickle

import bed_level


# Function to parse input data from a file and return a NumPy array
def parse_file(file_path):
    data_list = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        # Skip first four lines
        if idx >= 4:
            # Split the line by whitespace and parse numbers (starting with the second element)
            values = [float(val) for val in line.split()[1:]]
            data_list.append(values)

    return np.array(data_list)


def main():
    parsed_arrays = []

    data_dir = bed_level.data_dir()

    for file_path in os.listdir(data_dir):
        parsed_array = parse_file(os.path.join(data_dir, file_path))
        parsed_arrays.append(parsed_array)

    positions = np.array(parsed_arrays).transpose(1, 2, 0)
    min_values = np.min(positions, axis=2)
    max_values = np.max(positions, axis=2)
    mean_values = np.mean(positions, axis=2)
    std_dev_values = np.std(positions, axis=2)

    print("Minimum: ")
    print(min_values)

    print("\nMaximum: ")
    print(max_values)

    print("\nMean: ")
    print(mean_values.round(4))

    print("\nStandard deviation: ")
    print(std_dev_values.round(4))

    objects = {
        'positions': positions,
        'min_values': min_values,
        'max_values': max_values,
        'mean_values': mean_values,
        'std_dev_values': std_dev_values,
    }

    if not os.path.exists(bed_level.OBJS_DIR):
        os.mkdir(bed_level.OBJS_DIR)

    with open(os.path.join(bed_level.OBJS_DIR, 'objects.pickle'), 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()

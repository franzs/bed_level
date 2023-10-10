# Collect and analyze bed level data from 3D printers

## Introduction

This is a collection of Python scripts for collecting and analyzing bed level data from 3D printers using automatic bed leveling (ABL). As a result, the analysis shows how accurate the ABL is. Inaccurate results may indicate mechanical problems with a 3D printer.

## Usage

To use the scripts, first install the required Python packages:

```bash
pip install -r requirements.txt
```

If you prefer a [virtual environment](https://virtualenvwrapper.readthedocs.io//) use something like:

```bash
mkvirtualenv bed_level -r requirements.txt
```

Have a look at the values in [`bed_level.py`](./bed_level.py). Set `PRINTER_BRAND` and `PRINTER_MODEL` to match your printer and generate a unique id using `uuidgen` for `PRINTER_UUID`. Find your device name to which your printer is connected for `SERIAL_DEVICE`. `/dev/ttyUSB0` is the first connected USB device on Linux. At least three runs should be made - the more the better. The GCODE settings should work for most printers using [Marlin Firmware](https://marlinfw.org/).

### Collect bed level data

To collect the bed level data just run:

```bash
./get_level_data.py
```

I use a Raspberry Pi used for [OctoPrint](https://octoprint.org/) for collecting the bed level data. Make sure to disconnect the printer from OctoPrint first.

The collected data is written to `./data/{PRINTER_BRAND}/{PRINTER_MODEL}/{PRINTER_UUID}/level_data_{nn}.txt`. If you run `get_level_data.py` multiple times the old collected data is preserved.

### Parse bed level data

This step is used for parsing the bed level data and converting it from ASCII input to Python objects. Subsequent steps can then utilize the data more conveniently.

```bash
./parse_level_data.py
```

For a first insight `parse_level_data.py` prints the minimum, the maximum, the mean and the standard deviation for each position in the bed level grid.

### Plot bed level data

To visualize the minimum, the maximum, the mean and the standard deviation as a 3D surface using [Plotly](https://plotly.com/python/) call:

```bash
./plot_level_data.py
```

### Generate GCODE for new level data

Generate GCODE for setting the bed level grid:

```bash
./gcode_level_data.py
```

By default, it calculates the mean values of the collected bed level data.

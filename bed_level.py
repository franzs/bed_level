import os

PRINTER_BRAND = 'Elegoo'
PRINTER_MODEL = 'Neptune 3 Pro'
PRINTER_UUID = '768345e9-a305-41c2-81e0-efda30a9dfda'  # generate with uuidgen

SERIAL_DEVICE = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 115200

NUM_RUNS = 3

START_GCODE = """
M140 S60  ; starting by heating the bed for nominal mesh accuracy
M104 S140 ; set hotend temperature
G28       ; home all axes
M109 S140 ; waiting until the hot end is fully warmed up
M190 S60  ; waiting until the bed is fully warmed up
"""

BED_LEVEL_GCODE = """
M420 S0   ; Turning off bed leveling while probing, if firmware is set to restore after G28
G29 V4    ; Level the bed and report results #NO_PROC#
"""

END_GCODE = """
M140 S0  ; turn off bed heating
M104 S0  ; turn off hotend
G91      ; relative positioning
G1 Z50   ; move z axis up by 50 mm
"""

DATA_DIR = 'data'
OBJS_DIR = 'objs'


def data_dir():
    return os.path.join(DATA_DIR, PRINTER_BRAND, PRINTER_MODEL, PRINTER_UUID)

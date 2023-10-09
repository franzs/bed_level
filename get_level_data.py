#!/usr/bin/env python

import os
import serial
import time

import constants

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

OK_STRING = 'ok\n'
PROCESSING_STRING = 'echo:busy: processing\n'

output_file_template = os.path.join(constants.DATA_DIR, 'level_data_{output_file_index:02d}.txt')


def send_commands(ser, commands):
    output_lines = []

    for command in commands.split('\n'):
        if command != '':
            output_lines += send_command(ser, command)

    return output_lines


def send_command(ser, command):
    print(f'-> {command}')

    ser.write(str.encode(command + '\r\n'))
    time.sleep(1)

    output_lines = []

    while True:
        line = ser.readline()

        decoded_line = line.decode('utf-8')

        # skip temperature reporting
        if not decoded_line.startswith(' T:'):
            if command.find('#NO_PROC#') == -1 or not decoded_line == PROCESSING_STRING:
                print('<- ' + decoded_line, end='')

        if not decoded_line == PROCESSING_STRING and not decoded_line.startswith(' T:') and decoded_line != OK_STRING:
            output_lines.append(decoded_line.rstrip())

        if decoded_line == OK_STRING:
            break

    return output_lines


def main():
    if not os.path.exists(constants.DATA_DIR):
        os.mkdir(constants.DATA_DIR)

    ser = serial.Serial(SERIAL_DEVICE, SERIAL_BAUDRATE)
    time.sleep(2)

    send_commands(ser, START_GCODE)

    output_file_index = 0

    while True:
        if os.path.exists(output_file_template.format(output_file_index=output_file_index)):
            output_file_index += 1
        else:
            break

    for i in range(0, NUM_RUNS):
        output_lines = send_commands(ser, BED_LEVEL_GCODE)

        level_data = []
        is_level_data = False

        for output_line in output_lines:
            if output_line == 'Bilinear Leveling Grid:':
                is_level_data = True

            if is_level_data is True and output_line == '':
                break

            if is_level_data:
                level_data.append(output_line)

        with open(output_file_template.format(output_file_index=output_file_index), 'w') as file:
            for line in level_data:
                file.write(line + '\n')

            output_file_index += 1

    send_commands(ser, END_GCODE)

    time.sleep(2)
    ser.close()


if __name__ == "__main__":
    main()

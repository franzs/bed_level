#!/usr/bin/env python

import os
import serial
import time

import constants

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

    ser = serial.Serial(constants.SERIAL_DEVICE, constants.SERIAL_BAUDRATE)
    time.sleep(2)

    send_commands(ser, constants.START_GCODE)

    output_file_index = 0

    while True:
        if os.path.exists(output_file_template.format(output_file_index=output_file_index)):
            output_file_index += 1
        else:
            break

    for i in range(0, constants.NUM_RUNS):
        output_lines = send_commands(ser, constants.BED_LEVEL_GCODE)

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

    send_commands(ser, constants.END_GCODE)

    time.sleep(2)
    ser.close()


if __name__ == "__main__":
    main()

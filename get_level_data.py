#!/usr/bin/env python

import os
import serial
import time

import bed_level

OK_STRING = 'ok\n'
PROCESSING_STRING = 'echo:busy: processing\n'

output_file_template = os.path.join(bed_level.DATA_DIR, 'level_data_{output_file_index:02d}.txt')


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
    if not os.path.exists(bed_level.DATA_DIR):
        os.mkdir(bed_level.DATA_DIR)

    ser = serial.Serial(bed_level.SERIAL_DEVICE, bed_level.SERIAL_BAUDRATE)
    time.sleep(2)

    firmware_version = send_command(ser, "M115")[0]

    send_commands(ser, bed_level.START_GCODE)

    output_file_index = 0

    while True:
        if os.path.exists(output_file_template.format(output_file_index=output_file_index)):
            output_file_index += 1
        else:
            break

    for i in range(0, bed_level.NUM_RUNS):
        output_lines = send_commands(ser, bed_level.BED_LEVEL_GCODE)

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
            file.write(f'# Brand: {bed_level.PRINTER_BRAND}, Model: {bed_level.PRINTER_MODEL}, UUID: {bed_level.PRINTER_UUID}\n')
            file.write(f'# {firmware_version}\n')
            for line in level_data:
                file.write(line + '\n')

            output_file_index += 1

    send_commands(ser, bed_level.END_GCODE)

    time.sleep(2)
    ser.close()


if __name__ == "__main__":
    main()

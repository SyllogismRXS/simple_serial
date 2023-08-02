#!/usr/bin/env python3

import serial
import argparse
from time import sleep

def parse_response(response):
    return response.strip().decode("utf-8")

def send_command(ser, user_cmd, tx_eol, show_hidden_rx_chars):
    cmd = user_cmd.encode('utf-8') + tx_eol.encode('utf-8')
    ser.write(cmd)

    sleep(1.0)

    if show_hidden_rx_chars:
        return ser.readline()
    else:
        return parse_response(ser.readline())

def main():
    parser = argparse.ArgumentParser(description='Simple Serial')
    parser.add_argument('device', type=str, help='Serial device')
    parser.add_argument('-b', '--baudrate', type=int, default=115200, help='Baud rate')
    parser.add_argument('--tx_eol', default='\n', help='Transmit end-of-line character sequence.')
    parser.add_argument('--rx_timeout', default=1, type=int, help='Rx timeout')
    parser.add_argument('-s', '--show_hidden_rx_chars', action='store_true', help='Show hidden received characters (e.g., new lines, carriage returns, etc.')
    args = parser.parse_args()

    ser = serial.Serial(args.device, baudrate=args.baudrate,
                        bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, timeout=args.rx_timeout)

    try:
        while True:
            cmd = input('>> ')
            response = send_command(ser, cmd, args.tx_eol, args.show_hidden_rx_chars)
            if len(response) == 0:
                print('Warning: No response.')
            else:
                print('Response: %s' % response)
    except KeyboardInterrupt:
        print('Keyboard interrupt. Closing serial connection.')

    ser.close()


if __name__ == '__main__':
    main()

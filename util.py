import re
import sys
import argparse

# Regex patterns for timestamps and IPs
TIMESTAMP_PATTERN = r'\b\d{2}:\d{2}:\d{2}\b'
IPV4_PATTERN = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
IPV6_PATTERN = r'\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'

def highlight_ip(line, pattern, ip_type):
    return re.sub(pattern, lambda x: f"\033[93m{x.group(0)}\033[0m", line)

def parse_log(options, file):
    with open(file, 'r') if file != '-' else sys.stdin as f:
        lines = f.readlines()
        
        if options.first is not None:
            lines = lines[:options.first]
        if options.last is not None:
            lines = lines[-options.last:]
        
        result_lines = []
        for line in lines:
            if options.timestamps and re.search(TIMESTAMP_PATTERN, line):
                result_lines.append(line)
            elif options.ipv4 and re.search(IPV4_PATTERN, line):
                result_lines.append(highlight_ip(line, IPV4_PATTERN, 'ipv4'))
            elif options.ipv6 and re.search(IPV6_PATTERN, line):
                result_lines.append(highlight_ip(line, IPV6_PATTERN, 'ipv6'))
            elif not options.timestamps and not options.ipv4 and not options.ipv6:
                result_lines.append(line)

        return result_lines

def print_help():
    help_text = """
Usage: ./util.py [OPTION]... [FILE]

Supported options:
---------------------
  -h, --help         Print help
  -f, --first=NUM    Print first NUM lines
  -l, --last=NUM     Print last NUM lines
  -t, --timestamps   Print lines that contain a timestamp in HH:MM:SS format
  -i, --ipv4         Print lines that contain an IPv4 address, matching IPs
                     are highlighted
  -I, --ipv6         Print lines that contain an IPv6 address (standard
                     notation), matching IPs are highlighted

If FILE is omitted, standard input is used instead.
If multiple options are used at once, the result is the intersection of their
results.
The result (matching lines) is printed to standard output.
"""
    print(help_text)

def main():
    parser = argparse.ArgumentParser(description='Log parser utility')
    parser.add_argument('file', nargs='?', default='-', help='Log file to process (default: stdin)')
    parser.add_argument('-f', '--first', type=int, help='Print first NUM lines')
    parser.add_argument('-l', '--last', type=int, help='Print last NUM lines')
    parser.add_argument('-t', '--timestamps', action='store_true', help='Print lines containing timestamp')
    parser.add_argument('-i', '--ipv4', action='store_true', help='Print lines containing IPv4 address')
    parser.add_argument('-I', '--ipv6', action='store_true', help='Print lines containing IPv6 address')

    args = parser.parse_args()
    result_lines = parse_log(args, args.file)
    for line in result_lines:
        print(line, end='')

if __name__ == '__main__':
    main()

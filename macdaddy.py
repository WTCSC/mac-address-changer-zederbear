import sys
import os
import subprocess
import random
import argparse
import textwrap
import re

# Define the custom description text
description_text = textwrap.dedent('''\
                                                             Usage: python3 macdaddy.py [-i <eth0|eth1|...>] [-a <mac-address>] [-r] [-u]
                                                                Examples:
                                                                    python3 macdaddy.py -i   eth0 -r
                                                                    python3 macdaddy.py -i enp0s3 -a 97:1a:d9:aa:a6:fd
                                                                    python3 macdaddy.py -i  wlan1 -u
                                                             
                                                                Options:
                                                                    -h, --help             Shows this message          (Not required)
                                                                    -i, --interface        Network interface           (Always required)
                                                                    -a, --address          Mac Address                 (Required unless using -r or -u)
                                                                    -r, --randomize        Randomizes your mac address (Not required)
                                                                    -u, --undo             Resets your mac address     (Not required)
                                                             ''')

# Initialize the ArgumentParser with add_help=False to disable default help
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description_text,
    add_help=False  # Disable the default help message
)

PERMANENT_ADDRESS_FILE=""

# Add a custom help argument
parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")

# Define other arguments
parser.add_argument("-i", "--interface", help="Interface for network traffic")
parser.add_argument("-a", "--address", help="MAC address")
parser.add_argument("-r", "--randomize", help="Randomizes your MAC address", action="store_true")
parser.add_argument("-u", "--undo", help="Resets your MAC address", action="store_true")

# Parse arguments
args = parser.parse_args()

# Handle the custom help option
if args.help:
    print(description_text)  # Print only the custom description
    sys.exit(0)  # Exit after printing the help message

if not args.help and not args.interface: # Force you to use interface
    parser.error("The -i/--interface option is required.")

if not args.randomize and not args.undo and not args.address and not args.help: # Force you to use one of these three options, you cannot use just i
    parser.error("Address must be included if randomize and undo are not included")

def save_perm_address(iface):
    PERMANENT_ADDRESS_FILE = f'/tmp/{iface}_perm_mac.txt'
    if not os.path.exists(PERMANENT_ADDRESS_FILE):
        mac = open(f'/sys/class/net/{iface}/address', 'r')
        maca = mac.read()
        with open(PERMANENT_ADDRESS_FILE, 'w') as f:
            f.write(maca)
        mac.close()

def reset_address(iface):
    PERMANENT_ADDRESS_FILE = f'/tmp/{iface}_perm_mac.txt'
    if not os.path.exists(PERMANENT_ADDRESS_FILE):
        print("File not found")
        sys.exit(1)
    PERM_ADDRESS = ""
    with open(PERMANENT_ADDRESS_FILE, 'r') as f:
        PERM_ADDRESS=f.read()
    subprocess.run(['sudo', 'ifconfig', iface, 'down'])
    subprocess.run(['sudo', 'ifconfig', iface, 'hw', 'ether', PERM_ADDRESS])
    subprocess.run(['sudo', 'ifconfig', iface, 'up'])
    os.remove(PERMANENT_ADDRESS_FILE)

def random_mac_address():
    first_byte = random.randint(0, 255)
    first_byte = (first_byte & 0xFC) | 0x02  # e.g. 0bxxxxxx10 in binary
    rest_bytes = [random.randint(0, 255) for _ in range(5)]

    mac_bytes = [first_byte] + rest_bytes
    return ':'.join(f"{b:02x}" for b in mac_bytes)

def verify_mac_address(mac_address):
    return bool(re.search(r"^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$", mac_address()))

save_perm_address(args.interface)
if args.randomize:
    subprocess.run(['sudo', 'ifconfig', args.interface, 'down'])
    subprocess.run(['sudo', 'ifconfig', args.interface, 'hw', 'ether', random_mac_address()])
    subprocess.run(['sudo', 'ifconfig', args.interface, 'up'])
elif args.undo:
    reset_address(args.interface)
else:
    subprocess.run(['sudo', 'ifconfig', args.interface, 'down'])
    subprocess.run(['sudo', 'ifconfig', args.interface, 'hw', 'ether', args.address])
    subprocess.run(['sudo', 'ifconfig', args.interface, 'up'])

new_mac_address = open(f'/sys/class/net/{args.interface}/address', 'r').read()
try:
    perm_address = open(f'/tmp/{args.interface}_perm_mac.txt').read()
except:
    perm_address = None
print(f"New MAC address: {new_mac_address}")
if perm_address:
    print(f"Permanent MAC address: {perm_address}")
else:
    print("No permanent address file")
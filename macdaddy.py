import sys
import argparse
import textwrap

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,  # Use only one formatter_class
    description=textwrap.dedent('''\
                                                             Usage: ./macdaddy.sh [-i <eth0|eth1|...>] [-a <mac-address>] [-r] [-u]
                                                                Examples:
                                                                    ./macdaddy.sh -i   eth0 -r
                                                                    ./macdaddy.sh -i enp0s3 -a 97:1a:d9:aa:a6:fd
                                                                    ./macdaddy.sh -i  wlan1 -u
                                                             
                                                                Options:
                                                                    -h, --help             Shows this message          (Not required)
                                                                    -i, --interface        Network interface           (Always required)
                                                                    -a, --address          Mac Address                 (Required unless using -r or -u)
                                                                    -r, --randomize        Randomizes your mac address (Not required)
                                                                    -u, --undo             Resets your mac address     (Not required)
                                                             '''),
    add_help=False
)

# Add your custom usage function (optional)
def usage():
    print("Custom usage message.")
    sys.exit(1)

# Define arguments
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="Show this help message and exit")
parser.add_argument("-i", "--interface", help="Interface for network traffic", required=True)
parser.add_argument("-a", "--address", help="MAC address")
parser.add_argument("-r", "--randomize", help="Randomizes your MAC address", action="store_true")
parser.add_argument("-u", "--undo", help="Resets your MAC address", action="store_true")

# Parse arguments
args = parser.parse_args()
print(vars(args))

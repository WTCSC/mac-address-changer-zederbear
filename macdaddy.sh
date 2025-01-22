#!/bin/bash
PERMANENT_ADDRESS_FILE=""

usage() { echo "Usage: $0 [-i <eth0|eth1|...>] [-a <mac-address>] [-r] [-u]"
echo "Example: $0 -i eth0 -a 00:00:00:00:00:00 -r "
echo "Example: $0 -i eth0 -a 97:1a:d9:aa:a6:fd"
echo "-i = interface name"
echo "-a = mac address"
echo "-r = randomize the MAC address" 
echo "-u = undo mac-address change (back to original mac address)"
echo "If you want to get a random mac-address put -a as 00:00:00:00:00:00" 1>&2; exit 1; }

save_perm_address() {
    local iface="$1"
    PERMANENT_ADDRESS_FILE="/tmp/${iface}_perm_mac.txt"
    if [ ! -f $PERMANENT_ADDRESS_FILE ]; then
        cat "/sys/class/net/${iface}/address" > "$PERMANENT_ADDRESS_FILE"
    fi
}

get_mac_address_on_network() {
    local iface="$1"
    SUBNET=$(ip -o -f inet addr show dev "$iface" | awk '{print $4}')

    sudo arp-scan --interface="$iface" "$SUBNET" 2>/dev/null \
    | awk '/([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}/ {print $1, $2}' \
    | while read -r ip mac; do
        vendor="$(curl -s "https://api.macvendors.com/$mac")"
        echo "$ip   $mac   ${vendor:-UNKNOWN}"
    done
    exit 0
}

reset_address() {
    local iface="$1"
    PERMANENT_ADDRESS_FILE="/tmp/${iface}_perm_mac.txt"
    if [ ! -f "$PERMANENT_ADDRESS_FILE" ]; then
        echo "File not found"
        exit 1
    fi
    local PERM_ADDRESS
    PERM_ADDRESS=$(cat $PERMANENT_ADDRESS_FILE)
    sudo ifconfig "$iface" down || { echo "failed to bring interface down"; exit 1; }
    sudo ifconfig "$iface" hw ether $PERM_ADDRESS || { echo "failed to reset mac address"; exit 1; }
    sudo ifconfig "$iface" up || { echo "failed to bring interface up"; exit 1; }
    rm $PERMANENT_ADDRESS_FILE
}

random_mac_address() {
    first_byte=$(printf '%02x' $(( (RANDOM % 256) & 0xFE | 0x02 )))
    echo "$first_byte:$(printf '%02x' $((RANDOM % 256))):$(printf '%02x' $((RANDOM % 256))):$(printf '%02x' $((RANDOM % 256))):$(printf '%02x' $((RANDOM % 256))):$(printf '%02x' $((RANDOM % 256)))"
}


verify_mac_address() {
    echo "${1}" | grep -E "^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$" >/dev/null 2>&1
}

while getopts ":i:a:rug" o; do
    case "${o}" in
        i)
            i=${OPTARG}
            ;;
        a)
            a=${OPTARG}
            if ! verify_mac_address "${a}"; then
                echo Error: "${a}" is not a valid MAC address
                usage
            fi
            ;;
        r)
            r=true
            ;;
        u)
            u=true
            ;;
        g)
            g=true
            ;;
        *) 
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${i}" ]; then
    usage
fi

if [ "$g" != true ] && [ "$u" != true ] && [ "$r" != true ]; then
    if [ -z "$a" ]; then
        usage
    fi
fi

save_perm_address "${i}"
if [ "$r" = true ]; then
    sudo ifconfig "${i}" down
    sudo ifconfig "${i}" hw ether "$(random_mac_address)"
    sudo ifconfig "${i}" up
elif [ "$g" = true ]; then
    get_mac_address_on_network ${i}
elif [ "$u" = true ]; then
    reset_address "${i}"
else
    sudo ifconfig "${i}" down
    sudo ifconfig "${i}" hw ether "${a}"
    sudo ifconfig "${i}" up
fi

echo "i = ${i}"
echo "a = ${a}"


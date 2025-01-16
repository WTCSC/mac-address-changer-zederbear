#!/bin/bash

usage() { echo "Usage: $0 [-i <eth0|eth1|...>] [-a <mac-address>]" 1>&2; exit 1; }

verify_mac_address() {
    echo "${1}" | grep -E "^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$" >/dev/null 2>&1
}

while getopts ":i:a:" o; do
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
        *) 
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${i}" ] ||  [ -z "${a}" ]; then
    usage
fi


sudo ifconfig "${i}" down
sudo ifconfig "${i}" hw ether "${a}"
sudo ifconfig "${i}" up


echo "i = ${i}"
echo "a = ${a}"


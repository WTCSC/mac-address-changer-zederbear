[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tp86o73G)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17744419)

# Installation
Install net-tools for ifconfig
```sh
$ sudo apt install net-tools
```

# Usage
```sh
$ ./macdaddy.sh -i eth0 -a 55:d9:73:08:af:e7
$ ./macdaddy.sh -i wlan1 -a 6e:4f:12:e4:77:e3
$ ./macdaddy.sh -i enp0s3 -r
$ ./macdaddy.sh -i eth0 -u
$ ./macdaddy.sh -i wlan1 -u
$ ./macdaddy.sh enp0s3 -u
```
```sh
Usage: ./macdaddy.sh [-i <eth0|eth1|...>] [-a <mac-address>] [-r] [-u]
    Examples:
         ./macdaddy.sh -i   eth0 -r
         ./macdaddy.sh -i enp0s3 -a 97:1a:d9:aa:a6:fd
         ./macdaddy.sh -i  wlan1 -u

    Options:
        -i        Network interface           (Always required)
        -a        Mac Address                 (Required unless using -r or -u)
        -r        Randomizes your mac address (Not required)
        -u        Resets your mac address     (Not required)
```

# Error Handling/Validation
Checks the given mac address to see if it follows the specified format of 6 base 16 numbers with commas inbetween them
-- I should probably check for valid interfaces

# Troubleshooting
Double check your mac address by going to a regex website and using the regex pattern "^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$" and the mac address. See if it matches.
Use wireshark to check what your active interface is.

# Demonstration

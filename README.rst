Cisco Switch MAC Vendor Finder
==========================================
A fun little project I made that will obtain information specific to MAC addresses learned over access ports only and write it to a CSV file. 

MAC Address specific information obtained:

- MAC address
- Access switchport interface MAC address is learned on
- VLAN
- Whether the MAC address was learned statically or dynamically
- MAC vendor information (obtained by doing API calls to macvendors.co)


This project was tested with the following device:

- Tested on a WS-C3850-24U Running CIsco IOS-XE Version 03.06.05E
- Cisco IOS Software, IOS-XE Software, Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Version 03.06.05E RELEASE SOFTWARE (fc2)

How it works
------------

- The ``vendor_finder.py`` program will initialize an SSH session to the switch
- With that SSH session commands are sent to obtain the MAC address table
- The MAC address table is then parsed to obtain MAC address specific info and then added to a dictionary
- The MAC addresses are then used to query an API mentioned above to obtain vendor information for that MAC address
- All information is written to a csv file

Usage
-----

- Run ``vendor_finder.py`` from the terminal
- You will be prompted for the following:
    - ``IP address``: IP address of the Cisco switch
    - ``username``: Cisco switch's administrative password
    - ``password``: Cisco switch's administrative password
- The script will run and return no output in the terminal (see how it works above for what is done)


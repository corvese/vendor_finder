from netmiko import ConnectHandler
import requests
import json
import csv
import re
import getpass

def connect_to_switch(switch, username, password):
    """Connects to a switch and creates an SSH session to send commands to
    
    params
    switch(str) = switch IP address
    username(str) = switch login username
    password(str0) = switch login password

    returns: 
    switch(class): switch ssh session"""
    switch = ConnectHandler(ip=switch, device_type='cisco_ios', username=username, password=password)
    return switch

def obtain_mac_address_table(switch_session):
    """Sends commands to a Cisco switch and returns the output of the MAC address table
    
    Params:
    switch_session(class) = switch ssh session
    
    Returns:
    mac_address_table_output(list): MAC address table split by lines"""
    mac_table = switch_session.send_command('show mac address-table')
    switch_session.disconnect()
    mac_address_table_output = mac_table.splitlines()
    return mac_address_table_output
    
def mac_parser(mac_address_table_output):
    """Parses MAC address table for MAC address, VLAN, Interface found and how MAC address is learned
    
    Params:
    mac_address_table_output(list): MAC address table split by lines
    
    Returns:
    list_of_mac_address_info(list): List of dicts containing MAC address, VLAN, how MAC is learned, interface found"""
    mac_table_regex = '(\d*)\s*(([0-9a-fA-F]{4}[.-:|]?){3})\s*(\w*)\s*(.*)'
    list_of_mac_address_info = []
    for item in mac_address_table_output:
        if re.search(mac_table_regex, item):
            found = re.search(mac_table_regex, item)
            if found.group(5) == 'CPU':  #Ignores entries in MAC address table with PORT as CPU
                pass
            else:
                dict = {}
                dict['VLAN'] = found.group(1)
                dict['MAC_ADDRESS'] = found.group(2)
                dict['LEARNED_VIA']= found.group(4) 
                dict['INTERFACE'] = found.group(5)
                list_of_mac_address_info.append(dict)
    return list_of_mac_address_info

def mac_vendor_api_call(list_of_mac_address_info):
    """Searches a list of dictionaries to do an API call against the MAC address to obtain vendor information
    
    Params:
    mac_vendor_api_call(dict): Contains output from function mac_parser that has MAC addr, VLAN, interface
    
    Returns:
    list_of_mac_address_info(list): Returns a new list of dictionaries with a new key value pair of 
           Company(key) with the vendor name(value)"""

    for dict in list_of_mac_address_info:
        r = requests.get('https://macvendors.co/api/{0}'.format(dict['MAC_ADDRESS']))
        api_return = json.loads(r.text)
        if api_return['result']['company']:
            dict['COMPANY'] = api_return['result']['company']
        else:
            dict['COMPANY'] = 'NOT FOUND'
    return list_of_mac_address_info
 
def write_mac_info_to_csv(mac_address_info, switch_ip):
    """Takes a list of dictionaries containing information about a MAC address and adds it to a CSV file

    Params:
    mac_address_info(list): List of dicts that contains info specific to a MAC address
    switch_ip(str): Str of the switch IP address to add to the CSV file name
    
    Returns:
    CSV file to local dir"""
    csvfile = open('mac_information-{0}.csv'.format(switch_ip), 'w') 
    fieldnames = ['COMPANY', 'INTERFACE', 'LEARNED_VIA', 'MAC_ADDRESS', 'VLAN']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(mac_address_info)

if __name__ == "__main__":
    switch_ip = input("IP address: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    switch_session = connect_to_switch(switch_ip, username, password)
    mac_address_table = obtain_mac_address_table(switch_session)
    mac_address_info = mac_parser(mac_address_table)
    mac_api_call = mac_vendor_api_call(mac_address_info)
    write_mac_info_to_csv(mac_api_call, switch_ip)





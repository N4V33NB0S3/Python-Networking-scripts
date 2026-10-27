#!/bin/python3 
#Author: Naveen Bose

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor

username = input("Enter username :")
password = getpass("Enter Password :")

def connect_device(ip,vendor):
    device = {
        "device_type" : vendor,
        "host" : ip,
        "username" : username,
        "password" : password,
        "timeout" : 30,
        "conn_timeout" : 15,
        "banner_timeout" : 30
    }

    conn = ConnectHandler(**device)
    return conn


def get_hostname(conn, vendor):
    prompt = conn.base_prompt

    if vendor == "juniper_junos":
        hostname = prompt.split("@")[-1]
    elif vendor == "nokia_sros":
        hostname = prompt.replace("A:", "")
    elif vendor == "huawei":
        hostname = prompt
    else:
        raise ValueError(f"Unsupported vendor: {vendor}")

    return hostname

def get_configuration(conn, vendor):
    if vendor == "juniper_junos":
       output = conn.send_command("show configuration | display set")
    elif vendor == "nokia_sros":
        output = conn.send_command("admin display-config")
    elif vendor == "huawei":
        output = conn.send_command("display current-configuration")
    else:
        raise ValueError(f"Unsupported vendor - {vendor}")
    
    return output

def save_configuration(hostname, output):
    filename = f"{hostname}.txt"
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(output)

    print(f"Configuration saved to {filename}")

def load_devices(filename):
    devices = []

    with open(filename, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            ip, vendor = line.split(",")

            devices.append(
                {
                    "ip": ip.strip(),
                    "vendor": vendor.strip()
                }
            )
    return devices

def backup_device(device):
    ip = device["ip"]
    vendor = device["vendor"]

    print(f"[START] Connecting to {ip} ({vendor})")

    conn = connect_device(ip, vendor)

    try:
        hostname = get_hostname(conn, vendor)
        output = get_configuration(conn, vendor)
        save_configuration(hostname, output)

        print(f"[DONE] {hostname} backup completed")
        
    finally:
        conn.disconnect()
    
def main():
    devices = load_devices("devices.txt")

    try:
         with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(backup_device, devices)
        
    except KeyboardInterrupt:
        print("\nBackup interrupted by user.")

if __name__ == "__main__":
    main()

    


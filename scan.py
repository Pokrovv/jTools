import csv
from scapy.all import *
from termcolor import colored
from upnpclient import Device

def get_device_info(ip_address):
    try:
        device = Device(f"http://{ip_address}:49152/description.xml")
        device_info = device.device.friendlyName, device.device.deviceType
        return device_info
    except Exception as e:
        return colored(f"Error: {e}", "red"), colored("N/A", "red")

def ip_scan(target, output_file="scan_results.csv", num_pings=2, upnp_port=49152):
    try:
        with open(output_file, mode="w", newline="") as csvfile:
            fieldnames = ["IP", "MAC", "Vendor", "Device Type", "Device Name"]
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()

            print(colored(f"Scanning {target}...", "blue"))

            ans, _ = arping(target, verbose=0, retry=num_pings)

            for _, summary in ans:
                ip = summary[ARP].psrc
                mac = summary[ARP].hwsrc

                # Get device information using upnpclient package
                device_type, device_name = get_device_info(ip)

                # You can use other APIs or databases to get vendor information based on MAC address(es)
                vendor = "N/A"

                csv_writer.writerow({"IP": ip, "MAC": mac, "Vendor": vendor, "Device Type": device_type, "Device Name": device_name})

            print(colored("[✔] ", "green") + f"Scan completed, you can see results in {colored(output_file, 'blue')}")



    except Exception as e:
        print(colored(f"Error: {e}", "red"))

if __name__ == "__main__":
    target_ip = input(colored("Enter the target IP range (e.g., 192.168.1.1/24): ", "light_magenta"))
    output_filename = input(colored("Enter the output filename (default is scan_results.csv): ", "light_magenta"))
    num_pings = int(input(colored("Enter the number of pings p./host (max 2): ", "light_magenta")) or 2)
    upnp_port = int(input(colored("Enter the UPnP server port (default is 49152): ", "light_magenta")) or 49152)

    if not output_filename:
        output_filename = "scan_results.csv"

    ip_scan(target_ip, output_filename, num_pings, upnp_port)

import time
from collections import Counter

import pandas as pd
from ouilookup import OuiLookup
from requests import get
from rich import print


def find_most_common_string2(string_list):
    counter = Counter(string_list)
    if most_common := counter.most_common(1):
        most_common_string, count = most_common[0]
        confidence = count / len(string_list) * 100
        return most_common_string, round(confidence, 2)
    else:
        return "Unknown", 0


def print_full(x):
    pd.set_option("display.max_rows", len(x))
    print(x)
    pd.reset_option("display.max_rows")


# Read the CSV file
df = pd.read_csv("output.csv")

for mac_addr, vendor1 in zip(df["macaddress"], df["macaddrvendor"]):
    if type(mac_addr) != str:
        print("No MAC address Found [Skipping...]")
        continue
    else:
        vendor2 = list(OuiLookup().query(mac_addr)[0].values())[0]
        vendor3 = get(f"https://api.macvendors.com/{mac_addr}", timeout=3).text
        if "errors" in vendor3 or vendor3 is None:
            print("No MAC address Vendor Found [Skipping...]")
            continue
        else:
            while "Too Many Requests" in vendor3 or "Too Many Requests" in vendor3:
                time.sleep(1)
                vendor3 = get(f"https://api.macvendors.com/{mac_addr}", timeout=3).text
        vendors = [vendor1, vendor2, vendor3]

        print(mac_addr)
        print(vendors)
        print(find_most_common_string2(vendors))
        print()


# Identify common networking devices based on vendors
common_devices = df["macaddrvendor"].value_counts().head(5)
print_full(df["macaddrvendor"])


# Print the common networking devices
print("Common Networking Devices:")
print(common_devices)

# TODO make the dataframe use the new vendors if there is any

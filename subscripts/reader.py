import time
from collections import Counter

import pandas as pd
from ouilookup import OuiLookup
from requests import get
from rich import print

from utils import connection, CURRENT_DATA, MAC_ADDR_API_TOKEN


def find_most_common_string2(string_list):
    counter = Counter(string_list)
    if most_common := counter.most_common(1):
        most_common_string, count = most_common[0]
        confidence = count / len(string_list) * 100
        return most_common_string, round(confidence, 2)
    else:
        return "Unknown", 0

headers = {
    "Authorization": f"Bearer {MAC_ADDR_API_TOKEN}",
    "Accept": "application/json"
}




cursor = connection.cursor()
cursor.execute(f"SELECT ip_address, macaddress, macaddrvendor FROM {CURRENT_DATA}")

rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=["ip_address", "macaddress", "macaddrvendor"])

print(df)

# Close the cursor and the database connection
cursor.close()
connection.close()


for mac_addr, vendor1 in zip(df["macaddress"], df["macaddrvendor"]):
    if type(mac_addr) != str:
        print("No MAC address Found [Skipping...]")
        continue
    else:
        vendor2 = ""
        if lookup_results := OuiLookup().query(mac_addr):
            vendor2 = list(lookup_results[0].values())[0]
        print(mac_addr)
        vendor3 = get(f"https://api.macvendors.com/v1/lookup/{mac_addr}", headers=headers).json()["data"]["organization_name"]
        if "errors" in vendor3 or vendor3 is None:
            print("No MAC address Vendor Found [Skipping...]")
            continue
        else:
            while "Too Many Requests" in vendor3 or "Too Many Requests" in vendor3:
                time.sleep(1)
                vendor3 = get(f"https://api.macvendors.com/v1/lookup/{mac_addr}", headers=headers).json()
        vendors = [vendor1, vendor2, vendor3]

        print(mac_addr)
        print(vendors)
        print(find_most_common_string2(vendors))
        print()


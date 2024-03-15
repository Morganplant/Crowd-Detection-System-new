import csv
import os

import pandas as pd
from fuzzywuzzy import fuzz
from rich import print

from extras import DATA_DIR


def get_known_network_vendors():
    file_path = os.path.join(DATA_DIR, "networking_vendors.csv")
    with open(file_path, "r") as fh:
        return [item.rstrip("\n") for item in list(fh)]

    return vendors


def get_scan_data():
    file_path = os.path.join(DATA_DIR, "scan_output.csv")
    return pd.read_csv(file_path)


known_vendors = get_known_network_vendors()

scanned_vendors = zip(get_scan_data()["macaddrvendor"], get_scan_data()["ip_address"])

matched_items = {}
for scanned_vendor, scanned_ip in scanned_vendors:
    for known_vendor in known_vendors:
        if not isinstance(scanned_vendor, str):
            continue
        similarity = fuzz.ratio(scanned_vendor, known_vendor)
        if similarity >= 80:
            # print([scanned_vendor, known_vendor])
            # print(similarity)
            # print()
            matched_items[scanned_ip] = known_vendor
print("Network Devices:")
print(matched_items)

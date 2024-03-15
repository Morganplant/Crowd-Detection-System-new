import datetime as dt
import ipaddress
import logging

import nmap3
import pandas as pd
from rich.logging import RichHandler
import pymysql

from arp import get_arp_data
from utils import connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

arp_dataframe = get_arp_data()
addrs = list(ipaddress.ip_network("192.168.0.0/16"))

nmap = nmap3.Nmap()

for addr in addrs:
    addr = str(addr)
    results = nmap.nmap_os_detection(addr)
    try:
        data = results[addr]
    except Exception: # Privledges required to run scan
        if "error" in results:
            logging.error(results["msg"])
            exit()

    active_ports = [port["portid"] for port in data["ports"] if port["state"] == "open"]
    hostname = data["hostname"][0]["name"] if data.get("hostname") else ""
    macaddress = data["macaddress"]["addr"] if data.get("macaddress") else ""
    macaddrvendor = data["macaddress"].get("vendor", "") if data.get("macaddress") else ""
    likely_os = data["osmatch"][0]["name"] if data.get("osmatch") else ""

    

    if active_ports or hostname or macaddress or macaddrvendor or likely_os:
        logging.info(f"Scanned [{addr}] ...")
        if len(hostname) > 1:
            logging.info(f"[{addr}] : '{hostname}'")
        if len(macaddrvendor) > 1:
            logging.info(f"[{addr}] : '{macaddrvendor}' ")
        new_data = {
            "ip_address": addr,
            "active_ports": active_ports,
            "hostname": hostname,
            "macaddress": macaddress,
            "macaddrvendor": macaddrvendor,
            "likely_os": likely_os,
        }
        logging.debug(f"Inserting: \n{new_data}\n into the database...")
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO scan_data (ip_address, active_ports, hostname, macaddress, macaddrvendor, likely_os)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            active_ports = VALUES(active_ports),
            hostname = VALUES(hostname),
            macaddress = VALUES(macaddress),
            macaddrvendor = VALUES(macaddrvendor),
            likely_os = VALUES(likely_os)
            """
            cursor.execute(sql, (
                new_data["ip_address"],
                ",".join(new_data["active_ports"]),
                new_data["hostname"],
                new_data["macaddress"],
                new_data["macaddrvendor"],
                new_data["likely_os"],
            ))
        logging.debug("Data inserted into the database.")
        connection.commit()
    # else:
    #     logging.info(f"Scanned [{addr}] ... No data found.")
# Close the cursor and the database connection
cursor.close()
connection.close()

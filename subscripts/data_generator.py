import random
from faker import Faker
import pymysql
from rich.progress import Progress

# Set up the database connection
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="crowd_pulse",
)

fake_num = 12

# Create an instance of the Faker class
fake = Faker()

# Generate fake data for the table
data_list = []
with Progress() as progress:
    task = progress.add_task("[cyan]Generating fake data...", total=fake_num)
    for _ in range(fake_num):  # Generate 100 rows of fake data
        ip_address = fake.ipv4()
        active_ports = [fake.port_number() for _ in range(random.randint(0, 5))]
        hostname = fake.hostname()
        macaddress = fake.mac_address()
        macaddrvendor = fake.company()
        likely_os = f"{fake.language_name()} {fake.last_name()} {fake.century()}"

        new_data = {
            "ip_address": ip_address,
            "active_ports": ",".join(str(port) for port in active_ports),
            "hostname": hostname,
            "macaddress": macaddress,
            "macaddrvendor": macaddrvendor,
            "likely_os": likely_os,
        }
        data_list.append(new_data)
        progress.update(task, advance=1)

# Insert the fake data into the database
print("Inserting fake data into the database...")
with connection.cursor() as cursor:
    sql = """
    INSERT INTO fake_data (ip_address, active_ports, hostname, macaddress, macaddrvendor, likely_os)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    active_ports = VALUES(active_ports),
    hostname = VALUES(hostname),
    macaddress = VALUES(macaddress),
    macaddrvendor = VALUES(macaddrvendor),
    likely_os = VALUES(likely_os)
    """
    for data in data_list:
        cursor.execute(sql, (
            data["ip_address"],
            data["active_ports"],
            data["hostname"],
            data["macaddress"],
            data["macaddrvendor"],
            data["likely_os"],
        ))
    connection.commit()

# Close the database connection
connection.close()
print("Fake data inserted into the database.")
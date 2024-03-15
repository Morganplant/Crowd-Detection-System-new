import os
import pymysql

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
SRC_DIR = os.path.join(ROOT_DIR, "src")
DATA_DIR = os.path.join(SRC_DIR, "data")

CURRENT_DATA = "fake_data"
CURRENT_DATA = "scan_data"

connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="crowd_pulse",
)

MAC_ADDR_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImp0aSI6ImVlNmIxZGI0LTRkOGUtNDg4YS04MTQxLWZlNGJiM2IxNWE1YiJ9.eyJpc3MiOiJtYWN2ZW5kb3JzIiwiYXVkIjoibWFjdmVuZG9ycyIsImp0aSI6ImVlNmIxZGI0LTRkOGUtNDg4YS04MTQxLWZlNGJiM2IxNWE1YiIsImlhdCI6MTcxMDQzNjM0NywiZXhwIjoyMDI0OTMyMzQ3LCJzdWIiOiIxNDM2NCIsInR5cCI6ImFjY2VzcyJ9.T7EWoecErkEJVcY5PLxfXL3uagxXhsYOrCvrGjjvmq-lMD9kA4gkYyrXarGmiTP-0U0Qh1Zo3HrlAIvvt2MArg"
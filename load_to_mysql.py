"""Load the clean event log into the MySQL table Careflow (works from VS Code, no Workbench needed).
Before running: create the database and table by running your CREATE TABLE Careflow command.
Install once:   pip install pandas sqlalchemy pymysql
Run:            python load_to_mysql.py
"""
import sys
from getpass import getpass
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine, text

csv_path = sys.argv[1] if len(sys.argv) > 1 else "Validation and cleaning.csv"
user = input("MySQL user (default root): ") or "root"
password = getpass("MySQL password: ")

engine = create_engine(f"mysql+pymysql://{user}:{quote_plus(password)}@localhost:3306/careflow")

df = pd.read_csv(csv_path, parse_dates=["Timestamp", "Activity_End_Time"])
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE Careflow"))        # safe to re-run
    df.to_sql("Careflow", conn, if_exists="append", index=False)
    events, cases = conn.execute(text("SELECT COUNT(*), COUNT(DISTINCT Case_ID) FROM Careflow")).one()
print(f"Loaded {events} events, {cases} cases")              # expect 2635 events, 300 cases

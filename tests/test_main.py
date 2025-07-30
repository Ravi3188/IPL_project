import pandas as pd
import sqlite3
import os

# Test 1: Check if CSV files load properly
def test_csv_load():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    assert not matches.empty, "Matches CSV is empty"
    assert not deliveries.empty, "Deliveries CSV is empty"
    assert "season" in matches.columns, "Missing 'season' column"

# Test 2: Check if SQLite tables are created
def test_sqlite_tables():
    conn = sqlite3.connect(":memory:")
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    matches.to_sql("matches", conn, index=False, if_exists="replace")
    deliveries.to_sql("deliveries", conn, index=False, if_exists="replace")

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    table_names = [t[0] for t in tables]
    assert "matches" in table_names
    assert "deliveries" in table_names
    conn.close()

# Test 3: Check if reports were generated
def test_reports_exist():
    assert os.path.exists("reports/team_report.csv"), "Team report not found"
    assert os.path.exists("reports/season_report.csv"), "Season report not found"

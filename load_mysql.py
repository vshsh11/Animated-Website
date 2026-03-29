#!/usr/bin/env python3
"""
load_mysql.py  —  Loads all 10 tables into demand_forecast_dw
Run:  python3 load_mysql.py
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os, sys

# ══════════════════════════════════════════════════════════════
#  CHANGE ONLY THESE TWO LINES
# ══════════════════════════════════════════════════════════════
PASSWORD   = "12345678"        # your MySQL root password
CSV_FOLDER = "/Users/vishesh/Downloads"   # folder with all CSV files
# ══════════════════════════════════════════════════════════════

DB_URL = f"mysql+pymysql://root:{PASSWORD}@localhost/demand_forecast_dw"

# ── Connect ───────────────────────────────────────────────────
print("Connecting to MySQL...")
try:
    engine = create_engine(DB_URL, echo=False)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Connected!\n")
except Exception as e:
    print(f"❌ Cannot connect: {e}")
    print("   Check: password correct? MySQL running?")
    sys.exit(1)

# ── Tables in load order (dim before fact) ────────────────────
TABLES = [
    ("dim_date",             "dim_date.csv",             1461),
    ("dim_product",          "dim_product.csv",            20),
    ("dim_region",           "dim_region.csv",              7),
    ("dim_factory",          "dim_factory.csv",             4),
    ("dim_distributor",      "dim_distributor.csv",        30),
    ("dim_external_factors", "dim_external_factors.csv", 29157),
    ("fact_sales",           "fact_sales.csv",           29220),
    ("fact_production",      "fact_production.csv",      29220),
    ("fact_inventory",       "fact_inventory.csv",       29220),
    ("fact_supply_chain",    "fact_supply_chain.csv",    29220),
]

results = []

for table, csv_file, expected in TABLES:

    path = os.path.join(CSV_FOLDER, csv_file)

    # Check file exists
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        results.append((table, 0, expected, "FILE NOT FOUND"))
        continue

    print(f"Loading {csv_file} → {table} ...", end=" ", flush=True)

    try:
        # Read CSV
        df = pd.read_csv(path)

        # Load into MySQL
        with engine.begin() as conn:
            # Disable FK checks so tables load without constraint errors
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            conn.execute(text(f"TRUNCATE TABLE `{table}`"))

        # Write data in chunks of 500 rows
        df.to_sql(
            name      = table,
            con       = engine,
            if_exists = "append",
            index     = False,
            method    = "multi",
            chunksize = 500,
        )

        # Re-enable FK checks
        with engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        print(f"✅  {len(df):,} rows")
        results.append((table, len(df), expected, "OK"))

    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        results.append((table, 0, expected, str(e)[:80]))

# ── Verify ────────────────────────────────────────────────────
print()
print("=" * 65)
print("VERIFICATION — FINAL ROW COUNTS")
print("=" * 65)
print(f"  {'Table':<28} {'In DB':>8} {'Expected':>10} {'Status'}")
print("  " + "-" * 60)

all_ok = True
with engine.connect() as conn:
    for table, loaded, expected, status in results:
        try:
            actual = conn.execute(
                text(f"SELECT COUNT(*) FROM `{table}`")
            ).scalar()
        except:
            actual = 0

        ok   = (actual == expected)
        icon = "✅" if ok else "❌"
        note = "OK" if ok else "MISMATCH"
        if not ok:
            all_ok = False
        print(f"  {icon} {table:<28} {actual:>8,} {expected:>10,}   {note}")

print("  " + "-" * 60)
print()
if all_ok:
    print("✅  ALL TABLES LOADED CORRECTLY!")
    print("    Your database is ready. Open Jupyter Notebook and start coding!")
else:
    print("⚠️   Some tables failed. Read the errors above.")
print("=" * 65)

import pandas as pd
from sqlalchemy import create_engine, text
import os

# === Configuration ===
CSV_PATH = "../data/airbnb_properties.csv"
TABLE_NAME = "airbnb_properties"
SCHEMA_TABLE = "table_schemas"
DB_CONFIG = {
    "user": "admin",
    "password": "admin",
    "host": "localhost",
    "port": 5432,
    "database": "airbnbdb",
    "table": TABLE_NAME,
    "schema": SCHEMA_TABLE

}

# === Load CSV ===
df = pd.read_csv(CSV_PATH)

# Optional: Clean column names (PostgreSQL compatibility)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace(".", "_")

# === Connect to PostgreSQL ===
db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(db_url)
# engine = create_engine("postgresql://admin:admin@localhost:5432/airbnbdb")
# engine = create_engine("postgresql://admin:admin@172.17.0.2:5432/airbnbdb")


# === Upload to Postgres ===
df.to_sql(TABLE_NAME, con=engine, if_exists='replace', index=False)
print(f"✅ Table '{TABLE_NAME}' uploaded successfully to PostgreSQL")



# === Save schema table if it doesn't exist ===

# Extract and format schema as DataFrame
schema_df = pd.DataFrame({
    "table_name": TABLE_NAME,
    "column_name": df.columns,
    "data_type": [str(dtype) for dtype in df.dtypes]
})


with engine.connect() as conn:
    conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA_TABLE} (
            table_name TEXT,
            column_name TEXT,
            data_type TEXT
        );
    """))
    conn.commit()

# Save schema into schema table
schema_df.to_sql(SCHEMA_TABLE, con=engine, if_exists='replace', index=False)
print(f"✅ Saved schema to `{SCHEMA_TABLE}`.")

# ================================================== #


# # === Save schema to .sql file ===
# def export_table_schema(engine, table_name, output_file):
#     with engine.connect() as conn:
#         result = conn.execute(
#             f"SELECT 'CREATE TABLE ' || relname || E'\n(\n' || "
#             f"string_agg('    ' || column_name || ' ' || data_type, ',\n') || E'\n);' AS schema "
#             f"FROM information_schema.columns "
#             f"JOIN pg_class ON table_name = relname "
#             f"WHERE table_name = '{table_name}' "
#             f"GROUP BY relname;"
#         )
#         schema_sql = result.scalar()
#         with open(output_file, "w") as f:
#             f.write(schema_sql or "")
#         print(f"📄 Schema saved to {output_file}")

# export_table_schema(engine, TABLE_NAME, "schema.sql")
# # ================================================== #
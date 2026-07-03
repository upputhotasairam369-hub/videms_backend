import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(user="postgres", password="upputhota@123", host="localhost", port="5432")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE "ProductsDatabase";')
    print("Database created successfully")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn:
        cursor.close()
        conn.close()

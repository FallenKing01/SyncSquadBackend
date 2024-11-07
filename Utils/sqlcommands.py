import pyodbc  # Assuming you're using pyodbc for SQL Server connections

def add_row(cursor, table, obj):
    data = vars(obj)
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    values = tuple(data.values())

    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    try:
        cursor.execute(sql, values)
        cursor.connection.commit()

    except pyodbc.IntegrityError:

        cursor.connection.rollback()

        raise Exception("email already exists")

    except Exception as e:
        print(f"Failed to insert row into {table}: {e}")
        raise Exception(f"Failed to insert row into {table}: {e}")


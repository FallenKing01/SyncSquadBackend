import pyodbc


# Database connection details
server = "ip4c.database.windows.net"
port = 1433
user = "stud"
password = "Andrei2002"  # Replace with your actual password
database = "ip4c"

def dbInit():

    # Build connection string
    conn_string = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={server},{port};"
        f"Database={database};"
        f"Uid={user};"
        f"Pwd={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        # Create a connection
        cnxn = pyodbc.connect(conn_string)
        cursor = cnxn.cursor()
        return cnxn, cursor

    except Exception as e:
        raise Exception(f"Error while connecting to the database: {str(e)}")
        return None, None
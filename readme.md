To build a database backup CLI utility in Python that can back up an entire database (including tables, their structure, and data), you'll need to break the project into manageable tasks. Below is a structured list of tasks that you can follow to implement this tool:

---

### **1. Setup the Project Environment**
- **Task 1.1:** Set up a Python environment (use `venv` or `conda` for isolation).
- **Task 1.2:** Install necessary dependencies, such as:
  - `mysql-connector-python` (for MySQL database interactions)
  - `psycopg2` (for PostgreSQL database interactions, if applicable)
  - `argparse` (for command-line argument parsing)
  - `os` and `shutil` (for file and directory operations)
  - `subprocess` (if needed for executing system commands like `mysqldump`)

```bash
pip install mysql-connector-python psycopg2 argparse
```

---

### **2. Parse Command-Line Arguments**
- **Task 2.1:** Use `argparse` to define the command-line arguments for:
  - Host (e.g., `localhost`)
  - Username (e.g., `root`)
  - Password (e.g., `password123`)
  - Database name (e.g., `my_database`)
  - Destination folder (e.g., `./backups`)
  
- **Task 2.2:** Validate the inputs to ensure no required fields are missing or invalid.

```python
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Database Backup Utility")
    parser.add_argument('host', type=str, help="Database host")
    parser.add_argument('username', type=str, help="Database username")
    parser.add_argument('password', type=str, help="Database password")
    parser.add_argument('dbname', type=str, help="Database name to back up")
    parser.add_argument('dest_folder', type=str, help="Destination folder for backup files")
    return parser.parse_args()
```

---

### **3. Establish Database Connection**
- **Task 3.1:** Depending on the type of database (e.g., MySQL, PostgreSQL), connect to the database using the provided credentials.
- **Task 3.2:** Test the connection and handle any errors that arise.

```python
import mysql.connector

def connect_to_database(host, username, password, dbname):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=dbname
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
```

---

### **4. Retrieve List of Tables**
- **Task 4.1:** Query the database to get the list of all tables in the specified database.
- **Task 4.2:** Store the list of table names for backup.

```python
def get_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    return [table[0] for table in tables]
```

---

### **5. Backup Each Table's Structure and Data**
- **Task 5.1:** For each table:
  - Use `SHOW CREATE TABLE <table_name>` to get the table schema.
  - Use `SELECT * FROM <table_name>` to get the data.

- **Task 5.2:** Create separate files for each table:
  - A file containing the table structure (schema).
  - A file containing the table data (insert statements or CSV).

```python
import os

def backup_table_structure(cursor, table_name, dest_folder):
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    create_table_sql = cursor.fetchone()[1]
    with open(os.path.join(dest_folder, f"{table_name}_structure.sql"), 'w') as file:
        file.write(create_table_sql)

def backup_table_data(cursor, table_name, dest_folder):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    with open(os.path.join(dest_folder, f"{table_name}_data.csv"), 'w') as file:
        # Write the headers
        file.write(','.join(columns) + '\n')
        for row in rows:
            file.write(','.join(map(str, row)) + '\n')
```

---

### **6. Backup the Entire Database**
- **Task 6.1:** For each table, call the backup functions for both structure and data.
- **Task 6.2:** Ensure all backups are saved in the specified destination folder.

```python
def backup_database(connection, tables, dest_folder):
    cursor = connection.cursor()
    for table in tables:
        print(f"Backing up table: {table}")
        backup_table_structure(cursor, table, dest_folder)
        backup_table_data(cursor, table, dest_folder)
    cursor.close()
```

---

### **7. Handling Errors and Edge Cases**
- **Task 7.1:** Ensure that the destination folder exists, or create it if it doesn't.
- **Task 7.2:** Handle any database connection failures, table retrieval issues, or write failures.
- **Task 7.3:** Log errors or print them to the console as necessary.

```python
import os

def ensure_dest_folder_exists(dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

def main():
    args = parse_arguments()
    ensure_dest_folder_exists(args.dest_folder)

    connection = connect_to_database(args.host, args.username, args.password, args.dbname)
    if connection:
        tables = get_tables(connection)
        backup_database(connection, tables, args.dest_folder)
        print(f"Backup completed for {args.dbname} at {args.dest_folder}")
        connection.close()
    else:
        print("Failed to connect to the database.")
```

---

### **8. (Optional) Add Compression**
- **Task 8.1:** Use a compression method (like `gzip`) to compress backup files into a `.tar.gz` or `.zip` format.
- **Task 8.2:** Compress each table file after it's generated to save space.

```python
import gzip
import shutil

def compress_file(file_path):
    with open(file_path, 'rb') as f_in:
        with gzip.open(f"{file_path}.gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(file_path)  # Delete original file after compression
```

---

### **9. Testing the Backup Utility**
- **Task 9.1:** Test the utility with different database types and configurations.
- **Task 9.2:** Verify the correctness of the backed-up files by restoring them to a different database.
- **Task 9.3:** Ensure the backup utility can handle edge cases such as large tables, long table names, or special characters in data.

---

### **10. Document the CLI Utility**
- **Task 10.1:** Create usage documentation (how to run the utility, what arguments it expects).
- **Task 10.2:** Include any potential troubleshooting tips, such as resolving database connection issues.

```bash
python backup_utility.py localhost root password123 my_database ./backups
```

---

### **11. (Optional) Add Additional Features**
- **Task 11.1:** Add support for backing up multiple databases.
- **Task 11.2:** Implement incremental backups (only back up tables that have changed since the last backup).
- **Task 11.3:** Add encryption to backup files for additional security.

---

### **Final Notes:**
- Ensure the backup files include all necessary SQL to recreate the database schema and data.
- The tool should be robust, with proper error handling and logging.
- Make sure the backup process is efficient, especially if the database is large.

By breaking down the project into these tasks, you can systematically work on implementing each part of the CLI utility and ensure it performs as expected.
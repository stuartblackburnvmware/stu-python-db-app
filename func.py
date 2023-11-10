# func.py
from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    # Read database settings from files
    with open('/bindings/db/database') as f:
        database = f.read().strip()
    with open('/bindings/db/host') as f:
        host = f.read().strip()
    with open('/bindings/db/password') as f:
        password = f.read().strip()
    with open('/bindings/db/port') as f:
        port = f.read().strip()
    with open('/bindings/db/provider') as f:
        provider = f.read().strip()
    with open('/bindings/db/type') as f:
        type_ = f.read().strip()
    with open('/bindings/db/username') as f:
        username = f.read().strip()

    # Build connection string
    conn_str = f"dbname={database} user={username} password={password} host={host} port={port}"

    # Connect to the database
    conn = psycopg2.connect(conn_str)

    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create a simple table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS t1 (id serial PRIMARY KEY, value varchar);")

    conn.commit()
    conn.close()

def delete_all_records():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete all records from the table
    cursor.execute("DELETE FROM t1;")

    conn.commit()
    conn.close()

def get_values():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve values from the database
    cursor.execute("SELECT * FROM t1;")
    values = cursor.fetchall()

    conn.close()

    return values

@app.route('/', methods=['GET', 'POST'])
def main():
    create_table()

    display_clicked = request.args.get('display_clicked', False)
    delete_clicked = request.args.get('delete_clicked', False)
    
    if request.method == 'POST':
        value = request.form['value']
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the value into the database
        cursor.execute("INSERT INTO t1 (value) VALUES (%s);", (value,))

        conn.commit()
        conn.close()

    if display_clicked:
        # If the 'Display Values' button is clicked, retrieve and display values
        values = get_values()
        return render_template('index.html', values=values, display_clicked=True)

    elif delete_clicked:
        # If the 'Delete All Records' button is clicked, delete all records
        delete_all_records()

    return render_template('index.html', values=None, display_clicked=False)

if __name__ == '__main__':
    app.run(debug=True)

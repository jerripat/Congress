import sqlite3
from Presidents import list_of_us_presidents  # list of tuples: (name, years, vp)

# Connect to the SQLite database
conn = sqlite3.connect("presidents.db")
cursor = conn.cursor()

# Create the presidents table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS presidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        years INTEGER,
        vp TEXT
    )
''')

# Insert presidents into the table
for president in list_of_us_presidents:
    cursor.execute("INSERT INTO presidents (name, years, vp) VALUES (?, ?, ?)", president)
    print(f"Added {president[0]} to the database.")

# Commit once after all inserts (more efficient)
conn.commit()

# Fetch and display all presidents
cursor.execute("SELECT * FROM presidents")
all_presidents = cursor.fetchall()

print("\nInserted Presidents:")
for pres in all_presidents:
    print(pres)

# Close the connection
conn.close()

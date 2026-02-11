import psycopg2

conn = psycopg2.connect(dbname = "first_db", user = "user", password ="password")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Customers")

cur.execute("""
CREATE TABLE Customers(
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    email_address VARCHAR(100),
    phone_number VARCHAR(20),
    registry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
""")

cur.execute(
    "INSERT INTO Customers (name, email_address, phone_number) VALUES (%s, %s, %s)",
    ("Lina O", "example0@gmail.com", "+4475684587854")
)

cur.execute(
    "INSERT INTO Customers (name, email_address, phone_number) VALUES (%s, %s, %s)",
    ("Reda O", "example1@gmail.com", "+4478744587854")
)


conn.commit()

cur.execute("SELECT * FROM Customers")
print(cur.fetchall())

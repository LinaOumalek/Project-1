from fastapi import FastAPI, status
import psycopg2
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

class Customer(BaseModel):
    name: str
    email_address : Optional[str] = None
    phone_number : str

#a second class to make some fields optional for patch endpoints
class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None

#start with one connection per endpoint, later scale to connection pool to mimic production systems

@app.post("/customers")
def add_customer(customer: Customer):
    #add to table
    conn = psycopg2.connect(dbname = "first_db", user = "linao", password = "Linareda123")
    cur = conn.cursor()

    cur.execute("INSERT INTO Customers (name, email_address, phone_number) VALUES (%s ,%s ,%s)", (customer.name, customer.email_address, customer.phone_number))
    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse(content = {"Message" : "Customer added"}, status_code = 201)

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    conn = psycopg2.connect(dbname = "first_db", user = "linao", password = "Linareda123")
    cur = conn.cursor()

    data = cur.execute("SELECT * FROM Customers WHERE customer_id = %s", (customer_id, )).fetchone()

    cur.close()
    conn.close()
    return JSONResponse(content = {"Message" : {"Name" : data[1], "Email Address" : data[2], "Phone number" : data[3]}}, status_code = 200)


@app.patch("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate):
    conn = psycopg2.connect(dbname = "first_db", user = "linao", password = "Linareda123")
    cur = conn.cursor()
    fields = []
    values = []

    if customer.name is not None:
        fields.append("name = %s")
        values.append(customer.name)
    if customer.email_address is not None:
        fields.append("email_address = %s")
        values.append(customer.email_address)
    if customer.phone_number is not None:
        fields.append("phone_number = %s")
        values.append(customer.phone_number)

    if fields:
        sql = "UPDATE Customers SET " + ", ".join(fields) + " WHERE customer_id = %s"
        values.append(customer_id)
        cur.execute(sql, tuple(values))
        conn.commit()
    cur.close()
    conn.close()
    return JSONResponse(content = {"Message" : "Customer Information Updated"}, status_code = 200)

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = psycopg2.connect(dbname = "first_db", user = "linao", password = "Linareda123")
    cur = conn.cursor()

    cur.execute("DELETE FROM Customers WHERE customer_id = %s" , (customer_id, ))

    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse(content = {"Message" : "Customer Information Deleted"}, status_code = 200)

#checks around if customers exist needed (extra safety checks/to be covered later) 
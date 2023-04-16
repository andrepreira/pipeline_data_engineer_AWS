import random
import os

import psycopg2
from faker import Faker
from dotenv import load_dotenv

import consts

def create_tables(cur):
    try:
        # create table Customers
        cur.execute("""CREATE TABLE IF NOT EXISTS Customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        );""")

        # create table Products
        cur.execute("""CREATE TABLE IF NOT EXISTS Products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10,2)
        );""")
        
        # create table Orders
        cur.execute("""CREATE TABLE IF NOT EXISTS Orders (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES Customers(id),
            product_id INTEGER REFERENCES Products(id),
            quantity INTEGER,
            total DECIMAL(10,2),
            status VARCHAR(20)
        );""")
        print("Tables created successfully")
    except Exception as e:
        print("Error while creating tables: {0}".format(e))
    return 0
        
        
def random_create_users(cur, conn, num_users, fake: Faker):
    customers = []
    try:
        # Insert random clients on Customers table
        for _ in range(num_users):
            name = fake.name()
            email = fake.email()
            cur.execute("INSERT INTO Customers (name, email) VALUES (%s, %s)", (name, email))
            customers.append(name)
        conn.commit()
        print("Customers created successfully")
    except Exception as e:
        print("Error while creating clients: {0}".format(e))
        
    if not customers:
        raise Exception("No customers created")
        
    products = consts.PRODUCTS
        
    categories = consts.CATEGORIES
    
    try:
        # Insert random products on Products table
        
        for i in range(len(products)):
            name = products[i]
            category = categories[i % len(categories)]
            price = round(random.uniform(50, 1000), 2)
            cur.execute(
                "INSERT INTO Products (name, category, price) VALUES (%s, %s, %s)", 
                (name, category, price)
            )
        conn.commit()
        print("Products created successfully")
    except Exception as e:
        print("Error while creating products: {0}".format(e))
    
    try:
        # Insert random orders on Orders table
        for _ in range(len(products)):
            customer_id = random.randint(1, len(customers))
            product_id = random.randint(1, len(products))
            quantity = random.randint(1, 5)
            cur.execute("SELECT price FROM Products WHERE id = %s", (product_id,))
            price = cur.fetchone()[0]
            total = round(quantity * price, 2)
            status = random.choice(['PENDING', 'APPROVED', 'REJECTED'])
            cur.execute(
                "INSERT INTO Orders (customer_id, product_id, quantity, total, status) VALUES (%s, %s, %s, %s, %s)",
                (customer_id, product_id, quantity, total, status)
            )
        conn.commit()
        print("Orders created successfully")
    except Exception as e:
        print("Error while creating orders: {0}".format(e))
    
    # close communication with the PostgreSQL database server
    cur.close()
    conn.close()        
        
if __name__ == "__main__":
    fake = Faker(locale='pt_BR')
    # environment variables
    load_dotenv(".env.dev.aws")
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect(
     host = os.environ.get('DB_HOST'),
     port = os.environ.get('DB_PORT'),
     database = os.environ.get('DB_NAME'),
     password = os.environ.get('DB_PASSWORD'),
     user= os.environ.get('DB_USER'),  
    )
    
    clients_number = os.environ.get('CLIENTS_NUMBER')
    
    if clients_number:
        clients_number = int(clients_number)
    else:
        raise Exception('Invalid clients_number')
    
    # create a exec cur for sql instructions
    cur = conn.cursor()
    create_tables(cur)
    random_create_users(cur, conn, clients_number, fake) 
    

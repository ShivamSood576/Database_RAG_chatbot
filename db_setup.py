import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv


load_dotenv()

def create_database():
    print("Step 1: Creating database...")
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD')
        )
        # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        db_name = os.getenv('DB_NAME', 'vosco')
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {db_name}')
            print(f"Created database '{db_name}'")
        else:
            print(f"Database '{db_name}' already exists")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(e)
        raise

def create_tables():
    print("Creating tables")
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'vosco'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD')
        )
        cursor = conn.cursor()
        
        # 1. Departments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            )
        """)
        print("Departments table ")
        
       
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department_id INT REFERENCES departments(id),
                email VARCHAR(255) UNIQUE,
                salary DECIMAL(10,2)
            )
        """)
        print("Employees table")
        
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2)
            )
        """)
        print("Products table")
        
        # 4. Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                employee_id INT REFERENCES employees(id),
                order_total DECIMAL(10,2),
                order_date DATE
            )
        """)
        print("✓Orders table ready")
        
        # Create indexes for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_employees_dept ON employees(department_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_employee ON orders(employee_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)")
        print("✓ Indexes created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Database done")
       
        
    except Exception as e:
        print(e)
        raise

if __name__ == "__main__":
    create_database()
    create_tables()

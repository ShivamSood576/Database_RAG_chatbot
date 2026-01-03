"""
Insert Sample Data & Create Embeddings
This script does two things:
1. Inserts sample data into PostgreSQL
2. Creates FAISS vector embeddings for semantic search
"""

import psycopg2
import os
from dotenv import load_dotenv
from datetime import date, timedelta
import faiss
import numpy as np
import pickle
from google import genai

# Load environment settings
load_dotenv()

# Setup Gemini API for embeddings
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# ==============================================================================
# EMBEDDING FUNCTIONS
# ==============================================================================

def get_embedding(text):
    """
    Convert text to a vector using Google Gemini
    Returns: 768-dimensional numpy array
    """
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return np.array(result.embeddings[0].values, dtype='float32')

def create_faiss_index(table_name, texts, ids):
    """
    Create FAISS index for fast similarity search
    
    Args:
        table_name: Name of the table (e.g., 'employees')
        texts: List of text strings to embed
        ids: List of corresponding database IDs
    """
    if len(texts) == 0:
        return
    
    print(f"  Creating embeddings for {table_name}...")
    
    # Generate embeddings for all texts
    embeddings = []
    for text in texts:
        emb = get_embedding(text)
        embeddings.append(emb)
    
    embeddings_array = np.array(embeddings, dtype='float32')
    
    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings_array)
    
    # Create FAISS index using Inner Product (cosine similarity)
    dimension = 768  # Gemini embedding size
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings_array)
    
    # Save index to disk
    os.makedirs("faiss_indexes", exist_ok=True)
    faiss.write_index(index, f"faiss_indexes/{table_name}.index")
    
    # Save metadata (IDs and texts)
    metadata = {'ids': ids, 'texts': texts}
    with open(f"faiss_indexes/{table_name}_metadata.pkl", 'wb') as f:
        pickle.dump(metadata, f)
    
    print(f"  ✓ Saved {len(texts)} embeddings for {table_name}")

# ==============================================================================
# DATABASE INSERTION
# ==============================================================================

def insert_sample_data():
    """Insert sample data and create vector embeddings"""
    
    print("Connecting to database...")
    
    # Connect to database
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'vosco'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = conn.cursor()
    
    print("\n1️⃣ Inserting Departments...")
    # Department data
    departments = [
        "Engineering",
        "Human Resources",
        "Sales",
        "Marketing",
        "Finance"
    ]
    
    dept_ids = {}
    dept_names = []
    dept_id_list = []
    
    for dept in departments:
        cursor.execute("""
            INSERT INTO departments (name) 
            VALUES (%s) 
            ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
            RETURNING id
        """, (dept,))
        dept_id = cursor.fetchone()[0]
        dept_ids[dept] = dept_id
        dept_names.append(dept)
        dept_id_list.append(dept_id)
    
    print(f"✓ Inserted {len(departments)} departments")
    create_faiss_index('departments', dept_names, dept_id_list)
    
    print("\n2️⃣ Inserting Employees...")
    # Employee data
    employees_data = [
        ("John Smith", "Engineering", "john.smith@company.com", 85000.00),
        ("Sarah Johnson", "Engineering", "sarah.j@company.com", 92000.00),
        ("Mike Davis", "Sales", "mike.d@company.com", 75000.00),
        ("Emily Brown", "Sales", "emily.b@company.com", 78000.00),
        ("David Wilson", "Marketing", "david.w@company.com", 70000.00),
        ("Lisa Anderson", "Marketing", "lisa.a@company.com", 72000.00),
        ("Robert Taylor", "Human Resources", "robert.t@company.com", 65000.00),
        ("Jennifer Martinez", "Finance", "jennifer.m@company.com", 88000.00),
        ("James Thomas", "Engineering", "james.t@company.com", 95000.00),
        ("Maria Garcia", "Sales", "maria.g@company.com", 76000.00),
    ]
    
    emp_ids = {}
    emp_names = []
    emp_id_list = []
    
    for name, dept, email, salary in employees_data:
        cursor.execute("""
            INSERT INTO employees (name, department_id, email, salary) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
            RETURNING id
        """, (name, dept_ids[dept], email, salary))
        emp_id = cursor.fetchone()[0]
        emp_ids[name] = emp_id
        emp_names.append(name)
        emp_id_list.append(emp_id)
    
    print(f"✓ Inserted {len(employees_data)} employees")
    create_faiss_index('employees', emp_names, emp_id_list)
    
    print("\n3️⃣ Inserting Products...")
    # Product data
    products_data = [
        ("Laptop Pro 15", 1299.99),
        ("Wireless Mouse", 29.99),
        ("Mechanical Keyboard", 149.99),
        ("USB-C Hub", 49.99),
        ("Monitor 27 inch", 399.99),
        ("Webcam HD", 89.99),
        ("Desk Lamp LED", 39.99),
        ("Office Chair", 299.99),
        ("Standing Desk", 599.99),
        ("Noise Cancelling Headphones", 249.99),
    ]
    
    product_names = []
    product_ids = []
    
    for name, price in products_data:
        cursor.execute("""
            INSERT INTO products (name, price) 
            VALUES (%s, %s)
            RETURNING id
        """, (name, price))
        prod_id = cursor.fetchone()[0]
        product_names.append(name)
        product_ids.append(prod_id)
    
    print(f"✓ Inserted {len(products_data)} products")
    create_faiss_index('products', product_names, product_ids)
    
    print("\n4️⃣ Inserting Orders...")
    # Customer names
    customers = [
        "Acme Corporation",
        "TechStart Inc",
        "Global Solutions Ltd",
        "Innovation Hub",
        "Digital Dynamics",
        "Future Systems",
        "Smart Tech Co",
        "Precision Engineering",
        "Data Insights LLC",
        "Cloud Services Pro"
    ]
    
    base_date = date.today() - timedelta(days=90)
    customer_names = []
    order_ids = []
    
    for i in range(20):
        customer = customers[i % len(customers)]
        employee_name = list(emp_ids.keys())[i % len(emp_ids)]
        order_total = round(100 + (i * 50.5), 2)
        order_date = base_date + timedelta(days=i*4)
        
        cursor.execute("""
            INSERT INTO orders (customer_name, employee_id, order_total, order_date) 
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (customer, emp_ids[employee_name], order_total, order_date))
        order_id = cursor.fetchone()[0]
        customer_names.append(customer)
        order_ids.append(order_id)
    
    print(f"✓ Inserted 20 orders")
    create_faiss_index('orders', customer_names, order_ids)
    
    # Commit all changes
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ SUCCESS! Database populated and embeddings created")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"  • Departments: {len(departments)}")
    print(f"  • Employees: {len(employees_data)}")
    print(f"  • Products: {len(products_data)}")
    print(f"  • Orders: 20")
    print(f"\n📁 Embeddings stored in: faiss_indexes/")
    print(f"\n🚀 Ready to run: streamlit run app.py")

if __name__ == "__main__":
    print("="*60)
    print("INSERT DATA & CREATE EMBEDDINGS")
    print("="*60)
    print()
    insert_sample_data()

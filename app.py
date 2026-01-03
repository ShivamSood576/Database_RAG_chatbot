"""
Natural Language Database Search
Ask questions in plain English and get SQL results + semantic search
"""

import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import re
import pandas as pd
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import faiss
import numpy as np
import pickle


load_dotenv()

gemini_client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

def get_embedding(text):
    """Convert text to vector using Gemini"""
    result = gemini_client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return np.array(result.embeddings[0].values, dtype='float32')

def search_similar(table_name, query_text, top_k=5):
    """
    Search for similar items using FAISS
    Returns: List of {id, text, similarity} dictionaries
    """
    try:
        index = faiss.read_index(f"faiss_indexes/{table_name}.index")
        with open(f"faiss_indexes/{table_name}_metadata.pkl", 'rb') as f:
            metadata = pickle.load(f)
        
        query_vector = get_embedding(query_text).reshape(1, -1)
        faiss.normalize_L2(query_vector)
        
        similarities, indices = index.search(query_vector, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(metadata['ids']):
                results.append({
                    'id': metadata['ids'][idx],
                    'text': metadata['texts'][idx],
                    'similarity': float(similarities[0][i])
                })
        
        return results
    except:
        return []


def get_db_connection():
    """Connect to PostgreSQL"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'vosco'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD')
    )

def run_query(sql):
    """Execute SQL query and return results"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in results]

def get_full_records(table_name, ids):
    if not ids:
        return []
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    if table_name == 'employees':
        cursor.execute("SELECT id, name, email, salary FROM employees WHERE id = ANY(%s)", (ids,))
    elif table_name == 'departments':
        cursor.execute("SELECT id, name FROM departments WHERE id = ANY(%s)", (ids,))
    elif table_name == 'products':
        cursor.execute("SELECT id, name, price FROM products WHERE id = ANY(%s)", (ids,))
    elif table_name == 'orders':
        cursor.execute("SELECT id, customer_name, order_total, order_date FROM orders WHERE id = ANY(%s)", (ids,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in results]

def initialize_llm():
    """Setup Google Gemini"""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.1
    )

def create_sql_from_question(question, llm):
    """Convert natural language to SQL using Gemini"""
    schema = """
    TABLES:
    - departments (id, name)
    - employees (id, name, department_id, email, salary)
    - products (id, name, price)
    - orders (id, customer_name, employee_id, order_total, order_date)
    
    RELATIONSHIPS:
    - employees.department_id → departments.id
    - orders.employee_id → employees.id
    """
    
    prompt = PromptTemplate(
        input_variables=["schema", "question"],
        template="""You are a SQL expert. Convert this question to PostgreSQL SQL.

DATABASE:
{schema}

RULES:
- Generate ONLY the SQL query
- Use JOINs when needed
- Only SELECT statements (no INSERT/UPDATE/DELETE)
- Add LIMIT 50 to avoid huge results

QUESTION: {question}

SQL:"""
    )
    
    # Create chain and run
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"schema": schema, "question": question})
    
    # Clean up the response
    sql = response.strip()
    sql = re.sub(r'```sql\n?', '', sql)  # Remove markdown
    sql = re.sub(r'```\n?', '', sql)
    return sql.strip()

def is_safe_sql(sql):
    """Check if SQL is safe (prevent injection)"""
    sql_upper = sql.strip().upper()
    sql_upper = re.sub(r'--.*$', '', sql_upper, flags=re.MULTILINE)
    
    dangerous = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 'TRUNCATE', 'EXEC']
    
    for keyword in dangerous:
        if keyword in sql_upper:
            return False, f"Blocked keyword: {keyword}"
    
    if not sql_upper.startswith('SELECT'):
        return False, "Only SELECT queries allowed"
    
    return True, "OK"

st.set_page_config(page_title="Natural Language Database Search", page_icon="🔍", layout="wide")

# Title
st.title("🔍 Natural Language Database Search")
st.markdown("Ask questions about your database in plain English!")

with st.sidebar:
    st.header("ℹ️ Information")
    
    if st.button("🔌 Test Connection"):
        try:
            conn = get_db_connection()
            conn.close()
            st.success("✓ Connected to database!")
        except Exception as e:
            st.error(f"✗ Connection failed: {e}")
    
    st.markdown("---")
    st.subheader("📝 Example Questions")
    st.markdown("""
    - Show all employees in Engineering
    - What's the average salary by department?
    - List top 5 highest paid employees
    - Show recent orders
    - Find products under $100
    - Count employees per department
    """)

st.markdown("---")

llm = initialize_llm()

col1, col2 = st.columns([4, 1])

with col1:
    user_question = st.text_input(
        "🗣️ Your question:",
        placeholder="e.g., Show me all employees in Sales department",
        key="question"
    )

with col2:
    search_btn = st.button("🔍 Search", type="primary", use_container_width=True)

if search_btn and user_question:
    try:
        st.info("🤖 Generating SQL with Gemini...")
        sql = create_sql_from_question(user_question, llm)
        st.code(sql, language='sql')
        
        safe, message = is_safe_sql(sql)
        if not safe:
            st.error(f"❌ Security check failed: {message}")
            st.stop()
        
        st.info("⚡ Running query...")
        sql_results = run_query(sql)
        
        st.success(f"✅ Found {len(sql_results)} results")
        
        if len(sql_results) > 0:
            st.subheader("📊 Query Results")
            df = pd.DataFrame(sql_results)
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                "results.csv",
                "text/csv"
            )
        else:
            st.info("No results found")
        
        st.info("🔍 Finding similar items...")
        question_lower = user_question.lower()
        
        if 'employee' in question_lower or 'staff' in question_lower:
            similar = search_similar('employees', user_question, top_k=5)
            if similar:
                st.subheader("🎯 Similar Employees (Semantic Search)")
                for item in similar[:3]:
                    records = get_full_records('employees', [item['id']])
                    if records:
                        rec = records[0]
                        st.write(f"**{rec['name']}** ({item['similarity']*100:.0f}% match)")
                        st.caption(f"Email: {rec['email']} | Salary: ${rec['salary']:,.2f}")
        
        elif 'department' in question_lower:
            similar = search_similar('departments', user_question, top_k=3)
            if similar:
                st.subheader("🎯 Similar Departments")
                for item in similar:
                    st.write(f"• {item['text']} ({item['similarity']*100:.0f}% match)")
        
        elif 'product' in question_lower:
            similar = search_similar('products', user_question, top_k=5)
            if similar:
                st.subheader("🎯 Similar Products")
                for item in similar[:3]:
                    records = get_full_records('products', [item['id']])
                    if records:
                        rec = records[0]
                        st.write(f"**{rec['name']}** - ${rec['price']} ({item['similarity']*100:.0f}% match)")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

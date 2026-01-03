# 🔍 Natural Language Database Search Interface

A powerful AI-powered search interface that lets you query PostgreSQL databases using plain English. Built with Streamlit, LangChain, and Google Gemini.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- **Natural Language Queries**: Ask questions in plain English
- **AI-Powered SQL Generation**: Google Gemini converts questions to SQL
- **Hybrid Search**: Combines SQL queries with vector similarity search
- **SQL Injection Protection**: Automatic query validation
- **Interactive UI**: Clean Streamlit interface with real-time results
- **Vector Embeddings**: FAISS-based semantic search
- **Export Results**: Download query results as CSV

## 📋 Database Schema

The system includes four main tables:

```
departments → employees ← orders
              ↓
           products
```

**Tables:**
- `departments` - Company departments (Engineering, Sales, HR, etc.)
- `employees` - Employee information with salary and department
- `products` - Product catalog with prices
- `orders` - Customer orders linked to employees

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Google Gemini API key (free at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nl-database-search.git
cd nl-database-search
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r req.txt
```

4. **Configure environment**

Copy `.env.example` to `.env` and add your credentials:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vosco
DB_USER=postgres
DB_PASSWORD=your_password

GOOGLE_API_KEY=your_gemini_api_key
```

5. **Set up database**
```bash
python db_setup.py
```

6. **Insert sample data**
```bash
python insert_sample_data.py
```

7. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 💬 Example Queries

Try these natural language questions:

**Employee Queries:**
- "Show all employees in Engineering"
- "List top 5 highest paid employees"
- "Who works in Sales department?"
- "What's the average salary by department?"

**Product Queries:**
- "Find products under $100"
- "Show all products"
- "What's the most expensive product?"

**Order Queries:**
- "Show recent orders from last 30 days"
- "Who handled the most orders?"
- "What's the total revenue?"

**Complex Queries:**
- "Show employees and their departments with average salary"
- "Count orders per employee in Sales department"

## 🏗️ Project Structure

```
nl-database-search/
├── app.py                   # Main Streamlit application
├── db_setup.py             # Database schema creation
├── insert_sample_data.py   # Sample data & embeddings
├── req.txt                 # Python dependencies
├── .env.example            # Environment template
├── .env                    # Your credentials (not in repo)
├── faiss_indexes/          # Vector embeddings storage
│   ├── employees.index
│   ├── departments.index
│   ├── products.index
│   └── orders.index
├── README.md               # This file
└── architecture.txt        # System architecture details
```

## 🔧 How It Works

1. **User Input**: You type a question in plain English
2. **SQL Generation**: Google Gemini LLM converts it to SQL
3. **Validation**: System checks for SQL injection attempts
4. **Execution**: Query runs on PostgreSQL database
5. **Vector Search**: FAISS finds semantically similar results
6. **Display**: Results shown in interactive table

See [architecture.txt](architecture.txt) for detailed system design.

## 🛡️ Security Features

- ✅ SQL injection prevention
- ✅ Query validation (only SELECT allowed)
- ✅ Dangerous keyword blocking
- ✅ Environment variable protection
- ✅ Safe query patterns only

## 🔍 Technologies Used

### Core
- **Python 3.8+** - Programming language
- **PostgreSQL** - Database
- **Streamlit** - Web interface

### AI & ML
- **Google Gemini** - LLM for SQL generation
- **LangChain** - LLM framework
- **FAISS** - Vector similarity search
- **NumPy** - Numerical operations

### Database
- **psycopg2** - PostgreSQL adapter
- **python-dotenv** - Environment management

## 📊 Sample Data

The system includes pre-populated sample data:
- 5 departments
- 10 employees
- 10 products
- 20 orders

Perfect for testing and demonstration!

## 🐛 Troubleshooting

### Database Connection Error
```
Error: connection failed
```
**Solution**: Verify PostgreSQL is running and credentials in `.env` are correct

### Gemini API Error
```
Error: invalid API key
```
**Solution**: Check your `GOOGLE_API_KEY` in `.env` file

### Import Error
```
ModuleNotFoundError: No module named 'X'
```
**Solution**: Run `pip install -r req.txt` again

### No Embeddings Found
```
Vector search unavailable
```
**Solution**: Run `python insert_sample_data.py` to create embeddings

## 🔄 Resetting Data

To clear and repopulate the database:

```bash
python db_setup.py
python insert_sample_data.py
```

## 📝 Requirements Satisfaction

✅ **Database Schema** - All 4 tables implemented exactly as specified  
✅ **Sample Data** - Populated with realistic test data  
✅ **Vector Embeddings** - FAISS storage (pgvector alternative)  
✅ **Natural Language** - Full NL to SQL conversion  
✅ **LLM Integration** - Google Gemini (GPT alternative)  
✅ **SQL Validation** - Comprehensive injection protection  
✅ **Hybrid Search** - SQL + Vector similarity  
✅ **Streamlit UI** - Input, button, results display  

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Built with ❤️ using LangChain, Google Gemini, and PostgreSQL

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- LangChain for LLM framework
- Streamlit for rapid UI development
- FAISS for vector search

## 📞 Support

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/nl-database-search/issues)
- 📖 Docs: [Wiki](https://github.com/yourusername/nl-database-search/wiki)

---

**⭐ If you find this project helpful, please give it a star!**

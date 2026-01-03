# Contributing to Natural Language Database Search

Thank you for considering contributing! 🎉

## 📋 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow

## 🚀 How to Contribute

### Reporting Bugs
1. Check if the bug already exists in [Issues](https://github.com/yourusername/nl-database-search/issues)
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version, etc.)

### Suggesting Features
1. Open an issue with tag `enhancement`
2. Describe the feature and use case
3. Explain why it would be useful

### Pull Requests

#### Setup Development Environment
```bash
git clone https://github.com/yourusername/nl-database-search.git
cd nl-database-search
python -m venv venv
venv\Scripts\activate
pip install -r req.txt
```

#### Making Changes
1. Create a new branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
   - Write clean, readable code
   - Add comments for complex logic
   - Follow existing code style

3. Test your changes
   ```bash
   python db_setup.py
   python insert_sample_data.py
   streamlit run app.py
   ```

4. Commit with clear messages
   ```bash
   git add .
   git commit -m "Add: feature description"
   ```

5. Push and create PR
   ```bash
   git push origin feature/your-feature-name
   ```

#### PR Guidelines
- ✅ Describe what changes you made
- ✅ Explain why these changes are needed
- ✅ Link related issues
- ✅ Test that everything works
- ✅ Update documentation if needed

## 🎯 Areas to Contribute

### Easy (Good First Issues)
- Improve error messages
- Add more example queries
- Update documentation
- Fix typos

### Medium
- Add new query types
- Improve UI styling
- Add query caching
- Performance optimizations

### Advanced
- Multi-database support
- Authentication system
- API endpoints
- Advanced analytics

## 📝 Coding Standards

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused

### Example
```python
def calculate_similarity(vector1, vector2):
    """
    Calculate cosine similarity between two vectors
    
    Args:
        vector1: First embedding vector
        vector2: Second embedding vector
    
    Returns:
        float: Similarity score (0-1)
    """
    # Implementation here
```

### Comments
- Explain WHY, not WHAT
- Use comments for complex logic
- Keep comments up-to-date

## 🧪 Testing

Before submitting:
1. Test all main features work
2. Try edge cases
3. Test on clean database
4. Verify no console errors

## 📚 Documentation

Update docs when you:
- Add new features
- Change existing behavior
- Add dependencies
- Change setup process

## 🎉 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Credited in commits

## 💬 Questions?

- Open a discussion on GitHub
- Ask in issues with `question` tag

## 🙏 Thank You!

Every contribution helps make this project better!

---
Happy coding! 🚀

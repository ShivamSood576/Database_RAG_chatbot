# Installing pgvector on Windows PostgreSQL 13

## Option 1: Using Pre-built Binary (Easiest)

1. Download pgvector for PostgreSQL 13 Windows:
   ```
   https://github.com/pgvector/pgvector/releases
   ```

2. Extract the files and copy:
   - `vector.dll` to `C:\Program Files\PostgreSQL\13\lib`
   - `vector.control` and `vector--*.sql` to `C:\Program Files\PostgreSQL\13\share\extension`

3. Restart PostgreSQL service:
   ```powershell
   Restart-Service postgresql-x64-13
   ```

## Option 2: Using pgvector-windows installer

1. Download from: https://github.com/pgvector/pgvector/releases
2. Look for Windows installer (.msi or .exe)
3. Run installer and select PostgreSQL 13

## Option 3: Build from Source (Advanced)

Requires Visual Studio and PostgreSQL development files - not recommended for quick setup.

## Verify Installation

After installation, run:
```powershell
python db_setup.py
```

It should show: ✓ pgvector extension enabled

## Quick Alternative: Skip pgvector

If installation is difficult, I can implement Python-based vector search (slower but works immediately).

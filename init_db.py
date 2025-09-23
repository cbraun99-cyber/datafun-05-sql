import sqlite3
import csv
import os

def initialize_database():
    """Initialize the SQLite database by reading from existing CSV files"""
    
    # Connect to SQLite database
    conn = sqlite3.connect('project.sqlite3')
    cursor = conn.cursor()
    
    # Create authors table (matches your CSV structure)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            author_id TEXT PRIMARY KEY,
            first TEXT NOT NULL,
            last TEXT NOT NULL
        )
    ''')
    
    # Create books table (matches your CSV structure)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            year_published INTEGER,
            author_id TEXT,
            FOREIGN KEY (author_id) REFERENCES authors(author_id)
        )
    ''')
    
    # Read and insert authors from CSV
    authors_file = os.path.join('data', 'authors.csv')
    with open(authors_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        authors_data = [(row['author_id'], row['first'], row['last']) for row in reader]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO authors (author_id, first, last)
        VALUES (?, ?, ?)
    ''', authors_data)
    
    # Read and insert books from CSV
    books_file = os.path.join('data', 'books.csv')
    with open(books_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        books_data = [(row['book_id'], row['title'], int(row['year_published']), row['author_id']) for row in reader]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO books (book_id, title, year_published, author_id)
        VALUES (?, ?, ?, ?)
    ''', books_data)
    
    conn.commit()
    
    # Verify the data was inserted correctly
    cursor.execute("SELECT COUNT(*) FROM authors")
    author_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"Database initialized successfully!")
    print(f"Authors inserted: {author_count}")
    print(f"Books inserted: {book_count}")

def query_database():
    """Run some sample queries to verify the data"""
    conn = sqlite3.connect('project.sqlite3')
    cursor = conn.cursor()
    
    print("\n=== Sample Data Verification ===")
    
    # Show first 3 authors
    cursor.execute("SELECT * FROM authors LIMIT 3")
    print("First 3 authors:")
    for row in cursor.fetchall():
        print(f"  {row}")
    
    # Show first 3 books
    cursor.execute("SELECT * FROM books LIMIT 3")
    print("\nFirst 3 books:")
    for row in cursor.fetchall():
        print(f"  {row}")
    
    # Show books with author names (JOIN example)
    cursor.execute('''
        SELECT b.title, b.year_published, a.first, a.last 
        FROM books b 
        JOIN authors a ON b.author_id = a.author_id 
        LIMIT 3
    ''')
    print("\nBooks with author names:")
    for row in cursor.fetchall():
        print(f"  '{row[0]}' ({row[1]}) by {row[2]} {row[3]}")
    
    conn.close()

if __name__ == "__main__":
    initialize_database()
    query_database()
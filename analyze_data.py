import sqlite3

def analyze_data():
    """Run analytical queries on the database"""
    conn = sqlite3.connect('project.sqlite3')
    cursor = conn.cursor()
    
    print("=== Database Analysis ===")
    
    # Count books per author
    cursor.execute('''
        SELECT a.first, a.last, COUNT(b.book_id) as book_count
        FROM authors a 
        LEFT JOIN books b ON a.author_id = b.author_id
        GROUP BY a.author_id
        ORDER BY book_count DESC
    ''')
    print("\nBooks per author:")
    for row in cursor.fetchall():
        print(f"  {row[0]} {row[1]}: {row[2]} book(s)")
    
    # Books by publication year range
    cursor.execute('''
        SELECT 
            CASE 
                WHEN year_published < 1900 THEN 'Before 1900'
                WHEN year_published BETWEEN 1900 AND 1949 THEN '1900-1949'
                WHEN year_published BETWEEN 1950 AND 1999 THEN '1950-1999'
                ELSE '2000 and later'
            END as period,
            COUNT(*) as book_count
        FROM books
        GROUP BY period
        ORDER BY MIN(year_published)
    ''')
    print("\nBooks by time period:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} book(s)")
    
    # Find duplicate authors (noticing you have J.R.R. Tolkien twice)
    cursor.execute('''
        SELECT first, last, COUNT(*) as count
        FROM authors
        GROUP BY first, last
        HAVING COUNT(*) > 1
    ''')
    duplicates = cursor.fetchall()
    if duplicates:
        print("\nDuplicate author entries found:")
        for row in duplicates:
            print(f"  {row[0]} {row[1]}: {row[2]} entries")
    
    conn.close()

if __name__ == "__main__":
    analyze_data()
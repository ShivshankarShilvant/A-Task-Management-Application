import sqlite3

def init_db():
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    # Create the table for tasks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Pending'
    )
    ''')
    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()
    
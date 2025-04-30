from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('tasks.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    tasks = connection.execute('SELECT * FROM tasks').fetchall()
    connection.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        connection = get_db_connection()
        connection.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    connection = get_db_connection()
    task = connection.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        
        connection.execute('UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?', (title, description, status, id))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    
    connection.close()
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:id>')
def delete(id):
    connection = get_db_connection()
    connection.execute('DELETE FROM tasks WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
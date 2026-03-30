from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Set the path to the DB file relative to this script
DB_FILE = os.path.join(os.path.dirname(__file__), 'memo.db')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS memo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB when the script starts
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # Only render the empty page initially without loading DB
    return render_template('index.html', memos=None)

@app.route('/save', methods=['POST'])
def save():
    content = request.form.get('content')
    if content and content.strip():
        conn = get_db_connection()
        conn.execute('INSERT INTO memo (content) VALUES (?)', (content.strip(),))
        conn.commit()
        conn.close()
    return redirect(url_for('load'))

@app.route('/load', methods=['GET'])
def load():
    conn = get_db_connection()
    memos = conn.execute('SELECT * FROM memo ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', memos=memos)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM memo WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('load'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

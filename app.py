from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Vercel 환경에서는 쓰기 가능한 /tmp 폴더로 데이터베이스 경로 변경
if os.environ.get('VERCEL') == '1':
    DB_FILE = '/tmp/memo.db'
else:
    DB_FILE = 'memo.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# DB 초기화 함수
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memo (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
    conn.commit()
    conn.close()

# 서버리스 환경(Vercel)에서는 구동 시마다 DB 초기화 필수
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    # 저장된 메모를 최신순으로 가져옵니다
    memos = conn.execute('SELECT * FROM memo ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', memos=memos)

@app.route('/save', methods=['POST'])
def save():
    content = request.form.get('content')
    if content:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO memo (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM memo WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    # 서버 실행 (로컬 호스트에서만 접근 가능)
    app.run(debug=True, port=5000)

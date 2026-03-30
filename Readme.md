요청하신 메모장 웹사이트 개발 방법을 **Markdown(MD)** 형식으로 정리해 드립니다. 초보자도 따라 하기 쉽도록 가장 대중적인 **Python(Flask) + SQLite** 조합을 기준으로 설명하겠습니다.

---

# 📝 심플 메모 웹 애플리케이션 개발 가이드

이 프로젝트는 텍스트를 입력하고 DB에 저장, 조회, 삭제하는 기능을 갖춘 웹 페이지 제작을 목표로 합니다.

## 1. 기술 스택 (Tech Stack)
* **Frontend**: HTML5, CSS3 (화면 구성 및 디자인)
* **Backend**: Python Flask (서버 로직)
* **Database**: SQLite (가벼운 파일 기반 데이터베이스)

---

## 2. 데이터베이스(DB) 설계
메모를 저장하기 위해 간단한 테이블 구조가 필요합니다. SQLite를 사용하여 `memo` 테이블을 생성합니다.

| 컬럼명 | 타입 | 설명 |
| :--- | :--- | :--- |
| **id** | Integer | 고유 번호 (Primary Key) |
| **content** | Text | 메모 내용 (2~3줄) |
| **created_at** | Timestamp | 생성 시간 |

---

## 3. 화면 디자인 (UI Structure)
요청하신 구조에 따라 직관적인 레이아웃을 구성합니다.



* **입력창**: `<textarea>` 태그를 사용하여 2~3줄 분량의 공간 확보.
* **버튼 그룹**: 저장, 불러오기, 삭제 버튼을 가로로 배치.
* **출력창**: 불러온 메모가 표시될 하단 영역.

---

## 4. 프로그램 작성 (Code Implementation)

### ① 프로젝트 구조
```text
memo_project/
├── app.py          (서버 코드)
├── memo.db         (DB 파일 - 자동생성)
└── templates/
    └── index.html  (화면 코드)
```

### ② Backend: `app.py`
```python
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DB 초기화 함수
def init_db():
    conn = sqlite3.connect('memo.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memo (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    content = request.form.get('content')
    if content:
        conn = sqlite3.connect('memo.db')
        c = conn.cursor()
        c.execute('INSERT INTO memo (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
    return redirect('/')

# 추가적인 '불러오기' 및 '삭제' 로직을 여기에 구현합니다.

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```

### ③ Frontend: `templates/index.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Simple Memo</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; padding-top: 50px; }
        .container { width: 300px; }
        textarea { width: 100%; height: 80px; margin-bottom: 10px; }
        .btn-group { display: flex; justify-content: space-between; }
        button { padding: 5px 15px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>My Memo</h2>
        <form action="/save" method="post">
            <textarea name="content" placeholder="메모를 입력하세요..."></textarea>
            <div class="btn-group">
                <button type="submit">저장</button>
                <button type="button">불러오기</button>
                <button type="button">삭제</button>
            </div>
        </form>
    </div>
</body>
</html>
```

---

## 5. 개발 순서 (Workflow)
1.  **환경 설정**: Python과 Flask 라이브러리를 설치합니다 (`pip install flask`).
2.  **파일 생성**: 위의 폴더 구조에 맞춰 코드를 복사합니다.
3.  **서버 실행**: 터미널에서 `python app.py`를 실행합니다.
4.  **확인**: 브라우저에서 `http://127.0.0.1:5000`에 접속합니다.

---

**다음 단계로 "불러오기" 기능을 눌렀을 때 DB의 데이터를 화면에 리스트로 뿌려주는 전체 코드를 완성해 드릴까요?**
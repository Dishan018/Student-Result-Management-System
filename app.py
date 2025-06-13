# app.py
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
conn = sqlite3.connect('results.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                marks INTEGER NOT NULL
            )''')
conn.commit()

@app.route('/')
def home():
    c.execute("SELECT * FROM results")
    data = c.fetchall()
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    subject = request.form['subject']
    marks = request.form['marks']
    c.execute("INSERT INTO results (name, subject, marks) VALUES (?, ?, ?)", (name, subject, marks))
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    c.execute("DELETE FROM results WHERE id=?", (id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, abort
import sqlite3
from pathlib import Path

DB_PATH = Path('todo.db')

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        ''')

@app.before_first_request
def setup():
    init_db()

@app.route('/tasks', methods=['GET'])
def list_tasks():
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM tasks').fetchall()
        tasks = [dict(row) for row in rows]
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        abort(400, description='"title" is required')
    with get_db() as conn:
        cur = conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
        task_id = cur.lastrowid
    return jsonify({'id': task_id, 'title': title, 'completed': 0}), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    with get_db() as conn:
        row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if row is None:
            abort(404)
        task = dict(row)
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    title = data.get('title')
    completed = data.get('completed')
    if title is None and completed is None:
        abort(400, description='nothing to update')
    with get_db() as conn:
        row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if row is None:
            abort(404)
        new_title = title if title is not None else row['title']
        new_completed = int(completed) if completed is not None else row['completed']
        conn.execute('UPDATE tasks SET title = ?, completed = ? WHERE id = ?',
                     (new_title, new_completed, task_id))
    return jsonify({'id': task_id, 'title': new_title, 'completed': new_completed})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with get_db() as conn:
        cur = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        if cur.rowcount == 0:
            abort(404)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

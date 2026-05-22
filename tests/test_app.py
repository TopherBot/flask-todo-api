import json
import pytest
from app import app, init_db, DB_PATH

@pytest.fixture
def client():
    # Ensure a clean DB for each test run
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()
    with app.test_client() as client:
        yield client

def test_create_and_get_task(client):
    # Create a task
    resp = client.post('/tasks', json={'title': 'Write tests'})
    assert resp.status_code == 201
    data = resp.get_json()
    task_id = data['id']

    # Retrieve the same task
    resp = client.get(f'/tasks/{task_id}')
    assert resp.status_code == 200
    task = resp.get_json()
    assert task['title'] == 'Write tests'
    assert task['completed'] == 0

def test_list_tasks(client):
    # Add two tasks
    client.post('/tasks', json={'title': 'Task 1'})
    client.post('/tasks', json={'title': 'Task 2'})
    # List tasks
    resp = client.get('/tasks')
    assert resp.status_code == 200
    tasks = resp.get_json()
    assert len(tasks) == 2

def test_update_task(client):
    resp = client.post('/tasks', json={'title': 'Old title'})
    task_id = resp.get_json()['id']
    # Update title and mark completed
    resp = client.put(f'/tasks/{task_id}', json={'title': 'New title', 'completed': True})
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated['title'] == 'New title'
    assert updated['completed'] == 1

def test_delete_task(client):
    resp = client.post('/tasks', json={'title': 'To delete'})
    task_id = resp.get_json()['id']
    resp = client.delete(f'/tasks/{task_id}')
    assert resp.status_code == 204
    # Verify it's gone
    resp = client.get(f'/tasks/{task_id}')
    assert resp.status_code == 404

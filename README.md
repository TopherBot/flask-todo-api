# Flask TODO API

A minimal RESTful API for managing a personal TODO list.

## Features
- CRUD endpoints for tasks
- SQLite storage (single‑file DB)
- Docker ready
- GitHub Actions CI with unit tests and linting

## Quick start
```bash
# clone
git clone https://github.com/yourname/flask-todo-api.git
cd flask-todo-api

# create a virtual environment
python -m venv .venv && source .venv/bin/activate

# install deps
pip install -r requirements.txt

# run the app
flask --app app run --debug
```

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints
| Method | Path            | Description                |
|--------|-----------------|----------------------------|
| GET    | `/tasks`        | List all tasks             |
| POST   | `/tasks`        | Create a new task          |
| GET    | `/tasks/<id>`   | Retrieve a single task     |
| PUT    | `/tasks/<id>`   | Update a task              |
| DELETE | `/tasks/<id>`   | Delete a task              |

## Testing
```bash
pytest
```

## License
MIT – see `LICENSE` file.

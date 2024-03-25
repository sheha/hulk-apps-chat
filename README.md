poetry install

export FLASK_APP=hulk_apps_chat
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

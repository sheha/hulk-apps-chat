poetry install
docker-compose up -d
export FLASK_APP=hulk_apps_chat
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

local development uses dockerized postgres and redis,
on heroku we use heroku's redis and postgres service, 
we control this through env variables DATABASE_URI and REDIS_URL



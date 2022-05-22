#!/usr/bin/env sh

echo 'Export flask app'
export FLASK_APP=api/v1/app.py
#flask run
export DB_URI="postgresql://yhpbilfwujdysg:1f3b0e3e3bdf11db470886bca71aaa0a6357820b81a743e0eb2410b0fe0e4398@ec2-34-242-8-97.eu-west-1.compute.amazonaws.com:5432/d48n23iroieiq3"
flask db migrate
flask db upgrade

#gunicorn --worker=2 api.v1.app:app

#!/bin/bash

cd "$(dirname "$0")"

echo "Installing pipenv for python3"
pip3 install pipenv

echo "Creating pipenv virtual enviroment and installing dependencies"
export PIPENV_VENV_IN_PROJECT=true
pipenv install

echo "Virtual enviroment created, dependencies from Pipfile installed"
echo "Enter virtual env. with \"pipenv shell\""
echo "Then start dev. webserver with \"python manage.py runserver\""
echo "Server will run on port 8000"
echo "Visit site on http://localhost:8000/"

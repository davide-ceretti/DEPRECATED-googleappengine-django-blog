# A simple Django Blog built on Google App Engine

Django Google App Engine integration provided by: https://github.com/potatolondon/djappengine

## System Requirements

Python 2.7
Google Appengine Python SDK 1.9.5

## Setup

    export PATH=$PATH:<path-to-google_appengine>

## Run locally

    ./serve.sh

App @ http://localhost:8080
DevEngine @ Visit http://localhost:8000

## Run tests

    ./test.sh

## Play with shell

    ipython -i shell.py

## Deploy

    appcfg.py update .

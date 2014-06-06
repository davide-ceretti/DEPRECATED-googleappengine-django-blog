# A simple Django Blog built on Google App Engine

The idea is to create a simple blog with Django on Google App Engine by using App Engine models.

I'm using the Django Google App Engine integration (https://github.com/potatolondon/djappengine), tweaked so that it runs with the latest SDK and it has a couple of additional features.

The blog is currently deployed at http://dav-ceretti.appspot.com/.

Note: in order to make the application work correctly you need a Blog record in the datastore. At the moment you are supposed to add it manually by using the shell or the dev engine page (Issue raised https://github.com/davide-ceretti/googleappengine-django-blog/issues/3).

## System Requirements

Python 2.7
Google Appengine Python SDK 1.9.5

## Setup

    export PATH=$PATH:<path-to-google_appengine>

## Run locally

    ./serve.sh

* App @ http://localhost:8080
* DevEngine @ http://localhost:8000

## Run tests

    ./test.sh

## Play with shell

    ./shell.py

## Deploy

    ./deploy.sh

## Play with remote shell

    ./remote_shell.sh

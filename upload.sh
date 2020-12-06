#!/usr/bin/bash
pipenv lock -r > requirements.txt
gcloud app deploy

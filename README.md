# Dependent task testing

This repository contains example code for running a test with dependent subtasks in celery. 

## Running example

See https://gist.github.com/halfak/277975af5de6153719e1985d06210a23 for example output.

1. `$ celery worker --app=dtt.celery_tasks --loglevel=INFO` starts the celery worker
2. `$ python generate_score_requests.py foo bar -d 0.1` starts the a requester

You'll want to start at least 2 requesters to ensure that the test demonstrates that 
in-progress tasks can be identified and that processing is not duplicated.

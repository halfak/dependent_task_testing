# Dependent task testing

This repository contains example code for running a test with dependent subtasks in celery. 

## Running example

See https://gist.github.com/halfak/277975af5de6153719e1985d06210a23 for example output.

1. `$ celery worker --app=dtt.celery_tasks --loglevel=INFO` starts the celery worker
2. `$ python generate_score_requests.py foo bar -d 0.1` starts the a requester

You'll want to start at least 2 requesters to ensure that the test demonstrates that 
in-progress tasks can be identified and that processing is not duplicated.

## The worker

```
$ python generate_score_requests.py -h
Generates 1000 sequential scoring requests against a celery worker

Usage: generate_score_requests <model-name>... [-d <secs>] [--start <i>] [--end <i>]
                                               [--shuffle]

Arguments:
    <model-name>  A comma-separated list a model names to score.

Options:
    -h --help          Prints this documentation
    -d --delay <secs>  Min delay between requests in seconds [default: 0.5]
    --start <i>        ID to start counting from scoring requests [default: 0]
    --end <i>          ID to end counting in scoring requests [default: 1000]
    --shuffle          Shuffle the order of IDs
```

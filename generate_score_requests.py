"""
Generates 1000 sequential scoring requests against a celery worker

Usage: generate_score_requests <model-name>... [-d <secs>]

Arguments:
    <model-name>  A comma-separated list a model names to score.

Options:
    -h --help          Prints this documentation
    -d --delay <secs>  Min delay between requests in seconds [default: 0.5]
"""
import time

import docopt

from dtt import celery_tasks


def main():
    args = docopt.docopt(__doc__)
    delay = float(args['--delay'])
    model_names = args['<model-name>']

    for rev_id in range(0, 1000):
        print("Processing fake rev_id {0}".format(rev_id))
        start = time.time()

        # Look for in-progress tasks
        print("Looking for in-progress tasks:")
        score_results = []
        missing_models = []
        for model_name in model_names:
            id_string = id_stringify(model_name, rev_id)
            print("\tChecking if {0} is already being processed..."
                  .format(id_string))
            model_result = celery_tasks.score_model.AsyncResult(id_string)
            if model_result.state not in ("SENT", "STARTED", "SUCCESS"):
                print("\tCould not find result for {0}".format(id_string))
                missing_models.append(model_name)
            else:
                print("\tFound in-progress result for {0}".format(id_string))
                score_results.append(model_result)

        # Start a scoring job for missing models
        if len(missing_models) > 0:
            print("Submitting scoring request...")
            models_result = \
                celery_tasks.score_many_models.apply_async(args=(model_names,))
            for model_name in model_names:
                model_result = celery_tasks.score_model.apply_async(
                    args=(models_result.id, model_name),
                    task_id=model_name + ":" + str(rev_id))
                score_results.append(model_result)
        else:
            print("No models need to be applied!")

        for model_result in score_results:
            score = model_result.get(timeout=15)
            print(model_result.id, score)

        duration = time.time() - start
        sleep_time = max(delay - duration, 0)
        print("Sleeping for remaining {0} seconds".format(sleep_time))
        time.sleep(sleep_time)
        print("\n")


def id_stringify(model_name, rev_id):
    return ":".join([model_name, str(rev_id)])


if __name__ == "__main__": main()

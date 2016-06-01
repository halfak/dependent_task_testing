from celery import Celery
from celery.signals import before_task_publish

from . import simple_ores

TIMEOUT = 15

app = Celery('celery_tasks', backend='redis://localhost',
             broker='redis://localhost')


@before_task_publish.connect
def update_sent_state(sender=None, body=None, **kwargs):

    task = app.tasks.get(sender)
    backend = task.backend if task else app.backend
    backend.store_result(body['id'], result=None, status="SENT")


@app.task
def score_many_models(model_names):
    return simple_ores.score_many_models(model_names)


@app.task
def score_model(models_task_id, model_name):
    models_result = score_many_models.AsyncResult(models_task_id)
    return simple_ores.score_model(
        models_result.get(timeout=TIMEOUT), model_name)

from flask import current_app
from flask_truss.async.base import celery_instance


@celery_instance.task(bind=True)
def _task(self):
    current_app.logger.info("I'm an example async task. Call me synchronously with _task() or asynchronously with "
                            "_task.delay().")

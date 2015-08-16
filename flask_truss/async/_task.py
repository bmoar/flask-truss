from flask_truss.async.base import celery_instance


@celery_instance.task(bind=True)
def _task(self):
    pass

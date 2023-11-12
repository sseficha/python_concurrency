import time

from celery import Celery

celery = Celery(__name__,
                broker='redis://redis:6379/0',
                backend='redis://redis:6379/0')


# simulate some intensive calculation
@celery.task
def add(x, y):
    time.sleep(10)
    return x + y

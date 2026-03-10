from celery import shared_task
import time

@shared_task
def add(x, y, seconds=0):
    time.sleep(seconds)
    return f"Result: {x + y} (slept: {seconds}s)"

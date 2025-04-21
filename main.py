import time

from prefect import flow, task
from prefect_ray import RayTaskRunner


@task
def source_task(source):
    time.sleep(10)
    print(source)


@task
def transform_task():
    time.sleep(5)
    print("transformation")


@task
def load_task():
    time.sleep(5)
    print("load")



@flow(task_runner=RayTaskRunner)
def main_flow():
    sources = ["A", "B", "C", "D"]
    source_futures = [source_task.submit(node) for node in sources]
    print(source_futures)
    transform_future = transform_task.submit(wait_for=source_futures)
    load_task.submit(wait_for=[transform_future])
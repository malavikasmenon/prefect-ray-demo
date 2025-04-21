from prefect import flow, task, Task
# from prefect.task_runners import RayTaskRunner

"""
DAG
E: source_1, source_2, source_3, source_4
T: transform_1
L: load_1
"""

def source_task(source):
    import time
    time.sleep(10)
    print(source)


@task
def transform_task():
    print("transformation")


@task
def load_task():
    pass



@flow()
def main_flow():
    sources = ["A", "B", "C", "D"]
    source_task_map = {node: Task(name=f"source_{node}", fn=source_task) for node in sources}
    source_futures_map = {
        node: source_task_map[node].submit(node) for node in sources
    }
    transform_task.submit(wait_for=source_futures_map.values())    
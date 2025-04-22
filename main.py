import time

from prefect import flow, task, get_run_logger
from prefect_ray import RayTaskRunner
from pyspark.sql import functions as F

from spark_session import get_spark_session


@task
def source_task(source):
    spark = get_spark_session()
    data = [("Alice", 34), ("Bob", 45), ("Charlie", 29)]
    df = spark.createDataFrame(data, ["name", "age"])
    df = df.withColumn('source', F.lit(source))
    df.write.mode("overwrite").option("header", True).parquet(f"source_{source}.parquet")
    get_run_logger().info(f"Source {source} completed.")
    


@task
def transform_task(sources):
    spark = get_spark_session()
    unioned_df = None
    for src in sources:
        src_df = spark.read.format("parquet").load(f"source_{src}.parquet")
        if unioned_df:
            unioned_df = unioned_df.union(src_df)
        else:
            unioned_df = src_df
    unioned_df.show()
    unioned_df.write.mode("overwrite").option("header", True).parquet(f"transformed.parquet")
    get_run_logger().info("Transformation completed.")


@task
def load_task():
    spark = get_spark_session()
    df =  spark.read.format("parquet").load(f"transformed.parquet")
    df.write.mode("overwrite").option("header", True).csv("output.csv")
    get_run_logger().info("Load to disk complete")



@flow(task_runner=RayTaskRunner)
def main_flow():
    sources = ["A", "B", "C", "D"]
    source_futures = [source_task.submit(node) for node in sources]
    print(source_futures)
    transform_future = transform_task.submit(sources, wait_for=source_futures)
    load_task.submit(wait_for=[transform_future])
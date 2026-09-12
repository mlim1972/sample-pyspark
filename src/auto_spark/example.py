"""Example PySpark usage for auto-spark project."""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def create_spark_session(app_name: str = "auto-spark") -> SparkSession:
    """Create and return a Spark session."""
    return (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )


def run_example() -> None:
    """Run a simple PySpark example."""
    spark = create_spark_session()
    
    try:
        # Create sample data
        data = [
            ("Alice", 25, "Engineering"),
            ("Bob", 30, "Marketing"),
            ("Charlie", 35, "Engineering"),
            ("Diana", 28, "Sales"),
            ("Eve", 32, "Engineering"),
        ]
        columns = ["name", "age", "department"]
        
        df = spark.createDataFrame(data, columns)
        
        print("=== Sample Data ===")
        df.show()
        
        # Filter engineers
        engineers = df.filter(F.col("department") == "Engineering")
        print("=== Engineers ===")
        engineers.show()
        
        # Average age by department
        avg_age = df.groupBy("department").agg(F.avg("age").alias("avg_age"))
        print("=== Average Age by Department ===")
        avg_age.show()
        
        print("PySpark version:", spark.version)
        print("Spark running successfully with Java 17!")
        
    finally:
        spark.stop()


if __name__ == "__main__":
    run_example()
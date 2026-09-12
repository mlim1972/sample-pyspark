"""Example PySpark usage with SQL syntax for auto-spark project."""

from pyspark.sql import SparkSession


def create_spark_session(app_name: str = "auto-spark-sql") -> SparkSession:
    """Create and return a Spark session."""
    return (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )


def run_sql_example() -> None:
    """Run PySpark examples using SQL syntax."""
    spark = create_spark_session()
    
    try:
        # Create sample data
        data = [
            ("Alice", 25, "Engineering", 90000),
            ("Bob", 30, "Marketing", 75000),
            ("Charlie", 35, "Engineering", 110000),
            ("Diana", 28, "Sales", 80000),
            ("Eve", 32, "Engineering", 95000),
            ("Frank", 29, "Marketing", 78000),
            ("Grace", 31, "Sales", 85000),
            ("Henry", 27, "Engineering", 88000),
        ]
        columns = ["name", "age", "department", "salary"]
        
        df = spark.createDataFrame(data, columns)
        
        # Register DataFrame as a temporary SQL view
        df.createOrReplaceTempView("employees")
        
        print("=== Sample Data (SQL) ===")
        spark.sql("SELECT * FROM employees").show()
        
        # Filter engineers using SQL WHERE clause
        print("=== Engineers (WHERE clause) ===")
        spark.sql("""
            SELECT name, age, salary 
            FROM employees 
            WHERE department = 'Engineering'
        """).show()
        
        # Aggregate with GROUP BY
        print("=== Average Age by Department (GROUP BY) ===")
        spark.sql("""
            SELECT department, AVG(age) as avg_age
            FROM employees
            GROUP BY department
        """).show()
        
        # Multiple aggregations
        print("=== Department Stats (Multiple Aggregations) ===")
        spark.sql("""
            SELECT 
                department,
                COUNT(*) as employee_count,
                AVG(age) as avg_age,
                AVG(salary) as avg_salary,
                MIN(salary) as min_salary,
                MAX(salary) as max_salary
            FROM employees
            GROUP BY department
        """).show()
        
        # Using HAVING clause
        print("=== Departments with Avg Salary > 85000 (HAVING) ===")
        spark.sql("""
            SELECT department, AVG(salary) as avg_salary
            FROM employees
            GROUP BY department
            HAVING AVG(salary) > 85000
        """).show()
        
        # ORDER BY
        print("=== Employees Ordered by Salary Desc ===")
        spark.sql("""
            SELECT name, department, salary
            FROM employees
            ORDER BY salary DESC
        """).show()
        
        # LIMIT
        print("=== Top 3 Highest Paid Employees (LIMIT) ===")
        spark.sql("""
            SELECT name, department, salary
            FROM employees
            ORDER BY salary DESC
            LIMIT 3
        """).show()
        
        # Subquery / CTE
        print("=== Engineers Above Average Salary (CTE) ===")
        spark.sql("""
            WITH eng_salaries AS (
                SELECT name, salary
                FROM employees
                WHERE department = 'Engineering'
            ),
            avg_eng_salary AS (
                SELECT AVG(salary) as avg_sal FROM eng_salaries
            )
            SELECT e.name, e.salary
            FROM eng_salaries e, avg_eng_salary a
            WHERE e.salary > a.avg_sal
        """).show()
        
        # CASE WHEN expression
        print("=== Salary Bands (CASE WHEN) ===")
        spark.sql("""
            SELECT 
                name,
                salary,
                CASE 
                    WHEN salary >= 100000 THEN 'Senior'
                    WHEN salary >= 85000 THEN 'Mid'
                    ELSE 'Junior'
                END as level
            FROM employees
            ORDER BY salary DESC
        """).show()
        
        print("PySpark version:", spark.version)
        print("SQL syntax examples completed successfully!")
        
    finally:
        spark.stop()


if __name__ == "__main__":
    run_sql_example()
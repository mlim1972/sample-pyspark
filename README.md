# sample-pyspark

A PySpark 3.5.3 project configured for Java 17, managed with [uv](https://github.com/astral-sh/uv).

## Requirements

- Python >= 3.11
- Java 17 (tested with Temurin-17.0.20)
- uv (for dependency management)

## Quick Start

### Install dependencies

```bash
uv sync
```

### Run the examples

```bash
# Method-chaining API example (DataFrame operations)
uv run python -m sample_pyspark.example

# SQL syntax example (using spark.sql)
uv run python src/sample_pyspark/sql_example.py
```

**Method-chaining API example** (`sample_pyspark.example`):
- Creates a DataFrame with sample employee data
- Filters for Engineering department employees
- Calculates average age by department

**SQL syntax example** (`sql_example.py`):
- Registers DataFrame as a temporary SQL view
- Demonstrates: WHERE, GROUP BY, HAVING, ORDER BY, LIMIT
- Shows CTEs (WITH clause), CASE WHEN expressions
- Multiple aggregations (COUNT, AVG, MIN, MAX)

### Start an interactive Spark session

```bash
uv run python -c "
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('test').master('local[*]').getOrCreate()
print('PySpark version:', spark.version)
spark.stop()
"
```

## Project Structure

```
sample-pyspark/
├── pyproject.toml          # Project configuration & dependencies
├── uv.lock                 # Locked dependencies
├── .python-version         # Python version (3.11)
├── src/
│   └── sample_pyspark/
│       ├── __init__.py     # Package entry point
│       ├── example.py      # Example PySpark usage (method-chaining API)
│       └── sql_example.py  # Example PySpark usage (SQL syntax)
└── .venv/                  # Virtual environment (created by uv)
```

## Development

### Add a new dependency

```bash
uv add <package-name>
```

### Add a development dependency

```bash
uv add --dev <package-name>
```

### Run tests (when added)

```bash
uv run pytest
```

### Format code

```bash
uv run ruff format .
```

### Lint code

```bash
uv run ruff check .
```

## Configuration

The project uses these Spark configurations by default (in `example.py`):

- `spark.sql.adaptive.enabled` - Enable adaptive query execution
- `spark.sql.adaptive.coalescePartitions.enabled` - Coalesce partitions adaptively
- `master("local[*]")` - Run locally with all available cores

## Compatibility Notes

| Component | Version |
|-----------|---------|
| Python    | >= 3.11 |
| PySpark   | 3.5.3   |
| Java      | 17      |
| py4j      | 0.10.9.7|

PySpark 3.5.x is compatible with Java 8, 11, and 17. This project uses Java 17.

## Troubleshooting

### "Unable to load native-hadoop library" warning

This is expected on macOS/ARM64 and doesn't affect functionality. Spark falls back to built-in Java classes.

### Hostname resolves to loopback address

Set `SPARK_LOCAL_IP` if you need to bind to a specific interface:

```bash
export SPARK_LOCAL_IP=127.0.0.1
uv run python -m sample_pyspark.example
```

## License

MIT
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max

# Start Spark session
spark = SparkSession.builder \
    .appName("F1TelemetryAggregation") \
    .getOrCreate()

# Read all telemetry CSVs into one DataFrame
df = spark.read.option("header", True).csv("telemetry_csv/*.csv")

# Convert numeric columns
df = df.withColumn("Speed", df["Speed"].cast("double")) \
       .withColumn("Distance", df["Distance"].cast("double"))

# Aggregate: average & max speed across all files
agg_df = df.agg(
    avg("Speed").alias("Avg_Speed"),
    max("Speed").alias("Max_Speed")
)

print("=== Aggregated Telemetry Metrics ===")
agg_df.show()

# Save results back to CSV
agg_df.coalesce(1).write.mode("overwrite").csv("aggregated_results")

spark.stop()

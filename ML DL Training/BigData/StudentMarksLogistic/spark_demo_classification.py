from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

# Initialize Spark
spark = SparkSession.builder \
    .appName("Live Spark ML Example - Logistic Regression") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Feature Assembler
assembler = VectorAssembler(
    inputCols=["temperature"],
    outputCol="features"
)

# TRAIN MODEL (RUNS ONLY ONCE)
def train_model():
    print("Training logistic regression model ONLY ONCE")

    # Example training data: temperature -> pass/fail
    # 1 = Pass, 0 = Fail
    train_data = spark.createDataFrame([
        (20.0, 0),  # too low, fail
        (25.0, 0),  
        (30.0, 1),  # optimal, pass
        (35.0, 1),
        (40.0, 1)   # high but acceptable, pass
    ], ["temperature", "label"])

    # Transform features
    train_features = assembler.transform(train_data)

    # Logistic Regression
    lr = LogisticRegression(
        featuresCol="features",
        labelCol="label"
    )

    return lr.fit(train_features)

# Train the model once
model = train_model()

# STREAMING DATA
schema = "timestamp STRING, temperature DOUBLE"

stream_df = spark.readStream \
    .schema(schema) \
    .csv("data/stream")  # same folder as your generator

feature_df = assembler.transform(stream_df)

# APPLY MODEL
predictions = model.transform(feature_df)

# Map numeric prediction to Pass/Fail
from pyspark.sql.functions import when

results = predictions.withColumn(
    "result",
    when(col("prediction") >= 0.5, "Pass").otherwise("Fail")
)

# STREAM TO CONSOLE
query = results.select(
    col("timestamp"),
    col("temperature"),
    col("result")
).writeStream \
 .outputMode("append") \
 .format("console") \
 .option("truncate", "false") \
 .option("numRows", 100) \
 .start()

query.awaitTermination()

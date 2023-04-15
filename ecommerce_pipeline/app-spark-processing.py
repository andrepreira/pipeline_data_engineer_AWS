import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# setup Spark
spark = SparkSession \
    .builder \
    .appName("job-1-spark") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

def read_csv(bucket, path):
    df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(f"s3a://{bucket}/{path}")
    print("\nPrint reading data from raw bucket")
    print(df.show(5))
    print("\nPrint reading dataframe schema from raw bucket")
    print(df.printSchema())
    return df

def read_delta(bucket, path):
    df = spark.read.format("delta") \
        .load(f"s3a://{bucket}/{path}")
    return df

def write_processed(df, bucket, path, data_format, mode):
    print("\nWriting raw data on processed layer..")
    try:
        df.write.format(data_format) \
            .mode(mode)\
            .save(f"{bucket}/{path}")
        print(f"Data written on s3a://{bucket}/{path}")
        return 0
    except Exception as err:
        print(f"Error on write data on s3a://{bucket}/{path}")
        print(err)
        return 1

def write_processed_partitioned(df, bucket, path, col_partition, data_format, mode):
    print("\nWriting raw data on processed layer..")
    try:
        df.write.format(data_format) \
            .partitionBy(col_partition) \
            .mode(mode) \
            .save(f"s3a://{bucket}/{path}")
        print(f"Data written on s3a://{bucket}/{path}")
        return 0
    except Exception as err:
        print(f"Error on write data on s3a://{bucket}/{path}")
        print(err)
        return 1

def write_curated(df, bucket, path, data_format, mode):
    print("\nWriting processed data on curated layer..")
    try:
        df.write.format(data_format) \
            .mode(mode) \
            .save(f"s3a://{bucket}/{path}")
        print(f"Data written on s3a://{bucket}/{path}")
        return 0
    except Exception as err:
        print(f"Error on write data on s3a://{bucket}/{path}")
        print(err)
        return 1
    
def process_table(table_name):
    print(f"Data from {table_name}.. \n")
    df = read_csv(bucket_raw, f"public/{table_name}/")
    
    #process data and write on processed layer
    write_processed(df, bucket_processed, f"{table_name}", "delta", "overwrite")
    
    #read processed data
    print(f"Reading data from s3a://{bucket_processed}/{table_name}")
    df = read_delta(bucket_processed, f"{table_name}")
    
    #Print database
    print(df.show())

if __name__ == "__main__":
    
    bucket_raw = os.environ.get('BUCKET_RAW')
    bucket_processed = os.environ.get('BUCKET_PROCESSED')
    bucket_curated = os.environ.get('BUCKET_CURATED')
    
    process_table("customers")
    process_table("products")
    process_table("orders")
        
    spark.stop()
    
import os

from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# environment variables
load_dotenv(str(os.getenv("PWD"))+"/env.dev")

RAW_DATA_BUCKET = os.getenv("RAW_DATA_BUCKET")
PROCESSED_DATA_BUCKET = os.getenv("PROCESSED_DATA_BUCKET")
CURATED_DATA_BUCKET = os.getenv("CURATED_DATA_BUCKET")

REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")

# Setup de aplicação spark
spark = SparkSession \
        .builder \
        .appName("job-1-spark") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

# logging level for spark [ ERROR, INFO]. Use INFO for dev
spark.sparkContext.setLogLevel("ERROR")

def read_csv(bucket, path):
    # Read data from Data Lake
    df = spark.read.format("csv") \
        .option("header", "True") \
        .option("inferSchema", "True") \
        .csv(f"s3a://{bucket}/{path}")
    print("\nImprime os dados lidos da raw:")
    print(df.show(5))
    print("\nImprime o schema do dataframe lido da raw:")
    print(df.printSchema())
    return df

def read_delta(bucket, path):
    df = spark.read.format("delta") \
        .load(f"s3a://{bucket}/{path}")
    return df

def write_processed(bucket, path, col_partition, data_format, mode):
    print(f"\nEscrevendo os dados lidso na raw para delta na processing zone..")
    try:
        df.write.format(data_format) \
            .partitionBy(col_partition) \
            .mode(mode) \
            .save(f"s3a://{bucket}/{path}")
        print(f"\nDados escritos na processed com sucesso!")
        return 0
    except Exception as e:
        print(f"\nFalha para escrever dados na processed: {e}")
        return 1

def write_curated(bucket,path,dataframe,data_format,mode):
    print(f"\nEscrevendo dados na curated zone..")
    try:
        dataframe.write.format(data_format) \
            .mode(mode) \
            .save(f"s3a://{bucket}/{path}")
        print(f"\nDados escritos na curated com sucesso!")
        return 0
    except Exception as e:
        print(f"\nFalha para escrever dados na curated: {e}")
        return 1

def write_redshifit(url_jdbc, table_name, dataframe):
    try:
        dataframe.write.format("jdbc") \
            .options(
                    url_jdbc=url_jdbc,
                    driver="com.amazon.redshift.jdbc42.Driver",
                    user=REDSHIFT_USER,
                    password=REDSHIFT_PASSWORD, 
                    table=table_name
            ) \
            .mode('overwrite') \
            .save()
        print(f"\nDados escritos na redshifit com sucesso!")
        return 0
    except Exception as e:
        print(f"\nFalha para escrever dados na redshifit: {e}")
        return 1

def analytics_tables(bucket,dataframe,table_name,flag_write_redshift,url_jdbc):
    dataframe.createOrReplaceTempView(table_name)
    
    df_query1 = dataframe.groupby("name")\
                .agg(sum("circulating_supply").alias("circulating_supply")) \
                .sort(desc("circulating_supply")) \
                .limit(10)
    df_query2 = dataframe.select(col('name'), col('symbol'), col('price')) \
                .sort(desc("price")) \
                .limit(10)
    print("\nTop 10 Cryptomoedas com maior fornecimento de circulação no mercado\n")
    print(df_query1.show())
    print("\nTop 10 Cryptomoedas com maior preço mais altos no mercad\n")
    print(df_query2.show())
    write_curated(f"{bucket}", "coins_circulating_supply",df_query1, "delta", "overwrite")
    write_curated(f"{bucket}", "top10_price_2022",df_query2, "delta", "overwrite")
    
    
    if flag_write_redshift == True:
        write_redshifit(url_jdbc,"coins_circulating_supply",df_query1)
        write_redshifit(url_jdbc,"top10_price_2022",df_query2)

# Ler os dados da raw
df = read_csv(f's3a://{RAW_DATA_BUCKET}', 'public/coins/')

df = df.withColumn("year", year(df.data_added))

write_processed(f's3a://{PROCESSED_DATA_BUCKET}', 'tb_coins', "year", "delta", "overwrite")

df = read_delta(f's3a://{PROCESSED_DATA_BUCKET}', 'tb_coins')

flag_write_redshift = True
url_jdbc = "jdbc:redshift://redshift-cluster-1.cufcxu0ztur8.us-east-1.redshift.amazonaws.com:5439/dev"
analytics_tables(F"s3a://{CURATED_DATA_BUCKET}",df,"tb_coins",flag_write_redshift,url_jdbc)

spark.stop()
#!/bin/bash

DNS_SPARK=hadoop@ec2-15-229-147-122.sa-east-1.compute.amazonaws.com
PATH_TO_FILE=app-spark-processing.py

# Copy the file to the Spark server
scp -i ~/.ssh/key-ssh-pipeline-ecommerce.pem -v $PATH_TO_FILE $DNS_SPARK:.

# Connect to the Spark server
ssh -i ~/.ssh/key-ssh-pipeline-ecommerce.pem $DNS_SPARK << EOF

# Submit the Spark job
spark-submit --packages io.delta:delta-core_2.12:2.0.0 \
--conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
--conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
app-spark-processing.py

EOF

# Implementation

#### Follow the below Steps to Implement the pipeline ####


I have a created a lambda function (on Python 3.2) to mock the Apache logs and produce the stream of logs as this lambda function is triggered every 1 min. Web Logs Generator function directly delivers the output to the Kinesis Data Firehose delivery system, which in-turn collects and stores the logs in a configured S3 buckets. 

##### Batch Processing #####
In the S3 bucket the logs are stored as csv file in YEAR/MONTH/DAY/HOUR folder based on the timestamp when the logs are generated. Now AWS Glue a fully managed ETL service is used to create Data Catalog convert these csv logs to extract metadata, cleanse and store in more optimize format like parquet in another S3 bucket. Once these logs are in S3, Athena a serverless interactive query service can be used to analyse the data using standard SQL.  

##### Realtime Processing #####
For the Realtime processing pipeline, I have created Kinesis Analysis application on top of Kinesis data firehose creating the stream of the Apache logs. A pre-processor lambda function is triggered evetime each stream is delivered from the firehose. This pre-processor created the json output in a set schema as accepted by the Kinesis Analysis application referred as Kinesis Data Firehose Request Data Model. Detail can be found at this AWS link. Now in the Kinesis Data analytics application, I have created stream using the SQL editor to create multiple scripts one of them is aggregating the web logs and the other stream to detect the anomaly in the stream using the random_cut_forest function provided by out of the box by AWS. This stream can then be fed into a lambda, which in turn can trigger Amazon Simple Notification Service (SNS). In this implementation, I have persisted the aggregated stream via a delivery firehose stream to a redshift table.

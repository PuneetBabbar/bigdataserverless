# Implementation

#### Follow the below Steps to Implement the pipeline ####


The first step is to create a lambda function (on Python 3.2) to mock the Apache logs and produce the stream of logs. Copy the code from this file [Web Logs Generator function](https://github.com/PuneetBabbar/bigdataserverless/blob/master/web_log_gen_func.py) and create a lambda function, choose Python 3.2 as the language. This lambda function will be triggered every 1 min and we need to create a cron job with the help of CloudWatch. The delivery of this lambda function will to the _Kinesis Data Firehose delivery system_. Follow these simple instructions on [AWS doc](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/event-publishing-kinesis-analytics-firehose-stream.html) to create a _Kinesis Data Firehose delivery system_ to a _raw logs_ S3 bucket. This delivery stream will stores the logs on the S3, configured when we the Firehose delivery stream is created.  

__Note__  : Add the Lambda Layer to provide the import libaries to execute all the lambda function. In the *Layer* section of the AWS labda function add this [zip file](https://github.com/PuneetBabbar/bigdataserverless/blob/master/lambda-layer/python.zip) 

##### Batch Processing #####
In the S3 bucket the logs are stored as csv file in YEAR/MONTH/DAY/HOUR folder based on the timestamp when the logs are generated. Now the next step is to run the AWS Glue data crawler over this S3 bucket. AWS Glue is a fully managed ETL service, and will be used to create Data Catalog. Glue will help to convert these csv logs to extract metadata, glue will crawl your data sources and construct your Data Catalog using pre-built classifiers. So this will create a _raw log table_ in the console of Glue. Now we want to convert this raw data present in the csv format in the _raw logs_ S3 bucket and tranform into a _target logs_ S3 bucket.  

cleanse and store in more optimize format like parquet in another S3 bucket. Once these logs are in S3, Athena a serverless interactive query service can be used to analyse the data using standard SQL.  

##### Realtime Processing #####
For the Realtime processing pipeline, I have created Kinesis Analysis application on top of Kinesis data firehose creating the stream of the Apache logs. A pre-processor lambda function is triggered evetime each stream is delivered from the firehose. This pre-processor created the json output in a set schema as accepted by the Kinesis Analysis application referred as Kinesis Data Firehose Request Data Model. Detail can be found at this AWS link. Now in the Kinesis Data analytics application, I have created stream using the SQL editor to create multiple scripts one of them is aggregating the web logs and the other stream to detect the anomaly in the stream using the random_cut_forest function provided by out of the box by AWS. This stream can then be fed into a lambda, which in turn can trigger Amazon Simple Notification Service (SNS). In this implementation, I have persisted the aggregated stream via a delivery firehose stream to a redshift table.

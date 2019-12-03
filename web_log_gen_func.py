
import os
import time
import datetime
import random
import json
import boto3
from faker import Faker
from tzlocal import get_localzone
local = get_localzone()
faker = Faker()

response = ["200", "404", "500", "301"]
verb = ["GET", "POST", "DELETE", "PUT"]
resources = ["/list", "/wp-content", "/wp-admin", "/explore", "/search/tag/list", "/app/main/posts", "/posts/posts/explore", "/apps/cart.jsp?appID="]
ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]
template = '{} - - [{} {}] "{} {} HTTP/1.0" {} {} "{}" "{}"'
timestr = time.strftime("%Y%m%d-%H%M%S")
firehose = boto3.client('firehose')

def lambda_handler(event, context):
    delivery_stream = os.environ['DELIVERY_STREAM']
    max_records = int(os.environ['MAX_RECORDS'])
    records = []
    #this will return 10 seconds
    max_ms = 10 * 1000

    while True:
        #getting the current remaining time
        remain_ms = context.get_remaining_time_in_millis() 
        #Checking if time is less than 10 seconds
        records.append({'Data': get_apache_log_entry() })

        if len(records) >= max_records:
            try:
                send_to_kinesis(records, delivery_stream)
                records = []
            except Exception as ex:
                print(ex)

        if remain_ms < max_ms:
            try:
                send_to_kinesis(records, delivery_stream)
                break
            except Exception as ex:
                print(ex)
                records=[]

def send_to_kinesis(data, stream_name):
    res = firehose.put_record_batch(DeliveryStreamName=stream_name, Records=data)
    print("Response from firehose put_record_batch is: %s" % res)

def get_apache_log_entry():
    otime = datetime.datetime.now()
    ip = faker.ipv4()
    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(local).strftime('%z')
    vrb = random.choice(verb)
    uri = random.choice(resources)

    if uri.find("apps") > 0:
        uri += str(random.randint(1000, 10000))

    resp = random.choice(response)
    byt = int(random.gauss(5000, 50))
    referer = faker.uri()
    useragent = random.choice(ualist)()
    res = template.format(ip, dt, tz, vrb, uri, resp, byt, "-", useragent)
    print(res)
    return res

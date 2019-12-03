from __future__ import print_function

import base64
import json
import re
from dateutil.parser import parse
from datetime import datetime, tzinfo, timedelta

print('Loading function')

def lambda_handler(event, context):
    output = []
    succeeded_record_cnt = 0
    failed_record_cnt = 0

    safe_string_to_int = lambda x: int(x) if x.isdigit() else x

    for record in event['records']:
        print(record['recordId'])
        payload = base64.b64decode(record['data'])
        print(payload)
        p = re.compile(r"^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] \"(\S+)\s?(\S+)?\s?(\S+)?\" (\d{3}|-) (\d+|-)\s?\"?([^\"]*)\"?\s?\"?([^\"]*)?\"?$")
        m = p.match(payload)
        if m:
            succeeded_record_cnt += 1

            ts = m.group(4)
            try:
                d = parse(ts.replace(':', ' ', 1))
                ts = d.isoformat()
            except:
                print('Parsing the timestamp to date failed.')

            data_field = {
                'host_address': m.group(1),
                'request_time': ts,
                'request_method': m.group(5),
                'request_path': m.group(6),
                'request_protocol': m.group(7),
                'response_code': m.group(8),
                'response_size': m.group(9),
                'referrer_host': m.group(10),
                'user_agent': m.group(11)
            }

            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(json.dumps(data_field))
            }
        else:
            print('Parsing failed')
            failed_record_cnt += 1
            output_record = {
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            }

        output.append(output_record)

    print('Processing completed.  Successful records {}, Failed records {}.'.format(succeeded_record_cnt, failed_record_cnt))
    return {'records': output}

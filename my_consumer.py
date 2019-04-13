import boto3
import time
import sys

stream_name = 'wildrydes'
r = boto3.client('kinesis', region_name='us-west-2')


try:
    response = r.describe_stream(StreamName=stream_name)

    status = response['StreamDescription']['StreamStatus']

    if status == 'ACTIVE':
        print('Shard is active')
        shard_id = response['StreamDescription']['Shards'][0]['ShardId']
        shard_itr = r.get_shard_iterator(StreamName=stream_name, ShardId=shard_id, ShardIteratorType="LATEST")['ShardIterator']
        while True:
                    out = r.get_records(ShardIterator=shard_itr, Limit=2)
                    for o in out["Records"]:
                        print (o["Data"])
                    #helps with throttling so that you don't get ProvisionedThroughputExceededException
                    time.sleep(0.5)

                    shard_itr = out["NextShardIterator"]

except:
        print(sys.exc_info())

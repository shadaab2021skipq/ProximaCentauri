import boto3

s3 = boto.client('s3')

def lambda_bucket(event, context):
    
    s3_client = boto3.client("s3")
    bucket_name = 'Adeelskipq'
    file = 'URLS.txt'
    response_of_bucket = s3.get_object(Bucket=bucket_name,Key=file)
    data = response_of_bucket['Body']
    jObj = json.loads(data.read())
    listUrl = []
    for a in range(len(jObj)):
        listUrl[a] = jObj['link'+str(a+1)]
    print(listUrl)
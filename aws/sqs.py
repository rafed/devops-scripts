import boto3

# Create SQS client
sqs = boto3.client(
    'sqs',
    region_name='eu-west-1',
    aws_access_key_id='',
    aws_secret_access_key=''
)

queue_url = ''

response = sqs.send_message(
    QueueUrl=queue_url,
    DelaySeconds=10,
    MessageAttributes={
        'Title': {
            'DataType': 'String',
            'StringValue': 'The Whistler'
        },
        'Author': {
            'DataType': 'String',
            'StringValue': 'John Grisham'
        },
    },
    MessageBody=(
        'Information about current NY Times fiction bestseller for '
        'week of 12/11/2016.'
    )
)

print(response)
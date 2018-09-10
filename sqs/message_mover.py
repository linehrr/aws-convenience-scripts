conf = {
  "sqs-access-key": "",
  "sqs-secret-key": "",
  "reader-sqs-queue": "",
  "writer-sqs-queue": "",
  "message-group-id": ""
}

import boto3
client = boto3.client(
	'sqs',
        aws_access_key_id       = conf.get('sqs-access-key'),
        aws_secret_access_key   = conf.get('sqs-secret-key')
)

while True:
	messages = client.receive_message(QueueUrl=conf['reader-sqs-queue'], MaxNumberOfMessages=10, WaitTimeSeconds=10)

	if 'Messages' in messages:
		for m in messages['Messages']:
			print(m['Body'])
			ret = client.send_message( QueueUrl=conf['writer-sqs-queue'], MessageBody=m['Body'], MessageGroupId=conf['message-group-id'])
			print(ret)
			client.delete_message(QueueUrl=conf['reader-sqs-queue'], ReceiptHandle=m['ReceiptHandle'])
	else:
		print('Queue is currently empty or messages are invisible')
		break

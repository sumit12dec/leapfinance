from extractor.utils.aws import ACCESS_KEY_ID, SECRET_ACCESS_KEY
import boto3
import json


def get_boto_client(resource, access_key, server_secret_key, region_name='us-east-1'):
	client = boto3.client(resource, 
			aws_access_key_id=access_key, 
                      aws_secret_access_key=server_secret_key, 
		region_name=region_name)
	return client

def get_item(url_id):
	print(type(url_id), "url_id")
	response = {}
	client = get_boto_client('dynamodb', ACCESS_KEY_ID, SECRET_ACCESS_KEY)
	key = {'url_id':{'N': str(url_id)}}
	response = client.get_item(TableName='leap_finance', 
						Key=key)

	if response:
		response = format_response(response)
	return response


def invoke_lambda(link, url_id):
	aws_lambda = get_boto_client('lambda', ACCESS_KEY_ID, SECRET_ACCESS_KEY)
	response = aws_lambda.invoke(
	FunctionName='crawl-it',
	InvocationType='Event',
	Payload=json.dumps({'request_url': link, 'url_id': url_id}),)

	return response

def unpack_aggregate(D):
	l = []
	for o in D.get('L'):
		l.append(o['S'])
	return l

def format_response(response):
	print(response, "response")
	data = {}
	
	if 'Item' in response:
		item = response.get('Item')

		# data[''] = 
		data['title'] = item.get('title').get('S')
		data['text'] = item.get('text').get('S').strip()
		# data['html'] = item.get('html').get('S')

		data['all_links'] = unpack_aggregate(item.get('all_links'))

		data['all_emails'] = unpack_aggregate(item.get('all_emails'))
		data['meta_keywords'] = item.get('meta_keywords').get('S')
		data['meta_desc'] = item.get('meta_desc').get('S')
		data['images'] = unpack_aggregate(item.get('images'))
		data['url_id'] = item.get('url_id').get('N')
		data['s3_link'] = item.get('s3_link').get('S')
	else:
		data["error"] = "In Process"

	return data






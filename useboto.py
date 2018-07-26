import boto3
import botocore

def botodownload(filename):
	BUCKET_NAME = 'armandolicurgodasilva' # replace with your bucket name
	KEY = filename # replace with your object key
	s3 = boto3.resource('s3')
	try:
		print("botodownload",filename)
		s3.Bucket(BUCKET_NAME).download_file(KEY, filename)
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("The object does not exist.")
		else:
			raise


def botoupload(filename, filedata):
	# Let's use Amazon S3
	s3 = boto3.resource('s3')
	for bucket in s3.buckets.all():
		print(bucket.name)
	data = open(filename, 'rb')
	s3.Bucket('armandolicurgodasilva').put_object(Key=filename, Body=data)
	return True


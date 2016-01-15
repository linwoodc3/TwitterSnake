#Import twitter api packages
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
#Import AWS SDKs
import boto3, botocore
#Import standard packages
import json, time, sys, os

#Write the access tokens and consumer tokens from your Twitter Appliation in these fields
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

#CUSTOM EXCPEPTIONS TO BE USED WITH STREAM

#This exception is thrown when the twitter api sends us an HTTP Error 420, which means we are being rate limited
class RateLimit(Exception):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return repr(self.value)


#This is the generic exception to be thrown when there is some kind of error that we need to react to
class HttpErr(Exception):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return repr(self.value)

#CUSTOM EXCEPTIONS END


#StdListener Class ####################################################################
#	 	Input: None, is implementing the StreamListener Class		      #
#		Output: Boolean on error, otherwise output tweets to .json file       #
#										      #
#		Listens for events from twitter streaming API and reacts appropriately#
#######################################################################################
class StdListener(StreamListener):
	def __init__(self, fprefix = 'streamer'):
		self.counter = 0
		self.fprefix = fprefix
		self.fileName = fprefix+'.'+time.strftime('%Y%m%d-%H%M%S')+'.json'
		self.output  = open(self.fileName,'w')
		self.delout  = open('delete.txt', 'a')

		self.s3 = boto3.resource('s3')

	def on_data(self, data):
		if  'id_str' in data:
			self.on_status(data)
		elif 'delete' in data:
			delete = json.loads(data)['delete']['status']
			if self.on_delete(delete['id'], delete['user_id']) is False:
				return False
		elif 'limit' in data:
			if self.on_limit(json.loads(data)['limit']['track']) is False:
				return False
		elif 'warning' in data:
			warning = json.loads(data)['warnings']
			print(warning['message'])
			return False

	def on_status(self, status):
		self.output.write(status + "\n")

		self.counter += 1
		if (self.counter%200==0):
			print(self.counter)
		if self.counter >= 20000:
			self.output.close()
			self.s3.meta.client.upload_file(self.fileName,'twitterharvestdctweets',self.fileName)
			#Once uploaded to S3, delete the file locally
			os.remove(self.filename)
			self.fileName = fprefix+'.'+time.strftime('%Y%m%d-%H%M%S')+'.json'
			self.output = open(self.fileName, 'w') 
			self.counter = 0

		return

	def on_delete(self, status_id, user_id):
		self.delout.write( str(status_id) + "\n")
		return

	def on_limit(self, track):
		#sys.stderr.write("Rate limit on " + track + " tweets\n")
		raise RateLimit(track)

	def on_error(self, status_code):
		#sys.stderr.write('Error: ' + str(status_code) + "\n")
		raise HttpErr(status_code)
		return False

	def on_timeout(self):
		sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
		time.sleep(60)
		return 

if __name__ == '__main__':

	l = StdListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth,l)

	backoff_network_error = 0.25
	backoff_http_error = 5
	backoff_rate_limit = 60

	while True:
		try:
			stream.filter(locations=(-77.212600708,38.7840634951,-76.8335723877,39.0229179452))	
			
			#No Exceptions, reset timers
			backoff_network_error = 0.25
			backoff_http_error = 5
			backoff_rate_limit = 60
		except RateLimit as e:
			print("Rate limit on " + e.value + " tweets\n")
			time.sleep(backoff_rate_limit)
			backoff_rate_limit *= 2
		except HttpErr as e:
			print('Http Error: ' + str(e.value) + "\n")
			print("Waiting {0} secs...".format(backoff_http_error))
			time.sleep(backoff_http_error)
			backoff_http_error = min(backoff_http_error * 2, 320)
		except:
			#Network error, linear back off
			print("Waiting {0} seconds before reconnect".format(backoff_network_error))
			time.sleep(backoff_network_error)
			backoff_network_error = min(backoff_network_error + 1, 16)
			continue


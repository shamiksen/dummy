import json
import urllib
from urllib2 import Request, urlopen
from md5 import md5


def lambda_handler(event, context):
	for message in event['Records']:
		payload = message['body']
		payload = json.loads(payload)
		app = payload['app']
		salt = payload['app_salt']
		del payload['app_salt']
		del payload['app']
		payload['add_links'] = json.dumps(payload['add_links'])
		payload['other'] = json.dumps(payload['other'])
		payload['hash'] = hash_generator(payload, salt)
		url = 'http://e90e3702.ngrok.io/notifier/subscribe/?app=' + app
		headers = {"content-type": "application/x-www-form-urlencoded;charset=UTF-8", "cache-control": "no-cache"}
		request = Request(url, urllib.urlencode(payload), headers)
		response = urlopen(request, timeout=120)


def hash_generator(request, app_salt):
	dict_keys = request.keys()
	hash_to_check = md5('|'.join([str(request[item]) for item in sorted(dict_keys)]) + "|" + app_salt).hexdigest()
	return hash_to_check


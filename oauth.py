import os
import sys
import time
import json
import requests

def eprint(*args, **kwargs):
    print("\033[31m")
    print(*args, file=sys.stderr, **kwargs)
    print("\033[0m")

def getToken(client_id, client_secret, rate_limit):
	url = "https://api.intra.42.fr"
	delay = 1 / rate_limit
	if not client_id or not client_secret:
		eprint("Invalid Credentials")
		os._exit(1)
	data = {
		'grant_type': 'client_credentials',
		'client_id': client_id,
		'client_secret': client_secret
	}
	time.sleep(delay)
	r = requests.post(url + "/oauth/token", data=data)
	if not r.status_code or r.status_code < 200 or r.status_code > 299:
		eprint("Couldn't get the token")
		os._exit(1)
	token = json.loads(r.content)['access_token']
	if len(token) != 64:
		eprint("Something went wrong with the token")
		os._exit(1)
	return token

def revokeToken(token, rate_limit):
	url = "https://api.intra.42.fr"
	delay = 1 / rate_limit
	data = {
		'token': token
	}
	headers = {
		'Accept': 'application/json',
		'Authorization': 'Bearer ' + str(token)
	}
	time.sleep(delay)
	r = requests.post(url + "/oauth/revoke", headers=headers, data=data)
	if not r.status_code or r.status_code < 200 or r.status_code > 299:
		eprint("Couldn't revoke the token")
		os._exit(1)

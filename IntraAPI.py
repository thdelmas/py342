import sys
import json
import time
import unidecode
from datetime import datetime
import requests
from . import oauth

class intraAPI:
	__url = "https://api.intra.42.fr/"
	headers = {}

	def __init__(self, client_id, client_secret, campus_id, scopes="", rate_limit=1):
		self.__token = oauth.getToken(client_id, client_secret, rate_limit)
		print(self.__token)
		self.rate_limit = rate_limit
		self.delay = 1 / rate_limit
		self.campus_id = campus_id

	def get(self, endpoint, headers=None, params=None, json=None):
		time.sleep(self.delay)
		r = requests.get(self.__url + endpoint, headers=headers, params=params, json=json)
		return r

	def delete(self, endpoint, headers=None, params=None, json=None):
		time.sleep(self.delay)
		r = requests.delete(self.__url + endpoint, headers=headers, params=params, json=json)
		return r

	def post(self, endpoint, headers=None, params=None, json=None):
		time.sleep(self.delay)
		r = requests.post(self.__url + endpoint, headers=headers, params=params, json=json)
		return r

	def patch(self, endpoint, headers=None, params=None, json=None):
		time.sleep(self.delay)
		r = requests.patch(self.__url + endpoint, headers=headers, params=params, json=json)
		return r

	def closeConnection(self):
		oauth.revokeToken(self.__token, self.rate_limit)

	def getPrimaryCampusUsers(self):
		users = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {
			"filter[primary_campus_id]": self.campus_id
		}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/users", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				users.append(i)
			page += 1
		return users
	
	def getCursusUsers(self, login):
		cursus_users = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/users/" + login + "/cursus_users", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				cursus_users.append(i)
			page += 1
		return cursus_users

	def hasCursus(self, login, cursus_ids, begin_at, end_at):
		cursus_users = self.getCursusUsers(login)
		xp = 0
		for i in cursus_users:
			if i['cursus']['id'] in cursus_ids:
				if i['begin_at']:
					if i['begin_at'] >= begin_at and i['begin_at'] <= end_at:
						return True
					if i['begin_at'] < begin_at and not i['end_at']:
						return True
				if i['end_at']:
					if i['end_at'] >= begin_at and i['end_at'] <= end_at:
						return True
				if i['begin_at'] and i['end_at']:
					if i['begin_at'] < begin_at and i['end_at'] > end_at:
						return True
		return False


	def getUserExperiences(self, login):
		experiences = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/users/" + login + "/experiences", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				experiences.append(i)
			page += 1
		return experiences

	def amountEarnedXP(self, login, cursus_ids, begin_at, end_at):
		experiences = self.getUserExperiences(login)
		xp = 0
		for i in experiences:
			if i['cursus_id'] in cursus_ids:
				if i['created_at']:
					if i['created_at'] >= begin_at and i['created_at'] <= end_at:
						xp += i['experience']
		return xp

	def getUserEvaluationsAsEvaluator(self, login):
		evaluations = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/users/" + login + "/scale_teams/as_corrector", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				evaluations.append(i)
			page += 1
		return evaluations

	def amountEvaluationsAsEvaluator(self, login, cursus_ids, begin_at, end_at):
		evals = self.getUserEvaluationsAsEvaluator(login)
		evalNb = 0
		for i in evals:
			if i['filled_at']:
				if i['filled_at'] >= begin_at and i['filled_at'] <= end_at:
					evalNb += 1
		return evalNb

	def getUserEvaluationsAsEvaluated(self, login):
		evaluations = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/users/" + login + "/scale_teams/as_corrected", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				evaluations.append(i)
			page += 1
		return evaluations

	def amountEvaluationsAsEvaluated(self, login, cursus_ids, begin_at, end_at):
		evals = self.getUserEvaluationsAsEvaluated(login)
		evalNb = 0
		for i in evals:
			if i['filled_at']:
				if i['filled_at'] >= begin_at and i['filled_at'] <= end_at:
					evalNb += 1
		return evalNb

	def getInternships(self, login, internships_ids):
		filterProject = ""
		for i in internships_ids:
			filterProject += str(i) + ","
		filterProject = filterProject[:-1]
		internships = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {
			'filter[project_id]': filterProject
		}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/users/" + login + "/projects_users", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				internships.append(i)
			page += 1
		return internships

	def isIntern(self, login, internships_ids, begin_at, end_at):
		internships = self.getInternships(login, internships_ids)
		for i in internships:
			if i['created_at']:
				if i['created_at'] >= begin_at and i['created_at'] <= end_at:
					return True
			if i['marked_at']:
				if i['marked_at'] >= begin_at and i['marked_at'] <= end_at:
					return True
		return False

	def getCampusJournal(self, begin_date, end_date):
		events = []
		jsObj = None
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		jsdata = {
			"begin_at": begin_date,
			"end_at": end_date,
		}
		r = self.post("/v2/campus/"+ str(self.campus_id) +"/journal", headers=headers, params=params, json=jsdata)
		jsObj = json.loads(r.content.decode("utf-8"))
		for i in jsObj:
			events.append(i)
		return events

	def amountDaysConnnected(self, user_id, journal):
		connected = 0
		previousDay = None
		for i in journal:
			if not previousDay or previousDay != i['event_at']:
				if str(i['user_id']) == str(user_id):
					if str(i['reason']) == "Used intranet":
						connected += 1
						previousDay = i['event_at']
		print("-> did connect " + str(connected) + " times to the intranet")
		return connected

	def isActiveUser(self, user_id, login, cursus_ids, internships_ids, begin_date, end_date, journal):
		if not self.hasCursus(login, cursus_ids, begin_date, end_date):
			print(login + " doesn't have required cursus")
			return False
		if self.amountEarnedXP(login, cursus_ids, begin_date, end_date) >= 1:
			print(login + " has earned xp")
			return True
		if self.amountEvaluationsAsEvaluator(login, cursus_ids, begin_date, end_date) >= 1:
			print(login + " did an evaluation")
			return True
		if self.amountEvaluationsAsEvaluated(login, cursus_ids, begin_date, end_date) >= 1:
			print(login + " was evaluated")
			return True
		if self.isIntern(login, internships_ids, begin_date, end_date):
			print(login + " was intern")
			return True
		if self.amountDaysConnnected(user_id, journal) >= 15:
			print(login + " did connect 15 times to the intranet")
			return True
		print(login + " didn't match criterias")
		return False

	def getActiveUsers(self, cursus_ids, internships_ids, begin_date, end_date):
		activeUsers = []
		print("Getting Users list")
		print("Between: " + begin_date + " & " + end_date)
		journal = self.getCampusJournal(begin_date, end_date)
		users = self.getPrimaryCampusUsers()
		for i in users:
			sys.stdout.flush()
			print(i['login'])
			if self.isActiveUser(i['id'], i['login'], cursus_ids, internships_ids, begin_date, end_date, journal):
				print(i['login'] + " is active")
				activeUsers.append(i)
		return activeUsers

	def getPoolUsers(self, pool_month, pool_year):
		pool_users = []
		print("Getting Users list pool " + str(pool_month) + " " + str(pool_year))
		users = self.getPrimaryCampusUsers()
		for i in users:
			if i["pool_year"] and i["pool_month"]:
				if str(i["pool_year"]) == str(pool_year) and i["pool_month"].lower() == pool_month.lower():
					pool_users.append(i)
		return pool_users

	def getUsersKickoff(self, pool_month, pool_year):
		ko_users = []
		print("Getting Users list pool " + str(pool_month) + " " + str(pool_year))
		users = self.getPrimaryCampusUsers()
		for i in users:
			if i["pool_year"] and i["pool_month"]:
				if i["pool_year"] == pool_year and i["pool_month"].lower() == pool_month.lower():
					ko_users.append(i)
		return ko_users

	def getUserCoalitions(self, login):
		coas = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/users/" + login + "/coalitions_users", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				coas.append(i)
			page += 1
		return coas
	
	def removeCoalitions(self, users):
		jsObj = None
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		jsdata = {
			"has_coalition": False,
		}
		for i in users:
			print("Remove Coalition for: " + str(i["login"]))
			params = {
				"filter[cursus_id]": 21
			}
			r = self.get("/v2/users/" + str(i["login"]) + "/cursus_users", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			if not jsObj:
				continue
			cursusUser_id = jsObj[0]["id"]
			coaUser = self.getUserCoalitions(i["login"])
			for j in coaUser:
				print("DELETING COA")
				print(j)
				r = self.delete("/v2/coalitions_users/" + str(j["id"]), headers=headers)
				print(r)
			r = self.patch("/v2/cursus_users/" + str(cursusUser_id), headers=headers, params=params, json=jsdata)
			print(r)

	def getLogin(self, user_id):
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		r = self.get("/v2/users/" + str(user_id), headers=headers, params=params)
		jsObj = None
		jsObj = json.loads(r.content.decode("utf-8"))
		return jsObj['login']

	def getUserId(self, login):
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		r = self.get("/v2/users/" + login, headers=headers, params=params)
		jsObj = None
		jsObj = json.loads(r.content.decode("utf-8"))
		return jsObj['id']

	def getQuestsUsers(self, login):
		quests_users = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/users/" + login + "/quests_users", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				quests_users.append(i)
			page += 1
		return quests_users

	def createPatronage(self, nephew, godfather):
		if isinstance(nephew, str):
			nephew = self.getUserId(nephew)
		if isinstance(godfather, str):
			godfather = self.getUserId(godfather)
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		jsObj = {
		"patronage": {
		"godfather_id": godfather,
		"user_id": nephew
			}
		}
		print(jsObj)
		r = self.post("/v2/patronages/", headers=headers, params=params, json=jsObj)
		jsObj = json.loads(r.content.decode("utf-8"))
		return jsObj

	def createCursusUser(self, user_id, cursus_id, begin_at):
		if isinstance(user_id, str):
			user_id = self.getUserId(user_id)
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		jsObj = {
		"cursus_user": {
			"user_id": user_id,
			"begin_at": begin_at,
			"blackholed_at": None,
	        "cursus_id": cursus_id,
    	    "skip_begin_validation": "true"
			}
		}
		print(jsObj)
		r = self.post("/v2/cursus_users/", headers=headers, params=params, json=jsObj)
		jsObj = json.loads(r.content.decode("utf-8"))
		return jsObj

	def deleteQuestsUser(self, questsUserId):
		print("Deleting Quest User: " + str(questsUserId))
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		r = self.delete("/v2/quests_users/" + str(questsUserId), headers=headers)
		print(r)

	def deleteCursusUser(self, cursusUserId):
		print("Deleting Quest User: " + str(cursusUserId))
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		jsObj = {
		"cursus_user": {
			"begin_at": "2422-01-10T09:00:00.000Z"
			}
		}
		print("Patch Begin_at")
		r = self.patch("/v2/cursus_users/" + str(cursusUserId), headers=headers, json=jsObj)
		print(r)
		print("Deletion")
		r = self.delete("/v2/cursus_users/" + str(cursusUserId), headers=headers, json=jsObj)
		print(r)

	def createQuestsUser(self, user_id, quest_id, validated_at):
		if isinstance(user_id, str):
			user_id = self.getUserId(user_id)
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		jsObj = {
			"quests_user": {
				"user_id": user_id,
				"quest_id": quest_id,
				"validated_at": validated_at,
				}
		}
		print(jsObj)
		r = self.post("/v2/quests_users/", headers=headers, params=params, json=jsObj)
		jsObj = json.loads(r.content.decode("utf-8"))
		return jsObj
	
	def createUser(self, body):
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		if 'email' in body and not body['email']:
			print("\033[0;31mCannot Create User without email\033[0;0m")
			return False
		if not 'kind' in body or not body['kind']:
			body['kind'] = 'external'
		if not 'campus_id' in body or not body['campus_id']:
			body['campus_id'] = self.campus_id
		if not 'pool_year' in body or not body['pool_year']:
			body['pool_year'] = datetime.today().year
		if not 'pool_month' in body or not body['pool_month']:
			body['pool_month'] = datetime.now().strftime("%B")
		if not 'first_name' in body or not body['first_name']:
			body['first_name'] = "Joy"
		else:
			body['first_name'] = unidecode.unidecode(body['first_name'])
		if not 'last_name' in body or not body['last_name']:
			body['last_name'] = "Doe"
		else:
			body['last_name'] = unidecode.unidecode(body['last_name'])
		if not 'staff?' in body or not body['staff?']:
			body['staff?'] = False
		jsObj = {
			"user": body
		}
		print(jsObj)
		r = self.post("/v2/users/", headers=headers, params=params, json=jsObj)
		jsObj = json.loads(r.content.decode("utf-8"))
		return jsObj

	def getCampusEvents(self):
		events = []
		jsObj = None
		page = 1
		headers = {
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + str(self.__token),
		}
		params = {}
		while page == 1 or \
		(r.status_code >= 200 and r.status_code < 300) and \
		int(r.headers['X-Per-Page']) * page <= int(r.headers['X-Total']):
			params['page'] = str(page)
			r = self.get("/v2/campus/" + self.campus_id + "/events", headers=headers, params=params)
			jsObj = json.loads(r.content.decode("utf-8"))
			for i in jsObj:
				events.append(i)
			page += 1
		return events

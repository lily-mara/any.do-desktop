#!/usr/bin/python3
from anydo.api import AnyDoAPI
from anydo.error import AnyDoAPIError
from getpass import getpass
import json

def main():
	user_info = get_un_pw()
	api = get_api(user_info)
	task_list = get_task_list(api)
	print_tasks(task_list)

def prompt_for_api():
	"""
	Prompts the user for a username and password, then returns
	the pair of strings given by the user as a tuple.
	"""
	username = input('What is your Any.do username? ')
	password = getpass('What is your Any.do password? ')

	return (username, password)

def get_api(user_info):
	"""
	Takes a tuple containing the user's information (username, password)
	and returns an AnyDoAPI object. If the username/password is wrong,
	or there is an authentication error, re-prompt for username/password.
	"""
	try:
		api = AnyDoAPI(user_info[0], user_info[1])
		return api
	except AnyDoAPIError:
		print('Invalid login')
		return prompt_for_api()

def get_task_list(api):
	"""
	returns a dict containing all tasks
	"""
	return api.get_all_tasks()

def print_tasks(task_list):
	"""
	Iterates through the list of tasks and prints the tiele of each
	task separated by newlines and numbered.
	"""
	print()
	print('Task list:')
	task_names = [i['title'] for i in task_list]
	for i in range(len(task_names)):
		task_names[i] = str(i + 1) + '. ' + task_names[i]
	print('\n'.join(task_names))
	print()

def get_un_pw():
	"""
	Parses the data file anydo.json for a user's saved info
	and returns a tuple containing the username and password
	from said data file.
	"""
	try:
		with open('anydo.json') as json_file:
			user_info = json.load(json_file)
		return (user_info['username'], user_info['password'])
	except FileNotFoundError:
		return prompt_for_api()

if __name__ == '__main__':
	main()

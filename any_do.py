#!/usr/bin/python3
from anydo.api import AnyDoAPI
from anydo.error import AnyDoAPIError
from getpass import getpass
from datetime import datetime
from time import strftime
from time import localtime
import json

api = ''
task_dict = {}

def main():
	global api
	global task_dict

	user_info = get_un_pw()
	api = get_api(user_info)
	task_dict = get_task_dict(api)

	task_names = [i['title'] for i in task_dict]

	print_tasks(task_names)

	while True:
		print(task_info(get_task_by_prompt(task_dict)))
		print()

def get_task_by_prompt(task_dict):
	index_str  = input('Enter a task number: ')
	try:
		index = int(index_str) - 1
		return task_dict[index]
	except ValueError:
		if index_str == 'exit':
			exit()
		print('Invalid Input!')
		print()
		return get_task_by_prompt(task_dict)

def task_info(task):
	epoch_creation = int(str(task['creationDate'])[:-3])
	datetime_creation = datetime.fromtimestamp(epoch_creation).strftime('%Y-%m-%d')


	info_string = 'Title: ' + task['title'] + '\n'
	info_string += 'Created on: ' + str(datetime_creation) + '\n'
	if task['status'] == 'UNCHECKED':
		info_string += 'Not '
	info_string += 'Done'

	return info_string

def prompt_for_api():
	"""
	Prompts the user for a username and password, then returns
	the pair of strings given by the user as a tuple.
	"""
	username = input('What is your Any.do username? ')
	password = getpass('What is your Any.do password? ')

	user_info = (username, password)

	save_info(user_info)

	return user_info

def save_info(user_info):
	"""
	prompts the user to save their information with a
	simple y/n prompt. If the user enters yes, it is saved
	as a file 'anydo.json'
	"""
	username = user_info[0]
	password = user_info[1]

	save = input('Would you like to save these credentials? (y/n) ')
	if save.lower() == 'y':
		userdata = {'username': username, 'password': password}
		with open('anydo.json', 'w') as outfile:
			json.dump(userdata, outfile)

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

def get_task_dict(api):
	"""
	returns a dict containing all tasks
	"""
	return api.get_all_tasks()

def print_tasks(task_names):
	"""
	Iterates through the list of tasks and prints the tiele of each
	task separated by newlines and numbered.
	"""
	print()
	print('Task list:')
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

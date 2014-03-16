#!/usr/bin/python3
from anydo.api import AnyDoAPI
from anydo.error import AnyDoAPIError
from getpass import getpass
from datetime import datetime
from time import strftime
import json
import sys

api = ''
task_dict = {}

def main():
	print_tasks(setup_tasks())
	print()

	while True:
		print(task_info(get_task()))
		print()

def setup_tasks():
	global task_dict

	setup_api()

	task_dict = get_task_dict(api)
	return [i['title'] for i in task_dict]

def setup_api():
	global api

	user_info = get_un_pw()
	api = get_api(user_info)

def get_task(index=None):
	"""
	Returns the task at the given index as a dict. If no task is given,
	prompt the user for a task.
	"""
	if index == None:
		index_str = input('Enter a task number: ')
		try:
			index = int(index_str) - 1
			return task_dict[index]
		except ValueError:
			if index_str == 'exit':
				sys.exit(0)
			elif 'delete' in index_str:
				delete_task(index_str)
			elif index_str == 'ls':
				print_tasks(setup_tasks())
			else:
				print('Invalid Input!')
			print()
			return get_task()
	else:
		return task_dict[index]


def delete_task(delete_string):
	"""
	Takes a delete command in the format 'delete (int)' and deletes that
	task from the server. Prompts the user for confirmation.
	"""
	try:
		delete_int = int(delete_string.split(' ')[1]) - 1
		response = input('Delete task: ' + task_dict[delete_int]['title'] + '? ')
		if response.lower() == 'y' or response.lower() == 'yes':
			api.delete_task_by_id(get_task(delete_int)['id'])
	except ValueError:
		print('You provided an incorrect delete command!')

def task_info(task):
	"""
	Returns a string containing all important info about the given task.
	"""
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

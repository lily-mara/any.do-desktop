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
	username = input('What is your Any.do username? ')
	password = getpass('What is your Any.do password? ')

	if '@' not in username:
		username += '@gmail.com'

	return (username, password)

def get_api(user_info):
	try:
		api = AnyDoAPI(user_info[0], user_info[1])
		return api
	except AnyDoAPIError:
		print('Invalid login')
		return prompt_for_api()

def get_task_list(api):
	return api.get_all_tasks()

def print_tasks(task_list):
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

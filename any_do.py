from anydo.api import AnyDoAPI
from anydo.error import AnyDoAPIError
from getpass import getpass

def main():
	print_tasks(get_task_list())

def get_task_list():
	username = input('What is your Any.do username? ')
	password = getpass('What is your Any.do password? ')

	if '@' not in username:
		username += '@gmail.com'

	try:
		api = AnyDoAPI(username, password)
		return api.get_all_tasks()
	except AnyDoAPIError:
		print('Invalid login')
		return get_task_list()

def print_tasks(task_list):
	print()
	print('Task list:')
	task_names = [i['title'] for i in task_list]
	for i in range(len(task_names)):
		task_names[i] = str(i + 1) + '. ' + task_names[i]
	print('\n'.join(task_names))
	print()

if __name__ == '__main__':
	main()

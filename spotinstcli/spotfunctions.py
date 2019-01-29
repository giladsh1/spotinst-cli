#!/usr/bin/env python

try:
	# native
	from json import loads as json_loads, dumps as json_dumps
	from commands import getoutput, getstatusoutput
	from threading import Thread
	from pkg_resources import DistributionNotFound
	from collections import OrderedDict
	from sys import stdout, exit as sys_exit
	# 3rd party
	from prettytable import PrettyTable
	from requests import put, get, post, delete
	from PyInquirer import prompt
	from clint.textui import colored, puts
except ImportError:
	print "Error while importing packages - please install all of the required packages in requirements.txt"
	sys_exit(1)


# This function opens a thread with args
def open_thread(thread_list, thread_target, thread_args):
	t = Thread(target=thread_target, args = (thread_args))
	t.daemon = True
	t.start()
	thread_list.append(t)


# This function prints error and exits
def error_and_exit(exception_message):
	print "\nERROR - %s\n" %(exception_message)
	exit()


# This function prints a text in color and returns to normal
def print_in_color(color, msg):
	if color == 'red':
		puts(colored.red(msg))
	elif color == 'green':
		puts(colored.green(msg))


# This function prints a group name
def print_header(text):
	text_len = len(text)
	print "\n" + ("-" * text_len)
	print text
	print ("-" * text_len)


# This function queries spotinst API endpoint and returns the result to a queue
def query_thread(queue, group, api_url, spotinst_token, http_method='GET', req_payload=None, account=None):
	try:
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer %s' % spotinst_token,
		}
		if account is not None:
			api_url = "{api_url}?accountId={account}".format(**locals())

		result = ""
		if http_method == 'GET':
			result = get(api_url, headers=headers)
		elif http_method == 'PUT':
			result = put(api_url, headers=headers, data=req_payload)
		elif http_method == 'POST':
			result = post(api_url, headers=headers, data=req_payload)
		elif http_method == 'DELETE':
			result = delete(api_url, headers=headers, data=req_payload)
		else:
			error_and_exit("wrong http method: {http_method}".format(**locals()))
		queue.append([http_method, result, group])
	except Exception as e:
		error_and_exit(e.message)


# This function queries spotinst API endpoint
def query_api(api_url, spotinst_token, http_method='GET', req_payload=None, account=None):
	try:
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer %s' % spotinst_token,
		}
		if account is not None:
			api_url = "{api_url}?accountId={account}".format(**locals())

		if http_method == 'GET':
			return get(api_url, headers=headers)
		elif http_method == 'PUT':
			return put(api_url, headers=headers, data=req_payload)
		elif http_method == 'POST':
			return post(api_url, headers=headers, data=req_payload)
		elif http_method == 'DELETE':
			return delete(api_url, headers=headers, data=req_payload)
		else:
			error_and_exit("wrong http method: {http_method}".format(**locals()))
	except Exception as e:
		error_and_exit(e.message)


# This function returns a groups dict, filtered by name (contains) or all if parameter is empty
def get_groups(base_api_path, token, account, grep_list, ungrep_list, json_format):
	if not json_format:
		print_message("Getting groups from Spotisnt, please wait...")
	result  = query_api(base_api_path, token, account=account)
	if result.status_code > 299:
		error_and_exit("bad response from Spotinst!\n{}".format(result.content))
	try:
		data = json_loads(result.content)
	except Exception as e:
		error_and_exit("while loading json response: {e.message}".format(**locals()))
	# apply grep and ungrep filters
	groups = {}
	all_groups = data['response']['items']
	if len(grep_list) == 0:
		for group in all_groups:
			groups[group['name']] = [group['id'], group['capacity']['minimum'], group['capacity']['target'], group['capacity']['maximum']]
	else:
		for group in all_groups:
			group_name = group['name'].lower()
			if [grep_term for grep_term in grep_list if grep_term.lower() in group_name] and not [ungrep_term for ungrep_term in ungrep_list if ungrep_term.lower() in group_name]:
				groups[group['name']] = [group['id'], group['capacity']['minimum'], group['capacity']['target'], group['capacity']['maximum']]
	# return a sorted list of groups
	return OrderedDict(sorted(groups.items()))


# This function prints groups as a table
def print_all_groups(groups_to_print, json_format, list_only):
	if not json_format:
		table = PrettyTable(['#' ,'Group name', 'ID', 'Min', 'Target', 'Max'])
		table.align = "l"
		table.border = True
		counter = 1
		for key, value in groups_to_print.iteritems():
			table.add_row([counter, key, value[0], value[1], value[2], value[3]])
			counter += 1
		print_message("Found the following groups: ")
		print "{table}\n".format(**locals())
	else:
		if list_only:
			groups_to_print = { "groups" : groups_to_print.keys()}
			print json_dumps(groups_to_print, indent=2)


# This function prints a bold message
def print_message(msg):
	all_lines = msg.splitlines()
	longest_line = 0
	for line in all_lines:
		if len(line.strip()) > longest_line:
			longest_line = len(line.strip())
	padding = 8
	print "\n" + ("=" * (longest_line + padding))
	for line in msg.splitlines():
		print (" " * (padding / 2)) + line
	print ("=" * (longest_line + padding)) + "\n"


# This function makes sure the user wants to process with his choice
def prompt_for_conformation():
	question = [
		{
			'type': 'confirm',
			'message': 'Are you sure you want to updated these groups?',
			'name': 'confirm',
			'default': False,
		}
	]
	try:
		return prompt(question)['confirm']
	except KeyError:
		return False




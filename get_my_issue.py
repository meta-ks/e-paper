#!/usr/bin/env python3

import time
import configparser
import os
import methods


def main():

	#today = time.asctime(time.localtime(time.time()))
	today = time.strftime("%a, %d %b %Y", time.gmtime())

	print('\nHi! today is {} '.format(today))
	print('[*]Going to download today\'s issue...')
	print('[>]In case connection error occurs try after sometime. Even then if problem persists, Github!!')
	print('[*]Reading the config file config.ini  ...')

	ini = configparser.ConfigParser()
	try:
		ini.read('config.ini')
	except:
		print('No config file found. Creating one...')	#create the ini file
		ini['DEFAULT']['auto_pilot'] = input('\nauto mode(0/1): ')
		ini['1']['url'] = input('\nurl :')
		ini['1']['method_name'] = input('\nmethod_name: ')
	#print(ini,'###########')
	mode = ini['DEFAULT']['auto_pilot'] 	# 1 for auto; no user interaction

	if(mode == '1'):
		stat = auto_pilot(today,ini)
	else:
		pass#stat = manual.main(today,ini)

	if stat:
		print('\n[*]Hope you have the file...Bye!!')
	else:
		print('\n[*]Din\'t work! Trace and pull or create an issue...you know :)')

def auto_pilot(today,ini):
	print('[*]Auto-mode...\n')

	file_name = '_the_Hindu__' + today + '.pdf'

	if os.path.exists(file_name):
		if  ini['DEFAULT']['repeated_download'] == 0:
			print('[*]File already exists!Need not download. \n')
			return True
		else:
			try:
				os.rename(file_name,'old_'+file_name) # to rename existin in format z_old.bah.pdf
			except:
				pass

	section_no = ini['DEFAULT']['use_section']
	url = ini[section_no]['url']
	method_name = ini[section_no]['method_name']

	stat = methods.use_method(method_name,url,file_name)

	if stat:
		if ini['DEFAULT']['move_old'] == '1':
			for l in os.listdir(os.curdir):		#to move older issues to old_issuse dir
				print(l)
				if l.endswith('.pdf') and not (l == file_name) and ('_the_Hindu__' in l):		#to avoid today's file to be copied to old dir
					try:
						old_issue_dir = ini['DEFAULT']['old_issue_dir']
						os.rename(l,'{}/{}'.format(old_issue_dir,l))
						print('{} moved to {}.'.format(l,old_issue_dir))
					except:
						print('\n[*]Failed to move the older issues. Do it manualy. :(')
		else:
			pass	#don't move the files to old_issues dir
		return True

	else:
		return False


if __name__ == '__main__':
	main()
#!/usr/bin/env python3
import requests
import re

def main():
	print('[*]This script will extract text between a html tag')
	#url = input('[*]Enter the url of the page: ')
	url = r'http://www.everexam.com/the-hindu-epaper-free-download-pdf'
	#tag = input('[+]Enter the name of the tag (like td or strong): ')
	tag = 'tr'
	#greedy = input('[+]Greedy: ')
	greedy = 0

	print('[*]Retreiving page...')
	ua = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0'}
	#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
	html_res = requests.get(url,headers=ua)

	if html_res.status_code == 200:
		print('[*]Page retreived. Now extracting data ...')
		html_text = html_res.text  #html code to be parsed by re
		data = extract_data(html_text,tag,greedy)

	else:
		print('[-]Staus code of {} not 200.'.format(url))
		print('[-]Nothing found!')
		return None
	# to ensure whole list is not printed in case of large list


	if len(data) > 10:
		if input('[*]More than 10 elements, Display all? '):
			for d in data:
				print(d)
		else:
			for i,d in enumerate(data):
				if i <= 10:
					print(d)
				else:
					print(' And more.......')
					break
	else:
		for d in data:
			print(d)

	print('[*]Exiting..')


def extract_data(html_text,tag,greedy=1,remove_comments=False):
	
	if remove_comments:
		#removing comments:
		comment_list = re.findall('<!--.*?-->|<comment>.*?</comment>',html_text,re.DOTALL)
		for comment in comment_list:
			html_text = html_text.replace(comment,'\n')	#replaces the comment block with a new line
		print('[*]Comments removed!')
		'''start_index_list, end_index_list = [],[]

		for match in re_obj.finditer(html_text):
			start_index_list = match.start()
			end_index_list = match.end()

		size = len(start_index_list)
		temp_text = html_text[:start_index_list[0]]+html_text[end_index_list[0]:]+html_text[]
		for k in range(size-1):
			start = start_index_list[k]
			end = end_index_list[k]
			start2 = start_index_list[k+1]
			temp_text = temp_text + html_text[endp:start]+'\n'+html_text[end:start2]
		html_text = temp_text + 

		#temp_text = html_text
		for match in re_obj.finditer(html_text):
			start = match.start()
			end = match.end()
			html_text = html_text[:start+1]+html_text[end:]'''

	if greedy:
		pattern = '<{}>(.*)</{}>'.format(tag,tag) 
	else:
		pattern = '<{}>(.*?)</{}>'.format(tag,tag)
	text_bet_tag = re.findall(pattern,html_text,re.DOTALL) #RE.DOTALL matches . with any char including \n and so
	#now extracting 
	'''try:
		print('length is ',len(text_bet_tag))
		print(text_bet_tag[:10])
	except:
		print(text_bet_tag)'''
	return text_bet_tag

#
def tabulate_data(data_list,tag):
	'''many times extracted data is <td></td>. so converting into list of list
		takes list or <tr> having <td> in it as input'''
	#tag = '<{}>'.format(tag)
	table = [] #like [['df','dfd'],['df','df']...]
	for l in data_list:
		if tag in l:
			table.append(extract_data(l,tag,greedy=0))	#non greedy for finding out all <td> val separately

	return table


if __name__ == '__main__':
	main()
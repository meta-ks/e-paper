#!/usr/bin/env python3
import requests
import gdrive
import scraper
import date_time

def main():
	method_name = input('Which method do you want: ')
	url = input('And url: ')
	file_name = input('And file name: ')
	print('Need to do maore abt main.')
	stat = True
	#stat = use_method(method_dict,file_name)
	if stat: print('Done!')
	else: print('Sth happened!')


def use_method(method_dict,file_name,match_time=False):

	method_name = method_dict['name']
	#if pdf is uploaded on a drive.
	if(method_name == 'google_drive'):
		bin_data = google_drive(method_dict,match_time)
		

	#if pdf of e-paper is accessible directly from some source
	elif(method_name == 'direct_link'):	#to do 
		bin_data,file_name = direct_link(method_dict)

	#a year ago the e-paper used to be directly accessible by a crafted link. No longer works
	elif(method_name == 'indirect_object'):  #to do
		bin_data,file_name = indirect_obj(method_dict)

	else:
		pass

	#writing to disk:
	if bin_data:
		print('[*]Writing to drive...')

		with open(file_name,'wb') as fo:
			fo.write(bin_data)

		print('[*]{} written to current directory!'.format(file_name))
		return True
	else:
		#try other methods
		return False

def google_drive(method_dict,local_time):

	url = method_dict['url']
	print('[*]Retreiving page at {}...'.format(url))
	ua = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0'}
	#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
	html_res = requests.get(url,headers=ua)

	if html_res.status_code == 200:
		print('[*]Page retreived. Now extracting data ...')
		html_text = html_res.text  #html code to be parsed by re
		tr_list = scraper.extract_data(html_text,'tr',greedy=0,remove_comments=True)	# rows of tables as a single string
		table = scraper.tabulate_data(tr_list,'td')	#extracting td values
		print('[*]Finding gdrive url...')

		#finding gdrive url:
		#date_pos = (method_dict['date_x'],method_dict['date_y'])
		#url_pos = (method_dict['url_x'],method_dict['url_y'])
		url_str = table[method_dict['url_x']][method_dict['url_y']]
		raw_date_str = table[method_dict['date_x']][method_dict['date_y']]
		
		#Now match the date string with today's date
		date_stat = date_time.match_date(raw_date_str,local_time)

		#g_url = date_time.today(table,date_position=date_pos,check=True)	#if position for date in table is known 

		
		if date_stat:
			g_url = url_str

		else:
			pass

		#print('[*]Retreiving {}....'.format(g_url))
		bin_data = gdrive.download(g_url,file_name_req=False) #the gdrive and source is different
		return bin_data

	else:
		print('[-]Staus code of {} not 200.'.format(url))
		print('[-]Nothing found!')
		return None
	

	
def direct_link(method_dict):
	pass


def indirect_obj(method_dict):		# used indirect object reference vuln in epaper.thehindu.sth
	pass
	


if __name__ == '__main__':
	main()


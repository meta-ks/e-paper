#!/usr/bin/env python

import requests
import re


'''
This script downloads publicly accessible google drive files. 
In future, it will support creating gmail sessions and downloading private files too.

'''

'''Following are link formats:
1.PDF's:
	https://drive.google.com/open?id=0B9oqV3QunSyPME9FcHpXZlFBRmFhQ1NGalpuY2FqNm9PX1V3
	https://drive.google.com/uc?id=0B9oqV3QunSyPME9FcHpXZlFBRmFhQ1NGalpuY2FqNm9PX1V3&export=download
	https://drive.google.com/file/d/0B69eWxM6NI3-ZmNuWW9IWlk0TFU/preview (the hindu)
	https://drive.google.com/file/d/0B69eWxM6NI3-ZmNuWW9IWlk0TFU/view  (for viewing)
	https://drive.google.com/uc?id=0B69eWxM6NI3-ZmNuWW9IWlk0TFU&export=download
	https://drive.google.com/uc?export=download&confirm=BHJy&id=0B69eWxM6NI3-ZmNuWW9IWlk0TFU

	
2.Docx:
	https://docs.google.com/document/d/1_XE-XQyinkvOtr4UAi5xw2o2tGgxdOsMt5Gq3Prcx14/edit?usp=drive_web
	https://docs.google.com/uc?export=download&confirm=em8Y&id=0B69eWxM6NI3-dmYteXlPR0V2OE0
	https://lh3.googleusercontent.com/z_dVaAGWaYGLulTy0drwYY6QpdABEOq718yBnFyw6Ejbu9T_r4-3FyOVCb0aNw=w400


'''


def main():
	print('[*]Will download public gdrive files for you :)')
	url = input('[*]Enter the url of the file shared: ')
	bin_data,file_name = download(url)
 
	if bin_data:
		with open(file_name,'wb') as fo:
			fo.write(bin_data)

		print('[*]{} written to disk in current dir'.format(file_name))

	else:
		print('[*]Failed :(')

	print('[*]Exiting...')


def download(url,file_name_req=True):	#if true also return the file name from header of server response
	print('[*]Extracting id of the file...')
	id = extract_id(url)
	print('[*]File id: {}'.format(id))
	#starting session s
	ua = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0'}
	s = requests.Session()
	
	s.headers.update(ua) #changes ua for all requests though they can be overriden in each individual requests
	#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
	#s.proxies.update(proxies)

	res1 = s.get('https://drive.google.com/uc?id={}&export=download'.format(id))
	#res1 = s.get('https://docs.google.com/uc?export=download&confirm={}&id={}'.format('haha',id))
	print('[*]1st request made {} ... '.format(res1.url))

	if res1.history:	#cheking the nature of response. If redirection happened then history contains [<Response [302]>]
		if res1.history[0].status_code == 302 and res1.status_code == 200:
			bin_data = res1.content
			f_res = res1 #f_res is final response
			print('[*]Cheers! Small file size.Conirmation not required.')

	else:
		cookie_names = s.cookies.keys()

		confirmation_cookie = None	#initialising
		for key in cookie_names:	#if THE COOKIE is found (cookie name for conf may get changed in future)
			if 'download_warning' in key:
				confirmation_cookie = key
				break

		if confirmation_cookie:
			confirmation_cookie_val = s.cookies[confirmation_cookie]
		else:
			print('[*]Issue at {}. Exiting!'.format(res1.url))
			bin_data = None
			return bin_data  #None is for file name

		print('[*]Finally downloading file after confirmation ...')
		res2 = s.get('https://drive.google.com/uc?export=download&confirm={}&id={}'.format(confirmation_cookie_val,id))
		#res2 = s.get('https://docs.google.com/uc?export=download&confirm={}&id={}'.format(confirmation_cookie_val,id)) can also be used but then s.cookies download_warning cookie is set for domain:drive.google.com so i won't be sent by default
		f_res = res2 #f_res is final respons

		
		if res2.status_code == 200: 
			try:
				if(res2.history[0].status_code == 302):	#302 for checking redirection	
					print('\n[*]Downloaded...')
					bin_data = res2.content
					#print(bin_data[:10])
					#return bin_data
				else:
					print('\n[*]Some problem with redirection... you may see \n'+res2.url+ ' manualy.')
					bin_data  = None
					#return bin_data
			except:
				print('\n[*]Oops! Unexpected behaviour by google...You may see \n'+res2.url+ ' manualy.')
				bin_data = None
		else:
			print('\n[*]Oops! Status code is not 200...You may see \n'+res2.url+ ' manualy.')
			bin_data  = None

	#determinig file type if set as True	
	if bin_data:
		con_type = f_res.headers['Content-Type']
		file_ext = con_type.split('/')[-1] #last part of the content-type tells the type of file
		raw_file_name = f_res.headers['Content-Disposition']
		file_name = re.findall('filename="(.+)"',raw_file_name) #headers have file name in format: 'Content-Disposition': 'attachment;filename="Assignment_2A.pdf";filename*=UTF-8\'\'Assignment_2A.pdf'
		if not len(file_name) == 1:
			file_name = input('[+]Suggested file named: {}\nEnter file name: '.format(file_name)) 
		else:
			file_name = file_name[0]
	else:
		file_name = None

	if file_name_req:
		return (bin_data,file_name)		#returns downloaded binary data and file name tuple
	else:
		return bin_data


def extract_id(url):
	#to extract id of the file

	#more to be added as more responses are observed
	pattern_list = [
						'id=([\w-]+)',	#id is a combo of alphanumeric and dash
						'/([\w-]+)/',
						'id%([\w-]+)'

					] 
	fid = None
	for pattern in pattern_list:
		id = re.findall(pattern,url)
		if id:
			#if just 1 entry in list means high probab of correct val
			if len(id) == 1:
				fid =  id[0]
			
			#various "indefinite" methods can be used to get id then if len is more than 1 
			else:
				#1. length of id is generally max compared to  any ther word
				max = 0
				for val in id:
					if len(val) > max:
						max = len(val)
						fid = val
		if fid: break

	return fid

	
	#return '0B0J-fAqsnH2qNE9KX0g0elJMcFU' #fid
	#>>> re.findall('(?<=/)([\w-]+)(?=/)',u)
	#['the-hindu-epaper-free-download-pdf', 'this45ef4ccecwissh', 'this-is-ranod']
	# use of (?=sth) doesn't consume the string known as  lookahead assertion


if __name__ == '__main__':
	main()
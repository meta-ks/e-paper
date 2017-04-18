#!/usr/bin/env python3

import re
import time

def main():
	pass

# these combos are popular: pass (table,signature) or pass (date_str,signature)
def today(table=False,date_sig='today',date_str=False,check=False,position=False): 

	if position:
		if check:
			pass
		x = position[0]
		y = position[1]
		raw_url = (table[x])[y]	#assuming 2nd row 2nd col contains the required url
		#print('returning ',raw_url)

	#else parse on date basis more confidence rate
	else:	
		
		date_str = extract_date()

	return raw_url


def extract_date(raw_date):
	
	date_list = re.findall('','',re.IGNORECASE)

	for date in date_list:
		pass
	return date_struct


def match_date(raw_date_str,ref_date_struct):

	return True

	in_date_struct = extract_date(raw_date_str)

	#now input date params
	in_date = in_date_struct.tm_mday
	in_month = in_date_struct.tm_mon
	in_year = in_date_struct.tm_year

	#now ref date params
	ref_date = ref_date_struct.tm_mday
	ref_month = ref_date_struct.tm_mon
	ref_year = ref_date_struct.tm_year

	if(in_date == ref_date and in_month == ref_month and in_year == ref_year):	
		return True
	else:
		return False



if __name__ == '__main__':
	main()
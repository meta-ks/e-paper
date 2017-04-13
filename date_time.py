#!/usr/bin/env python3

import re

def main():
	pass

def today(table,x=0,y=1):
	#print(table[0][0],'\n#####\n',table[0][1],'\n#####\n',table[1][0],'\n#####\n',table[1][1])
	raw_url = (table[x])[y]	#assuming 2nd row 2nd col contains the required url
	return raw_url


if __name__ == '__main__':
	main()
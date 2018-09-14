# Script to create a timeline of all the records within the iOS PowerLog that have a timestamp
# The idea for this came from Sarah Edward's iOS of Sauron talk
# Some of the timestamps appear to be a little unreliable, or default to the hour that an event occured rather than second.
# As a result, your mileage may vary and it's encouraged to test this on the specific iOS version.
# https://files.sans.org/summit/Digital_Forensics_and_Incident_Response_Summit_2016/PDFs/iOS-of-Sauron-How-iOS-Tracks-Everything-You-Do-Sarah-Edwards.pdf

# Tested on iOS 10.2

import sys, argparse, sqlite3

version_string = "processPowerLog v0.01"
print ("Running " + version_string)

parser = argparse.ArgumentParser(description='Parse powerlog from iOS file system')
parser.add_argument("db", help="Location of powerlog")
args = parser.parse_args()
	
conn = sqlite3.connect(args.db)
c = conn.cursor()


#list all tables in a given database
# to interact, use table_name[0]
alltables = conn.execute("select name from sqlite_master WHERE type='table';")
for table_name in alltables:
	#check if there's a timestamp heading
	
	#add quotes to deal with - special character
	table = '"' + table_name[0] + '"'
	#print(table)
	
	#get table heading
	c.execute('PRAGMA TABLE_INFO({})'.format(table))
	headings = [tup[1] for tup in c.fetchall()]
	if 'timestamp' in headings:
		
		#print(headings)
		for row in c.execute('select timestamp, datetime(timestamp, \'unixepoch\') as timestamp, * from {t}'.format(t=table)):
			i = 0
			rowlist = []
			while (i < (len(headings))):
				element = str(headings[i]) + ": " + str(row[i+2])
				rowlist.append (element)
				i += 1
				
			#print (rowlist)			
			
			item_tuple = (table_name[0], ) + (row[0],) + (row[1],) + (' | '.join(rowlist), )
			print (str(item_tuple)[1:-1])
		
conn.close()
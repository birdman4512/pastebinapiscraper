import pprint

import json
import requests
import urllib2
import os
from datetime import datetime
import time

#Variables
scraping_limit = "100" #max 250
scraping_url = "https://scrape.pastebin.com/api_scraping.php?limit=" + scraping_limit
dest_folder = "/media/pastebin/output"

while True:
	#Get the list of available posts
	#print("Hold on, getting data from PasteBin!")
	print("Getting data from: " + scraping_url)

	scrape_data = requests.get(scraping_url)

	#pprint(scrape_data)

	#convert to JSON
	scrape_json = scrape_data.json()
	#pprint(scrape_json)

	for paste in scrape_json:
		#Creating the details for the text file
		#variables
		filename = datetime.utcfromtimestamp(float(paste['date'])).strftime('%Y-%m-%d %H-%M-%S') + "_" + paste['key'] + ".txt"
		date =  datetime.utcfromtimestamp(float(paste['date'])).strftime('%Y-%m-%d')
		
		#Create the folder if not exists
		if not os.path.isdir(dest_folder + "/" + date + "/"):
			print("Creating folder: " + date)
			os.mkdir(dest_folder + "/" + date + "/")

		if os.path.exists(dest_folder + "/" + date + "/" + filename):
			append_write = 'a' # append if already exists
			print("Skipping " + filename + ", Already exists")
		else:
			append_write = 'w' # make a new file if not
	
			#Write out the file
			paste_file = open(dest_folder + "/" + date + "/" + filename, append_write)
		
			#Write the Name to the file
			paste_file.write("Name: " + paste['title'].encode('utf-8').strip())
			paste_file.write("\n")
			paste_file.write("Link: " + paste['full_url'].encode('utf-8').strip())

			#Now get the contents of the paste and dump it into the file
			paste_data = requests.get(paste['scrape_url'])
			paste_file.write("\n")
			paste_file.write("\n+----+----+\n")
			for line in paste_data:
				paste_file.write(line)	
			paste_file.write("\n+----+----+")
			paste_file.close()
			print(filename + " written")
	
	time.sleep(1)

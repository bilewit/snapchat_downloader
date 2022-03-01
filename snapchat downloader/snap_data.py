import json
from urllib.parse import urlparse
import requests
import time
import sys
import random

file = 'memories_history.json'
# global amazon_links
# global snap_links

def compress_json_info(file):
	#after we proccess our request we will store our amazon links in here
	amazon_links = []
	#we will store our snap links in here
	snap_links = []
	#This opens the Json file and gets the method link,media type and date
	with open(file) as json_file:
		data = json.load(json_file)
		for saved in data["Saved Media"]:
			link = saved["Download Link"]
			media_type = saved["Media Type"]
			date = saved["Date"]
			#then creates a tuple with all the grabbed data
			trio = (link,media_type,date)
			#adds the tuple to the snap_links list
			snap_links.append(trio)
	return snap_links
#this is the total number of snap links a.k.a requests we are about to make
#total_links = len(snap_links)
#init the status
# status = 2199

# #loop through each link in dictionary
#
# #this function will now take us online
# #it will update the previous trio w/ a static file link (expires in 7 days)
def online_final_trio(item):
	amazon_links = []
	#total_links = len(snap_links)
	status = 0
	#for item in snap_links:
	# if (status % 1000 == 0) and status > 2199:
	# 	print(status)
	# 	print("We are taking a big break of 10min")
	# 	time.sleep(600)
	#grab the link
	link = item[0]
	#grab media type
	media_type = item[1]
	#grab the date
	date = item[2]
	#print(link)
	#init our data dictionary which will hold all variables for post request
	data = {}
	#the data needs to be further split as the data is 'a=b', instead of 'a':'b'
	pre_data = []
	#this grabs the arguments from the link because the strings 'a=b&c=d&e=f' insteadof
	#'a=b',c=d,e=f
	query = urlparse(link).query[1:]
	#the data is 'a=b', instead of 'a':'b' so this makes it [['a','b']['c','d']]
	parts = query.split('&')
	#adds all parts to list [['a','b']['c','d']]
	for variable in parts:
		x = variable.split("=")
		pre_data.append(x)
	#adds each required arg to dictionary
	for args in pre_data:
		data.update({args[0]:args[1]})
		#print(data)

	#now we are about to go online >.>
	#this goes online
	r = requests.post(url=link, data=data)
	#this is the returned amazon link or insta download link
	new_url = r.text
	#tuple of all needed data and adds to list
	new_item = (new_url,media_type,date)
	amazon_links.append(new_item)
	# f = open("online_trio.txt", "a")
	# f.write(str(new_item) + ',')
	# f.close()
	return new_item
	#print(new_url)
		#print(new_item)
	#update status
	#	status += 1
		#print("currently: "+str(status)+" of "+str(total_links))
		#idk if theres a request limit so this is just a "precaution"

		#sleepy_time = random.randint(0,5)
	#sanity check cause i get scared
		#print("Time for a quick "+str(sleepy_time) +" second nap")
		#time.sleep(sleepy_time)
#we are back offline
#amazon links are done
# print("amazon links done :)")
# print(amazon_links)

def file_type_end(media_type):
	file_type = ""
	if media_type == 'PHOTO':
		file_type = '.jpg'
	else:
		file_type = '.mp4'
	return file_type



#'https://app.snapchat.com/dmd/memories?uid=a2c1c760-2c8f-480e-8fed-26ae779f0c9e&sid=AED2E0C5-3073-4E28-AF55-AA8CA9D1973B&mid=AED2E0C5-3073-4E28-AF55-AA8CA9D1973B&ts=1597015449593&proxy=true&sig=7ac571be150d6af4a28b2708d8fba083109564391630fe8e5914a4fe93a4cc29'


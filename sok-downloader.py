import wget
import requests
from bs4 import BeautifulSoup


cookie_info = {"first_thing_equals":"second_thing"}


def get_conference_listing(cookie_info):
	conference_listing = requests.get("https://www.sok-media.com/player?conf_search_input=",cookies=cookie_info)
	soup_to_filter = BeautifulSoup(conference_listing.text,"html.parser")
	conference_list_data = soup_to_filter.find_all("a",{"data-conf-id":True})
	conference_list = []
	for conference in conference_list_data:
		conference_list.append([conference["data-conf-id"],conference["data-conf-name"]])
	return conference_list


#Useless, Really. 
def get_conference_info(conference_id,cookie_info):
	conference_info = requests.get("https://www.sok-media.com/player?action=change_theme&conf_id="+str(conference_id),cookies=cookie_info)


def get_playlist_info(conference_id,cookie_info):
	conference_info = requests.get("https://www.sok-media.com/player?action=get_playlist&conf_id="+str(conference_id),cookies=cookie_info)	
	#Response will be in json, sort of... Giant block of HTML in the "html" piece
	html_soup_to_filter = conference_info.json()["html"]
	soup_to_filter = BeautifulSoup(html_soup_to_filter, 'html.parser')
	session_links_data = soup_to_filter.find_all("a",class_="session_link")
	session_links = []
	for session in session_links_data:
		session_links.append(session["data-session-id"])
	return session_links





#Get the session information
#https://www.sok-media.com/player?action=get_session_info&session_id=<X>
def get_session_information(session_number,cookie_info):
	session_info = requests.get("https://www.sok-media.com/player?action=get_session_info&session_id="+str(session_number),cookies=cookie_info)
	return session_info.json()

#Put that information to use
#https://www.sok-media.com/player?session_id=<X>&action=get_video
def get_video_information(session_number,cookie_info):
	video_information = requests.get("https://www.sok-media.com/player?session_id="+str(session_number)+"&action=get_video",cookies=cookie_info)	
	return video_information.json()

#for session in session_numbers:
#	session_info = get_session_information(session,cookie_info)
#	video_info = get_video_information(session,cookie_info)
#	file_name = session_info["session_name"].replace(":","").replace("?","").replace(" ","_")+".mp4"
#	print("Downloading: "+file_name)
#	video_data = requests.get(video_info["url"])
#	with open(file_name,"wb") as f:
#		f.write(video_data.content)


def download_video(session_name):
	wget.download(full_talk_info["url"],full_talk_info["session_file_name"])


gg  = get_conference_listing(cookie_info)
print(gg)

print("We have conferences lets grab 2017 Data")
playlist_info = get_playlist_info(40,cookie_info)
print(playlist_info)
full_talk_info = {}
for talk in playlist_info:
	session_information = get_session_information(talk,cookie_info)
	session_name = session_information["session_name"]
	full_talk_info[session_name] = {}
	full_talk_info[session_name]["number"] = talk
	full_talk_info[session_name]["session_name"] = session_name
	full_talk_info[session_name]["session_file_name"] = session_information["session_name"].replace(":","").replace("?","").replace(" ","_")+".mp4"
print("Finished Pulling Talk information, pulling "+ str(len(full_talk_info)) + "talk links")
#Grab the video information, separate to prevent duplicate runs
for talk_name in full_talk_info.keys():
	video_information = get_video_information(full_talk_info[talk_name]["number"],cookie_info)
	full_talk_info[talk_name]["url"] = video_information["url"]

print("Retreived List of Talks")
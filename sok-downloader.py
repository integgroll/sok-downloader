import wget
import requests
import getpass
from bs4 import BeautifulSoup


def get_conference_listing(cookie_info):
    conference_listing = requests.get("https://www.sok-media.com/player?conf_search_input=",cookies=cookie_info)
    soup_to_filter = BeautifulSoup(conference_listing.text,"html.parser")
    conference_list_data = soup_to_filter.find_all("a",{"data-conf-id":True})
    conference_list = []
    for conference in conference_list_data:
        conference_list.append([conference["data-conf-id"],conference["data-conf-name"]])
    return conference_list

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

def download_video(talk_info):
    wget.download(talk_info["url"],talk_info["session_file_name"])

def get_login_creds():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    credential_request = requests.post("https://www.sok-media.com/node?destination=node",data={"name":username,"pass":password,"form_id":"user_login_block","op":"Log+in"},cookies={"has_js":"1"},allow_redirects=False)
    return credential_request


cookie_info = get_login_creds().cookies.get_dict()
print("Lets grab 2017 Data")
playlist_info = get_playlist_info(40,cookie_info)
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
print("Retreived List of Talks - Starting Downloads")
for talk in full_talk_info.values():
    download_video(talk)







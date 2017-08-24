import requests
from bs4 import BeautifulSoup

cookie_info = {"first_thing_equals":"second_thing"}

#Huge list of video numbers
session_numbers = [5358,5256,5246,5403,5241,5385,5289,5222,5376,5339,5342,5392,5273,5305,5357,5227,5326,5321,5297,5296,5379,5330,5276,5361,5234,5334,5386,5293,5317,5263,4136,4138,4135,4137,4134,5311,5373,5355,5370,5359,5300,5412,5346,5243,5292,5348,5236,5216,5319,5262,5309,5364,5232,5251,5400,5270,5282,5267,5407,5344,5402,5240,5220,5378,5259,5410,5329,5405,5278,5324,5290,5237,5350,5368,5272,5280,5307,5397,5223,5318,5341,5268,5347,5416,5383,5215,5337,5242,5399,5374,5252,5360,5415,5279,4015,5226,5395,5352,5250,5229,5389,5345,5381,5244,5332,5363,5301,5291,5266,5354,5351,5338,5225,5396,5239,5254,5231,5335,5366,5390,5331,5275,5369,5284,5353,5214,5413,5308,5315,5371,5230,5277,5367,5249,5382,5253,5295,5219,5340,5258,5274,5285,5228,5312,5233,5269,4091,5414,5257,5264,5260,5255,5372,5288,5316,5314,5406,5299,5294,5391,5380,5394,5218,5302,5271,5283,5408,5235,5320,5281,5384,5286,5398,5356,5349,5303,5327,5322,5343,5401,5265,5310,5221,5365,5328,5325,5238,5333,5362,5313,5298,5287,5404,5217,5375,5393,5304,5306,5336,5213,5247,5377,5409,5248,5261,5323,5387,5245,5411,5388,5224]



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



gg  = get_conference_listing(cookie_info)
print(gg)

print("We have conferences lets grab 2017 Data")
playlist_info = get_playlist_info(40,cookie_info)
print(playlist_info)
full_talk_info = {}
for talk in playlist_info:
	print("Processing: "+str(talk))
	full_talk_info[talk] = {}
	session_information = get_session_information(talk,cookie_info)
	video_information = get_video_information(talk,cookie_info)
	full_talk_info[talk]["url"] = video_information["url"]
	full_talk_info[talk]["session_name"] = session_information["session_name"]
	full_talk_info[talk]["session_file_name"] = session_information["session_name"].replace(":","").replace("?","").replace(" ","_")+".mp4"

print(full_talk_info)

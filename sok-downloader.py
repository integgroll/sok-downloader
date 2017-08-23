import requests

cookie_info = {"first_thing_equals":"second_thing"}

#Huge list of video numbers
session_numbers = [5358,5256,5246,5403,5241,5385,5289,5222,5376,5339,5342,5392,5273,5305,5357,5227,5326,5321,5297,5296,5379,5330,5276,5361,5234,5334,5386,5293,5317,5263,4136,4138,4135,4137,4134,5311,5373,5355,5370,5359,5300,5412,5346,5243,5292,5348,5236,5216,5319,5262,5309,5364,5232,5251,5400,5270,5282,5267,5407,5344,5402,5240,5220,5378,5259,5410,5329,5405,5278,5324,5290,5237,5350,5368,5272,5280,5307,5397,5223,5318,5341,5268,5347,5416,5383,5215,5337,5242,5399,5374,5252,5360,5415,5279,4015,5226,5395,5352,5250,5229,5389,5345,5381,5244,5332,5363,5301,5291,5266,5354,5351,5338,5225,5396,5239,5254,5231,5335,5366,5390,5331,5275,5369,5284,5353,5214,5413,5308,5315,5371,5230,5277,5367,5249,5382,5253,5295,5219,5340,5258,5274,5285,5228,5312,5233,5269,4091,5414,5257,5264,5260,5255,5372,5288,5316,5314,5406,5299,5294,5391,5380,5394,5218,5302,5271,5283,5408,5235,5320,5281,5384,5286,5398,5356,5349,5303,5327,5322,5343,5401,5265,5310,5221,5365,5328,5325,5238,5333,5362,5313,5298,5287,5404,5217,5375,5393,5304,5306,5336,5213,5247,5377,5409,5248,5261,5323,5387,5245,5411,5388,5224]

#Get the session information
#https://www.sok-media.com/player?action=get_session_info&session_id=<X>
#{"session_name":"Behind the Plexiglass Curtain: Stats and Stories from the Black Hat NOC","session_desc":"<p>","speakers":"<h1>Speakers<\/h1><h2>Bart Stump<\/h2>\n                      <p><\/p><h2>Neil Wyler<\/h2>\n                      <p><\/p>"}
def get_session_information(session_number,cookie_info):
	session_info = requests.get("https://www.sok-media.com/player?action=get_session_info&session_id="+str(session_number),cookies=cookie_info)
	return session_info.json()

#Put that information to use
#https://www.sok-media.com/player?session_id=<X>&action=get_video
#{"url":"https:\/\/sokstreamvideo.s3.amazonaws.com\/17_bhb_usa\/mp4\/db86d4adf26d1c626baa665177f63ec9.mp4?x-amz-security-token=FQoDYXdzEPT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDLzcZxYh0XKz41fz%2BiKUASt4VcBO9aLQ4bt0cCPyUtVdNDwAHn7EVGsn%2BHUK5RWOJ2pL%2BjzRU9YZjXJwByIwCaBAxww%2F5Fbm4nkYSPnfBiW9VYg%2FjcL%2BRwUQiw4MIUlrtYVc6J%2FAKOi5F6aaPc0sA9zKFjBTfwtQLG8BSmGjHJPVS6TILUe853Wef45NQ5QdTgG%2BpamANIn1PS7poHNI61exeIIo1qb3zAU%3D&AWSAccessKeyId=ASIAIYZWQBINR7XXNU6A&Expires=1503526278&Signature=svoraQ0Kr0k5dUmf0PbEulicV3o%3D","type":"video\/mp4","srt":""}
def get_video_information(session_number,cookie_info):
	video_information = requests.get("https://www.sok-media.com/player?session_id="+str(session_number)+"&action=get_video",cookies=cookie_info)	
	return video_information.json()

for session in session_numbers:
	session_info = get_session_information(session,cookie_info)
	video_info = get_video_information(session,cookie_info)
	file_name = session_info["session_name"].replace(":","").replace(" ","_")+".mp4"
	print("Downloading: "+file_name)
	video_data = requests.get(video_info["url"])
	with open(file_name,"wb") as f:
		f.write(video_data.content)
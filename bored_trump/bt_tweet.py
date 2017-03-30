from textblob import TextBlob
from tweepy import OAuthHandler, API
from time import sleep
import pandas as pd

CONSUMER_KEY = "***"
CONSUMER_SECRET = "***"
ACCESS_TOKEN = "***"
ACCESS_TOKEN_SECRET = "***"

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth)

last_status = " "

while True:
	schedule = pd.read_csv("~/Desktop/trump_schedule.csv", header = None)
	schedule.columns = ['time', 'activity']
	schedule['time'] =  pd.to_datetime(schedule['time'], format='%Y-%m-%d %H:%M:%S')

	timeline = api.user_timeline(screen_name='realDonaldTrump', count = 1)
	tweet_time = timeline[0].created_at
	
	counter = 0
	while counter < (len(schedule) - 1):
		since = tweet_time - schedule.iloc[counter][0]
		before = tweet_time - schedule.iloc[counter + 1][0]
		if (since.days == 0) and (before.days < 0):
			activity = schedule.iloc[counter][1]
			activity = TextBlob(activity)
			tags = activity.tags
			verb_list = []
			for tag in tags:
				if tag[1].startswith("V"):
					verb_list.append(tag)
			first_verb_index = (tags.index(verb_list[0]) + 1)
			tags = tags[first_verb_index:]
			print(tags)
			while tags[0][1].startswith('PRP') or (tags[0][1] == "DT"):
				del tags[0]
			tweet_end = ""
			for tag in tags:
				tweet_end = tweet_end + " " + tag[0]
			tweet_end = tweet_end + "."
			tweet_id = timeline[0].id
			tweet_link = "https://twitter.com/realDonaldTrump/status/" + str(tweet_id)
			tweet = 'Trump just tweeted during his scheduled'+tweet_end
			while len(tweet + tweet_link) > 140:
				tweet_blob = TextBlob(tweet)
				words = tweet_blob.words[:-1]
				tweet = " ".join(words) + "..."
			status = tweet + tweet_link
			if status != last_status:
				api.update_status(status)
				last_status = status
		counter += 1
	sleep(300)
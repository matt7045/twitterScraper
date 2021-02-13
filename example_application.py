#A little test script, that uses twitterScraper.py to fetch tweets and save them
# to a file
import twitterScraper

#Get the screen name of the user whose tweets we want to fetch
screen_name = input('Screen Name: ')
tweet_string = twitterScraper.getTweetsAsString(screen_name)
with open ('text_dumps/'+screen_name+'.txt','w') as f:
    f.write(tweet_string)
print('Saved tweets to '+screen_name+'.txt')
input('Press ENTER to quit...')
quit()

import requests
import urllib.parse
import json

#Parses out the Bearer token that's hard-coded into one of twitter's javascript files
def _getToken1():
    request = requests.get("https://abs.twimg.com/responsive-web/client-web/main.a8574df5.js")
    text_block = request.text
    action_refresh_section = text_block[text_block.index('i="ACTION_REFRESH"'):]
    sections = action_refresh_section.split(',')
    for section in sections:
        if section[0:2]=='a=':
            token = urllib.parse.unquote(section[3:-1])
            break
    return(token)

#Gets the 'guest token' for the session
def _getToken2(token1):
    request = requests.post("https://api.twitter.com/1.1/guest/activate.json", headers={"Authorization":'Bearer '+token1})
    token = request.json()['guest_token']
    return(token)

#Get's the "rest ID' for a user on twitter
def _getUserRestID(screen_name, token1, token2):
    variables = {'variables':json.dumps({'screen_name':screen_name,'withHighlitedLabel':True})}
    headers = {"Authorization":'Bearer '+token1,
               "x-guest-token":token2}
    url = """https://api.twitter.com/graphql/4S2ihIKfF3xhp-ENxvUAfQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22"""+screen_name+"""%22%2C%22withHighlightedLabel%22%3Atrue%7D"""
    request = requests.get(url, headers=headers )
    return(request.json()['data']['user']['rest_id'])

#Takes a dictionary of tweets, and filters out everything that's not straight up words
def _filterTweets(tweets, exclude_hyperlinks=True, exclude_non_unicode_characters=True, format_amp_things=True):
    filtered_tweets = {}
    #Chop dem tweets
    for tweet_id, tweet_data in tweets.items():
        tweet_text = tweet_data['full_text']
        #If this tweet is a link, and we want to exclude hyperlinks
        if (exclude_hyperlinks and ("://" in tweet_text)):
            #Don't add it to our output
            continue
        #If this tweet contains weird characters, throw em away
        if exclude_non_unicode_characters:
            tweet_text = ''.join([char for char in tweet_text if ord(char) < 128])
        #If this tweet contains &amp; symbols, format them properly
        if format_amp_things:
            tweet_text = tweet_text.replace('&amp;','&')
        #Save our newly formatted tweet text, to the object
        filtered_tweets[tweet_id]=tweet_data
        filtered_tweets[tweet_id]['full_text'] = tweet_text
    #Return the formatted object to the user
    return(filtered_tweets)

#Gets a user's tweets from twitter
def getTweets(screen_name, number_of_tweets=2000):
    #Get all the weird ass tokens and IDs and ish from various parts of twitter
    token1       = _getToken1()
    token2       = _getToken2(token1)
    user_rest_id = _getUserRestID(screen_name, token1, token2)
    #Put together our GET request, for the user's tweets
    url = "https://api.twitter.com/2/timeline/profile/"+user_rest_id+".json"
    headers = {"Authorization":'Bearer '+token1,
               "x-guest-token":token2}
    params  = {"tweet_mode":"extended",
               "simple_quoted_tweet":True,
               "include_tweet_replies":True,
               "userId":user_rest_id,
               "count":number_of_tweets}
    #Make the get request
    request = requests.get(url, params=params, headers = headers)
    #Return the tweets from that get request
    return(request.json()['globalObjects']['tweets'])

#Gets a user's tweets, formats them, and shoves them into a text file
def getTweetsAsString(screen_name, number_of_tweets=2000):
    #Get dem tweets
    tweets = getTweets(screen_name,number_of_tweets)
    #Turn dem tweets into a loong string of text
    filtered_tweets = _filterTweets(tweets)
    #Turn the tweets into a long hex string
    tweet_string = '\n'.join([tweet['full_text'] for tweet_id, tweet in filtered_tweets.items()])
    #Return the string
    return(tweet_string)

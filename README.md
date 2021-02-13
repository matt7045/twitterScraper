# TwitterScraper
Goes out to twitter, and fetches all the tweets it can for a specific user's screen name. It then formats and dumps those tweets in a text file.

## Required Python Libraries
* requests - `pip install requests`

## Useful Endpoints

* `getUserTweets(screen_name, number_of_tweets=2000)`  - returns a dictionary of tweets and their respective metadatas. Can be easily json.dump'd directly to file.

* `getUserTweetsAsString(screen_name, number_of_tweets=2000)` -  Returns a long string of all the user's tweets, separated by newlines. Excludes all tweets that are just posting's of links. Most useful endpoint for trying to get the user's speech patterns. Can be easily written directly to file as English.

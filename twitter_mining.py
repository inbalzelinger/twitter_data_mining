import tweepy


class Twitter:

    def __init__(self, config_parser):
        self.twitter_api = self.create_twitter_authentication_api(config_parser)

    def create_twitter_authentication_api(self, config_parser):
        consumer_key = config_parser.twitter_for_developers_config['API_key']
        consumer_secret = config_parser.twitter_for_developers_config['API_secret_key']
        access_token = config_parser.twitter_for_developers_config['Access_token']
        access_token_secret = config_parser.twitter_for_developers_config['Access_token_secret']
        twitter_authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
        twitter_authentication.set_access_token(access_token, access_token_secret)
        return tweepy.API(twitter_authentication)

    def read_tweets(self, name, num_of_tweets_to_read):
        return self.twitter_api.user_timeline(id=name, count=num_of_tweets_to_read)




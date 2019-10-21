import tweepy
import secret_data

key_and_token = secret_data.getTwitterKeyAndToken()
CONSUMER_KEY = key_and_token['consumer_key']
CONSUMER_SECRET = key_and_token['consumer_secret']
ACCESS_TOKEN = key_and_token['access_token']
ACCESS_TOKEN_SECRET = key_and_token['access_token_secret']

SCREEN_NAME = '@PositiveYellBot'

# tweepyの設定
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)


# フォロバ
def followBack():
    followers = api.followers_ids(SCREEN_NAME)
    for follower in followers:

        try:
            api.create_friendship(follower)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    followBack()

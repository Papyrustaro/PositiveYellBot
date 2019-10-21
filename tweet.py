import tweepy
import random
import re
import mecab
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

# ツイート
def tweetPerTime():
    # TLの最新から10件取得
    try:
        timeline_status = api.home_timeline(count=10)
    except Exception as e:
        print(e)

    tweet_text = ''
    tweet_noun = getProperNoun(timeline_status)
    # テキストに固有名詞がなかったら、名詞を探す
    if(tweet_noun == ''):
        tweet_noun = getNoun(timeline_status)
        if(tweet_noun == ''):
            return

    # 5つの定型文からランダムでひとつ選ぶ
    n = random.randrange(5)
    if n == 0:
        tweet_text = 'よっ!!' + tweet_noun + '!!'
    elif n == 1:
        tweet_text = 'そこまで' + tweet_noun + 'するには眠れない夜もあっただろう!!'
    elif n == 2:
        tweet_text = tweet_noun + '頭にのせてんのかい!!'
    elif n == 3:
        tweet_text = tweet_noun + 'いいよぉ!!'
    elif n == 4:
        tweet_text = 'ナイス' + tweet_noun + '!!'

    # ツイート
    tweet_text = tweet_text.encode('utf-8')
    try:
        api.update_status(tweet_text)
    except Exception as e:
        print(e)


# フォロバ
def followBack():
    followers = api.followers_ids(SCREEN_NAME)
    for follower in followers:

        try:
            api.create_friendship(follower)
        except Exception as e:
            print(e)


# リプを返す(ダメでした...)
def reply():
    # リプライ先はわかるが、ツイートのリプライされた側からは観測できない
    # 通知欄からリプライを探して返信するという案→すでにBotがリプライをしているかの判断など難しいので断念
    reply_ids = api.user_timeline(screen_name = SCREEN_NAME, count = 1)[0].in_reply_to_status_id
    print(api.user_timeline(screen_name = SCREEN_NAME, count = 1)[0].in_reply_to_status_id)
    if reply_ids is not None:
        for i in range(min(3, len(reply_ids))):
            reply_status = get_status(reply_ids[i])
            if reply_status.in_reply_to_status_id is None:
                text = '@' + reply_status.screen_name + ' ' + rand_reply_text()
                api.update_status(text, in_reply_to_status_id=reply_status.id, auto_populate_reply_metadata=True)


# リプライ用テキスト(使うことはなく)
def rand_reply_text():
    n = random.randrange(3)
    tweet_text
    if n == 0:
        tweet_text = '進捗どうですか'
    elif n == 1:
        tweet_text = 'Just do it!!'
    elif n == 2:
        tweet_text = 'まだまだいける!!'
    return tweet_text


# status群からtextを取り出し、固有名詞を返す(なければ空文字)
def getProperNoun(timeline_statuses):
    for status in timeline_statuses:
        text = fixTLText(status.text)
        proper_noun = mecab.returnProperNoun(text)
        if(proper_noun != ''):
            return proper_noun
    return ''


# status群からtextを取り出し、名詞を返す(なければ空文字)
def getNoun(timeline_statuses):
    for status in timeline_statuses:
        text = fixTLText(status.text)
        noun = mecab.returnNoun(text)
        if(noun != ''):
            return noun
    return ''


# TLのtextからURL,垢名などを取り除く
def fixTLText(tweet_text):
    text = tweet_text.split()
    output = ''
    for word in text:
        word = word.replace('RT', '')
        word = re.sub('http.+', '', word)
        word = re.sub('@[a-zA-Z_0-9]+', '', word)
        word += ' '
        output += word
    return output


if __name__ == '__main__':
    tweetPerTime()

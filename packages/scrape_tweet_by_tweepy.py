# import packages
import tweepy   # extract tweets from Twitter
import math   # ceil & floor num


# params: term is word without hashtag, request number, language used
def main(term=None, number=None, lang=None):
    # set default value
    if term is None:
        term = '#あんスタ'
    if number is None:
        number = 3

    # get hashtag
    hashtag = "#" + term   # add hastag
    # print(f"hashtag = {hashtag}")   # D

    out = []

    # set credentials
    """# TEST CASE: test w wrong credentail
    consumer_key = "q1BwFxmCRcLt21Wwx33zXqQVR666"   # same as api key"""
    consumer_key = "q1BwFxmCRcLt21Wwx33zXqQVR"   # same as api key
    # same as api secret
    consumer_secret = "rjMIMoYhoOVg6K1wnFEi8vtMtn64hPZChHXDh8JxmcR0Sx9Myg"
    access_key = "1267374302971617282-IB4B6Lfi1QxitPTzw4h5wRRxjjRI6a"
    access_secret = "3iRqJsKLExVAj4tcUoQ0pw3yRAhpBEM1jpcWBvPLzGCfj"

    # Twitter authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # creating an API
    api = tweepy.API(auth)

    # white-list words
    whiteList = "(戦利品 OR ありがたい OR やばい OR ありがとう OR ありがとうございます OR うれしすぎる OR 嬉しすぎる OR 嬉しい OR 描いてみた OR 超ラブーい OR 妄想 OR ラブい OR 兄弟 OR おめでとう OR 誕生祭 OR お団子 OR うっすい OR お疲れ様でした OR イベント OR イベ頑張るぞ OR ヒートアップ OR ボルテージアップ OR フィーチャー OR 楽しみです OR スキ OR 好き OR 大好き OR 愛で)"

    # print("\n=== tweets ===")
    # get tweet by hashtag
    item_num = number / 2
    """ print(f"hashtag: math.ceil(item_num) = {math.ceil(item_num)}")   # D
    print(f"word: math.floor(item_num) = {math.floor(item_num)}") """
    query = "(" + hashtag + " OR #あんスタ OR " + whiteList + ")"
    tweets = tweepy.Cursor(
        # api.search_tweets, q=hashtag, tweet_mode="extended", lang=lang).items(math.ceil(item_num))   # OPT: compat, lang="en" / "zh"; .items(1)
        api.search_tweets, q=query, tweet_mode="extended", lang=lang).items(math.ceil(item_num))
    # out += tweets
    # get content & id col data only
    for tweet in tweets:   # TODO: remove redundant
        data = {}
        # OPT: tweet['content']
        """# TEST CASE: test server down w code 500
        data['content'] = tweet['content']"""
        data['content'] = tweet._json["full_text"]   # OPT: tweet['content']
        data['id'] = tweet._json["id_str"]   # OPT: tweet['id']
        out.append(data)
    # print(f"hashtag: tweets = {tweets}")   # D

    # get tweet by word
    query = "(" + term + " AND あんスタ AND " + whiteList + ")"
    tweets = tweepy.Cursor(
        api.search_tweets, q=query, tweet_mode="extended", lang=lang).items(math.floor(item_num))   # OPT: compat, lang="en" / "zh"; .items(1) // 2, 5
    # out += tweets
    # get content & id col data only
    for tweet in tweets:
        data = {}
        data['content'] = tweet._json["full_text"]   # OPT: tweet['content']
        data['id'] = str(tweet._json["id_str"])   # OPT: tweet['id']
        out.append(data)
    # print(f"word: tweets = {tweets}")   # D

    # result max_results of tweets' content & id (by hashtag & word)
    return out

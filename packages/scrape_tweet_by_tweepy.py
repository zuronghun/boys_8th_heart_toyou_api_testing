# import packages
import tweepy   # extract tweets from Twitter
import math   # ceil & floor num


# params: term is word without hashtag, request number, language used
def main(term=None, number=None, lang=None):
    # set default value
    if term is None:
        term = 'あんスタ'
    if number is None:
        number = 3

    # declare variables
    out = []
    queryNItemNum = dict()
    item_num = number / 2
    api = getTwitterApi()

    # get hashtag
    hashtag = "#" + term   # add hastag
    # print(f"hashtag = {hashtag}")   # D

    # character white-list words query
    # default value
    whiteListQuery = ""   # OPT: None
    # whiteList = "(戦利品 OR ありがたい OR やばい OR ありがとう OR ありがとうございます OR うれしすぎる OR 嬉しすぎる OR 嬉しい OR 描いてみた OR 超ラブーい OR 妄想 OR ラブい OR 兄弟 OR おめでとう OR 誕生祭 OR お団子 OR うっすい OR お疲れ様でした OR イベント OR イベ頑張るぞ OR ヒートアップ OR ボルテージアップ OR フィーチャー OR 楽しみです OR スキ OR 好き OR 大好き OR 愛で)"
    whiteList = {
        "天祥院英智": "天祥院 英智 OR 天祥院 OR 英智 OR 旧fine OR fine",
        "日々樹渉": "日々樹 渉 OR 日々樹 OR 渉 OR 英智 OR 五奇人 OR fine",
        "姫宮桃李": "姫宮 桃李 OR 姫宮 OR 桃李 OR 弓弦 OR fine",
        "伏見弓弦": "伏見 弓弦 OR 伏見 OR 弓弦 OR 桃李 OR fine",
        "氷鷹北斗": "氷鷹 北斗 OR 氷鷹 OR 北斗 OR Trickstar",
        "明星スバル": "明星 スバル OR 明星 OR スバル OR Trickstar",
        "遊木真": "遊木 真 OR 遊木 OR 真 OR Trickstar",
        "衣更真緒": "衣更 真緒 OR 衣更 OR 真緒 OR 凛月 OR Trickstar",
        "守沢千秋": "守沢 千秋 OR 守沢 OR 千秋 OR 奏汰 OR 流星隊",
        "深海奏汰": "深海 奏汰 OR 深海 OR 奏汰 OR 千秋 OR 五奇人 OR 流星隊",
        "南雲鉄虎": "南雲 鉄虎 OR 南雲 OR 鉄虎 OR 流星隊",
        "高峯翠": "高峯 翠 OR 高峯 OR 翠 OR 千秋 OR 流星隊",
        "仙石忍": "仙石 忍 OR 仙石 OR 忍 OR 流星隊",
        "天城一彩": "天城 一彩 OR 天城 OR 一彩 OR 燐音 OR ALKALOID",
        "白鳥藍良": "白鳥 藍良 OR 白鳥 OR 藍良 OR ALKALOID",
        "礼瀬マヨイ": "礼瀬 マヨイ OR 礼瀬 OR マヨイ OR ALKALOID",
        "風早巽": "風早 巽 OR 風早 OR 巽 OR HiMERU OR ALKALOID",
        "乱凪砂": "乱 凪砂 OR 乱 OR 凪砂 OR 日和 OR 旧fine OR Eden",
        "巴日和": "巴 日和 OR 巴 OR 日和 OR 凪砂 OR ジュン OR 旧fine OR Eden",
        "七種茨": "七種 茨 OR 七種 OR 茨 OR 凪砂 OR Eden",
        "漣ジュン": "漣 ジュン OR 漣 OR ジュン OR Eden",
        "斎宮宗": "斎宮 宗 OR 斎宮 OR 宗 OR みか OR 五奇人 OR Valkyrie",
        "影片みか": "影片 みか OR 影片 OR みか OR Valkyrie",
        "葵ひなた": "葵 ひなた OR 葵 OR ひなた OR ゆうた OR 2wink",
        "葵ゆうた": "葵 ゆうた OR 葵 OR ゆうた OR ひなた OR 2wink",
        "天城燐音": "天城 燐音 OR 天城 OR 燐音 OR 一彩 OR Crazy:B",
        "HiMERUHiMERU": "Crazy:B",
        "桜河こはく": "桜河 こはく OR 桜河 OR こはく OR HiMERU OR Crazy:B OR Double Face",
        "椎名ニキ": "椎名 ニキ OR 椎名 OR ニキ OR HiMERU OR Crazy:B",
        "朔間零": "朔間 零 OR 朔間 OR 零 OR 凛月 OR アドニス OR 五奇人 OR UNDEAD",
        "羽風薫": "羽風 薫 OR 羽風 OR 薫 OR アドニス OR UNDEAD",
        "大神晃牙": "大神 晃牙 OR 大神 OR 晃牙 OR アドニス OR UNDEAD",
        "乙狩アドニス": "乙狩 アドニス OR 乙狩 OR アドニス OR UNDEAD",
        "真白友也": "真白 友也 OR 真白 OR 友也 OR に〜ちゃん OR Ra*bits",
        "仁兎なずな": "仁兎 なずな OR 仁兎 OR なずな OR に〜ちゃん OR Ra*bits",
        "天満光": "天満 光 OR 天満 OR 光 OR に〜ちゃん OR Ra*bits",
        "紫之創": "紫之 創 OR 紫之 OR 創 OR に〜ちゃん OR Ra*bits",
        "蓮巳敬人": "蓮巳 敬人 OR 蓮巳 OR 敬人 OR 紅月",
        "鬼龍紅郎": "鬼龍 紅郎 OR 鬼龍 OR 紅郎 OR 紅月",
        "神崎颯馬": "神崎 颯馬 OR 神崎 OR 颯馬 OR 紅月",
        "朱桜司": "朱桜 司 OR 朱桜 OR 司 OR Knights",
        "月永レオ": "月永 レオ OR 月永 OR レオ OR Knights",
        "瀬名泉": "瀬名 泉 OR 瀬名 OR 泉 OR レオ OR Knights",
        "朔間凛月": "朔間 凛月 OR 朔間 OR 凛月 OR Knights",
        "鳴上嵐": "鳴上 嵐 OR 鳴上 OR 嵐 OR Knights",
        "逆先夏目": "逆先 夏目 OR 逆先 OR 夏目 OR つむぎ OR 五奇人 OR Switch",
        "青葉つむぎ": "青葉 つむぎ OR 青葉 OR つむぎ OR 夏目 OR 旧fine OR Switch",
        "春川宙": "春川 宙 OR 春川 OR 宙 OR Switch",
        "三毛縞斑": "三毛縞 斑 OR 三毛縞 OR 斑 OR 奏汰 OR MaM OR Double Face"
    }
    if term in whiteList:
        whiteListQuery = " AND (" + whiteList[term] + ")"   # run for 1st round
        # whiteListQuery = " OR (" + whiteList[term] + ")"   # run for 2nd round
    print(f"whiteListQuery = {whiteListQuery}")   # D

    # get queryNItemNum
    # 1) get tweet by hashtag
    """ print(f"hashtag: math.ceil(item_num) = {math.ceil(item_num)}")   # D
    print(f"word: math.floor(item_num) = {math.floor(item_num)}") """
    # query = "(" + hashtag + " AND #あんスタ OR " + whiteList + ")"
    # query = "(" + hashtag + " AND #あんスタ OR " + ")"
    query = "(" + hashtag + " AND #あんスタ" + whiteListQuery + ")"
    queryNItemNum[query] = math.ceil(item_num)   # add data into dict
    # 2) get tweet by word
    query = "(" + term + " AND あんスタ" + whiteListQuery + ")"
    queryNItemNum[query] = math.floor(item_num)   # add data into dict
    print(f"queryNItemNum = {queryNItemNum}")

    # loop thru param & use them to scrape tweet
    for ele in queryNItemNum:
        tweet_query = ele
        tweet_num = queryNItemNum[ele]
        print(f"tweet_query = {tweet_query}")
        print(f"tweet_num = {tweet_num}")

        # 1st round - must include ≥ 1 white list word
        output = getOutputFromTweets(tweet_query, tweet_num, api, lang)
        out += output

        # get len for scraped tweet
        """ print(f"tweets = {tweets}")
        len = 0
        for tweet in tweets:   # TODO: remove redundant
            len += 1 """
        length = len(output)
        # len = len(list(tweets))
        print(f"1) length = {length}")

        if (tweet_num > length):
            # update param
            tweet_query = tweet_query.replace(" AND (", " OR (")
            tweet_num = tweet_num - length
            print(f"tweet_query = {tweet_query}")
            print(f"tweet_num = {tweet_num}")
            # 2nd round - no need include ≥ 1 white list word
            output = getOutputFromTweets(tweet_query, tweet_num, api, lang)
            out += output

            # get len for scraped tweet
            length = len(output)
            print(f"2) length = {length}")

    # result max_results of tweets' content & id (by hashtag & word)
    return out


def getOutputFromTweets(tweet_query, tweet_num, api, lang):
    # declare var
    output = []

    # scrape tweets from api
    tweets = tweepy.Cursor(
        # api.search_tweets, q=hashtag, tweet_mode="extended", lang=lang).items(math.ceil(item_num))   # OPT: compat, lang="en" / "zh"; .items(1)
        api.search_tweets, q=tweet_query, tweet_mode="extended", lang=lang).items(tweet_num)

    # loop tweet to get full_text, id_str & store & return them
    for tweet in tweets:   # TODO: remove redundant
        print("Run getOutputFromTweets...")
        # print(f"tweet = {tweet}")   # D
        # print(f"tweet._json = {tweet._json}")   # D
        data = {}
        # OPT: tweet['content']
        """# TEST CASE: test server down w code 500
        data['content'] = tweet['content']"""
        data['content'] = tweet._json["full_text"]   # OPT: tweet['content']
        data['id'] = str(tweet._json["id_str"])   # OPT: tweet['id']
        output.append(data)
    # print(f"hashtag: tweets = {tweets}")   # D
    # output += tweets
    # get content & id col data only
    return output


# get Twitter Api to connect to it
def getTwitterApi():
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
    return api

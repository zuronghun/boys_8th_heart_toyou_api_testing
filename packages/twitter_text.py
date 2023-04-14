# search tweet_num/2 tweets by hashtag & tweet_num/2 by word (25 if tweet_num = 50)
def get_tweets(keyword=None, hashtag=None, lang=None, tweet_num=None):
    # query term
    if keyword is not None:
        query_term = keyword
    elif hashtag is not None:
        query_term = "#" + hashtag
    else:   # keyword is None & hashtag is None:
        query_term = "#VaccinationDrive"
    # print(f"query_term = {query_term}")
    # print(f"lang = {lang}")

    # get word without hashtag
    if query_term[0] != "#":
        word = query_term
    else:
        word = query_term[1:]   # remove hastag
    # print(f"word = {word}")   # D

    # lib = ""
    # tweet_num = 3   # OPT: 50
    if (tweet_num == None):
        tweet_num = 3

    try:   # default is tweepy lib
        lib = "tweepy"
        from packages.scrape_tweet_by_tweepy import main
        out = main(word, tweet_num, lang)
    except:  # switch to snscrape lib (if tweepy is down)
        lib = "snscrape"
        from packages.scrape_tweet_by_snscrape import main
        out = main(word, tweet_num)
    # print(f"=== lib used: {lib} ===")   # D

    # TODO: create a new folder, namely tweets_backup (if it is no exist yet)
    output_filename = "tweets_backup/" + \
        word.replace(" ", "_") + "_" + lib + ".txt"   # OPT: .json
    # print(f"=== create file: {output_filename} ===")   # D
    with open(output_filename, 'w') as f:
        # print(f"out = {out}")   # D
        # f.write(f"=== lib used: {lib} ===\n\nout = ")   # OPT: tweet.json()
        f.write(str(out))   # OPT: tweet.json()
        f.write('\n')
        f.flush()

    # print(f"OUT: out = {out}")   # D
    return out


def get_text(keyword=None, hashtag=None, lang=None):
    tweets = get_tweets(keyword, hashtag, lang)

    text = ""
    for tweet in tweets:
        # print(f"IMPORTANT: tweet = {tweet}")
        text += tweet._json["full_text"]
        # print("text:", text)

    return text


# TODO: rename "title" to "content"
# def get_data(keyword=None, hashtag=None, lang=None, prev_data=None):
def get_data(tweets, lang):
    import fugashi
    from wordcloud import STOPWORDS

    # create stopword list:
    stopwordSet = set(STOPWORDS)   # maybe can set at outer level
    if lang == "en":
        stopwordSet.update(["drink", "now", "wine", "flavor", "flavors"])
    elif lang == "ja":
        stopwordSet.update(['てる', 'いる', 'なる', 'れる', 'する', 'ある', 'こと', 'これ', 'さん', 'して',   # OPT: stopwords.update()
                            'くれる', 'やる', 'くださる', 'そう', 'せる', 'した',  '思う',
                            'それ', 'ここ', 'ちゃん', 'くん', '', 'て', 'に', 'を', 'は', 'の', 'が', 'と', 'た', 'し', 'で',
                            'ない', 'も', 'な', 'い', 'か', 'ので', 'よう', '', 'れ', 'さ', 'なっ',
                            # from ng col (https://docs.google.com/spreadsheets/d/1RF3nzLGfaQeENwMXYQOR3Dw6bH7l7dJ9a6IPlbYW6l8/edit#gid=235398883)
                            "SEX", "ちんこ", "うんこ", "ちんちん", "天城燐音であれば、「天城燐音」「天城」「燐音」など自身の名前は絶対1番ワードクラウド上で大きく表示されてしまうはずなので、各キャラクター自身の名前は表示しないようにしたいです", "あんスタ", "あんさんぶるスターズ"])
    # print("stopwordSet =", stopwordSet)

    """ tweets = get_tweets(keyword, hashtag, lang)

    text = ""
    for tweet in tweets:
        # print(f"IMPORTANT: tweet = {tweet}")
        text += tweet._json["full_text"]
        # print("text:", text) """

    """tweets = get_tweets(keyword, hashtag, lang)

    if prev_data is not None:
        # tweets += prev_data
        tweets = prev_data + tweets
    # tweets = ["aaa bbb ccc", "bbb ccc ddd", "eee fff ggg"]
    # print(f"tweets = {tweets}")"""

    count_dict = dict()
    titles_dict = dict()
    # tweet id used to get its url (http://twitter.com/twitter/statuses/{id})
    ids_dict = dict()
    out_dict = dict()

    for tweet in tweets:
        """ # print(f"tweet = {tweet}")   # D
        # print(f"tweet._json = {tweet._json}")
        # print(f"tweet._json['full_text'] = {tweet._json['full_text']}")
        # print(f"tweet.text = {tweet.text}")
        # print(f"tweet.id = {tweet.id}") """

        # get text & id
        text = tweet["content"]
        id = tweet["id"]
        # print(f"HERE: text = {text}")

        # words = text.split()   // ONLY work well in en
        # The Tagger object holds state about the dictionary.
        tagger = fugashi.Tagger()  # type: ignore
        words = [word.surface for word in tagger(text)]

        # print(text)
        # print(words)

        # if (word not in count_dict)
        # count_dict.

        for word in words:
            # print(word)

            if (word in stopwordSet):
                # print(f"this word {word} is a stopword")
                continue

            # count_dict[word] = ((word in count_dict) ? count_dict.get(word) : 0) + 1
            count = 0   # counter start from 0 by default
            titles = list()   # OPT: set()
            ids = list()   # OPT: set()

            if (word in count_dict):
                # set default value if value is None
                count = count_dict.get(word)
                titles = titles_dict.get(word)
                ids = ids_dict.get(word)

            # use back default value if None
            if count is None:
                count = 0
            if titles is None:
                titles = list()
            if ids is None:
                ids = list()

            # print("=====")
            # print(f"BFR: titles = {titles}")
            # avoid to add duplicate data (can't use set in JSONObject())
            if text not in titles:
                '''print(f"(text not in titles) = {(text not in titles)}")
                print(f"text = {text}")
                print(f"titles = {titles}")'''
                titles.append(text)   # OPT: add
            # avoid to add duplicate data (can't use set in JSONObject())
            if id not in ids:
                ids.append(id)   # OPT: add
            # print(f"AFR: titles = {titles}")

            count_dict[word] = count + 1
            titles_dict[word] = titles
            ids_dict[word] = ids
            # print(f"count_dict = {count_dict}")
            # print(f"titles_dict = {titles_dict}")

            out_dict = {
                "count": count_dict,
                "sample_title": titles_dict,
                "ids": ids_dict
            }
            # print(f"out_dict = {out_dict}")

    # return text
    return out_dict


def get_refined_tweet_list(keyword=None, hashtag=None):
    import pandas as pd   # make dataframe, export csv

    tweets = get_tweets(keyword, hashtag)

    refined_tweet_list = list()
    for tweet in tweets:
        # print(f"IMPORTANT: tweet = {tweet}")
        text = tweet._json["full_text"]
        # print("text:", text)

        refined_tweet = {'text': text,
                         'favorite_count': tweet.favorite_count,
                         'retweet_count': tweet.retweet_count,
                         'created_at': tweet.created_at}

        refined_tweet_list.append(refined_tweet)
        # print("refined_tweet_list:", refined_tweet_list)

    # make a dataframe of tweets with columns representing the different attributes of tweet
    df = pd.DataFrame(refined_tweet_list)
    df.to_csv('refined_tweets.csv')
    # print("df:", df)

    # return df
    return refined_tweet_list

# import packages
# pip3 install snscrape
from snscrape.modules import twitter
import json
import math


def main(term=None, number=None):   # term without hashtag
    # set default value
    if term is None:
        term = '氷鷹北斗'
    if number is None:
        number = 3

    out = []
    # print(f"number = {number}")   # D

    # scrape Twitter hashtags
    # print("===== hashtag =====")   # D
    # get hashtag & max results
    hashtag = [term]   # OPT: scraping, あんスタ, あんスタウェルカム祭, はじめてさんいらっしゃ〜い
    max_results = math.ceil(number/2)   # OPT: 50
    # print(f"max_results = {max_results}")   # D

    # scrape hashtag
    def scrape_hashtag(hashtag):
        scraper = twitter.TwitterHashtagScraper(hashtag)
        return scraper

    # loop max_results times to scrape hashtag to get content & id
    for query in hashtag:
        scraper = scrape_hashtag(query)
        i = 0
        for i, tweet in enumerate(scraper.get_items(), start=1):
            if max_results and i > max_results:
                break

            tweet_json = json.loads(tweet.json())
            # out.append(tweet_json)
            # out.append(tweet_json['content'])
            data = {}
            data['content'] = tweet_json['content']
            data['id'] = tweet_json['id']
            out.append(data)
            # print(f"\n{i}) Scraped tweet: {tweet_json}")   # D
            # print(f"\n{i}) Scraped tweet: {tweet_json['content']}")   # D
    ####################################################################################################

    # scrape Twitter word
    # print("===== word =====")   # D
    # get word & max results
    queries = [term]
    max_results = math.floor(number/2)   # OPT: 50
    # print(f"max_results = {max_results}")   # D

    # scrape word
    def scrape_search(query):
        scraper = twitter.TwitterSearchScraper(query)
        return scraper

    # loop max_results times to scrape word to get content & id
    for query in queries:
        scraper = scrape_search(query)
        i = 0
        for i, tweet in enumerate(scraper.get_items(), start=1):
            if max_results and i > max_results:
                break

            tweet_json = json.loads(tweet.json())
            # out.append(tweet_json)
            # out.append(tweet_json['content'])
            data = {}
            data['content'] = tweet_json['content']
            data['id'] = tweet_json['id']
            out.append(data)
            # print(f"\n{i}) Scraped tweet: {tweet_json['content']}")   # D

    # result max_results of tweets' content & id (by hashtag & word)
    return out

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from tweets.models import Tweet
from tweets.serializers import TweetSerializers
from rest_framework.decorators import api_view

# Create your views here.
# Global variables
tweet_num = 50   # number of tweet(s) per request
lang = "ja"     # language


@api_view(['GET', 'POST', 'DELETE'])
def tweet_list(request):
    # GET list of tweets, POST a new tweet, DELETE all tweets

    # retrieve objects (with condition)
    # retrieve all Tweets / find by term from PostgreSQL database
    if request.method == 'GET':
        tweets = Tweet.objects.all()

        term = request.GET.get('term', None)
        if term is not None:
            # partial value (similar to same)
            tweets = tweets.filter(term__icontains=term)

        tweets_serializers = TweetSerializers(tweets, many=True)
        return JsonResponse(tweets_serializers.data, safe=False)
        # 'safe=False' for objects serialization

    # create a new object
    # create and save a new Tweet
    elif request.method == 'POST':
        tweet_data = JSONParser().parse(request)
        tweet_serializer = TweetSerializers(data=tweet_data)
        if (tweet_serializer.is_valid()):
            tweet_serializer.save()
            return JsonResponse(tweet_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete all objects
    # delete all Tweets from database
    elif request.method == 'DELETE':
        count = Tweet.objects.all().delete()
        # print(f"count = {count}")   # DEBUG
        return JsonResponse({'message': '{} Tweets were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def tweet_detail(request, pk):
#     # ... tweet = Tweet.objects.get(pk=pk)
#     # ...
#     # find tweet by pk (id)
#     try:
#         tweet = Tweet.objects.get(pk=pk)
#     except Tweet.DoesNotExist:
#         return JsonResponse({'message': 'The tweet does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     # retrieve a single object
#     # find a single Tweet with an id
#     if request.method == 'GET':
#         tweet_serializer = TweetSerializers(tweet)
#         return JsonResponse(tweet_serializer.data)

#     # update an object
#     # update a Tweet by the id in the request
#     elif request.method == 'PUT':
#         tweet_data = JSONParser().parse(request)
#         tweet_serializer = TweetSerializers(tweet, data=tweet_data)
#         if tweet_serializer.is_valid():
#             tweet_serializer.save()
#             return JsonResponse(tweet_serializer.data)
#         return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def tweet_detail(request, pk):
    #  GET / PUT / DELETE tweet
    # ... tweet = Tweet.objects.get(pk=pk)
    # ...
    # find tweet by pk (id)
    try:
        tweet = Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return JsonResponse({'message': 'The tweet does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # retrieve a single object
    # find a single Tweet with an id
    if request.method == 'GET':
        tweet_serializer = TweetSerializers(tweet)
        return JsonResponse(tweet_serializer.data)

    # update an object
    # update a Tweet by the id in the request
    elif request.method == 'PUT':
        # print(f"HERE: request = {request}")
        tweet_data = JSONParser().parse(request)
        # print(f"HERE: tweet_data = {tweet_data}")
        tweet_serializer = TweetSerializers(tweet, data=tweet_data)
        if tweet_serializer.is_valid():
            tweet_serializer.save()
            return JsonResponse(tweet_serializer.data)
        return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete an object
    # delete a Tweet with the specified id
    elif request.method == 'DELETE':
        tweet.delete()
        return JsonResponse({'message': 'Tweet was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


""" @api_view(['GET'])
def tweet_list_published(request):
    # GET all published tweets
    tweets = Tweet.objects.filter(published=True)

    # find all objects by condition
    # find all objects with published = True
    if request.method == 'GET':
        tweets_serializers = TweetSerializers(tweets, many=True)
        return JsonResponse(tweets_serializers.data, safe=False) """

# v1 api for getTweetByTerm


@api_view(['POST', 'GET'])
def tweet_list_v1(request):
    # POST -> find by term; GET -> do refetch the data (cron job)
    # permission_classes = [AllowAny] # TODO

    # retrieve all Tweets from PostgreSQL database
    tweets = Tweet.objects.all()
    if request.method == 'POST':
        tweet_data = JSONParser().parse(request)

        # get term
        term = tweet_data['term']   # OPT = あんスタ, あんスタウェルカム祭, はじめてさんいらっしゃ〜い
        # print(f"term = {term}")   # D

        if term is not None:
            # chk if got this complete value (exactly same), else create a new Tweet object and save it
            """tweet = tweets.filter(term=term)   # OPT: term__icontains=term

            # if empty, means no found this data
            if len(tweet) < 1:"""

            # find tweet by term, else create a new tweet
            try:
                tweet = Tweet.objects.get(term=term)
            except Tweet.DoesNotExist:
                # get accumulated tweets
                # get a prev data by default
                # prev_tweets = get_tweets_from_twitter(term)
                prev_tweets = []
                curr_tweets = get_tweets_from_twitter(term)
                accu_tweets = prev_tweets + curr_tweets   # accumulate prev_tweets w curr data
                # print(f"prev_tweets = {prev_tweets}")   # D
                # print(f"curr_tweets = {curr_tweets}")   # D
                # print(f"accu_tweets = {accu_tweets}")   # D

                # get data
                # get_data_from_tweets(None, term, lang, prev_tweets)
                data = get_data_from_tweets(accu_tweets)

                # create new tweet obj
                tweet_data = dict()
                tweet_data["term"] = term
                tweet_data["data"] = data
                tweet_data["prev_tweets"] = accu_tweets
                # print(f"tweet_data = {tweet_data}")   # D

                tweet_serializer = TweetSerializers(
                    data=tweet_data)  # type: ignore
                # print(f"tweet_serializer = {tweet_serializer}")   # D

                if (tweet_serializer.is_valid()):
                    tweet_serializer.save()
                    return JsonResponse(tweet_serializer.data, status=status.HTTP_201_CREATED)
                return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # return single data only (no array w multiple data)
            # tweets_serializers = TweetSerializers(tweets, many=True)
            tweet_serializer = TweetSerializers(tweet)

            # return single data only (no array w multiple data)
            # return JsonResponse(tweets_serializers.data, safe=False)
            return JsonResponse(tweet_serializer.data)

    # refresh & update single tweet by its term
    elif request.method == 'GET':
        print("=== cron job is auto running ===")

        """ # get term   # TODO: remove this code block if unneeded
        term = request.GET.get('term', None) """

        for tweet in tweets:
            # print(f"tweet = {tweet}")   # D

            # get term
            term = getattr(tweet, "term")   # OPT: tweet["term"]
            # print(f"term = {term}")   # D

            # get accumulated tweets
            prev_tweets = getattr(tweet, "prev_tweets")
            if prev_tweets == []:   # handle prev empty list prev_tweets
                prev_tweets = get_tweets_from_twitter(term)
            # get the last num_tweet_per_request tweets from prev_tweets (eg. 50 if num_tweet_per_request = 50)
            """else:
                prev_tweets = prev_tweets[-tweet_num:]"""
            curr_tweets = get_tweets_from_twitter(term)
            # accumulate prev_tweets w curr data
            accu_tweets = prev_tweets[-tweet_num:] + curr_tweets
            # print(f"prev_tweets = {prev_tweets}")   # D
            # print(f"curr_tweets = {curr_tweets}")   # D
            # print(f"accu_tweets = {accu_tweets}")   # D

            # get data
            # data = {"num666": 123666}
            # data = get_data_from_tweets(None, term, lang, prev_tweets[-tweet_num:])
            data = get_data_from_tweets(accu_tweets)

            # update new tweet obj
            tweet_data = dict()
            tweet_data["term"] = term
            tweet_data["data"] = data
            # tweet_data["prev_tweets"] = accu_tweets   // it will discard prev value for prev_tweets
            tweet_data["prev_tweets"] = prev_tweets + curr_tweets

            # serialize & save into db
            tweet_serializer = TweetSerializers(
                tweet, data=tweet_data)  # type: ignore

            if (tweet_serializer.is_valid()):
                tweet_serializer.save()

        # return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'All tweets are updated by term successfully!'}, status=status.HTTP_204_NO_CONTENT)


# _v1 Reusable / small function(s)
# get tweet
# def get_tweets_from_twitter(keyword=None, hashtag=None, lang=None):
def get_tweets_from_twitter(term):
    from packages.twitter_text import get_tweets
    keyword = None
    hashtag = term
    tweets = get_tweets(keyword, hashtag, lang, tweet_num)
    return tweets

# get tweet text


# def get_data_from_tweets(keyword=None, hashtag=None, lang=None, prev_tweets=None):   # hashtag=アンスタ
def get_data_from_tweets(tweets):

    from packages.twitter_text import get_data
    # text = get_data(keyword, hashtag, lang, prev_tweets)
    text = get_data(tweets, lang)
    return text

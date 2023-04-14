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

    # set default value for tweet_num
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

    """# TEST CASE: add stopword into text
    for output in out:
        print(f'BFR: output["content"] = {output["content"]}')
        output["content"] += "天城燐音であれば、「天城燐音」「天城」「燐音」など自身の名前は絶対1番ワードクラウド上で大きく表示されてしまうはずなので、各キャラクター自身の名前は表示しないようにしたいです"
        print(f'AFR: output["content"] = {output["content"]}')"""

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
        # "う", "ぇ", "お", "く", "ご", "っ", "ひ", "ま", "ょ", "ら", "出", "弦", "斑", "方", "程", "見", "願",
        # "ざ", "だ", "ち", "ぬ", "り", "伏", "宜", "揃", "服", "欲", "着",
        #  "ぎ", "げ", "だ", "ほ", "ろ",
        # "人", "仕", "使", "奈", "島", "悟", "愛", "晒", "毛", "狙", "狼", "縞", "買", "踊", "馬",
        # "う", "お", "く", "っ", "ま", "み", "や", "よ", "キ", "ニ", "三", "厳", "回", "夢", "嬉", "旧", "樹", "流", "渉", "疲", "的", "私", "美", "色", "見",
        stopwordSet.update([
            # 2) from ng col (https://docs.google.com/spreadsheets/d/1RF3nzLGfaQeENwMXYQOR3Dw6bH7l7dJ9a6IPlbYW6l8/edit?fbclid=IwAR3W1apupfK4UJO-PtmszOF3Cuf9PCI5FNQIluY_JFWgWQ_lRkGLy1e1HMU#gid=235398883)
            "日本鬼子", "あんスタ", "あんさんぶるスターズ", "あーむかっと", "あえいで", "あしきり", "あすぺ", "-あすぺくと", "あどれす", "あぬらー", "あめ公", "あるちゅう", "ある中", "いたこう", "いた公", "いんばい", "ヴぁぎな", "うぇのむ", "うざい", "うじよりそだち", "えちごのこめつき", "えっち", "えんじょこうさい", "おーがずむ", "おーるどみす", "おなに", "おなぬ", "おなほ", "おにしまづ", "おぼれじぬ", "おまんたん", "おめこ", "-あけおめことよろ", "おめしゃん", "おめんちぃ", "おもてにほん", "おわい屋", "おんなこども", "かいしゅん", "がいじ", "-がいじん", "かうぱー", "かくしどり", "かくちょういん", "かくちょうだん", "かこちょう", "がちゃ目", "かつぎ屋", "かぶや", "かわらこじき", "かんきん", "がんじゃ", "かんたりじん", "きかれもの", "ぎっちょ", "きめえ", "ぎゃくさつ", "ぎゃくたい", "ぎゃくはん", "きょうせいわいせつ", "きょうはく", "きんしんそうかん", "き印", "くいちん棒", "ぐどん", "くぱぁ", "くびきり", "くんにりんぐす", "ぐんもう", "こーるがーる", "こかいん", "こっぱやくにん", "ごみ虫", "ころす", "ころせ", "ご無", "ご有", "ざーめん", "さつじん", "さんかんせいばつ", "さんごくじん", "しこって", "しっくすないん", "しのうこうしょう", "じへいしょうじ", "じゅうかん", "しゅうげき", "しゅうせんや", "しょういんしん", "しょくぶつにんげん", "しりぬぐい", "しんきんそうかん", "しんしんしょうがいしゃ", "じんしんばいばい", "しんへいみん", "ずーしゃー", "ずーじゃー", "すくーる水着", "すけまん", "すとーかー", "すとーきんぐ", "すぺしゃるk", "すぺるま", "すわっぴんぐ", "せいしんいじょう", "せいしんはくじゃくじ", "せいはくしゃ", "せくしゃるはらすめんと", "そーぷ", "そだちよりうじ", "そちん", "そりまん", "だいいんしん", "だいさんごく", "だいわんはげ", "たけのこいしゃ", "たけのこ医者", "たこ部屋", "ただまん", "たちあがれ日本", "たちんぼ", "たひね", "たれ流し", "ち○こ", "ちかん", "ちくび", "ちそこ", "ちそちそ", "ちそぽ", "ちゃんころ", "ちゅうきょう", "ちょうせんじん", "ちょうせんせいばつ", "ちょっぱり", "ちんかす", "ちんこ", "ちんしこ", "ちんちょう", "ちんぼう", "ちん長", "つんぼ", "ていかいはつこく", "でかちん", "でりへる", "てれくら", "てんさいときょうじんはかみひとえ", "どーてー", "とうあびょうふ", "とうさつ", "とうちょう", "どうてー", "どうてい", "とくしゅがっきゅう", "とくしゅがっこう", "とくしゅぶたい", "とくしゅぶらく", "どざえもん", "とさつじょう", "とさつにん", "どさまわり", "どさ回り", "どぴゅ", "どもり", "どやがい", "とやまのさんすけ", "どや街", "とるこじょう", "とるこぶろ", "とるこ嬢", "とるこ風呂", "どん百姓", "なまほんばん", "なま本番", "にぐろ", "にこよん", "にんぴにん", "ぬれまん", "のうなし", "のうまくえん", "ばーてい", "はいじゃっく", "ばいしゅん", "ぱいずり", "ぱいぱん", "ばいぶ", "-りばいぶ", "ばかちょん", "ぱこぱこ", "ばすじゃっく", "ばたや", "ばた屋", "はっきょう", "ばった屋", "はみちん", "はめ撮り", "ぱんつ", "-ぱんつぁー", "ぱんてぃ", "はんとうじん", "ぴーぴんぐ", "ぴっきんぐ", "びっち", "ひのもとおにこ", "ひんにゅー", "ひんにゅう", "ひんのう", "ふーぞく", "ふぁっく", "ふうぞく", "ふぇら", "-すふぇら", "-ふぇらーり", "-かふぇらて", "-ろっくふぇらー", "-ふぇらがも", "ぶさいく", "ふじのやまい", "ぷっしー", "ぶっしゅまん", "ふみきりばん", "ぶらくみん", "ぶるせら", "ふろうじ", "ふろうしゃ", "ぶんもう", "ぺーにす", "ぺい患", "ぺにーす", "ぺにす", "へろいん", "ほうけい", "ぼうこう", "ぽこちん", "ぽこぺん", "ぼっき", "ほてとる", "ぽり公", "ぽんこつ屋", "ぽんびき", "ぽん引き", "ほ込", "ほ別", "ま○こ", "まじきち", "ますたーべーしょん", "まそこ", "まりふぁな", "まわす", "まん○", "まんかす", "まんきん", "まんぐり", "まんこ", "まんごっこ", "まんずり", "まんたく", "まんちつ", "まんちん", "まんぴー", "まんびき", "まんびら", "まん開", "-わんまん開催", "まん金", "まん汁", "まん拓", "まん毛", "みかいはつこく", "みつくち", "みつばい", "みんなの党", "むこをとる", "むすめをかたづける", "めかけ", "めくらばん", "めくら縞", "めくら蛇におじず", "めくら判", "めくら滅法", "めるあど", "めんへら", "もうあい", "もうじん", "もはすきー", "もりまん", "やー様", "やぶにらみ", "やりまん", "よせば", "よめにやる", "らいびょう", "らい病", "らくにんぶらく", "らんかん", "りょうぎゃく", "りょうじょく", "りょうはん", "りんかん", "りんち", "るんぺん", "れいぷ", "ろーたー", "ろりこん", "ろりろり", "ろんぱり", "ろ助", "愛液", "暗殺", "伊勢こじき", "慰安婦", "育ちより氏", "引かれ者", "淫姦", "淫行", "淫売", "淫縛", "淫蜜", "淫毛", "淫乱", "陰核", "陰茎", "陰唇", "陰嚢", "陰毛", "隠し撮り", "隠亡屋", "右翼", "越後の米つき", "円光", "援交", "援助交際", "汚穢屋", "沖仲仕", "沖縄社会大衆党", "何かっぷ", "嫁にやる", "過去帳", "街宣車", "拡張員", "拡張団", "株屋", "姦淫", "姦通", "監禁", "顔騎", "顔射", "基地外", "寄せ場", "寄り目", "気違い", "騎乗位", "鬼石曼子", "虐殺", "虐待", "虐犯", "逆援", "巨ちん", "巨乳", "強姦", "強盗", "脅迫", "金玉", "銀行口座", "愚鈍", "群盲", "犬殺し", "減税日本", "後進国", "乞食", "交姦", "公明党", "幸福の科学", "幸福実現党", "紅毛人", "拷問", "国民新党", "左翼", "在日韓国人", "殺す", "殺る", "殺害", "殺人", "三韓征伐", "三国人", "三也", "士農工商", "子宮", "子種", "指まん", "支那人", "死ね", "死姦", "死体", "氏ね", "氏より育ち", "自慰", "自殺", "自閉症児", "自民党", "失禁", "射精", "社会党", "手こき", "手淫", "手首ちゃん", "酒鬼薔薇聖斗", "首切り", "受精", "周旋屋", "襲撃", "汁男優", "獣姦", "出会い系", "純とろ", "処女", "女子供", "女郎", "娼婦", "小根", "小使い", "小日本", "小便", "-小便小僧", "少年院", "上方のぜい六", "植物人間", "心身障害者", "新党改革", "新党大地", "新党日本", "新平民", "人身売買", "性器", "性交", "性芯異常", "正常位", "生せら", "生はめ", "精液", "精子", "精神異常", "精神薄弱児", "精薄者", "青姦", "赤旗", "賎民", "鮮人", "粗ちん", "創価学会", "早漏", "相姦", "足切り", "体位", "体罰", "台湾はげ", "大人のおもちゃ", "大人の関係", "大麻", "第三国", "男汁", "知恵の遅れている子供", "知恵遅れ", "地まわり", "恥姦", "痴漢", "痴女", "痴態", "痴呆", "遅漏", "中共", "中国共産党", "中出し", "中田氏", "仲だし", "朝鮮征伐", "潮ふき", "潮吹", "調教", "直あど", "直め", "低開発国", "剃毛", "泥棒", "溺れ死ぬ", "天安門事件", "天才と狂人は紙一重", "転売", "屠殺", "屠役", "土左衛門", "土人", "奴隷", "東亜病夫", "東夷", "東洋鬼", "盗む", "盗撮", "盗聴", "統一協会", "踏切番", "同和地区", "童貞", "特殊学級", "特殊学校", "毒殺", "南鮮", "南部のしゃけの鼻まがり", "軟禁", "二穴責め", "肉びら", "肉便器", "肉棒", "肉壺", "日本のちべっと", "日本鬼子", "日本共産党", "乳首", "尿道", "濡れまん", "覗く", "馬鹿でもちょんでも", "馬丁", "廃人", "排便", "排泄", "買春", "売春", "売女", "白痴", "発情液", "半島人", "犯し", "犯す", "犯る", "犯罪", "番太", "非人", "表日本", "貧乳", "貧農", "不治の病", "富山の三助", "浮浪児", "浮浪者", "部落", "風俗", "糞尿", "文盲", "変態", "包茎", "放尿", "法輪功", "暴姦", "暴行", "北鮮", "撲殺", "勃起", "本気汁", "麻薬", "万引き", "未開発国", "密売", "密輸", "民主党", "民進党", "婿をとる", "娘をかたづける", "毛唐", "毛等", "盲愛", "盲人", "木っ端役人", "目障り", "遊女屋", "乱姦", "乱交", "卵子", "裏びでお", "裏日本", "凌虐", "凌辱", "凌犯", "陵辱", "輪姦", "炉利", "炉理", "露助", "和姦", "賄賂", "喘いで", "媚薬", "嬲る", "嫐る", "浣腸", "猥褻", "睾丸", "穢多", "肛門", "膣", "クンニ", "asahinet.jp", "auone-net.jp", "biglobe.ne.jp", "b地区", "commufa.jp", "dion.ne.jp", "docomo.ne.jp", "eonet.ne.jp", "ezweb.ne.jp", "fuck", "gmail.com", "gすぽっと", "hotmail.co.jp", "live.jp", "manko", "nifty.com", "ocn.ne.jp", "pkga.jp", "plala.or.jp", "sex", "so-net.ne.jp", "softbank.ne.jp", "wakwak.com", "yahoo.co.jp",
                            # 1) from ng col (https://docs.google.com/spreadsheets/d/1RF3nzLGfaQeENwMXYQOR3Dw6bH7l7dJ9a6IPlbYW6l8/edit#gid=235398883)
                            "SEX", "うんこ", "ちんちん", "天城燐音であれば、「天城燐音」「天城」「燐音」など自身の名前は絶対1番ワードクラウド上で大きく表示されてしまうはずなので、各キャラクター自身の名前は表示しないようにしたいです",
                            # symbol
                            "http", "https", "#", ".", "/", ":", "@", "_", "b", "g", "s", "t", "90", "RQ", "RT", "co", "ou", "pV", "、", "。", "「", "」", "あ", "き", "こ", "す", "ず", "ど", "ね", "ば", "る", "ん", "七", "上", "中", "各", "弓", "当", "楽", "燐", "番", "種", "茨", "音", "（", "？", "🥸", "🥺",
                            "0", "1", "2", "3", "4", "5", "6", "7",  "8", "9",
                            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                            "！", "／", "～", "📢", "️", "💕", "🤍", "👶", "🌸",
                            "‼", "【", "】",

                            "…", "≫", "★", "♪",
                            "!", "é", "😢", "🙄", "🙆", "🙏", "‍♀",
                            "(", ")", "❓", "　", "・", "２", "５", "｡", "･", "ﾟ", "🤠",
                            # default
                            'てる', 'いる', 'なる', 'れる', 'する', 'ある', 'こと', 'これ', 'さん', 'して',   # OPT: stopwords.update()
                            'くれる', 'やる', 'くださる', 'そう', 'せる', 'した',  '思う',
                            'それ', 'ここ', 'ちゃん', 'くん', '', 'て', 'に', 'を', 'は', 'の', 'が', 'と', 'た', 'し', 'で',
                            'ない', 'も', 'な', 'い', 'か', 'ので', 'よう', '', 'れ', 'さ', 'なっ',
        ])
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

        # remove stop bfr split sentence into words
        for stopword in stopwordSet:
            text = text.replace(stopword, '')

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

            """# remove stop aft split sentence into words
            if (word in stopwordSet):
                # print(f"this word {word} is a stopword")
                continue"""

            # remove word if it has only one character
            if len(list(word)) <= 2:
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

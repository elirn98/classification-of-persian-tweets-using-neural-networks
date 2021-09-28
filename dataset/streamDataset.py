import csv
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import tweepy as tw
from pandas import DataFrame


access_token = "1147007926965432320-JjdyrxrL4bwWKv87yqoyJGkL1W1n5C"
access_secret = "GWqHR9PpbF0EFznWEFUI6gfxCR53QZJ7s0ry6Fj5M2pQo"
consumer_key = "Cmmy7mwnJ2R7DfZlGGp04Y6tT"
consumer_secret = "LqA83Q5xgH9HPVdL7D59xceg1dP9rJttu67IIXPNrNfllNtd2Z"


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)


class TweetListener(StreamListener):
    counter = 0

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            Tweet_Directory = 't.csv'

            if 'extended_tweet' in json_data:
                if 'full_text' in json_data['extended_tweet']:
                    tweet_text = json_data['extended_tweet']['full_text']
                else:
                    pass  # i need to figure out what is possible here
            elif 'text' in json_data:
                tweet_text = json_data['text']

            tweet_text = tweet_text.replace('\n', ' ').replace("\t"," ")
            if "RT" not in tweet_text:
                with open("tweets.csv", 'a', encoding="utf-8") as f:
                    self.counter += 1
                    str_out = json_data["id_str"] + "\t"
                    tags = ""
                    for hashtag in json_data["entities"]["hashtags"]:
                        tags = tags + "," + hashtag["text"]
                    if tags != "":
                        tags = tags[1:]
                    str_out = str_out + "\t" + tags + "\t" + tweet_text + "\r\n"
                    f.write(str_out)
                    print(str(self.counter) + " : \t" + str_out)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True


counter = 0

sport = ['پرسپولیس', 'استقلال', 'فوتبال', 'والیبال', 'بسکتبال', 'پینگ پنگ', 'لیگ برتر', 'فوتسال', 'شنا', 'ورزشی', 'قهرمانی', 'باشگاه', 'مدال']
social = ['دادگاه', 'قتل','کلاهبرداری', 'پرخاشگری', 'آلودگی هوا','مواد مخدر', 'سیل', 'زلزله', 'گرمایش زمین', 'اجتماعی']
politics = ['وزیر امور خارجه', 'رییس جمهور','بیگانگان', 'دولت','ج.ا', 'سیاست خارجی','قیمت بنزین', 'رهبر', 'سقوط هواپیا', 'سردار سلیمانی', 'سیاسی', 'تحریم دارو','اعتصاب', 'خاورمیانه', 'ج.ا', 'اعذام نکنید']
cultural = ['توریست','مفاخر ادبی', 'تئاتر', 'موسیقی', 'جشنواره فجر','فرهنگی','سینما', 'جشنواره حافظ', 'موزه', 'آثار باستانی', 'تبعیض_نژادی', 'تبعیض_جنسیتی']
health = ['کرونا', 'ویروس', 'درمان', 'پیشگیری', 'دارو', 'سلامتی_پوست', 'سلامت_روان', 'سلامتی','لاغری','کووید','ماسک_بزنیم']
economy = ['یاانه', 'ارز','قیمت طلا','حقوق بازنشستگان', 'دلار', 'بانک مرکزی', 'اقتصادی', 'کارت سوخت', 'طلا', 'تحریم اقتصادی', 'صادرات', 'واردات', 'کمک معیشتی']
scientific = ['هوافضا', 'هوش مصنوعی', 'گرمایش زمین','اصلاح ؤنتبیکی', 'المپیاد', 'رباتبک', 'ناسا' , 'علمی', 'آموزش', 'پؤوهش']
religious = ['دین', 'هیئت','پیامبر', 'قرآن', 'قیام_کربلا','حوزه_علمیه', 'امام_علی','امام_حسین', 'خدا']
university = ['دانشکده' ,'دانشگاه', 'کنکور', 'ارشد','انتخاب_رشته', 'پیام_نور', 'رشته_دانشگاهی', 'اساتید', 'پذیرش_بدون_آزمون']

clusters = [sport, social, politics, cultural, health, economy, scientific, religious, university]
clusterNames = ['sport', 'social', 'politics', 'cultural', 'health', 'economy', 'scientific', 'religious', 'university']

twitter_stream = Stream(auth, TweetListener())
df = DataFrame({'number': [], 'tweet': [], 'label': []})
i = -1
f = open("tweets.csv", 'a', encoding="utf-8")
csvWriter = csv.writer(f, delimiter=',')
csvWriter.writerow(['number', 'tweet', 'label'])
for cluster in clusters:
    i += 1
    for subject in cluster:
        tweets = tw.Cursor(api.search, q=['#'+subject], lang="fa", since="2020-6-1",tweet_mode='extended').items(10000)
        for tweet in tweets:
            print(tweet.full_text)
            tweet_text = tweet.full_text.replace('\n', ' ').replace("\t", " ")
            counter += 1
            if "RT" not in tweet_text:
                csvWriter.writerow([counter, tweet_text, clusterNames[i]])
f.close()

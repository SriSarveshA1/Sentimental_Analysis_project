import json
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from geopy.exc import GeocoderTimedOut #geopy makes easy for developers to locate coordinates of addresses,cities,countries across the globe using the third party geocoders
from geopy.geocoders import Nominatim


class MoodClassifier:
    def __init__(self, classifier_file='my_classifier.pickle'):
        f = open(classifier_file, 'rb')
        self.classifier = pickle.load(f)
        f.close()
        self.stop_words = stopwords.words('english')

    def clean_data(self, token):
        return [item for item in token if not item.startswith('@') and not item.startswith('http')]

    def to_lower(self, token):
        return [item.lower() for item in token]

    def lemmatize(self, token):
        lemmatizer = WordNetLemmatizer()

        result = []
        for item, tag in pos_tag(token):
            if tag[0].lower() in "nva":
                result.append(lemmatizer.lemmatize(item, tag[0].lower()))
            else:
                result.append((lemmatizer.lemmatize(item)))

        return result

    def remove_stop_words(self, token):
        return [item for item in token if item not in self.stop_words]

    def transform_features(self, token):
        feature_set = {}
        for feature in token:
            if feature not in feature_set:
                feature_set[feature] = 0
            feature_set[feature] += 1
        return feature_set

    def get_mood(self, token):
        custom_tokens = self.remove_stop_words(self.lemmatize(self.clean_data(self.to_lower(word_tokenize(token)))))
        category = self.classifier.classify(self.transform_features(custom_tokens))
        return category


class Locator:
    def __init__(self):
        self.geo_locator=Nominatim(user_agent="LearnPython") #User_Agent is an http request header that is sent with each request...#Nominatim requires this value to be set to your application name..M        self.geo_locator=Nominatim(user_agent="LearnPython") #User_Agent is an http request header that is sent with each request...#Nominatim requires this value to be set to your application name..M        self.geo_locator=Nominatim(user_agent="LearnPython") #User_Agent is an http request header that is sent with each request...#Nominatim requires this value to be set to your application name..
                                                             #Moreover, should you have a lot of queries, Nominatim asks that the user_agent also contains your email address (or that you use the email parameter)
        self.location_store={}
        self.lookups=0

    def get_location(self,location_name):
        if location_name in self.location_store:   #If the location_name is already there in the location_store we return the value of location_name from the location_store dictionary
            return self.location_store[location_name]
        try:
            self.lookups+=1   #Each time we are finding the location we are adding the lookups
            location=self.geo_locator.geocode(location_name,language='en')
            self.location_store[location_name]=location
        except GeocoderTimedOut:   #when the time taken to find the location went more we need to return None
            location=None
        return location




def process(input_file, output_file):
    tweets = None
    with open(input_file) as f:
        tweets = json.load(f)

    print("Number of tweets", len(tweets))

    classifier=MoodClassifier()
    locator=Locator()
    cnt=0
    stat={'Positive':0,'Negative':0}
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            tweet=tweet['retweeted_status']
        stat[classifier.get_mood(tweet['full_text'])]+=1

        if 'location' in tweet['user']:            #Every tweet has a user object inside which there is and location object which holds the location object
            location=locator.get_location(tweet['user']['location'])  #we pass the location name
            if location:
                print(location.address)
                print(location.latitude, location.longitude)

        cnt+=1
        if cnt > 10:
            break
    print(stat)
    print("The mood is",stat['Positive']/(stat['Positive']+ stat['Negative']))

    #The mood is 0.6401488592848282 (Java)
    #The mood is 0.5951257186990474 (Python)



if __name__ == "__main__":
    input_file = "tweets_with_python.json"
    process(input_file, None)
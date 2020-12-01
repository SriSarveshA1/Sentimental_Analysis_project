import json
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag


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


def process(input_file, output_file):
    tweets = None
    with open(input_file) as f:
        tweets = json.load(f)

    print("Number of tweets", len(tweets))

    classifier=MoodClassifier()
    cnt=0
    stat={'Positive':0,'Negative':0}
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            tweet=tweet['retweeted_status']
        stat[classifier.get_mood(tweet['full_text'])]+=1
        cnt+=1
        if cnt > 10:
            pass
    print(stat)
    print("The mood is",stat['Positive']/(stat['Positive']+ stat['Negative']))

    #The mood is 0.6401488592848282 (Java)
    #The mood is 0.5951257186990474 (Python)



if __name__ == "__main__":
    input_file = "tweets_with_python.json"
    process(input_file, None)
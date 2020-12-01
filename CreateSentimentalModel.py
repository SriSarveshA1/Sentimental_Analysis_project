from nltk.corpus import twitter_samples

#step1:Gather data
#step2:Clean,lemmatize and remove stop words from data
#step3:Transform data
#step4:Create data set
#step5:Train the model
#step6:Test Accuracy
#step7:Save the model

def main():
    positive_tweets=twitter_samples.tokenized('positive_tweets.json')
    negative_tweets=twitter_samples.tokenized('negative_tweets.json')
    print(positive_tweets[1])
    print(negative_tweets[1])

if __name__=="__main__":
    main()


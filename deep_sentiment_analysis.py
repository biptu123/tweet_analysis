from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax


def analyse_tweet_sentiment(tweet, flag=False):
    # precprcess tweet
    tweet_words = []

    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)

    tweet_proc = " ".join(tweet_words)

    # load model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    labels = ['Negative', 'Neutral', 'Positive']

    # sentiment analysis
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    index = scores.argmax()
    return labels[index]


print(analyse_tweet_sentiment("The BJP has been escorted by the accused in the country's largest #SEXGATE scam, not only to stand up with the rapists.It is ridiculous that there was no information about leaving the country #Prajwalrevanna.Is it difficult for the central government to use all departments including IT, ED and CBI through the Immigration Bureau?Prime Minister Modi has held his hand and campaigned for the first time, despite the fact that the allegations of rape were earlier.So the BJP's stand on the matter should be addressed by Prime Minister @narendramodi, @amitshah, @jpnadda, @rashokabJP, @byvijayendra.This is not the Congress, but the insistence of millions of Kannadigars."))
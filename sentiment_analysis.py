from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import pipeline
from collections import Counter
import string
import matplotlib.pyplot as plt
from deep_sentiment_analysis import analyse_tweet_sentiment
from nltk.sentiment.vader import SentimentIntensityAnalyzer



# Load emotions dictionary
emotions = {}
with open("emotions.txt", "r") as file:
    for line in file:
        word, emotion = line.strip().replace("'", "").split(": ")
        emotions[word] = emotion

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def analyse_tweet(text, flag=False):
    text = preprocess_text(text)
    tokenized_words = word_tokenize(text)
    final_words = [word for word in tokenized_words if word not in stopwords.words("english")]
    emotion_list = [emotions[word] for word in final_words if word in emotions]
    sentiment_labels = [emotions_sentiments(emotion) for emotion in emotion_list]
    sentiment_counts = Counter(sentiment_labels)

    if flag:
        # Print and plot analysis details
        print("Tokenized Words:\n", tokenized_words)
        print("Emotion List:\n", emotion_list)
        print("Sentiment Labels:\n", sentiment_labels)
        print("Sentiment Counts:\n", sentiment_counts)
        fig, ax = plt.subplots()
        ax.bar(sentiment_counts.keys(), sentiment_counts.values())
        fig.autofmt_xdate()
        plt.show()

    calculated_sentiment = emotions_sentiments(text)
    if calculated_sentiment in ["Positive", "Negative"]:
        return calculated_sentiment
    else:
        try: 
            return analyse_tweet_sentiment(text)
        except:
            return "Irrelevant"
    

def emotions_sentiments(emotion):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(emotion)
    pos = score['pos']
    neg = score['neg']
    neu = score['neu']
    compound = score['compound']
    if max(pos, neg, neu, compound) == pos:
        return "Positive"
    elif max(pos, neg, neu, compound) == neg:
        return "Negative"
    elif max(pos, neg, neu, compound) == neu:
        return "Neutral"
    return "Irrelevant"


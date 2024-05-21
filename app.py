import streamlit as st
import pickle
import time
from language import translate_text
import datetime
import pandas as pd
import os
from ntscraper import Nitter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))

# Function to generate and display Word Clouds for each sentiment category
def generate_wordclouds(df):
    fig, axes = plt.subplots(2, 2, figsize=(40, 20))
    for index, sentiment in enumerate(df['sentiment'].unique()):
        ax = axes[index // 2, index % 2]  
        df_sentiment = df[df['sentiment'] == sentiment]['trans_text']
        wordcloud = WordCloud(background_color='white', stopwords=stopwords, max_words=300, max_font_size=40, scale=5).generate(str(df_sentiment))
        ax.imshow(wordcloud)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(sentiment, fontsize=40)

    plt.tight_layout()
    st.pyplot(fig)

if 'scraper' not in st.session_state:
    st.session_state['scraper'] = "Loading...."
    try:
        st.session_state['scraper'] = Nitter(log_level=1, skip_instance_check=False)
    except Exception as e:
        st.session_state['scraper'] = None

scraper = st.session_state['scraper']

def get_tweets(name, mode, no):
    tweets = scraper.get_tweets(name, mode=mode, number=no)
    return tweets

model = pickle.load(open("twitter_sentiment.pkl", 'rb'))

# Sidebar
option = st.sidebar.selectbox(
    'Navigation',
    ('Analyse', 'Feedback', 'Insights')
)

if option == 'Analyse':
    st.header('Analyse your tweet')
    tweet = st.text_area("Enter your tweet")
    submit = st.button("Predict")
    prediction = None
    if submit:
        translated_text = translate_text(tweet)
        start = time.time()
        prediction = model.predict([translated_text])
        end = time.time()
        st.write(round(end-start, 2), ' seconds taken to predict')
        st.write("Your tweet is ", prediction[0])
        st.session_state['tweet_to_feedback'] = translated_text
        st.session_state['prediction'] = prediction[0]

elif option == 'Feedback':
    st.header('Feedback')
    
    # Check if tweet is sent from home
    if 'tweet_to_feedback' in st.session_state:
        translated_text = st.session_state['tweet_to_feedback']
        prediction = st.session_state['prediction']
        st.write("Tweet:", translated_text)
        st.write("Prediction:", prediction)
        
        feedback = st.selectbox("Was the prediction correct?", ("Correct", "Incorrect"), index=None)

        if feedback == "Incorrect":
            csv_filename = "tweets.csv"
            sentiment = st.selectbox("What is the correct sentiment?", ("Positive", "Negative", "Neutral", "Irrelevant"), index=None)
            if sentiment:
                date = datetime.datetime.now(datetime.timezone.utc)
                formatted_date = date.strftime('%b %d, %Y · %I:%M %p UTC')
                data = ["Feedback", formatted_date, sentiment, translated_text]
                data_df = pd.DataFrame([data])
                data_df.to_csv(csv_filename, mode='a', index=False, header=not os.path.isfile(csv_filename))
                st.write("Thanks for your feedback!")
        if feedback == "Correct":
            st.write("Thanks for your feedback!")
    else:
        tweet = st.text_area("Enter your tweet")
        submit = st.button("Predict")
        prediction = None
        if submit:
            translated_text = translate_text(tweet)
            start = time.time()
            prediction = model.predict([translated_text])
            end = time.time()
            st.write(round(end-start, 2), ' seconds taken to predict')
            st.write("Your tweet is ", prediction[0])

        feedback = st.selectbox("Was the prediction correct?", ("Correct", "Incorrect"), index=None)

        if feedback == "Incorrect":
            translated_text = translate_text(tweet)
            csv_filename = "tweets.csv"
            sentiment = st.selectbox("What is the correct sentiment?", ("Positive", "Negative", "Neutral", "Irrelevant"), index=None)
            if sentiment:
                date = datetime.datetime.now(datetime.timezone.utc)
                formatted_date = date.strftime('%b %d, %Y · %I:%M %p UTC')
                data = ["Feedback", formatted_date, sentiment, translated_text]
                data_df = pd.DataFrame([data])
                data_df.to_csv(csv_filename, mode='a', index=False, header=not os.path.isfile(csv_filename))
                st.write("Thanks for your feedback!")
elif option == 'Insights':
    username = st.text_input("Enter the username")
    tweets = []
    if st.button("Fetch Tweets"):
        while len(tweets) < 10:
            print(len(tweets))
            try:
                fetched_tweets = get_tweets(username, 'user', 10)
            except:
                continue
            if len(fetched_tweets.get('tweets', [])) > 0:
                if len(tweets) >= 10: 
                    break
                else:
                    tweets.extend(fetched_tweets.get('tweets', []))
        for tweet in tweets:
            translated_text = translate_text(tweet['text'])
            tweet['trans_text'] = translated_text
            prediction = model.predict([translated_text])
            tweet['sentiment'] = prediction[0]

            
        df = pd.DataFrame(tweets)
        st.subheader(f"Latest 10 tweets from {username}")
        st.dataframe(df[['text', 'sentiment']])
        
        sentiment_counts = df['sentiment'].value_counts()

        # Create a pie chart using Matplotlib
        fig, ax = plt.subplots()
        ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.0f%%")

        ax.axis('equal')

        st.pyplot(fig)
        st.header("Sentiment Word Clouds")
        generate_wordclouds(df)
    

st.sidebar.info("Developed by Dibya Ranjan Bora ")
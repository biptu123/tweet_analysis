import streamlit as st
import pickle
import time

st.title("Analysis your tweet")
model = pickle.load(open("twitter_sentiment.pkl", 'rb'))

tweet = st.text_area("Enter your tweet")

submit = st.button("Predict")

if submit:
    start = time.time()
    prediction = model.predict([tweet])
    end = time.time()
    st.write(round(end-start, 2), ' seconds taken to predict')
    st.write("Your tweet is ",prediction[0])



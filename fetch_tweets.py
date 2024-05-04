#!/usr/bin/env python
# coding: utf-8



import os
import random
import pandas as pd
from ntscraper import Nitter
from textblob import TextBlob
from sentiment_analysis import analyse_tweet
from deep_sentiment_analysis import analyse_tweet_sentiment
from language import translate_text
import time
import logging



# scrapper = Nitter()
scraper = Nitter(log_level=1, skip_instance_check=False)




def get_tweets(name, mode, no):
    tweets = scraper.get_tweets(name, mode=mode, number=no)
    return tweets



def save_tweets(tweets, csv_filename):
    final_tweets = []

    for tweet in tweets.get('tweets', []):
        # Check if the tweet is in English
        translated_text = translate_text(tweet['text'])
        print(translated_text)
        if translated_text:
            try:
                sentiment = analyse_tweet_sentiment(translated_text)  
            except:
                sentiment = "Irrelevant"
            print(sentiment)
            data = [tweet['user']['name'], tweet['date'], sentiment, translated_text]
            data_df = pd.DataFrame([data])
    
            # Append data to CSV file
            data_df.to_csv(csv_filename, mode='a', index=False, header=not os.path.isfile(csv_filename))
            final_tweets.append(data)


    
    return pd.DataFrame(final_tweets)

politicians = [
    "JoeBiden", "KamalaHarris", "BarackObama", "MichelleObama", "HillaryClinton",
    "BernieSanders", "NancyPelosi", "SenSchumer", "AOC",
    "PeteButtigieg", "CoryBooker", "AdamSchiff", "tedlieu", "RoKhanna",
    "ewarren", "ChrisMurphyCT", "SenWarren", "marcorubio", 
    "Mike_Pence", "IvankaTrump", "EricTrump", "DonaldJTrumpJr", "PressSec",
    "LindseyGrahamSC", "RandPaul", "senatemajldr", "HawleyMO", "tedcruz",
    "GovRonDeSantis",  "NYGovCuomo", "GavinNewsom", "GovAbbott",
    "RepMattGaetz",  "RepSwalwell", "RepJerryNadler",
    "RepAdamSmith", "RepTedLieu", "DevinNunes", "MarkMeadows", "GOPLeader",
    "SpeakerPelosi", "SenSanders",  "SenKamalaHarris",
    "SenatorCollins",   "SenBooker", "RepAOC",
    "RepLizCheney", "RepDebDingell", "RepDanCrenshaw", "RepRashida", "RepCummings",
    "RepAdamSchiff", "RepMaxineWaters", "RepDevinNunes", "RepLeeZeldin", "RepPressley",
    "SenToomey",  "SenKlobuchar",  "SenBlumenthal",
    "SenRubioPress", "SenatorBaldwin", "SenCoryGardner", "SenMikeLee", "SenGillibrand",
    "SenRickScott", "SenJeffMerkley", "SenStabenow", "SenFeinstein", "SenBennetCO",
    "GovWhitmer", "GovKemp",  "GovInslee", "GovParsonMO",
    "GovTimWalz", "GovMurphy", "GovRicketts", "GovRaimondo", "GovChrisSununu",
    "GovMikeDeWine", "GovEvers", "GovLarryHogan", "GovernorTomWolf", "GovHolcomb",
    "GovMikeParson",  "GovernorVA", "GovHerbert", "GovJanetMills",
    "GovBillLee", "GovSteveBullock", "GovPritzker", "GovDougBurgum", "GovMattBevin",
    "narendramodi", "AmitShah", "rajnathsingh", "nsitharaman", "smritiirani",
    "NitishKumar", "ArvindKejriwal", "RahulGandhi", "SoniaGandhi", "priyankagandhi",
    "yadavakhilesh", "yadavtejashwi", "MamataOfficial", "PawarSpeaks", "hd_kumaraswamy",
    "ncbn", "ikamalhaasan", "PawanKalyan", "mkstalin", "KTRTRS",
    "ysjagan", "BSYBJP", "siddaramaiah", "Dev_Fadnavis", "VNarayanasami",
    "OmarAbdullah", "MehboobaMufti", "AshokChavanINC", "BhupinderSHooda", "Jairam_Ramesh",
    "prakashraaj", "kanhaiyakumar", "DrRPNishank", "DrSJaishankar", "rajeevgowda",
    "nityanandraibjp", "JPNadda", "KanimozhiDMK", "Naveen_Odisha"
]


logging.basicConfig(level=logging.INFO)  # Set logging level

j = 1
counter = 0
max_failures = 100  # Maximum consecutive failures allowed
while len(politicians) > 0:
    politician = random.choice(politicians)
    logging.info(f"Iteration {j} started for {politician}")

    try:
        fetched_tweets = get_tweets(politician, 'user', 1000)

    except:
        continue

    if len(fetched_tweets.get('tweets', [])) > 0:
        previous_length = len(politicians)
        politicians.remove(politician)
        final_tweets = save_tweets(fetched_tweets, 'tweets.csv')
        logging.info(f"Fetched {len(final_tweets)} tweets for {politician}")
    else:
        logging.warning(f"No tweets fetched for {politician}")

    logging.info(f"Iteration {j} Ended")
    logging.info("#" * 100)
    j += 1



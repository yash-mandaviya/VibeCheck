#!/usr/bin/python
# -*- coding: utf-8 -*-

import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import base64
import os

def set_background_image(image_path):
    try:
        # Check if the file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image '{image_path}' not found.")
        
        page_bg_img = f'''
        <style>
        body {{
            background-image: url("{image_path}");  /* Provide relative path to the image */
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

    except FileNotFoundError as e:
        st.error(f"Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Define the image path (adjust as per your project structure)
image_path = "background.jpg" 
set_background_image(image_path)

st.title("Welcome to the Twitter Sentiment Analysis App")

# Twitter API v2 credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAALlMwQEAAAAAbc63AVlmTydwdN8AKVAW5ufIN0Y%3DP2BBtZrrynhP2gy5s7wex89sIi4sCVi4eEIclHbv01AVEATl8H"  # Replace with your actual bearer token

# Authenticate with tweepy Client for v2 API
client = tweepy.Client(bearer_token=bearer_token)

# Helper functions for text processing and sentiment analysis
def cleanTxt(text):
    text = re.sub(r'@[\w]+', '', text)  # Removing @mentions
    text = re.sub(r'#', '', text)  # Removing hashtag symbols
    text = re.sub(r'RT[\s]+', '', text)  # Removing "RT"
    text = re.sub(r'https?://\S+', '', text)  # Removing hyperlinks
    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

def app():
    st.title('News Analyzer from Tweets')
    activities = ['Tweet Analyzer', 'Generate Twitter Data', 'Text Analysis']
    choice = st.sidebar.selectbox('Select Your Activity', activities)

    if choice == 'Tweet Analyzer':
        st.subheader('Analyze the tweets of your favorite Personalities')
        raw_text = st.text_area('Enter the exact Twitter handle of the user (without @)')
        Analyzer_choice = st.selectbox('Select the Activity', ['Show Recent Tweets (5 Recent Tweets)', 'Generate WordCloud', 'Visualize Sentiment Analysis'])

        if st.button('Analyze'):
            if Analyzer_choice == 'Show Recent Tweets (5 Recent Tweets)':
                st.success('Fetching last 5 Tweets')

                def Show_Recent_Tweets(raw_text):
                    try:
                        user = client.get_user(username=raw_text)
                        user_id = user.data.id
                        response = client.get_users_tweets(id=user_id, max_results=5, tweet_fields=['text'])
                        tweets = [tweet.text for tweet in response.data]
                        return tweets
                    except tweepy.TweepyException as e:
                        st.error(f"Twitter API error: {str(e)}")
                        return None

                recent_tweets = Show_Recent_Tweets(raw_text)
                st.write(recent_tweets)

            elif Analyzer_choice == 'Generate WordCloud':
                st.success('Generating Word Cloud')

                def gen_wordcloud(raw_text):
                    try:
                        user = client.get_user(username=raw_text)
                        user_id = user.data.id
                        response = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['text'])
                        tweets = [tweet.text for tweet in response.data]
                    except tweepy.TweepyException as e:
                        st.error(f"Twitter API error: {str(e)}")
                        return None

                    allWords = ' '.join(tweets)
                    stopwords = set(STOPWORDS)
                    stopwords.update(['https', 't', 'co', 'RT', 'S'])
                    wordCloud = WordCloud(stopwords=stopwords, width=500, height=300, random_state=21, max_font_size=110, background_color='white').generate(allWords)
                    
                    plt.imshow(wordCloud, interpolation='bilinear')
                    plt.axis('off')
                    plt.savefig('WC.jpg')
                    img = Image.open('WC.jpg')
                    return img

                img = gen_wordcloud(raw_text)
                if img:
                    st.image(img)

            elif Analyzer_choice == 'Visualize Sentiment Analysis':
                st.success('Generating Visualization for Sentiment Analysis')

                def Plot_Analysis(raw_text):
                    try:
                        user = client.get_user(username=raw_text)
                        user_id = user.data.id
                        response = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['text'])
                        tweets = [tweet.text for tweet in response.data]
                    except tweepy.TweepyException as e:
                        st.error(f"Twitter API error: {str(e)}")
                        return None

                    df = pd.DataFrame(tweets, columns=['Tweets'])

                    # Clean and analyze tweets
                    df['Tweets'] = df['Tweets'].apply(cleanTxt)
                    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
                    df['Polarity'] = df['Tweets'].apply(getPolarity)
                    df['Analysis'] = df['Polarity'].apply(getAnalysis)

                    return df

                df = Plot_Analysis(raw_text)
                if df is not None and not df.empty:
                    fig, ax = plt.subplots()
                    sns.countplot(x='Analysis', data=df, ax=ax)
                    st.pyplot(fig)
                else:
                    st.error("Unable to generate plot. Please check if there's enough data.")

    elif choice == 'Generate Twitter Data':
        st.subheader('Fetch and analyze the last 100 tweets from the Twitter handle')
        user_name = st.text_area('Enter the exact Twitter handle of the user (without @)')

        def get_data(user_name):
            try:
                user = client.get_user(username=user_name)
                user_id = user.data.id
                response = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['text'])
                tweets = [tweet.text for tweet in response.data]
            except tweepy.TweepyException as e:
                st.error(f"Twitter API error: {str(e)}")
                return None

            df = pd.DataFrame(tweets, columns=['Tweets'])
            df['Tweets'] = df['Tweets'].apply(cleanTxt)
            df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
            df['Polarity'] = df['Tweets'].apply(getPolarity)
            df['Analysis'] = df['Polarity'].apply(getAnalysis)
            return df

        if st.button('Show Data'):
            st.success('Fetching Last 100 Tweets')
            df = get_data(user_name)
            if df is not None:
                st.write(df)

    else:
        st.subheader('This tool directly analyzes the text')
        content = st.text_area('Enter the text')

        def analyze_text(content):
            df = pd.DataFrame([content], columns=['Tweets'])
            df['Tweets'] = df['Tweets'].apply(cleanTxt)
            df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
            df['Polarity'] = df['Tweets'].apply(getPolarity)
            df['Analysis'] = df['Polarity'].apply(getAnalysis)
            return df

        if st.button('Show Data'):
            st.success('Analyzing your text')
            df = analyze_text(content)
            st.write(df)

    st.subheader('ArtificialMinds from GDEC ||| Smart Gujarat for New India Hackathon')

if __name__ == '__main__':
    app()

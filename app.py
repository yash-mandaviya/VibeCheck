#!/usr/bin/python
# -*- coding: utf-8 -*-

import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

# Set up background image
page_bg_img = '''
<style>
body {
background-color: lightblue;
background-repeat: no-repeat;
background-image: url("http://jaykadam.rf.gd/back.jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Twitter API v2 credentials
bearer_token = "YOUR_BEARER_TOKEN"

# Authenticate with tweepy Client for v2 API
client = tweepy.Client(bearer_token=bearer_token)

def app():
    st.title('News Analyzer from Tweets')

    activities = ['Tweet Analyzer', 'Generate Twitter Data', 'Text analysis']
    choice = st.sidebar.selectbox('Select Your Activity', activities)

    if choice == 'Tweet Analyzer':
        st.subheader('Analyze the tweets of your favourite Personalities')

        raw_text = st.text_area('Enter the exact twitter handle of the user(without @)')
        Analyzer_choice = st.selectbox('Select the Activities', ['Show Recent Tweets', 'Generate WordCloud', 'Visualize the Sentiment Analysis'])

        if st.button('Analyze'):
            if Analyzer_choice == 'Show Recent Tweets':
                st.success('Fetching last 5 Tweets')

                def Show_Recent_Tweets(raw_text):
                    try:
                        # Fetch user ID first
                        user = client.get_user(username=raw_text)
                        user_id = user.data.id
                        
                        # Fetch recent tweets
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
                        # Fetch user ID and then tweets
                        user = client.get_user(username=raw_text)
                        user_id = user.data.id
                        response = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['text'])
                        tweets = [tweet.text for tweet in response.data]
                    except tweepy.TweepyException as e:
                        st.error(f"Twitter API error: {str(e)}")
                        return None

                    # Generate word cloud
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

            elif Analyzer_choice == 'Visualize the Sentiment Analysis':
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
        # Similar updates for other choices would follow the same pattern as above

    else:
        st.subheader('This tool directly analyzes the text')
        content = st.text_area('Enter the text')
        # Analysis function here (no changes needed for API v2)
        df = get_data(content)
        st.write(df)

    st.subheader('ArtificialMinds from GDEC ||| Smart Gujarat for New India Hackathon')

if __name__ == '__main__':
    app()

# Helper functions
def cleanTxt(text):
    return re.sub(r'@[\w]+|https?://\S+', '', text)

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    return 'Positive' if score > 0 else 'Negative' if score < 0 else 'Neutral'

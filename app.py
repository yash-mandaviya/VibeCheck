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

# Set up background image using HTML and CSS
# Ensure that you place the image in the same directory as the Python file
background_image_path = 'background.jpg'  # Ensure the image file is in the same directory

# Attempt to load and display the background image
try:
    # Check if the image exists and convert it to base64 for embedding
    with open(background_image_path, 'rb') as img_file:
        image_data = img_file.read()
        base64_background = base64.b64encode(image_data).decode('utf-8')
        page_bg_img = f'''
        <style>
        body {{
        background-image: url("data:image/jpg;base64,{base64_background}");
        background-repeat: no-repeat;
        background-size: cover;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Background image '{background_image_path}' not found. Please ensure the image is in the correct directory.")
except Exception as e:
    st.error(f"An error occurred while loading the background image: {str(e)}")

# Twitter API v2 credentials (Replace with your actual credentials)
bearer_token = "AAAAAAAAAAAAAAAAAAAAALlMwQEAAAAAbc63AVlmTydwdN8AKVAW5ufIN0Y%3DP2BBtZrrynhP2gy5s7wex89sIi4sCVi4eEIclHbv01AVEATl8H"  # Replace with your actual bearer token

# Authenticate with Tweepy Client for v2 API
client = tweepy.Client(bearer_token=bearer_token)

# Helper functions for text processing and sentiment analysis
def cleanTxt(text):
    """
    Cleans the input text by removing unwanted characters like mentions, hashtags, URLs, etc.
    """
    text = re.sub(r'@[\w]+', '', text)  # Removing @mentions
    text = re.sub(r'#', '', text)  # Removing hashtag symbols
    text = re.sub(r'RT[\s]+', '', text)  # Removing "RT"
    text = re.sub(r'https?://\S+', '', text)  # Removing hyperlinks
    return text

def getSubjectivity(text):
    """
    Returns the subjectivity of the text using TextBlob.
    """
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    """
    Returns the polarity of the text using TextBlob.
    """
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    """
    Returns the sentiment based on the polarity score.
    """
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

# Main application function
def app():
    """
    Main Streamlit application function that provides functionality for different activities.
    """
    st.title('News Analyzer from Tweets')
    activities = ['Tweet Analyzer', 'Generate Twitter Data', 'Text Analysis']
    choice = st.sidebar.selectbox('Select Your Activity', activities)

    # Tweet Analyzer Activity
    if choice == 'Tweet Analyzer':
        st.subheader('Analyze the tweets of your favorite Personalities')
        raw_text = st.text_area('Enter the exact Twitter handle of the user (without @)')
        Analyzer_choice = st.selectbox('Select the Activity', ['Show Recent Tweets (5 Recent Tweets)', 'Generate WordCloud', 'Visualize Sentiment Analysis'])

        if st.button('Analyze'):
            if Analyzer_choice == 'Show Recent Tweets (5 Recent Tweets)':
                st.success('Fetching last 5 Tweets')

                def Show_Recent_Tweets(raw_text):
                    """
                    Fetches the last 5 tweets from the specified Twitter user.
                    """
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
                if recent_tweets:
                    st.write(recent_tweets)

            elif Analyzer_choice == 'Generate WordCloud':
                st.success('Generating Word Cloud')

                def gen_wordcloud(raw_text):
                    """
                    Generates a word cloud from the user's tweets.
                    """
                    try:
                        # Fetch tweets
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

            elif Analyzer_choice == 'Visualize Sentiment Analysis':
                st.success('Generating Visualization for Sentiment Analysis')

                def Plot_Analysis(raw_text):
                    """
                    Generates a sentiment analysis plot based on the user's tweets.
                    """
                    try:
                        # Fetch tweets
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

    # Generate Twitter Data Activity
    elif choice == 'Generate Twitter Data':
        st.subheader('Fetch and analyze the last 100 tweets from the Twitter handle')
        user_name = st.text_area('Enter the exact Twitter handle of the user (without @)')

        def get_data(user_name):
            """
            Fetches the last 100 tweets from the specified Twitter user.
            """
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

    # Text Analysis Activity
    else:
        st.subheader('This tool directly analyzes the text')
        content = st.text_area('Enter the text')

        def analyze_text(content):
            """
            Analyzes the input text for sentiment and returns a DataFrame with results.
            """
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

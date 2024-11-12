#!/usr/bin/python
# -*- coding: utf-8 -*-

import streamlit as st

# import streamlit.components.v1 as comp

import tweepy
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

# comp.html("<html><body background="back.jpg"></body></html>")

page_bg_img = \
    '''
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

# consumerKey = "PmpUrUVJJ8enACNHMNmLydg8T"
# consumerSecret = "QTRRR1vwJyjAg5ZsXk0hgToMZz3zMG4VoSRwJ3R8ro5wibwSrm"
# accessToken = "985205126175404032-tLLZvtgJxSsioklQXORNCqij2XiAEKt"
# accessTokenSecret = "yam77qumqgtzzI2xUHsYJJfLz7t9n9WjmUUzq3uMVvCDi"
# Dev. Account: @KADAMJAYV

consumerKey = 'D2NcYlX47tpxFIGz8jDiWSH5h'
consumerSecret = 'JK1WuauFdS48hnEjR8DGUy2bTxud5xGmAjbGYt4DP6CUPYQW4s'
accessToken = '1202642668737589250-6pxdevwsHeqq1O3QevcvCLBgnd0Z7D'
accessTokenSecret = '9yROGNItODZQjlSgOvcTckiAEg5TM50RXYckB2u38B5ty'

# Dev. Account:@YashMandaviya4

# Create the authentication object

authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret

authenticate.set_access_token(accessToken, accessTokenSecret)

# Creating the API object while passing in auth information

api = tweepy.API(authenticate, wait_on_rate_limit=True)


# plt.style.use('fivethirtyeight')

def app():

    st.title('News Analyzer from Tweets')

    activities = ['Tweet Analyzer', 'Generate Twitter Data',
                  'Text analysis']

    choice = st.sidebar.selectbox('Select Your Activity', activities)

    if choice == 'Tweet Analyzer':

        st.subheader('Analyze the tweets of your favourite Personalities'
                     )

        st.subheader('This tool performs the following tasks :')

        st.write('1. Fetches the 5 most recent tweets from the given twitter handel'
                 )
        st.write('2. Generates a Word Cloud')
        st.write('3. Performs Sentiment Analysis a displays it in form of a Bar Graph'
                 )

        raw_text = \
            st.text_area('Enter the exact twitter handle of the user(without @)'
                         )

        st.markdown('')

        Analyzer_choice = st.selectbox('Select the Activities',
                ['Show Recent Tweets', 'Generate WordCloud',
                'Visualize the Sentiment Analysis'])

        if st.button('Analyze'):

            if Analyzer_choice == 'Show Recent Tweets':

                st.success('Fetching last 5 Tweets')

                def Show_Recent_Tweets(raw_text):

                    # Extract 100 tweets from the twitter user
                    # posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

                    try:
                        posts = api.user_timeline(screen_name=raw_text,
                                count=100, tweet_mode='extended')
                    except tweepy.TweepError, e:
                        st.error('Twitter API error: {str(e)}')
                        return None
                    except tweepy.RateLimitError, e:
                        st.error('Twitter API rate limit exceeded. Please try again later.'
                                 )
                        return None
                    except Exception, e:
                        st.error('An unexpected error occurred: {str(e)}'
                                 )
                        return None

                    def get_tweets():

                        l = []
                        i = 1
                        for tweet in posts[:5]:
                            l.append(tweet.full_text)
                            i = i + 1
                        return l

                        recent_tweets = get_tweets()
                        return recent_tweets

                    recent_tweets = Show_Recent_Tweets(raw_text)

                    st.write(recent_tweets)

            elif Analyzer_choice == 'Generate WordCloud':

                st.success('Generating Word Cloud')

                def gen_wordcloud():
                    try:
                        posts = api.user_timeline(screen_name=raw_text,
                                count=100, tweet_mode='extended')
                    except tweepy.TweepError, e:
                        st.error('Twitter API error: {str(e)}')
                        return None
                    except tweepy.RateLimitError, e:
                        st.error('Twitter API rate limit exceeded. Please try again later.'
                                 )
                        return None
                    except Exception, e:
                        st.error('An unexpected error occurred: {str(e)}'
                                 )
                        return None

                    # posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")
                    # posts = api.user_timeline(screen_name=raw_text, count=100, tweet_mode="extended")
                    # Create a dataframe with a column called Tweets

                    df = pd.DataFrame([tweet.full_text for tweet in
                            posts], columns=['Tweets'])

                    # word cloud visualization

                    allWords = ' '.join([twts for twts in df['Tweets']])
                    stopwords = set(STOPWORDS)
                    stopwords.update(['https', 't', 'co', 'RT', 'S'])

                    wordCloud = WordCloud(
                        stopwords=stopwords,
                        width=500,
                        height=300,
                        random_state=21,
                        max_font_size=110,
                        background_color='white',
                        ).generate(allWords)
                    plt.imshow(wordCloud, interpolation='bilinear')
                    plt.axis('off')
                    plt.savefig('WC.jpg')
                    img = Image.open('WC.jpg')
                    return img

                img = gen_wordcloud()

                st.image(img)
            else:

                def Plot_Analysis():

                    st.success('Generating Visualisation for Sentiment Analysis'
                               )
                    try:
                        posts = api.user_timeline(screen_name=raw_text,
                                count=100, tweet_mode='extended')
                    except tweepy.TweepError, e:
                        st.error('Twitter API error: {str(e)}')
                        return None
                    except tweepy.RateLimitError, e:
                        st.error('Twitter API rate limit exceeded. Please try again later.'
                                 )
                        return None
                    except Exception, e:
                        st.error('An unexpected error occurred: {str(e)}'
                                 )
                        return None

                    # posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")
                    # posts = api.user_timeline(screen_name=raw_text, count=100, tweet_mode="extended")

                    df = pd.DataFrame([tweet.full_text for tweet in
                            posts], columns=['Tweets'])

                    # Create a function to clean the tweets

                    def cleanTxt(text):

                        text = re.sub('@[A-Za-z0\xe2\x80\x939]+', '',
                                text)  # Removing @mentions
                        text = re.sub(r'#', '', text)  # Removing '#' hash tag
                        text = re.sub(r'RT[\s]+', '', text)  # Removing RT
                        text = re.sub(r'https?:\/\/\S+', '', text)  # Removing hyperlink

                        return text

                    # Clean the tweets

                    df['Tweets'] = df['Tweets'].apply(cleanTxt)

                    def getSubjectivity(text):
                        return TextBlob(text).sentiment.subjectivity

                    # Create a function to get the polarity

                    def getPolarity(text):
                        return TextBlob(text).sentiment.polarity

                    # Create two new columns 'Subjectivity' & 'Polarity'

                    df['Subjectivity'] = df['Tweets'
                            ].apply(getSubjectivity)
                    df['Polarity'] = df['Tweets'].apply(getPolarity)

                    def getAnalysis(score):
                        if score < 0:
                            return 'Negative'
                        elif score == 0:
                            return 'Neutral'
                        else:
                            return 'Positive'

                    df['Analysis'] = df['Polarity'].apply(getAnalysis)

                    return df

                df = Plot_Analysis()

                st.write(sns.countplot(x=df['Analysis'], data=df))

                st.set_option('deprecation.showPyplotGlobalUse', False)

                st.pyplot(use_container_width=True)
    elif choice == 'Generate Twitter Data':

        st.subheader('This tool fetches the last 100 tweets from the twitter handel & Performs the following tasks'
                     )

        st.write('1. Converts it into a DataFrame')
        st.write('2. Cleans the text')
        st.write('3. Analyzes Subjectivity of tweets and adds an additional column for it'
                 )
        st.write('4. Analyzes Polarity of tweets and adds an additional column for it'
                 )
        st.write('5. Analyzes Sentiments of tweets and adds an additional column for it'
                 )

        user_name = \
            st.text_area('Enter the exact twitter handle of the Personality (without @)'
                         )

        st.markdown('<--------     Also Do checkout the another cool tool from the sidebar'
                    )

        def get_data(user_name):
            try:
                posts = api.user_timeline(screen_name=raw_text,
                        count=100, tweet_mode='extended')
            except tweepy.TweepError, e:
                st.error('Twitter API error: {str(e)}')
                return None
            except tweepy.RateLimitError, e:
                st.error('Twitter API rate limit exceeded. Please try again later.'
                         )
                return None
            except Exception, e:
                st.error('An unexpected error occurred: {str(e)}')
                return None

            # posts = api.user_timeline(screen_name=user_name, count = 100, lang ="en", tweet_mode="extended")

            df = pd.DataFrame([tweet.full_text for tweet in posts],
                              columns=['Tweets'])

            def cleanTxt(text):
                text = re.sub('@[A-Za-z0\xe2\x80\x939]+', '', text)  # Removing @mentions
                text = re.sub(r'#', '', text)  # Removing '#' hash tag
                text = re.sub(r'RT[\s]+', '', text)  # Removing RT
                text = re.sub(r'https?:\/\/\S+', '', text)  # Removing hyperlink
                return text

            # Clean the tweets

            df['Tweets'] = df['Tweets'].apply(cleanTxt)

            def getSubjectivity(text):
                return TextBlob(text).sentiment.subjectivity

                        # Create a function to get the polarity

            def getPolarity(text):
                return TextBlob(text).sentiment.polarity

                        # Create two new columns 'Subjectivity' & 'Polarity'

            df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
            df['Polarity'] = df['Tweets'].apply(getPolarity)

            def getAnalysis(score):
                if score < 0:
                    return 'Negative'
                elif score == 0:

                    return 'Neutral'
                else:

                    return 'Positive'

            df['Analysis'] = df['Polarity'].apply(getAnalysis)
            return df

        if st.button('Show Data'):

            st.success('Fetching Last 100 Tweets')

            df = get_data(user_name)

            st.write(df)
    else:

        st.subheader('This tool directly analyzes the text')
        content = st.text_area('Enter the text')

        def get_data(content):

            # posts = api.user_timeline(screen_name=user_name, count = 100, lang ="en", tweet_mode="extended")

            df = pd.DataFrame([content], columns=['Tweets'])

            def cleanTxt(text):
                text = re.sub('@[A-Za-z0\xe2\x80\x939]+', '', text)  # Removing @mentions
                text = re.sub(r'#', '', text)  # Removing '#' hash tag
                text = re.sub(r'RT[\s]+', '', text)  # Removing RT
                text = re.sub(r'https?:\/\/\S+', '', text)  # Removing hyperlink
                return text

            # Clean the tweets

            df['Tweets'] = df['Tweets'].apply(cleanTxt)

            def getSubjectivity(text):
                return TextBlob(text).sentiment.subjectivity

                        # Create a function to get the polarity

            def getPolarity(text):
                return TextBlob(text).sentiment.polarity

                        # Create two new columns 'Subjectivity' & 'Polarity'

            df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
            df['Polarity'] = df['Tweets'].apply(getPolarity)

            def getAnalysis(score):
                if score < 0:
                    return 'Negative'
                elif score == 0:

                    return 'Neutral'
                else:

                    return 'Positive'

            df['Analysis'] = df['Polarity'].apply(getAnalysis)
            return df

        if st.button('Show Data'):

            st.success('Analyzing your text')

            df = get_data(content)

            st.write(df)

    st.subheader('ArtificialMinds from GDEC |||  Smart Gujarat for New India Hackathon'
                 )


if __name__ == '__main__':
    app()

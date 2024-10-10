# VibeCheck - News Sentiment Analysis with a Twist!

Welcome to **VibeCheck**, your go-to tool for analyzing the emotional tone behind news headlines. Whether you're wondering if today's news is uplifting or downbeat, **VibeCheck** gives you the power to dissect and visualize the sentiments that shape the media!

![VibeCheck Banner](https://via.placeholder.com/1200x300.png?text=VibeCheck+News+Sentiment+Analysis)

## 📰 Project Overview
**VibeCheck** is a news sentiment analysis web application built using **Streamlit**. With this app, you can:

- **Analyze Sentiment**: Input news headlines or articles and receive real-time sentiment analysis.
- **Generate Word Clouds**: Visualize frequent words in the news you're analyzing.
- **Graphical Insights**: Dive into charts and graphs to get a clearer picture of sentiment trends over time.

Built for simplicity, this app is designed to help you cut through the noise and understand the emotional undertones of the latest headlines.

## 🚀 Features

- **Sentiment Analysis**: Input any news article or text, and **VibeCheck** will tell you if it's positive, neutral, or negative.
- **WordCloud Generation**: Visualize key terms dominating the news.
- **Graphical Representations**: Get insights through beautifully crafted charts and graphs.
- **Seamless UI**: Powered by **Streamlit** for an interactive and easy-to-use experience.

## 🛠 Installation and Setup

To get **VibeCheck** running locally, follow these simple steps:

### 1. Prerequisites

Ensure you have **Python** installed on your machine along with any preferred IDE. Then, install the required libraries:

```bash
pip install streamlit tweepy textblob wordcloud pandas numpy re matplotlib pillow seaborn
2. Run the Application
Once you’ve installed all necessary libraries, navigate to the project directory and run the following command in your terminal (I'm using conda but any terminal works):

bash
Copy code
streamlit run app.py
This will launch VibeCheck in your browser and you’ll be able to start analyzing news sentiment instantly!

🖥 Screenshots
Here's what you can expect when running VibeCheck:

1. Sentiment Dashboard
2. WordCloud View
3. Graphical Insights

📂 Project Structure
bash
Copy code
VibeCheck/
│
├── app.py                     # Main file to run the Streamlit app
├── requirements.txt            # List of dependencies
├── README.md                   # Project documentation
├── assets/                     # Images and static content
└── data/                       # Any sample data used for testing
🧠 How It Works
Sentiment Analysis: Utilizes TextBlob to calculate polarity and subjectivity scores of input text.
WordCloud: Generates a word cloud from the analyzed text using WordCloud.
Graphs: Leverages Matplotlib and Seaborn to create visual insights.
🌐 Explore More
Want to contribute or dive deeper into the code? Check out the GitHub Repository.

📧 Contact
For any questions, reach out to:
Yash Mandaviya – mandaviy@uwindsor.ca

⚡ Credits
Created by Yash Mandaviya as part of the News-Analysis-2.0 project. Special thanks to the awesome open-source community and libraries that made this possible!

VibeCheck – Analyzing the mood behind the headlines.
“Because every story has a vibe!”

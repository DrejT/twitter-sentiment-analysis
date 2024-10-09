import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Function to perform sentiment analysis using TextBlob
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Function to generate word clouds for each sentiment
def generate_wordcloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    st.pyplot(plt)

# Streamlit UI
def main():
    st.title("Twitter Sentiment Analysis with Visualization")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Display the uploaded data
        st.write("Uploaded Data")
        st.write(df)

        # Check if the required column exists
        if 'Text' in df.columns:
            # Perform sentiment analysis on each tweet in the 'Text' column
            df['Sentiment'] = df['Text'].apply(analyze_sentiment)

            # Display results in a DataFrame
            st.write("Tweets with Sentiment Analysis")
            st.write(df[['Username', 'Text', 'Sentiment', 'Retweets', 'Likes', 'Timestamp']])

            # Sentiment counts
            sentiment_counts = df['Sentiment'].value_counts()
            st.write("Sentiment Distribution")
            st.bar_chart(sentiment_counts)

            # Scatter plot of Likes vs Sentiment
            st.write("Scatter plot of Likes vs Sentiment")
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x='Likes', y='Retweets', hue='Sentiment', palette="deep")
            plt.title("Likes and Retweets vs Sentiment")
            st.pyplot(plt)

            # Word clouds for each sentiment
            st.write("Word Cloud for Positive Tweets")
            positive_tweets = " ".join(df[df['Sentiment'] == 'Positive']['Text'])
            generate_wordcloud(positive_tweets, "Positive Sentiment Tweets")

            st.write("Word Cloud for Negative Tweets")
            negative_tweets = " ".join(df[df['Sentiment'] == 'Negative']['Text'])
            generate_wordcloud(negative_tweets, "Negative Sentiment Tweets")

            st.write("Word Cloud for Neutral Tweets")
            neutral_tweets = " ".join(df[df['Sentiment'] == 'Neutral']['Text'])
            generate_wordcloud(neutral_tweets, "Neutral Sentiment Tweets")

        else:
            st.error("The uploaded CSV does not contain a 'Text' column.")
        
if __name__ == "__main__":
    main()

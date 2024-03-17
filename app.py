import pandas as pd
import streamlit as st
import altair as alt
import os
from b2sdk.v2 import B2Api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize B2Api instance
b2 = B2Api()

# Retrieve environment variables
application_key_id = os.getenv('keyID')
application_key = os.getenv('applicationKey')

# Authorize B2 account
b2.authorize_account("production", application_key_id, application_key)

def load_data(b2):
    # Get the bucket
    bucket = b2.get_bucket_by_name("Rushyfirstbucket")

    # Download file from Backblaze B2 bucket
    with open("Apple-Twitter-Sentiment-DFE.csv", 'rb') as file:
        bucket.download_file_by_name("Apple-Twitter-Sentiment-DFE.csv", file)
    
    # Load DataFrame from the downloaded file
    df = pd.read_csv("Apple-Twitter-Sentiment-DFE.csv", encoding='latin1')
    df['date'] = pd.to_datetime(df['date'], format='%a %b %d %H:%M:%S %z %Y')
    df['day_month_year'] = df['date'].dt.strftime('%d/%m/%Y')   
    return df

def app():
    # Load data
    st.title("Sentiment Confidence by Day")
    df = load_data(b2)
    df = df.rename(columns={'sentiment:confidence': 'sentiment_confidence'})
    sentiment_by_day = df.groupby('day_month_year')['sentiment_confidence'].mean().reset_index()
    
    # Plot
    chart = alt.Chart(sentiment_by_day).mark_bar().encode(
        x='day_month_year',
        y='sentiment_confidence',
        tooltip=['day_month_year', 'sentiment_confidence']
    ).properties(
        width=800,
        height=500
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # Print loaded DataFrame
    st.write(df)

if __name__ == "__main__":
    app()

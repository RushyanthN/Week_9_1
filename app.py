import pandas as pd
import streamlit as st
import altair as alt
import os
import b2
from b2sdk.v2 import B2Api
from dotenv import load_dotenv
from b2sdk.exception import FileNotPresent

load_dotenv()
b2 = B2Api()

application_key_id = st.secrets('keyID')
application_key = st.secrets('applicationKey')

b2.authorize_account("production", application_key_id, application_key)


def load_data(b2):
    try:
        bucket = b2.get_bucket_by_name("Rushyfirstbucket")
        with open("Apple-Twitter-Sentiment-DFE.csv", 'rb') as file:
            bucket.download_file_by_name("Apple-Twitter-Sentiment-DFE.csv", file)
        
        # Load DataFrame from the downloaded file
        df = pd.read_csv("Apple-Twitter-Sentiment-DFE.csv", encoding='latin1')
        df['date'] = pd.to_datetime(df['date'], format='%a %b %d %H:%M:%S %z %Y')
        df['day_month_year'] = df['date'].dt.strftime('%d/%m/%Y')   
        return df
    except FileNotPresent:
        st.error("Error: File not found in Backblaze B2 bucket. Please check if the file exists and try again.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def app():
    st.title("Sentiment Confidence by Day")
    df = load_data(b2)
    if df is not None:
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

if __name__ == "__main__":
    app()

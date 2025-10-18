import streamlit as st
from google.cloud import language_v1
import os

st.set_page_config(page_title="GCP Sentiment Analysis App", page_icon="☁️")

st.title("🌤 Google Cloud Sentiment Analysis App")
st.write("This app uses the Google Cloud Natural Language API to analyze the sentiment of your text.")

text = st.text_area("Enter some text to analyze:")

if st.button("Analyze Sentiment"):
    if not text.strip():
        st.warning("Please enter text before analyzing.")
    else:
        try:
            # Authenticate using your GCP credentials JSON
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-key.json"
            client = language_v1.LanguageServiceClient()

            document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

            st.success(f"Sentiment Score: {sentiment.score:.2f}")
            st.info(f"Sentiment Magnitude: {sentiment.magnitude:.2f}")

            if sentiment.score > 0.25:
                st.write("🟢 **Overall Sentiment: Positive**")
            elif sentiment.score < -0.25:
                st.write("🔴 **Overall Sentiment: Negative**")
            else:
                st.write("🟡 **Overall Sentiment: Neutral**")

        except Exception as e:
            st.error("⚠️ Could not connect to Google Cloud API. (Did you add your key?)")
            st.write(e)

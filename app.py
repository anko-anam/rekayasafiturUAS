import streamlit as st
import requests
import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
from google_play_scraper import reviews, Sort
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# =====================
# SETUP
# =====================
st.set_page_config(
    page_title="Analisis Sentimen Komentar & Ulasan",
    layout="wide"
)

nltk.download('punkt')
nltk.download('stopwords')

st.title("📊 Aplikasi Analisis Sentimen")
st.caption("YouTube Comments & Google Play Reviews | Streamlit Web App")

# =====================
# SIDEBAR
# =====================
menu = st.sidebar.selectbox(
    "Pilih Sumber Data",
    ["YouTube", "Google Play Store"]
)

# =====================
# UTIL FUNCTION
# =====================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in stopwords.words("english")]
    return " ".join(tokens)

def sentiment_label(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# =====================
# YOUTUBE
# =====================
if menu == "YouTube":
    st.subheader("📺 Analisis Komentar YouTube")

    api_key = st.text_input("YouTube API Key", type="password")
    video_id = st.text_input("Video ID", value="qkIr0i_rS2c")

    if st.button("🔍 Ambil Komentar YouTube"):
        if api_key == "":
            st.error("API Key wajib diisi!")
        else:
            with st.spinner("Mengambil komentar..."):
                comments = []
                next_page = None

                while True:
                    url = "https://www.googleapis.com/youtube/v3/commentThreads"
                    params = {
                        "part": "snippet",
                        "videoId": video_id,
                        "key": api_key,
                        "maxResults": 100,
                        "pageToken": next_page,
                        "textFormat": "plainText"
                    }

                    res = requests.get(url, params=params)
                    data = res.json()

                    for item in data.get("items", []):
                        s = item["snippet"]["topLevelComment"]["snippet"]
                        comments.append({
                            "author": s["authorDisplayName"],
                            "comment": s["textDisplay"],
                            "likeCount": s["likeCount"],
                            "publishedAt": s["publishedAt"]
                        })

                    next_page = data.get("nextPageToken")
                    if not next_page:
                        break

            df = pd.DataFrame(comments)
            df["clean"] = df["comment"].apply(clean_text)
            df["sentiment"] = df["clean"].apply(sentiment_label)

            st.success(f"Berhasil mengambil {len(df)} komentar")

            st.dataframe(df, use_container_width=True)

            fig, ax = plt.subplots()
            df["sentiment"].value_counts().plot(kind="bar", ax=ax)
            ax.set_title("Distribusi Sentimen Komentar YouTube")
            st.pyplot(fig)

            st.download_button(
                "⬇️ Download CSV",
                df.to_csv(index=False),
                "komentar_youtube_sentimen.csv",
                "text/csv"
            )

# =====================
# GOOGLE PLAY
# =====================
if menu == "Google Play Store":
    st.subheader("📱 Analisis Ulasan Google Play")

    app_id = st.text_input(
        "App ID Google Play",
        value="id.go.pajak.djp"
    )

    jumlah = st.slider("Jumlah Ulasan", 100, 1000, 600)

    if st.button("🔍 Ambil Ulasan Google Play"):
        with st.spinner("Mengambil ulasan..."):
            result, _ = reviews(
                app_id,
                lang="id",
                country="id",
                sort=Sort.NEWEST,
                count=jumlah
            )

        df = pd.DataFrame(result)[["userName", "score", "at", "content"]]
        df["clean"] = df["content"].apply(clean_text)
        df["sentiment"] = df["clean"].apply(sentiment_label)

        st.success(f"Berhasil mengambil {len(df)} ulasan")

        st.dataframe(df, use_container_width=True)

        fig, ax = plt.subplots()
        df["sentiment"].value_counts().plot(kind="bar", ax=ax)
        ax.set_title("Distribusi Sentimen Ulasan Google Play")
        st.pyplot(fig)

        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False),
            "ulasan_google_play_sentimen.csv",
            "text/csv"
        )

st.sidebar.info("📌 Cocok untuk skripsi, riset, dan analisis opini publik")

from flask import Flask, render_template, request
from youtube_scraper import get_comments
from playstore_scraper import get_reviews
from sentiment import clean_text, analyze_sentiment
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    source = request.form.get("source")

    if source == "youtube":
        texts = get_comments()
        title = "Analisis Sentimen YouTube"
    elif source == "playstore":
        texts = get_reviews()
        title = "Analisis Sentimen Play Store"
    else:
        texts = []
        title = "Tidak ada data"

    df = pd.DataFrame({"text": texts})
    df["clean"] = df["text"].apply(clean_text)
    df["sentiment"] = df["clean"].apply(analyze_sentiment)

    summary = df["sentiment"].value_counts()

    plt.figure(figsize=(6,4))
    summary.plot(kind="bar")
    plt.title(title)
    plt.tight_layout()
    plt.savefig("static/chart.png")
    plt.close()

    return render_template(
        "index.html",
        data=df.head(30).to_dict(orient="records"),
        summary=summary.to_dict(),
        chart=True,
        title=title
    )

if __name__ == "__main__":
    app.run(debug=True)

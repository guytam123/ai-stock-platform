
from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    chartJSON = ""
    if request.method == "POST":
        ticker = request.form["ticker"].upper()
        df = yf.download(ticker, period="6mo")
        df["SMA_20"] = df["Close"].rolling(window=20).mean()
        df["SMA_50"] = df["Close"].rolling(window=50).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close Price"))
        fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], name="SMA 20"))
        fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], name="SMA 50"))
        chartJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        data = df.tail(1).to_dict("records")[0]

    return render_template("index.html", data=data, chartJSON=chartJSON)

if __name__ == "__main__":
    app.run(debug=True)

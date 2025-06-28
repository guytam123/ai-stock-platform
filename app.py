
from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    ticker = request.form["ticker"]
    data = yf.download(ticker, period="5d", interval="1d")
    if data.empty:
        return f"No data found for {ticker}"
    return f"<h2>{ticker} - Last Close: {data['Close'][-1]:.2f}</h2><br><a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)

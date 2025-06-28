
from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    ticker = request.form['ticker']
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close Price'))
    fig.update_layout(title=f"{ticker} Stock Price", xaxis_title="Date", yaxis_title="Price")

    graph_html = fig.to_html(full_html=False)
    return render_template('result.html', ticker=ticker, graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
